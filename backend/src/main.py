"""FastAPI main application."""
import logging
import os
import time

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from .api import auth, chat, documents

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Marketing Second Brain API",
    description="AI-powered marketing strategy assistant",
    version="0.1.0"
)

# CORS configuration
ALLOWED_ORIGINS = os.getenv("BACKEND_CORS_ORIGINS", "http://localhost:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ⚡ GOTCHA 3: Middleware que respeta endpoints de streaming
@app.middleware("http")
async def logging_middleware(request: Request, call_next):
    """
    Log requests but SKIP body reading for streaming endpoints.

    GOTCHA 3: Reading request.body() breaks streaming!
    Solution: Exclude /stream endpoints from body logging.
    """
    # Lista de paths que usan streaming (SSE)
    streaming_paths = ["/stream", "/sse"]

    # Check if this is a streaming endpoint
    is_streaming = any(path in request.url.path for path in streaming_paths)

    start_time = time.time()

    if is_streaming:
        # ✅ NO read body, pass directly
        logger.info(f"[STREAM] {request.method} {request.url.path}")
        response = await call_next(request)
    else:
        # ✅ Normal logging with body (for non-streaming)
        try:
            body = await request.body()
            logger.info(
                f"[REQ] {request.method} {request.url.path} - "
                f"Body: {body[:200].decode() if body else 'empty'}"
            )
        except Exception as e:
            logger.warning(f"Could not read body: {e}")

        response = await call_next(request)

    # Log response time
    duration_ms = (time.time() - start_time) * 1000
    logger.info(
        f"[RES] {request.method} {request.url.path} - "
        f"Status: {response.status_code} - Duration: {duration_ms:.2f}ms"
    )

    return response

# Include routers
app.include_router(auth.router)
app.include_router(chat.router)
app.include_router(documents.router)


@app.get("/")
async def root() -> dict[str, str]:
    """Root endpoint."""
    return {"message": "Marketing Second Brain API", "status": "running"}


@app.get("/health")
async def health() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "healthy"}
