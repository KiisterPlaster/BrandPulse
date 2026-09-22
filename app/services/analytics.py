from app.models.resposta import Resposta
from app.repositories.respostas import RespostaRepository
from app.schemas.analytics import (
    PlatformShare,
    ShareOfVoiceResponse,
    TopCitacaoResponse,
)


def calcular_share_of_voice(
    repository: RespostaRepository,
    marca: str,
) -> ShareOfVoiceResponse:
    """
    Calcula o Share of Voice de uma marca.

    O cálculo considera a quantidade total de respostas e quantas
    dessas respostas possuem menção à marca informada.

    Também calcula o Share of Voice separadamente para cada plataforma.

    Retorna zero quando não existem respostas cadastradas.
    """
    respostas = repository.listar()

    total_respostas = len(respostas)

    if total_respostas == 0:
        return ShareOfVoiceResponse(
            marca=marca,
            respostas_com_mencao=0,
            total_respostas=0,
            percentual=0.0,
            por_plataforma=[],
        )

    respostas_com_marca = repository.listar_por_marca(marca)

    quantidade_com_mencao = len(respostas_com_marca)

    percentual = (quantidade_com_mencao / total_respostas) * 100

    plataformas = {}

    for resposta in respostas:
        plataformas.setdefault(resposta.plataforma, []).append(resposta)

    por_plataforma = []

    for plataforma, respostas_plataforma in plataformas.items():
        total = len(respostas_plataforma)

        ids_com_marca = {
            resposta.id
            for resposta in respostas_com_marca
            if resposta.plataforma == plataforma
        }

        com_mencao = len(ids_com_marca)

        percentual_plataforma = (com_mencao / total) * 100

        por_plataforma.append(
            PlatformShare(
                plataforma=plataforma,
                respostas_com_mencao=com_mencao,
                total_respostas=total,
                percentual=percentual_plataforma,
            )
        )

    return ShareOfVoiceResponse(
        marca=marca,
        respostas_com_mencao=quantidade_com_mencao,
        total_respostas=total_respostas,
        percentual=percentual,
        por_plataforma=por_plataforma,
    )


def calcular_score_citacao(resposta: Resposta) -> float:
    """
    Calcula o score de uma resposta com base nas menções.

    O score considera dois fatores:
    - quantidade de marcas distintas mencionadas, multiplicada por 2;
    - quantidade total de ocorrências das marcas.

    Quanto maior o score, maior a relevância da resposta
    para o ranking de citações.
    """
    marcas_distintas = len(resposta.mencoes)

    ocorrencias_totais = sum(mencao.ocorrencias for mencao in resposta.mencoes)

    return (marcas_distintas * 2) + ocorrencias_totais


def obter_top_citacoes(
    respostas: list[Resposta],
    n: int,
) -> list[TopCitacaoResponse]:
    """
    Retorna as respostas com maior score de citação.

    Apenas respostas que possuem pelo menos uma menção são
    consideradas no ranking.

    As respostas são ordenadas pelo score em ordem decrescente
    e limitadas à quantidade solicitada pelo parâmetro n.
    """
    respostas_com_mencoes = [resposta for resposta in respostas if resposta.mencoes]

    respostas_ordenadas = sorted(
        respostas_com_mencoes,
        key=calcular_score_citacao,
        reverse=True,
    )

    return [
        TopCitacaoResponse(
            resposta_id=resposta.id,
            plataforma=resposta.plataforma,
            modelo=resposta.modelo,
            resposta_texto=resposta.resposta_texto,
            marcas=[mencao.marca for mencao in resposta.mencoes],
            score=calcular_score_citacao(resposta),
        )
        for resposta in respostas_ordenadas[:n]
    ]


if __name__ == "__main__":
    pass