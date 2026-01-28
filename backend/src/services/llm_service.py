"""LLM Service - Configurable provider (OpenAI/OpenRouter) with retry logic."""

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


class LLMService:
    """
    Configurable LLM service supporting OpenAI and OpenRouter.

    Provider selection via LLM_PROVIDER environment variable:
    - "openai" (default): Uses OpenAI API directly
    - "openrouter": Uses OpenRouter API (supports multiple models including Claude)

    Includes automatic retry with exponential backoff for transient errors.
    """

    def __init__(self):
        """Initialize LLM service based on LLM_PROVIDER env var."""
        self.provider = os.getenv("LLM_PROVIDER", "openai").lower()

        if self.provider == "openai":
            self.client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            self.model = os.getenv("OPENAI_MODEL", "gpt-4o")
        elif self.provider == "openrouter":
            self.client = AsyncOpenAI(
                api_key=os.getenv("OPENROUTER_API_KEY"),
                base_url="https://openrouter.ai/api/v1"
            )
            self.model = os.getenv("OPENROUTER_MODEL", "anthropic/claude-3.5-sonnet")
        else:
            raise ValueError(
                f"Invalid LLM_PROVIDER: {self.provider}. "
                "Must be 'openai' or 'openrouter'"
            )

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
        temperature: float = 0.7
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

        response = await self.client.chat.completions.create(
            model=self.model,
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
        temperature: float = 0.7
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

        stream = await self.client.chat.completions.create(
            model=self.model,
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
        temperature: float = 0.7
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

        response = await self.client.chat.completions.create(
            model=self.model,
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
        temperature: float = 0.7
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

        stream = await self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
            stream=True
        )

        async for chunk in stream:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content
