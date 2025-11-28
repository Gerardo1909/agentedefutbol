# ⚽ Agente de Fútbol

> Chatbot inteligente especializado en fútbol construido con **FastAPI**, **LangChain** y **LangGraph**

**Desarrollado por:** Gerardo Toboso

![CI Status](https://github.com/Gerardo1909/agentedefutbol/actions/workflows/ci.yml/badge.svg)
[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.121+-green.svg)](https://fastapi.tiangolo.com)
[![LangChain](https://img.shields.io/badge/LangChain-1.0+-orange.svg)](https://docs.langchain.com)

## Descripción

Agente conversacional que responde preguntas sobre fútbol, analiza partidos y proporciona recomendaciones. Construido siguiendo las mejores prácticas de LangChain/LangGraph observadas en proyectos profesionales.

### Características Actuales 

- **Chat interactivo** sobre fútbol usando LLM (Groq)
- **Análisis de partidos** con prompts estructurados
- **Arquitectura modular** con separación de responsabilidades
- **Tools preparadas** para futuras integraciones (stubs)
- **FastAPI** con validación Pydantic
- **Tests** configurados con pytest

## Inicio Rápido

### Prerequisitos

- Python 3.13+
- [uv](https://github.com/astral-sh/uv) (recomendado) o pip

### Instalación con uv

```bash
# Instalar uv (si no lo tienes)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clonar el repositorio
git clone https://github.com/Gerardo1909/agentedefutbol.git
cd agentedefutbol

# Instalar dependencias
uv sync

# Configurar variables de entorno
cp .env.example .env
# Editar .env con tu GROQ_API_KEY
```

### Ejecutar la API

```bash
# Con uv
uv run uvicorn src.main:app --reload

# O activar el entorno virtual
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows
uvicorn src.main:app --reload
```

La API estará disponible en: `http://localhost:8000`

Documentación interactiva: `http://localhost:8000/docs`

## Testing

```bash
# Ejecutar todos los tests
uv run pytest

# Tests unitarios solamente
uv run pytest tests/unit -v

# Tests con cobertura
uv run pytest --cov=src --cov-report=html

# Tests smoke (rápidos)
uv run pytest -m smoke
```

## Estructura del Proyecto

```
agentedefutbol/
├── .github/
│   └── workflows/
│       └── ci.yml           # GitHub Actions con uv
├── src/
│   ├── agents/              # Lógica del agente
│   ├── api/                 # Endpoints FastAPI
│   ├── core/                # Configuración y utilidades
│   ├── models/              # Esquemas Pydantic
│   └── services/            # Servicios (LLM, APIs externas)
├── tests/
│   ├── unit/                # Tests unitarios
│   ├── integration/         # Tests de integración
│   ├── e2e/                 # Tests end-to-end
│   └── conftest.py          # Fixtures compartidos y configuraciones varias
├── .env.example             # Plantilla de variables de entorno
├── pyproject.toml           # Configuración del proyecto
├── pytest.ini               # Configuración de pytest
└── README.md                # Este archivo
```

## Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT. Ver [LICENSE](LICENSE) para más detalles.