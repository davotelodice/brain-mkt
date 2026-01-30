"""
MCP server: marketing-brain

Objetivo (TAREA 9):
- Exponer herramientas READ-ONLY del sistema Marketing Brain para que Cursor/IA pueda:
  - listar chats
  - inspeccionar análisis (buyer persona + foro + dolor + journey)
  - (futuro) generar ideas de contenido usando el backend o un LLM separado

⚠️ Importante:
- Este servidor NO toca el backend ni la BD existente.
- Solo hace llamadas HTTP al backend ya desplegado.
- Si BACKEND_API_URL o BACKEND_API_TOKEN no están configurados, las tools fallan
  con un error claro (no silencioso).
"""

from __future__ import annotations

import json
import os
from typing import Any

import httpx
from mcp.server.fastmcp import FastMCP

# Crear instancia del servidor MCP
mcp = FastMCP("marketing-brain")


def _get_backend_config() -> tuple[str, str]:
    """Lee configuración del backend desde variables de entorno.

    BACKEND_API_URL: base URL del backend (ej: http://localhost:8000)
    BACKEND_API_TOKEN: token JWT o API key para Authorization (si aplica)
    """
    base_url = os.getenv("BACKEND_API_URL", "http://localhost:8000")
    token = os.getenv("BACKEND_API_TOKEN", "")
    return base_url.rstrip("/"), token


async def _backend_get(path: str) -> Any:
    """Helper genérico para GET al backend con manejo de errores claro."""
    base_url, token = _get_backend_config()
    url = f"{base_url}{path}"

    headers: dict[str, str] = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    async with httpx.AsyncClient(timeout=15) as client:
        try:
            resp = await client.get(url, headers=headers)
        except httpx.RequestError as e:
            raise RuntimeError(f"Error de red al llamar backend ({url}): {e}") from e

    if resp.status_code == 401:
        raise RuntimeError(
            "Backend devolvió 401 (no autorizado). "
            "Revisa BACKEND_API_TOKEN o la configuración de auth."
        )
    if not resp.is_success:
        try:
            detail = resp.json().get("detail")
        except Exception:
            detail = resp.text
        raise RuntimeError(
            f"Backend devolvió {resp.status_code} para {url}: {detail}"
        )

    try:
        return resp.json()
    except ValueError as e:
        raise RuntimeError(
            f"Respuesta del backend no es JSON válido para {url}: {resp.text[:200]}..."
        ) from e


@mcp.tool()
async def mb_list_chats() -> str:
    """Lista todos los chats del usuario/proyecto actual (vista resumida).

    IMPORTANTE:
    - Depende de que BACKEND_API_URL apunte al backend autenticado.
    - Usa las credenciales asociadas al BACKEND_API_TOKEN (si se usa JWT/API key).

    Devuelve:
    - JSON con la lista de chats tal como el endpoint `/api/chats` del backend.
    """
    data = await _backend_get("/api/chats")
    return json.dumps(data, ensure_ascii=False, indent=2)


@mcp.tool()
async def mb_get_chat_analysis(chat_id: str) -> str:
    """Obtiene el análisis completo de un chat (buyer persona + foro + dolor + journey).

    Args:
        chat_id: UUID del chat (string).

    Devuelve:
        JSON con estructura de `ChatAnalysisResponse` del backend:
        - buyer_persona
        - has_buyer_persona
        - has_forum_simulation
        - has_pain_points
        - has_customer_journey
    """
    path = f"/api/chats/{chat_id}/analysis"
    data = await _backend_get(path)
    return json.dumps(data, ensure_ascii=False, indent=2)


@mcp.tool()
def mb_generate_content_ideas_stub() -> str:
    """(Stub) Placeholder para futura integración con generación de contenido.

    NOTA:
    - No implementamos aquí la generación de contenido para NO duplicar lógica
      del `ContentGeneratorAgent` del backend ni tocar el sistema actual.
    - En una iteración futura, este tool podría:
        - llamar a un endpoint dedicado de generación (si se crea),
        - o construir prompts a partir de `mb_get_chat_analysis` + LLM separado.
    """
    return (
        "mb_generate_content_ideas aún no está implementado en este MCP.\n"
        "Usa el chat normal del sistema para generar ideas, o extiende este tool "
        "en una iteración futura conectándolo al ContentGeneratorAgent."
    )


if __name__ == "__main__":
    import sys
    
    # Determinar transporte según argumento o variable de entorno
    # - stdio: para uso local con Cursor/Claude Desktop
    # - http: para Docker/deployment (expone en 0.0.0.0:8080)
    transport = os.getenv("MCP_TRANSPORT", "stdio")
    if len(sys.argv) > 1:
        transport = sys.argv[1]
    
    # Normalizar alias
    if transport in ("http", "streamable-http"):
        # Para Docker: usar uvicorn directamente con la app ASGI
        import uvicorn
        
        host = os.getenv("MCP_HOST", "0.0.0.0")
        port = int(os.getenv("MCP_PORT", "8080"))
        
        # Obtener la app ASGI de FastMCP
        app = mcp.streamable_http_app()
        
        uvicorn.run(app, host=host, port=port)
    else:
        # STDIO para uso local
        mcp.run(transport="stdio")
