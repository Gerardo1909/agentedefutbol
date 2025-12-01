"""
Módulo principal del agente de fútbol.
Orquesta las interacciones del usuario con el LLM y las herramientas usando ReAct.
"""

from datetime import date, datetime
from typing import Any, Optional

from langchain.agents import create_agent

from agents.prompts import match_analysis_prompt, system_prompt
from agents.tools import tools
from core.config import Settings
from core.logging import agent_logger
from models.schemas import ChatResponse, MatchRecommendationResponse

settings = Settings()


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
        agent_logger.info(f"Inicializando agente para usuario: {user_name or 'anonimo'}")
        prompt_text = (
            system_prompt.format(
                user_name=user_name, today=date.today().strftime("%Y-%m-%d")
            )
            if user_name
            else system_prompt.format(today=date.today().strftime("%Y-%m-%d"))
        )
        try:
            self.agent: Any = create_agent(
                model=f"groq:{settings.groq_model}", tools=tools, system_prompt=prompt_text
            )
            agent_logger.info(f"Agente inicializado correctamente con modelo {settings.groq_model}")
        except Exception as e:
            agent_logger.error(f"Error inicializando agente: {str(e)}")
            raise

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
        agent_logger.info(f"Procesando mensaje - Session: {session_id or 'none'} - Mensaje: {message[:100]}")
        try:
            result = await self.agent.ainvoke(
                {"messages": [{"role": "user", "content": message}]}
            )
            last_message = result["messages"][-1]

            used_tools = []
            for msg in result["messages"]:
                if hasattr(msg, "tool_calls") and msg.tool_calls:
                    tool_names = [tc["name"] for tc in msg.tool_calls]
                    used_tools.extend(tool_names)
                    agent_logger.info(f"Tools invocadas: {', '.join(tool_names)}")

            if not used_tools:
                agent_logger.info("Respuesta generada sin usar tools - Solo LLM")

            agent_logger.info(f"Mensaje procesado exitosamente - Tools usadas: {len(used_tools)}")
            return ChatResponse(
                response=last_message.content,
                confidence=0.85,
                sources=["Fuentes externas + LLM"] if used_tools else ["LLM"],
                used_tools=used_tools or None,
                timestamp=datetime.now(),
            )

        except Exception as e:
            agent_logger.error(f"Error procesando mensaje: {str(e)}", exc_info=True)
            return ChatResponse(
                response=f"Error al procesar tu solicitud: {str(e)}",
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
        agent_logger.info(f"Analizando partido: {home_team} vs {away_team} - Fecha: {match_date}")
        try:
            # Prompt específico para análisis de partido
            prompt_text = match_analysis_prompt.format(
                home_team=home_team, away_team=away_team, match_date=match_date
            )

            result = await self.agent.ainvoke(
                {"messages": [{"role": "user", "content": prompt_text}]}
            )
            last_message = result["messages"][-1]

            used_tools = []
            for msg in result["messages"]:
                if hasattr(msg, "tool_calls") and msg.tool_calls:
                    tool_names = [tc["name"] for tc in msg.tool_calls]
                    used_tools.extend(tool_names)
                    agent_logger.info(f"Tools usadas en analisis: {', '.join(tool_names)}")

            if not used_tools:
                agent_logger.warning("Analisis generado sin datos API - Solo conocimiento LLM")

            agent_logger.info(f"Analisis completado - {home_team} vs {away_team}")
            return MatchRecommendationResponse(
                recommendation=last_message.content,
                prediction="Fuentes externas" if used_tools else "Conocimiento general",
                key_factors=[
                    "Forma reciente",
                    "Historial directo",
                    "Ventaja local",
                ],
                used_tools=used_tools or None,
                confidence=0.85,
            )

        except Exception as e:
            agent_logger.error(f"Error analizando partido {home_team} vs {away_team}: {str(e)}", exc_info=True)
            return MatchRecommendationResponse(
                recommendation=f"Error: {str(e)}",
                prediction="Error",
                key_factors=[],
                used_tools=None,
                confidence=0.0,
            )
