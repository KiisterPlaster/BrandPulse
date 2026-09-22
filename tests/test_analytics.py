from datetime import datetime
from unittest.mock import Mock

from app.models.resposta import Resposta
from app.schemas.analytics import ShareOfVoiceResponse
from app.services.analytics import calcular_share_of_voice


def criar_resposta(
    id: str,
    plataforma: str,
    resposta_texto: str = "Resposta de teste.",
) -> Resposta:
    return Resposta(
        id=id,
        pergunta="Qual a melhor marca?",
        plataforma=plataforma,
        modelo="gpt-5",
        resposta_texto=resposta_texto,
        data_hora=datetime(2026, 9, 22, 10, 0),
        sentimento=None,
    )


def criar_repository(respostas, respostas_com_marca):
    repository = Mock()

    repository.listar.return_value = respostas
    repository.listar_por_marca.return_value = respostas_com_marca

    return repository


def test_share_of_voice_sem_respostas():
    repository = criar_repository(
        respostas=[],
        respostas_com_marca=[],
    )

    resultado = calcular_share_of_voice(repository, "Acme")

    assert isinstance(resultado, ShareOfVoiceResponse)
    assert resultado.marca == "Acme"
    assert resultado.total_respostas == 0
    assert resultado.respostas_com_mencao == 0
    assert resultado.percentual == 0.0
    assert resultado.por_plataforma == []


def test_share_of_voice_sem_mencoes():
    respostas = [
        criar_resposta("1", "ChatGPT"),
        criar_resposta("2", "Gemini"),
        criar_resposta("3", "Perplexity"),
    ]

    repository = criar_repository(
        respostas=respostas,
        respostas_com_marca=[],
    )

    resultado = calcular_share_of_voice(repository, "Acme")

    assert resultado.total_respostas == 3
    assert resultado.respostas_com_mencao == 0
    assert resultado.percentual == 0.0


def test_share_of_voice_50_por_cento():
    respostas = [
        criar_resposta("1", "ChatGPT"),
        criar_resposta("2", "ChatGPT"),
        criar_resposta("3", "Gemini"),
        criar_resposta("4", "Gemini"),
    ]

    respostas_com_marca = [
        respostas[0],
        respostas[2],
    ]

    repository = criar_repository(
        respostas=respostas,
        respostas_com_marca=respostas_com_marca,
    )

    resultado = calcular_share_of_voice(repository, "Acme")

    assert resultado.total_respostas == 4
    assert resultado.respostas_com_mencao == 2
    assert resultado.percentual == 50.0


def test_share_of_voice_100_por_cento():
    respostas = [
        criar_resposta("1", "ChatGPT"),
        criar_resposta("2", "Gemini"),
        criar_resposta("3", "Perplexity"),
    ]

    repository = criar_repository(
        respostas=respostas,
        respostas_com_marca=respostas,
    )

    resultado = calcular_share_of_voice(repository, "Acme")

    assert resultado.total_respostas == 3
    assert resultado.respostas_com_mencao == 3
    assert resultado.percentual == 100.0


def test_share_of_voice_por_plataforma():
    respostas = [
        criar_resposta("1", "ChatGPT"),
        criar_resposta("2", "ChatGPT"),
        criar_resposta("3", "ChatGPT"),
        criar_resposta("4", "Gemini"),
        criar_resposta("5", "Gemini"),
    ]

    respostas_com_marca = [
        respostas[0],
        respostas[1],
        respostas[3],
    ]

    repository = criar_repository(
        respostas=respostas,
        respostas_com_marca=respostas_com_marca,
    )

    resultado = calcular_share_of_voice(repository, "Acme")

    assert resultado.total_respostas == 5
    assert resultado.respostas_com_mencao == 3
    assert resultado.percentual == 60.0

    plataformas = {
        plataforma.plataforma: plataforma
        for plataforma in resultado.por_plataforma
    }

    assert plataformas["ChatGPT"].total_respostas == 3
    assert plataformas["ChatGPT"].respostas_com_mencao == 2
    assert plataformas["ChatGPT"].percentual == 2 / 3 * 100

    assert plataformas["Gemini"].total_respostas == 2
    assert plataformas["Gemini"].respostas_com_mencao == 1
    assert plataformas["Gemini"].percentual == 50.0


def test_multiplas_ocorrencias_da_marca_contam_como_uma_resposta():
    resposta_1 = criar_resposta(
        "1",
        "ChatGPT",
        "A Acme é boa. A Acme possui excelentes produtos.",
    )

    resposta_2 = criar_resposta(
        "2",
        "ChatGPT",
        "A Zenith é uma alternativa.",
    )

    respostas = [resposta_1, resposta_2]

    repository = criar_repository(
        respostas=respostas,
        respostas_com_marca=[resposta_1],
    )

    resultado = calcular_share_of_voice(repository, "Acme")

    assert resultado.total_respostas == 2
    assert resultado.respostas_com_mencao == 1
    assert resultado.percentual == 50.0