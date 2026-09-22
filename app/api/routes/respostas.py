from fastapi import APIRouter, Depends, status

from app.database.connection import SessionLocal
from app.models.mencao import Mencao
from app.models.resposta import Resposta
from app.repositories.respostas import RespostaRepository
from app.schemas.respostas import RespostaCreate, RespostaResponse
from app.services.mencoes import detectar_mencoes

router = APIRouter()


def get_repository():
    session = SessionLocal()

    try:
        yield RespostaRepository(session)
    finally:
        session.close()


@router.post(
    "/respostas",
    response_model=list[RespostaResponse],
    status_code=status.HTTP_201_CREATED,
)
def criar_respostas(
    dados: list[RespostaCreate],
    repository: RespostaRepository = Depends(get_repository),
):
    respostas = []

    for dado in dados:
        mencoes_detectadas = detectar_mencoes(dado.resposta_texto)

        mencoes = [
            Mencao(
                marca=marca,
                ocorrencias=ocorrencias,
            )
            for marca, ocorrencias in mencoes_detectadas.items()
        ]

        resposta = Resposta(
            id=dado.id,
            pergunta=dado.pergunta,
            plataforma=dado.plataforma,
            modelo=dado.modelo,
            resposta_texto=dado.resposta_texto,
            data_hora=dado.data_hora,
            sentimento=dado.sentimento,
            mencoes=mencoes,
        )

        repository.criar(resposta)
        respostas.append(resposta)

    return respostas
