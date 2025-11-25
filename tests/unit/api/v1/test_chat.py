"""
Pruebas unitarias para rutas de chat del agente de fútbol en la API v1.
"""

from datetime import datetime
from unittest.mock import Mock, patch

import pytest
from fastapi import status
from fastapi.testclient import TestClient

from main import app
from models.schemas import (
    ChatRequest,
    ChatResponse,
    MatchRecommendationRequest,
    MatchRecommendationResponse,
)

client = TestClient(app)


@pytest.fixture
def mock_football_agent():
    """Mock del agente de fútbol (LangGraph)."""
    return Mock()


@pytest.fixture
def sample_chat_request():
    """Request de ejemplo para chat."""
    return ChatRequest(
        message="¿Cuál fue el resultado del último partido del Real Madrid?",
        session_id="test-session-123",
    )


@pytest.fixture
def sample_chat_response():
    """Response de ejemplo del agente."""
    return ChatResponse(
        response="El Real Madrid ganó 3-1 contra el Barcelona en el último clásico.",
        confidence=0.95,
        sources=["API-Football", "ESPN"],
        timestamp=datetime.now(),
    )


@pytest.mark.unit
@pytest.mark.api
@pytest.mark.smoke
class TestHealthCheck:
    """Tests para el endpoint de health check del chat."""

    def test_health_check_should_return_200_when_service_is_healthy(self):
        """Debe retornar 200 con status healthy cuando el servicio funciona correctamente."""
        # Act
        response = client.get("/health")

        # Assert
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["status"] == "healthy"
        assert data["version"] == "1.0.0"
        assert "timestamp" in data


@pytest.mark.unit
@pytest.mark.api
class TestChatEndpoint:
    """Tests para el endpoint principal de chat."""

    def test_chat_should_return_200_when_valid_message(self, sample_chat_request):
        """Debe retornar 200 con respuesta del agente cuando el mensaje es válido."""
        # Arrange
        # TODO: Mockear el agente de fútbol cuando se implemente

        # Act
        response = client.post("/api/v1/chat/", json=sample_chat_request.model_dump())

        # Assert
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "response" in data
        assert isinstance(data["response"], str)
        assert len(data["response"]) > 0

    def test_chat_should_return_422_when_empty_message(self):
        """Debe retornar 422 cuando el mensaje está vacío."""
        # Act
        response = client.post("/api/v1/chat/", json={"message": ""})

        # Assert
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_chat_should_return_422_when_message_too_long(self):
        """Debe retornar 422 cuando el mensaje excede el límite de caracteres."""
        # Arrange
        long_message = "a" * 1001  # Excede max_length=1000

        # Act
        response = client.post("/api/v1/chat/", json={"message": long_message})

        # Assert
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_chat_should_accept_message_without_session_id(self):
        """Debe aceptar mensaje sin session_id (campo opcional)."""
        # Act
        response = client.post(
            "/api/v1/chat/", json={"message": "¿Quién ganó la Champions League?"}
        )

        # Assert
        assert response.status_code == status.HTTP_200_OK

    def test_chat_should_return_confidence_in_response(self):
        """Debe incluir campo de confianza en la respuesta."""
        # Act
        response = client.post("/api/v1/chat/", json={"message": "¿Resultados de hoy?"})

        # Assert
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "confidence" in data

    def test_chat_should_return_timestamp_in_response(self):
        """Debe incluir timestamp en la respuesta."""
        # Act
        response = client.post("/api/v1/chat/", json={"message": "¿Próximos partidos?"})

        # Assert
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "timestamp" in data


@pytest.mark.unit
@pytest.mark.api
class TestMatchRecommendation:
    """Tests para el endpoint de recomendaciones de partidos."""

    def test_recommend_should_return_200_when_valid_teams(self):
        """Debe retornar 200 con recomendación cuando los equipos son válidos."""
        # Arrange
        request_data = {
            "home_team": "Real Madrid",
            "away_team": "Barcelona",
            "match_date": "2025-12-01",
        }

        # Act
        response = client.post("/api/v1/chat/recommend", json=request_data)

        # Assert
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "recommendation" in data
        assert isinstance(data["recommendation"], str)

    def test_recommend_should_return_422_when_missing_teams(self):
        """Debe retornar 422 cuando faltan datos de equipos."""
        # Act
        response = client.post(
            "/api/v1/chat/recommend",
            json={"home_team": "Real Madrid"},  # Falta away_team
        )

        # Assert
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_recommend_should_accept_request_without_match_date(self):
        """Debe aceptar request sin fecha de partido (campo opcional)."""
        # Act
        response = client.post(
            "/api/v1/chat/recommend",
            json={"home_team": "Manchester United", "away_team": "Liverpool"},
        )

        # Assert
        assert response.status_code == status.HTTP_200_OK

    def test_recommend_should_include_prediction_in_response(self):
        """Debe incluir predicción en la respuesta."""
        # Act
        response = client.post(
            "/api/v1/chat/recommend",
            json={"home_team": "Bayern Munich", "away_team": "Borussia Dortmund"},
        )

        # Assert
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "prediction" in data

    def test_recommend_should_include_key_factors_in_response(self):
        """Debe incluir factores clave en la respuesta."""
        # Act
        response = client.post(
            "/api/v1/chat/recommend",
            json={"home_team": "PSG", "away_team": "Marseille"},
        )

        # Assert
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "key_factors" in data
        assert isinstance(data["key_factors"], list)

    def test_recommend_should_include_confidence_score(self):
        """Debe incluir score de confianza en la recomendación."""
        # Act
        response = client.post(
            "/api/v1/chat/recommend",
            json={"home_team": "Juventus", "away_team": "AC Milan"},
        )

        # Assert
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "confidence" in data
        if data["confidence"] is not None:
            assert 0.0 <= data["confidence"] <= 1.0
