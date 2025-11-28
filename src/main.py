"""
Módulo principal de la aplicación.
"""

import uvicorn
from fastapi import FastAPI, status, APIRouter
from api.v1.chat import router as chat_router
from models.schemas import HealthResponse
from core.config import settings

app = FastAPI(
    title=settings.API_TITLE,
    description=settings.API_DESCRIPTION,
    version=settings.API_VERSION,
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
