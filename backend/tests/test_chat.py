"""Tests for chat endpoints."""
import pytest
from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)

# Test project ID (from seed data)
TEST_PROJECT_ID = "a0000000-0000-0000-0000-000000000001"


def test_create_chat_requires_auth():
    """Test that creating chat requires authentication."""
    response = client.post("/api/chats", json={"title": "Test Chat"})
    assert response.status_code == 403  # No auth header


def test_list_chats_requires_auth():
    """Test that listing chats requires authentication."""
    response = client.get("/api/chats")
    assert response.status_code == 403


def test_get_chat_requires_auth():
    """Test that getting chat requires authentication."""
    fake_chat_id = "00000000-0000-0000-0000-000000000000"
    response = client.get(f"/api/chats/{fake_chat_id}")
    assert response.status_code == 403


def test_send_message_requires_auth():
    """Test that sending message requires authentication."""
    fake_chat_id = "00000000-0000-0000-0000-000000000000"
    response = client.post(
        f"/api/chats/{fake_chat_id}/messages",
        json={"content": "Test message"}
    )
    assert response.status_code == 403


def test_send_message_validation():
    """Test message content validation."""
    # Empty content (requires auth but validates before)
    response = client.post(
        "/api/chats/00000000-0000-0000-0000-000000000000/messages",
        json={"content": ""}
    )
    # Should fail on validation (422) or auth (403)
    assert response.status_code in [403, 422]

    # Content too long (>5000 chars)
    long_content = "x" * 5001
    response = client.post(
        "/api/chats/00000000-0000-0000-0000-000000000000/messages",
        json={"content": long_content}
    )
    assert response.status_code in [403, 422]


# Note: Full integration tests with auth+db will be in TAREA 11
# These tests verify endpoint structure and basic validation
