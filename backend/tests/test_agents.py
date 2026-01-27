"""Tests for AI agents."""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

from src.agents.router_agent import RouterAgent, AgentState
from src.agents.buyer_persona_agent import BuyerPersonaAgent


class TestRouterAgent:
    """Tests for Router Agent."""
    
    @pytest.fixture
    def mock_llm_service(self):
        """Mock LLM service."""
        return MagicMock()
    
    @pytest.fixture
    def mock_memory_manager(self):
        """Mock Memory Manager."""
        mock = MagicMock()
        mock.get_context = AsyncMock()
        mock.add_message_to_short_term = AsyncMock()
        return mock
    
    @pytest.fixture
    def router_agent(self, mock_llm_service, mock_memory_manager):
        """Router agent instance."""
        return RouterAgent(mock_llm_service, mock_memory_manager)
    
    @pytest.mark.asyncio
    async def test_route_no_buyer_persona(self, router_agent, mock_memory_manager):
        """Router should return BUYER_PERSONA when no buyer persona exists."""
        # Setup: No buyer persona
        mock_memory_manager.get_context.return_value = {
            'has_buyer_persona': False,
            'documents_count': 0,
            'recent_chat': {},
            'relevant_docs': []
        }
        
        # Execute
        state = await router_agent.route(
            chat_id=uuid4(),
            project_id=uuid4(),
            user_message="Hola"
        )
        
        # Assert
        assert state == AgentState.BUYER_PERSONA
    
    @pytest.mark.asyncio
    async def test_route_with_buyer_persona_waiting(self, router_agent, mock_memory_manager):
        """Router should return WAITING when buyer persona exists and no content request."""
        # Setup: Has buyer persona
        mock_memory_manager.get_context.return_value = {
            'has_buyer_persona': True,
            'documents_count': 2,
            'recent_chat': {},
            'relevant_docs': []
        }
        
        # Execute
        state = await router_agent.route(
            chat_id=uuid4(),
            project_id=uuid4(),
            user_message="¿Cómo estás?"
        )
        
        # Assert
        assert state == AgentState.WAITING
    
    @pytest.mark.asyncio
    async def test_route_content_generation(self, router_agent, mock_memory_manager):
        """Router should return CONTENT_GENERATION when user requests content."""
        # Setup: Has buyer persona
        mock_memory_manager.get_context.return_value = {
            'has_buyer_persona': True,
            'documents_count': 2,
            'recent_chat': {},
            'relevant_docs': []
        }
        
        # Execute
        state = await router_agent.route(
            chat_id=uuid4(),
            project_id=uuid4(),
            user_message="Dame ideas de posts para Instagram"
        )
        
        # Assert
        assert state == AgentState.CONTENT_GENERATION
    
    def test_is_content_request_true(self, router_agent):
        """Detect content request keywords."""
        messages = [
            "Dame ideas de contenido",
            "Genera posts para Instagram",
            "Crea un video script",
            "Escribe un artículo",
        ]
        
        for msg in messages:
            assert router_agent._is_content_request(msg) is True
    
    def test_is_content_request_false(self, router_agent):
        """Should NOT detect content request in normal messages."""
        messages = [
            "Hola, ¿cómo estás?",
            "¿Qué puedes hacer?",
            "Gracias por la ayuda",
        ]
        
        for msg in messages:
            assert router_agent._is_content_request(msg) is False


class TestBuyerPersonaAgent:
    """Tests for Buyer Persona Agent."""
    
    @pytest.fixture
    def mock_llm_service(self):
        """Mock LLM service."""
        mock = MagicMock()
        mock.generate = AsyncMock()
        return mock
    
    @pytest.fixture
    def mock_memory_manager(self):
        """Mock Memory Manager."""
        mock = MagicMock()
        mock.get_context = AsyncMock()
        return mock
    
    @pytest.fixture
    def mock_db(self):
        """Mock database session."""
        mock = MagicMock()
        mock.add = MagicMock()
        mock.commit = AsyncMock()
        return mock
    
    @pytest.fixture
    def buyer_persona_agent(self, mock_llm_service, mock_memory_manager, mock_db):
        """Buyer persona agent instance."""
        return BuyerPersonaAgent(mock_llm_service, mock_memory_manager, mock_db)
    
    @pytest.mark.asyncio
    async def test_execute_success(
        self, 
        buyer_persona_agent, 
        mock_llm_service, 
        mock_memory_manager,
        mock_db
    ):
        """Buyer Persona Agent should generate complete persona."""
        # Setup
        chat_id = uuid4()
        project_id = uuid4()
        
        mock_memory_manager.get_context.return_value = {
            'relevant_docs': [
                {
                    'content': 'Empresa de software',
                    'source_title': 'documento.pdf',
                    'similarity': 0.9
                }
            ]
        }
        
        # Mock LLM response (valid JSON)
        mock_llm_service.generate.return_value = '{"nombre": "Ana", "edad": 35}'
        
        # Execute
        result = await buyer_persona_agent.execute(
            chat_id=chat_id,
            project_id=project_id,
            user_message="Empresa de cursos online"
        )
        
        # Assert
        assert result['success'] is True
        assert result['buyer_persona'] == {"nombre": "Ana", "edad": 35}
        assert 'generado exitosamente' in result['message']
        
        # Verify LLM was called
        mock_llm_service.generate.assert_called_once()
        
        # Verify database save
        mock_db.add.assert_called_once()
        mock_db.commit.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_execute_json_decode_error(
        self,
        buyer_persona_agent,
        mock_llm_service,
        mock_memory_manager
    ):
        """Should handle JSON decode errors gracefully."""
        # Setup
        mock_memory_manager.get_context.return_value = {'relevant_docs': []}
        
        # Mock invalid JSON response
        mock_llm_service.generate.return_value = 'Invalid JSON {'
        
        # Execute
        result = await buyer_persona_agent.execute(
            chat_id=uuid4(),
            project_id=uuid4(),
            user_message="Test"
        )
        
        # Assert
        assert result['success'] is False
        assert result['buyer_persona'] is None
        assert 'Error al parsear' in result['message']
    
    def test_build_buyer_persona_prompt(self, buyer_persona_agent):
        """Prompt should include all template sections."""
        prompt = buyer_persona_agent._build_buyer_persona_prompt(
            user_message="Empresa de software",
            relevant_docs=[]
        )
        
        # Check that all 11 categories are present
        assert "1. Aspectos Demográficos" in prompt
        assert "2. Hogar y Familia" in prompt
        assert "3. Trabajo" in prompt
        assert "4. Comportamiento" in prompt
        assert "5. Problema" in prompt
        assert "6. Búsqueda de la Solución" in prompt
        assert "7. Objeciones y Barreras" in prompt
        assert "8. Miedos e Inseguridades" in prompt
        assert "9. Comparación con Competencia" in prompt
        assert "10. Tu Producto o Servicio" in prompt
        assert "11. Información Adicional" in prompt
        
        # Check critical instructions
        assert "TODAS las preguntas" in prompt
        assert "No puedes saltarte ninguna" in prompt
        assert "JSON" in prompt
        
        # Check example is present
        assert "Ana" in prompt
        assert "Enfermera" in prompt
