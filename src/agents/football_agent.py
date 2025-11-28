"""
Módulo principal del agente de fútbol.
Orquesta las interacciones del usuario con el LLM y las herramientas usando ReAct.
"""

from datetime import date, datetime
from typing import Any, Optional

from langchain.agents import create_agent

from agents.prompts import match_analysis_prompt, system_prompt
from agents.tools import tools
from core.config import settings
from models.schemas import ChatResponse, MatchRecommendationResponse


class FootballAgent:
    """
    Agente de fútbol que coordina las respuestas del sistema.
    """

    def __init__(self, user_name: Optional[str] = None):
        """
        Inicializa el agente con ReAct pattern.

        Args:
            user_name: Nombre del usuario para personalización (opcional)
        """
        prompt_text = (
            system_prompt.format(
                user_name=user_name, today=date.today().strftime("%Y-%m-%d")
            )
            if user_name
            else system_prompt.format(today=date.today().strftime("%Y-%m-%d"))
        )
        self.agent: Any = create_agent(
            model=f"groq:{settings.GROQ_MODEL}", tools=tools, system_prompt=prompt_text
        )

    async def process_message(
        self, message: str, session_id: Optional[str] = None
    ) -> ChatResponse:
        """
        Procesa un mensaje del usuario.

        Args:
            message: Mensaje del usuario
            session_id: ID de sesión para mantener contexto (opcional)

        Returns:
            ChatResponse con la respuesta y metadata
        """
        try:
            result = self.agent.invoke(
                {"messages": [{"role": "user", "content": message}]}
            )
            last_message = result["messages"][-1]
            used_tools = []
            for msg in result["messages"]:
                if hasattr(msg, "tool_calls") and msg.tool_calls:
                    used_tools.extend([tc["name"] for tc in msg.tool_calls])
            return ChatResponse(
                response=last_message.content,
                confidence=0.85,
                sources=["Conocimiento del modelo + Tools"]
                if used_tools
                else ["Conocimiento del modelo"],
                used_tools=used_tools if used_tools else None,
                timestamp=datetime.now(),
            )

        except Exception as e:
            return ChatResponse(
                response=f"Lo siento, hubo un error al procesar tu solicitud: {str(e)}",
                confidence=0.0,
                sources=[],
                used_tools=None,
                timestamp=datetime.now(),
            )

    async def analyze_match(
        self, home_team: str, away_team: str, match_date: str
    ) -> MatchRecommendationResponse:
        """
        Analiza un partido futuro y genera una recomendación.

        Args:
            home_team: Equipo local
            away_team: Equipo visitante
            match_date: Fecha del partido

        Returns:
            MatchRecommendationResponse con el análisis completo
        """
        try:
            # Prompt específico para análisis de partido
            prompt_text = match_analysis_prompt.format(
                home_team=home_team, away_team=away_team, match_date=match_date
            )

            # Se obtiene respuesta del agente
            result = self.agent.invoke(
                {"messages": [{"role": "user", "content": prompt_text}]}
            )
            last_message = result["messages"][-1]
            used_tools = []
            for msg in result["messages"]:
                if hasattr(msg, "tool_calls") and msg.tool_calls:
                    used_tools.extend([tc["name"] for tc in msg.tool_calls])

            # Se retorna recomendacion
            return MatchRecommendationResponse(
                recommendation=last_message.content,
                prediction="Análisis basado en conocimiento"
                + (" + herramientas" if used_tools else " general"),
                key_factors=[
                    "Forma reciente de los equipos",
                    "Historial de enfrentamientos",
                    "Ventaja de jugar en casa",
                ],
                used_tools=used_tools if used_tools else None,
                confidence=0.85,
            )

        except Exception as e:
            return MatchRecommendationResponse(
                recommendation=f"Error al generar análisis: {str(e)}",
                prediction="Error",
                key_factors=[],
                used_tools=None,
                confidence=0.0,
            )
