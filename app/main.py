from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api import analytics_router, respostas_router
from app.database.init_db import create_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()

    yield


app = FastAPI(
    title="BrandPulse API",
    summary="API para análise de menções de marcas em respostas de IA",
    description="""
    API responsável por analisar a presença de marcas
    em respostas de ferramentas de Inteligência Artificial.

    Funcionalidades:

    - Análise de Share of Voice das marcas monitoradas
    - Análise de citações de marcas
    - Ranking das respostas com citações mais fortes
    - Ingestão de novas respostas
    - Detecção de menções às marcas
    - Persistência das respostas processadas

    Marcas monitoradas:

    - Acme
    - Zenith
    - Nimbus
    """,
    version="0.1.0",
    lifespan=lifespan,
)


app.include_router(analytics_router)
app.include_router(respostas_router)


if __name__ == "__main__":
    pass
