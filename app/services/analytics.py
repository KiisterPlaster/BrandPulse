from app.repositories.respostas import RespostaRepository
from app.schemas.analytics import (
    PlatformShare,
    ShareOfVoiceResponse,
)


def calcular_share_of_voice(
    repository: RespostaRepository,
    marca: str,
) -> ShareOfVoiceResponse:
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


if __name__ == "__main__":
    pass
