from datetime import datetime

import pytest
from pydantic import ValidationError

from app.schemas.respostas import RespostaCreate


def test_resposta_create_valida():
    resposta = RespostaCreate(
        id="resposta-001",
        pergunta="Quais são as melhores marcas?",
        plataforma="ChatGPT",
        modelo="gpt-5",
        resposta_texto="A Acme é uma boa opção.",
        data_hora=datetime(2026, 9, 22, 10, 30),
        sentimento="positivo",
    )

    assert resposta.id == "resposta-001"
    assert resposta.pergunta == "Quais são as melhores marcas?"
    assert resposta.plataforma == "ChatGPT"
    assert resposta.modelo == "gpt-5"
    assert resposta.resposta_texto == "A Acme é uma boa opção."
    assert resposta.sentimento == "positivo"


def test_resposta_permite_campos_opcionais_nulos():
    resposta = RespostaCreate(
        id="resposta-002",
        pergunta="Quais marcas existem?",
        plataforma="Gemini",
        modelo=None,
        resposta_texto="Acme, Zenith e Nimbus.",
        data_hora=datetime(2026, 9, 22, 11, 0),
        sentimento=None,
    )

    assert resposta.modelo is None
    assert resposta.sentimento is None


def test_resposta_sem_id_e_invalida():
    with pytest.raises(ValidationError):
        RespostaCreate(
            pergunta="Quais são as melhores marcas?",
            plataforma="ChatGPT",
            modelo="gpt-5",
            resposta_texto="A Acme é uma boa opção.",
            data_hora=datetime(2026, 9, 22, 10, 30),
            sentimento="positivo",
        )


def test_resposta_sem_pergunta_e_invalida():
    with pytest.raises(ValidationError):
        RespostaCreate(
            id="resposta-003",
            plataforma="ChatGPT",
            modelo="gpt-5",
            resposta_texto="A Acme é uma boa opção.",
            data_hora=datetime(2026, 9, 22, 10, 30),
            sentimento="positivo",
        )


def test_resposta_sem_plataforma_e_invalida():
    with pytest.raises(ValidationError):
        RespostaCreate(
            id="resposta-004",
            pergunta="Quais são as melhores marcas?",
            modelo="gpt-5",
            resposta_texto="A Acme é uma boa opção.",
            data_hora=datetime(2026, 9, 22, 10, 30),
            sentimento="positivo",
        )


def test_resposta_sem_texto_e_invalida():
    with pytest.raises(ValidationError):
        RespostaCreate(
            id="resposta-005",
            pergunta="Quais são as melhores marcas?",
            plataforma="ChatGPT",
            modelo="gpt-5",
            data_hora=datetime(2026, 9, 22, 10, 30),
            sentimento="positivo",
        )


def test_data_hora_e_convertida_para_datetime():
    resposta = RespostaCreate(
        id="resposta-006",
        pergunta="Teste",
        plataforma="ChatGPT",
        resposta_texto="Resposta de teste.",
        data_hora="2026-09-22T10:30:00",
    )

    assert isinstance(resposta.data_hora, datetime)
    assert resposta.data_hora == datetime(2026, 9, 22, 10, 30)
