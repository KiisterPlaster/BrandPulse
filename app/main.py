from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from app.api import analytics_router, respostas_router
from app.core.limiter import limiter
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

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
        "http://127.0.0.1:5000",
        "http://localhost:5000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)


@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request, exc):
    return JSONResponse(status_code=429, content={"detail": "Rate limit exceeded"})


@app.exception_handler(404)
async def rota_nao_encontrada(
    request: Request,
    exc,
):
    return JSONResponse(
        status_code=404,
        content={
            "error": "rota_nao_encontrada",
            "message": f"A rota {request.url.path} não existe.",
        },
    )


app.include_router(analytics_router)
app.include_router(respostas_router)


if __name__ == "__main__":
    pass
