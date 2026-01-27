"""Tests for authentication endpoints."""
import pytest
from fastapi.testclient import TestClient
from uuid import UUID

from src.main import app

client = TestClient(app)

# Test project ID (from seed data)
TEST_PROJECT_ID = "a0000000-0000-0000-0000-000000000001"


def test_root_endpoint():
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Marketing Second Brain API", "status": "running"}


def test_health_endpoint():
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_register_endpoint_validation():
    """Test registration endpoint with invalid data."""
    # Missing required fields
    response = client.post("/api/auth/register", json={})
    assert response.status_code == 422
    
    # Invalid email
    response = client.post("/api/auth/register", json={
        "email": "not-an-email",
        "password": "Test1234",
        "project_id": TEST_PROJECT_ID
    })
    assert response.status_code == 422
    
    # Weak password (no uppercase)
    response = client.post("/api/auth/register", json={
        "email": "test@example.com",
        "password": "test1234",
        "project_id": TEST_PROJECT_ID
    })
    assert response.status_code == 422
    
    # Weak password (no digit)
    response = client.post("/api/auth/register", json={
        "email": "test@example.com",
        "password": "TestTest",
        "project_id": TEST_PROJECT_ID
    })
    assert response.status_code == 422


def test_login_endpoint_validation():
    """Test login endpoint with invalid data."""
    # Missing fields
    response = client.post("/api/auth/login", json={})
    assert response.status_code == 422
    
    # Invalid email format
    response = client.post("/api/auth/login", json={
        "email": "not-an-email",
        "password": "Test1234",
        "project_id": TEST_PROJECT_ID
    })
    assert response.status_code == 422


# Note: Full integration tests require database connection
# These will be added in TAREA 11 (Testing Completo)
