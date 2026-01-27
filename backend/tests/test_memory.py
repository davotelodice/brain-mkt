"""Tests for Memory Manager."""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

from src.services.memory_manager import MemoryManager


class TestMemoryManager:
    """Tests for Memory Manager."""
    
    @pytest.fixture
    def mock_db(self):
        """Mock database session."""
        return MagicMock()
    
    @pytest.fixture
    def mock_rag_service(self):
        """Mock RAG service."""
        mock = MagicMock()
        mock.search_relevant_docs = AsyncMock()
        return mock
    
    @pytest.fixture
    def memory_manager(self, mock_db, mock_rag_service):
        """Memory manager instance."""
        return MemoryManager(mock_db, mock_rag_service)
    
    @pytest.mark.asyncio
    async def test_get_context_combines_all_memory_types(
        self,
        memory_manager,
        mock_rag_service
    ):
        """MemoryManager should combine short/long/semantic memory."""
        chat_id = uuid4()
        project_id = uuid4()
        
        # Mock RAG results
        mock_rag_service.search_relevant_docs.return_value = [
            {"content": "doc1", "similarity": 0.9},
            {"content": "doc2", "similarity": 0.8}
        ]
        
        # Mock buyer persona query
        with patch.object(memory_manager, '_get_buyer_persona', return_value={"nombre": "Ana"}):
            with patch.object(memory_manager, '_count_user_documents', return_value=3):
                # Execute
                context = await memory_manager.get_context(
                    chat_id=chat_id,
                    project_id=project_id,
                    current_message="Test query"
                )
        
        # Assert all three memory types are present
        assert 'recent_chat' in context
        assert 'buyer_persona' in context
        assert 'relevant_docs' in context
        assert 'has_buyer_persona' in context
        assert 'documents_count' in context
        
        # Assert buyer persona is correct
        assert context['buyer_persona'] == {"nombre": "Ana"}
        assert context['has_buyer_persona'] is True
        assert context['documents_count'] == 3
        
        # Assert RAG was called
        mock_rag_service.search_relevant_docs.assert_called_once_with(
            query="Test query",
            project_id=project_id,
            chat_id=chat_id,
            limit=5
        )
    
    @pytest.mark.asyncio
    async def test_get_context_no_buyer_persona(
        self,
        memory_manager,
        mock_rag_service
    ):
        """Should handle missing buyer persona gracefully."""
        mock_rag_service.search_relevant_docs.return_value = []
        
        with patch.object(memory_manager, '_get_buyer_persona', return_value=None):
            with patch.object(memory_manager, '_count_user_documents', return_value=0):
                context = await memory_manager.get_context(
                    chat_id=uuid4(),
                    project_id=uuid4(),
                    current_message="Test"
                )
        
        assert context['buyer_persona'] is None
        assert context['has_buyer_persona'] is False
        assert context['documents_count'] == 0
    
    @pytest.mark.asyncio
    async def test_add_message_to_short_term_user(self, memory_manager):
        """Should add user message to short-term memory."""
        await memory_manager.add_message_to_short_term("user", "Hello")
        
        # Verify message was added
        messages = memory_manager.short_term.chat_memory.messages
        assert len(messages) > 0
        assert messages[-1].content == "Hello"
    
    @pytest.mark.asyncio
    async def test_add_message_to_short_term_assistant(self, memory_manager):
        """Should add assistant message to short-term memory."""
        await memory_manager.add_message_to_short_term("assistant", "Hi there")
        
        # Verify message was added
        messages = memory_manager.short_term.chat_memory.messages
        assert len(messages) > 0
        assert messages[-1].content == "Hi there"
    
    @pytest.mark.asyncio
    async def test_short_term_memory_window_limit(self, memory_manager):
        """Short-term memory should only keep last k=10 messages."""
        # Add 15 messages
        for i in range(15):
            await memory_manager.add_message_to_short_term("user", f"Message {i}")
        
        # Only last 10 should remain
        messages = memory_manager.short_term.chat_memory.messages
        assert len(messages) == 10
        
        # Should have messages 5-14
        assert messages[0].content == "Message 5"
        assert messages[-1].content == "Message 14"
