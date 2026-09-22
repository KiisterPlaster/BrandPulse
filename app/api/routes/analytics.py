from fastapi import APIRouter, Depends, Query

from app.database.connection import SessionLocal
from app.repositories.respostas import RespostaRepository
from app.schemas.analytics import (
    ShareOfVoiceResponse,
    TopCitacaoResponse,
)
from app.services.analytics import (
    calcular_share_of_voice,
    obter_top_citacoes,
)

router = APIRouter()


def get_repository():
    session = SessionLocal()

    try:
        yield RespostaRepository(session)
    finally:
        session.close()


@router.get(
    "/share-of-voice",
    response_model=ShareOfVoiceResponse,
    summary="Calcula o Share of Voice de uma marca",
    description=(
        "Retorna a participação de uma marca entre as respostas "
        "armazenadas na aplicação."
    ),
    response_description="Dados de Share of Voice da marca.",
)
def share_of_voice(
    marca: str = Query(
        min_length=1,
        description="Nome da marca que será analisada.",
        examples=["Acme"],
    ),
    repository: RespostaRepository = Depends(get_repository),
):
    return calcular_share_of_voice(
        repository=repository,
        marca=marca,
    )


@router.get(
    "/top-citacoes",
    response_model=list[TopCitacaoResponse],
    summary="Retorna as respostas com mais citações",
    description=(
        "Retorna as respostas que possuem maior quantidade de "
        "citações de marcas, ordenadas de acordo com o score calculado."
    ),
    response_description="Lista das respostas com maior número de citações.",
)
def top_citacoes(
    n: int = Query(
        default=5,
        ge=1,
        description="Quantidade máxima de respostas a serem retornadas.",
        examples=[5],
    ),
    repository: RespostaRepository = Depends(get_repository),
):
    respostas = repository.listar()

    return obter_top_citacoes(
        respostas=respostas,
        n=n,
    )
