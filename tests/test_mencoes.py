from pathlib import Path

import pytest

from app.services.ingestao import carregar_respostas
from app.services.mencoes import detectar_mencoes

FIXTURES_DIR = Path(__file__).parent / "fixtures"


def test_detectar_uma_marca():
    texto = "A Acme oferece boas soluções."

    resultado = detectar_mencoes(texto)

    assert resultado == {
        "Acme": 1,
    }


def test_detectar_multiplas_marcas():
    texto = "Acme, Zenith e Nimbus são marcas conhecidas."

    resultado = detectar_mencoes(texto)

    assert resultado == {
        "Acme": 1,
        "Zenith": 1,
        "Nimbus": 1,
    }


def test_detectar_multiplas_ocorrencias_da_mesma_marca():
    texto = (
        "A A.C.M.E possui boas soluções. "
        "A A C M E também oferece suporte. "
        "A Acme atua em diversos mercados."
    )

    resultado = detectar_mencoes(texto)

    assert resultado == {
        "Acme": 3,
    }


def test_deteccao_case_insensitive():
    texto = "ACME, acme e AcMe são a mesma marca."

    resultado = detectar_mencoes(texto)

    assert resultado == {
        "Acme": 3,
    }


def test_resposta_sem_marcas():
    texto = "Essa resposta não menciona nenhuma marca monitorada."

    resultado = detectar_mencoes(texto)

    assert resultado == {}


def test_nao_detectar_marca_dentro_de_outra_palavra():
    texto = "O termo Acme aparece, mas Acme123 não deve ser considerado."

    resultado = detectar_mencoes(texto)

    assert resultado == {
        "Acme": 1,
    }


def test_detectar_marcas_em_texto_com_pontuacao():
    texto = "Acme! Zenith? Nimbus."

    resultado = detectar_mencoes(texto)

    assert resultado == {
        "Acme": 1,
        "Zenith": 1,
        "Nimbus": 1,
    }


def test_texto_vazio():
    resultado = detectar_mencoes("")

    assert resultado == {}


@pytest.mark.parametrize(
    "arquivo",
    sorted(FIXTURES_DIR.glob("*.json")),
    ids=lambda caminho: caminho.name,
)
def test_detectar_mencoes_nos_fixtures(arquivo):
    respostas = carregar_respostas(arquivo)

    assert isinstance(respostas, list)

    for resposta in respostas:
        resultado = detectar_mencoes(resposta.resposta_texto)

        assert isinstance(resultado, dict)

        for marca, ocorrencias in resultado.items():
            assert isinstance(marca, str)
            assert isinstance(ocorrencias, int)
            assert ocorrencias > 0
