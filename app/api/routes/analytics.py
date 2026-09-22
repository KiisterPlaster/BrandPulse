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
)
def share_of_voice(
    marca: str = Query(min_length=1),
    repository: RespostaRepository = Depends(get_repository),
):
    return calcular_share_of_voice(
        repository=repository,
        marca=marca,
    )


@router.get(
    "/top-citacoes",
    response_model=list[TopCitacaoResponse],
)
def top_citacoes(
    n: int = Query(default=5, ge=1),
    repository: RespostaRepository = Depends(get_repository),
):
    respostas = repository.listar()

    return obter_top_citacoes(
        respostas=respostas,
        n=n,
    )
