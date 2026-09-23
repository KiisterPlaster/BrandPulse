from fastapi import APIRouter, Depends, HTTPException, status

from app.database.connection import SessionLocal
from app.models.mencao import Mencao
from app.models.resposta import Resposta
from app.repositories.respostas import RespostaRepository
from app.schemas.respostas import RespostaCreate, RespostaResponse
from app.services.mencoes import detectar_mencoes
from app.services.plataformas import normalizar_plataforma

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
    summary="Cria novas respostas",
    description=(
        "Recebe uma lista de respostas, valida cada item individualmente, "
        "descarta os dados inválidos, detecta automaticamente as menções "
        "de marcas presentes no texto e persiste as respostas válidas "
        "e suas respectivas menções."
    ),
    response_description="Lista das respostas válidas criadas.",
)
def criar_respostas(
    dados: list[dict],
    repository: RespostaRepository = Depends(get_repository),
):
    respostas = []
    respostas_invalidas = []

    for dado in dados:
        try:
            resposta_validada = RespostaCreate.model_validate(dado)

        except Exception as erro:
            respostas_invalidas.append(
                {
                    "dados": dado,
                    "erro": str(erro),
                }
            )
            continue

        mencoes_detectadas = detectar_mencoes(resposta_validada.resposta_texto)

        mencoes = [
            Mencao(
                marca=marca,
                ocorrencias=ocorrencias,
            )
            for marca, ocorrencias in mencoes_detectadas.items()
        ]

        resposta = Resposta(
            resposta_id=resposta_validada.id,
            pergunta=resposta_validada.pergunta,
            plataforma=normalizar_plataforma(resposta_validada.plataforma),
            modelo=resposta_validada.modelo,
            resposta_texto=resposta_validada.resposta_texto,
            data_hora=resposta_validada.data_hora,
            sentimento=resposta_validada.sentimento,
            mencoes=mencoes,
        )

        if repository.existe_duplicata(resposta):
            continue

        repository.criar(resposta)
        respostas.append(resposta)

    if respostas:
        return respostas

    raise HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        detail={
            "message": (
                "Todos os dados enviados já estão no banco de dados "
                "ou você enviou apenas dados inválidos."
            ),
            "respostas_invalidas": respostas_invalidas,
        },
    )
