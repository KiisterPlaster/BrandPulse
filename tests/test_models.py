from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from app.database.tables import Base
from app.models.mencao import Mencao
from app.models.resposta import Resposta


def create_test_engine():
    return create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )


def test_criar_resposta():
    engine = create_test_engine()
    Base.metadata.create_all(engine)

    resposta = Resposta(
        id="resposta-001",
        pergunta="Quais são as melhores ferramentas de IA?",
        plataforma="ChatGPT",
        modelo="gpt-5",
        resposta_texto="A Acme é uma das opções disponíveis.",
        data_hora=datetime(2026, 9, 22, 10, 30),
        sentimento="positivo",
    )

    with Session(engine) as session:
        session.add(resposta)
        session.commit()

        resultado = session.get(Resposta, "resposta-001")

    assert resultado is not None
    assert resultado.id == "resposta-001"
    assert resultado.pergunta == "Quais são as melhores ferramentas de IA?"
    assert resultado.plataforma == "ChatGPT"
    assert resultado.modelo == "gpt-5"
    assert resultado.resposta_texto == "A Acme é uma das opções disponíveis."
    assert resultado.sentimento == "positivo"


def test_criar_mencao():
    engine = create_test_engine()
    Base.metadata.create_all(engine)

    resposta = Resposta(
        id="resposta-002",
        pergunta="Quais marcas são recomendadas?",
        plataforma="Gemini",
        modelo="gemini-2",
        resposta_texto="A Acme é uma opção.",
        data_hora=datetime(2026, 9, 22, 11, 0),
        sentimento=None,
    )

    mencao = Mencao(
        resposta_id="resposta-002",
        marca="Acme",
        ocorrencias=1,
    )

    with Session(engine) as session:
        session.add(resposta)
        session.add(mencao)
        session.commit()

        resultado = session.get(Mencao, 1)

    assert resultado is not None
    assert resultado.resposta_id == "resposta-002"
    assert resultado.marca == "Acme"
    assert resultado.ocorrencias == 1


def test_resposta_possui_multiplas_mencoes():
    engine = create_test_engine()
    Base.metadata.create_all(engine)

    resposta = Resposta(
        id="resposta-003",
        pergunta="Compare as marcas.",
        plataforma="ChatGPT",
        modelo="gpt-5",
        resposta_texto="Acme, Zenith e Nimbus são opções.",
        data_hora=datetime(2026, 9, 22, 12, 0),
        sentimento=None,
    )

    resposta.mencoes = [
        Mencao(
            marca="Acme",
            ocorrencias=1,
        ),
        Mencao(
            marca="Zenith",
            ocorrencias=1,
        ),
        Mencao(
            marca="Nimbus",
            ocorrencias=1,
        ),
    ]

    with Session(engine) as session:
        session.add(resposta)
        session.commit()

        resultado = session.get(Resposta, "resposta-003")

        assert resultado is not None
        assert len(resultado.mencoes) == 3

        marcas = {mencao.marca for mencao in resultado.mencoes}

        assert marcas == {"Acme", "Zenith", "Nimbus"}


def test_mencao_armazena_quantidade_de_ocorrencias():
    engine = create_test_engine()
    Base.metadata.create_all(engine)

    resposta = Resposta(
        id="resposta-004",
        pergunta="Fale sobre a Acme.",
        plataforma="Perplexity",
        modelo="sonar",
        resposta_texto=(
            "A Acme é uma empresa conhecida. A Acme possui diversas soluções."
        ),
        data_hora=datetime(2026, 9, 22, 13, 0),
        sentimento="positivo",
    )

    resposta.mencoes = [
        Mencao(
            marca="Acme",
            ocorrencias=2,
        )
    ]

    with Session(engine) as session:
        session.add(resposta)
        session.commit()

        resultado = session.get(Resposta, "resposta-004")

        assert resultado is not None
        assert len(resultado.mencoes) == 1
        assert resultado.mencoes[0].marca == "Acme"
        assert resultado.mencoes[0].ocorrencias == 2
