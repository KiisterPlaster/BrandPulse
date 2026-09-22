from pathlib import Path

import pytest

from app.schemas.respostas import RespostaCreate
from app.services.ingestao import carregar_respostas


FIXTURES_DIR = Path(__file__).parent / "fixtures"


def test_carregar_respostas_minimas():
    caminho = FIXTURES_DIR / "respostas_minimas.json"

    respostas = carregar_respostas(caminho)

    assert len(respostas) > 0
    assert all(isinstance(resposta, RespostaCreate) for resposta in respostas)


def test_carregar_respostas_teste():
    caminho = FIXTURES_DIR / "respostas_teste.json"

    respostas = carregar_respostas(caminho)

    assert len(respostas) > 0
    assert all(isinstance(resposta, RespostaCreate) for resposta in respostas)


def test_carregar_respostas_validas():
    caminho = FIXTURES_DIR / "respostas_validas.json"

    respostas = carregar_respostas(caminho)

    assert len(respostas) > 0
    assert all(isinstance(resposta, RespostaCreate) for resposta in respostas)


def test_ignorar_respostas_invalidas():
    caminho = FIXTURES_DIR / "respostas_invalidas.json"

    respostas = carregar_respostas(caminho)

    assert all(isinstance(resposta, RespostaCreate) for resposta in respostas)


def test_respostas_invalidas_nao_interrompem_ingestao():
    caminho_validas = FIXTURES_DIR / "respostas_validas.json"
    caminho_invalidas = FIXTURES_DIR / "respostas_invalidas.json"

    respostas_validas = carregar_respostas(caminho_validas)
    respostas_invalidas = carregar_respostas(caminho_invalidas)

    assert len(respostas_validas) > 0
    assert len(respostas_invalidas) < len(respostas_validas)


def test_arquivo_deve_conter_uma_lista(tmp_path):
    caminho = tmp_path / "dados.json"

    caminho.write_text(
        '{"id": "1"}',
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="lista de respostas"):
        carregar_respostas(caminho)


def test_arquivo_inexistente():
    caminho = FIXTURES_DIR / "arquivo_inexistente.json"

    with pytest.raises(FileNotFoundError):
        carregar_respostas(caminho)