"""LLM Service - Configurable provider (OpenAI/OpenRouter) with retry logic."""

import logging
import os
from collections.abc import AsyncIterator
from typing import cast

from openai import APIError, APITimeoutError, AsyncOpenAI, RateLimitError
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

logger = logging.getLogger(__name__)

# Prefijos de modelos que requieren OpenRouter
OPENROUTER_PREFIXES = ("anthropic/", "deepseek/", "meta-llama/", "google/", "mistral/")


class LLMService:
    """
    Configurable LLM service supporting OpenAI and OpenRouter.

    Provider selection:
    - Default provider via LLM_PROVIDER environment variable
    - Auto-detection: modelos con prefijo (anthropic/, deepseek/) usan OpenRouter

    Includes automatic retry with exponential backoff for transient errors.
    """

    def __init__(self):
        """Initialize LLM service with BOTH clients available."""
        self.default_provider = os.getenv("LLM_PROVIDER", "openai").lower()

        # Cliente OpenAI (siempre disponible si hay API key)
        openai_key = os.getenv("OPENAI_API_KEY")
        self.openai_client = AsyncOpenAI(api_key=openai_key) if openai_key else None

        # Cliente OpenRouter (siempre disponible si hay API key)
        openrouter_key = os.getenv("OPENROUTER_API_KEY")
        self.openrouter_client = AsyncOpenAI(
            api_key=openrouter_key,
            base_url="https://openrouter.ai/api/v1"
        ) if openrouter_key else None

        # Modelo default según provider configurado
        if self.default_provider == "openrouter":
            self.model = os.getenv("OPENROUTER_MODEL", "anthropic/claude-3.5-sonnet")
            self.client = self.openrouter_client
            self.provider = "openrouter"
        else:
            self.model = os.getenv("OPENAI_MODEL", "gpt-4o")
            self.client = self.openai_client
            self.provider = "openai"

    def _get_client_for_model(self, model: str) -> tuple[AsyncOpenAI, str]:
        """
        Determina qué cliente usar según el modelo.

        Returns:
            tuple: (client, provider_name)
        """
        # Si el modelo tiene prefijo de OpenRouter, usar OpenRouter
        if model.startswith(OPENROUTER_PREFIXES):
            if not self.openrouter_client:
                raise ValueError(
                    f"Model '{model}' requires OpenRouter but OPENROUTER_API_KEY not set"
                )
            return self.openrouter_client, "openrouter"

        # Modelos de OpenAI (gpt-*, o1-*, o3-*)
        if not self.openai_client:
            raise ValueError(
                f"Model '{model}' requires OpenAI but OPENAI_API_KEY not set"
            )
        return self.openai_client, "openai"

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((RateLimitError, APITimeoutError, APIError))
    )
    async def generate(
        self,
        prompt: str,
        system: str = "",
        max_tokens: int = 4096,
        temperature: float = 0.7,
        model: str | None = None,
    ) -> str:
        """
        Generate text synchronously (for analysis, planning).

        Args:
            prompt: User message/prompt
            system: System message (optional)
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature (0.0-1.0)

        Returns:
            Generated text

        Raises:
            RateLimitError: After 3 retry attempts
            APITimeoutError: After 3 retry attempts
            APIError: After 3 retry attempts
        """
        messages = []

        if system:
            messages.append({"role": "system", "content": system})

        messages.append({"role": "user", "content": prompt})

        effective_model = model or self.model
        client, provider = self._get_client_for_model(effective_model)
        logger.info("[LLM] generate model=%s provider=%s", effective_model, provider)

        response = await client.chat.completions.create(
            model=effective_model,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature
        )

        content = response.choices[0].message.content
        if content is None:
            raise ValueError("LLM returned None content")
        return cast(str, content)

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((RateLimitError, APITimeoutError, APIError))
    )
    async def stream(
        self,
        prompt: str,
        system: str = "",
        max_tokens: int = 4096,
        temperature: float = 0.7,
        model: str | None = None,
    ) -> AsyncIterator[str]:
        """
        Generate text with streaming (for real-time chat responses).

        Args:
            prompt: User message/prompt
            system: System message (optional)
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature (0.0-1.0)

        Yields:
            Text chunks as they are generated

        Raises:
            RateLimitError: After 3 retry attempts
            APITimeoutError: After 3 retry attempts
            APIError: After 3 retry attempts
        """
        messages = []

        if system:
            messages.append({"role": "system", "content": system})

        messages.append({"role": "user", "content": prompt})

        effective_model = model or self.model
        client, provider = self._get_client_for_model(effective_model)
        logger.info("[LLM] stream model=%s provider=%s", effective_model, provider)

        stream = await client.chat.completions.create(
            model=effective_model,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
            stream=True
        )

        async for chunk in stream:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((RateLimitError, APITimeoutError, APIError))
    )
    async def generate_with_messages(
        self,
        messages: list[dict[str, str]],
        max_tokens: int = 4096,
        temperature: float = 0.7,
        model: str | None = None,
    ) -> str:
        """
        Generate text with full conversation history.

        Args:
            messages: List of message dicts with "role" and "content"
                Format: [{"role": "system", "content": "..."},
                         {"role": "user", "content": "..."},
                         {"role": "assistant", "content": "..."}, ...]
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature (0.0-1.0)

        Returns:
            Generated text

        Raises:
            ValueError: If messages format is invalid
            RateLimitError: After 3 retry attempts
            APITimeoutError: After 3 retry attempts
            APIError: After 3 retry attempts
        """
        # CRÍTICO: Validar formato de messages
        if not messages or not isinstance(messages, list):
            raise ValueError("messages must be a non-empty list")

        for i, msg in enumerate(messages):
            if not isinstance(msg, dict):
                raise ValueError(f"Message {i} must be a dict, got {type(msg)}")
            if "role" not in msg or "content" not in msg:
                raise ValueError(f"Message {i} must have 'role' and 'content' keys")
            if msg["role"] not in ["system", "user", "assistant"]:
                raise ValueError(
                    f"Message {i} has invalid role: {msg['role']}. "
                    "Must be 'system', 'user', or 'assistant'"
                )

        effective_model = model or self.model
        client, provider = self._get_client_for_model(effective_model)
        logger.info("[LLM] generate_with_messages model=%s provider=%s", effective_model, provider)

        response = await client.chat.completions.create(
            model=effective_model,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature
        )

        content = response.choices[0].message.content
        if content is None:
            raise ValueError("LLM returned None content")
        return cast(str, content)

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((RateLimitError, APITimeoutError, APIError))
    )
    async def stream_with_messages(
        self,
        messages: list[dict[str, str]],
        max_tokens: int = 4096,
        temperature: float = 0.7,
        model: str | None = None,
    ) -> AsyncIterator[str]:
        """
        Generate text with streaming and full conversation history.

        Args:
            messages: List of message dicts with "role" and "content"
                Format: [{"role": "system", "content": "..."},
                         {"role": "user", "content": "..."},
                         {"role": "assistant", "content": "..."}, ...]
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature (0.0-1.0)

        Yields:
            Text chunks as they are generated

        Raises:
            ValueError: If messages format is invalid
            RateLimitError: After 3 retry attempts
            APITimeoutError: After 3 retry attempts
            APIError: After 3 retry attempts
        """
        # CRÍTICO: Validar formato de messages (misma validación que generate_with_messages)
        if not messages or not isinstance(messages, list):
            raise ValueError("messages must be a non-empty list")

        for i, msg in enumerate(messages):
            if not isinstance(msg, dict):
                raise ValueError(f"Message {i} must be a dict, got {type(msg)}")
            if "role" not in msg or "content" not in msg:
                raise ValueError(f"Message {i} must have 'role' and 'content' keys")
            if msg["role"] not in ["system", "user", "assistant"]:
                raise ValueError(
                    f"Message {i} has invalid role: {msg['role']}. "
                    "Must be 'system', 'user', or 'assistant'"
                )

        effective_model = model or self.model
        client, provider = self._get_client_for_model(effective_model)
        logger.info("[LLM] stream_with_messages model=%s provider=%s", effective_model, provider)

        stream = await client.chat.completions.create(
            model=effective_model,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
            stream=True
        )

        async for chunk in stream:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content
