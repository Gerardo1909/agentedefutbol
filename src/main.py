"""
Módulo principal de la aplicación.
"""

from pathlib import Path

import uvicorn
from dotenv import load_dotenv
from fastapi import APIRouter, FastAPI, status

# Cargar variables de entorno ANTES de importar cualquier configuración
load_dotenv(Path(__file__).parent.parent / ".env")

from api.v1.chat import router as chat_router
from core.config import Settings
from models.schemas import HealthResponse

app_settings = Settings()

app = FastAPI(
    title=app_settings.api_title,
    description=app_settings.api_description,
    version=app_settings.api_version,
)

health_router = APIRouter(prefix="/health", tags=["Estado de salud de la aplicación."])


# Ruta de salud
@health_router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=HealthResponse,
    summary="Health check del servicio",
)
async def health_check():
    """Verifica que el servicio esté funcionando correctamente."""
    return HealthResponse(status="healthy", version="1.0.0")


# Incluir routers
app.include_router(chat_router)
app.include_router(health_router)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
