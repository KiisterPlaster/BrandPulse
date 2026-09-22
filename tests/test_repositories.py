from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.database.tables import Base
from app.models.resposta import Resposta
from app.repositories.respostas import RespostaRepository


def create_test_engine():
    return create_engine("sqlite:///:memory:")


def test_criar_resposta():
    engine = create_test_engine()
    Base.metadata.create_all(engine)

    resposta = Resposta(
        id="resposta-001",
        pergunta="Qual a melhor marca?",
        plataforma="ChatGPT",
        modelo="gpt-5",
        resposta_texto="A Acme é uma boa opção.",
        data_hora=datetime(2026, 9, 22, 10, 0),
        sentimento="positivo",
    )

    with Session(engine) as session:
        repository = RespostaRepository(session)

        resultado = repository.criar(resposta)

        assert resultado.id == "resposta-001"


def test_buscar_resposta_por_id():
    engine = create_test_engine()
    Base.metadata.create_all(engine)

    resposta = Resposta(
        id="resposta-002",
        pergunta="Compare as marcas.",
        plataforma="Gemini",
        modelo="gemini",
        resposta_texto="Acme e Zenith são opções.",
        data_hora=datetime(2026, 9, 22, 11, 0),
        sentimento=None,
    )

    with Session(engine) as session:
        repository = RespostaRepository(session)

        repository.criar(resposta)

        resultado = repository.buscar_por_id("resposta-002")

        assert resultado is not None
        assert resultado.id == "resposta-002"


def test_buscar_resposta_inexistente():
    engine = create_test_engine()
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        repository = RespostaRepository(session)

        resultado = repository.buscar_por_id("nao-existe")

        assert resultado is None


def test_listar_respostas():
    engine = create_test_engine()
    Base.metadata.create_all(engine)

    resposta_1 = Resposta(
        id="resposta-003",
        pergunta="Pergunta 1",
        plataforma="ChatGPT",
        modelo="gpt-5",
        resposta_texto="Resposta 1",
        data_hora=datetime(2026, 9, 22, 12, 0),
        sentimento=None,
    )

    resposta_2 = Resposta(
        id="resposta-004",
        pergunta="Pergunta 2",
        plataforma="Gemini",
        modelo="gemini",
        resposta_texto="Resposta 2",
        data_hora=datetime(2026, 9, 22, 13, 0),
        sentimento=None,
    )

    with Session(engine) as session:
        repository = RespostaRepository(session)

        repository.criar(resposta_1)
        repository.criar(resposta_2)

        resultados = repository.listar()

        assert len(resultados) == 2


def test_resposta_existe():
    engine = create_test_engine()
    Base.metadata.create_all(engine)

    resposta = Resposta(
        id="resposta-005",
        pergunta="Pergunta",
        plataforma="Perplexity",
        modelo="sonar",
        resposta_texto="Resposta",
        data_hora=datetime(2026, 9, 22, 14, 0),
        sentimento=None,
    )

    with Session(engine) as session:
        repository = RespostaRepository(session)

        repository.criar(resposta)

        assert repository.existe("resposta-005") is True
        assert repository.existe("nao-existe") is False
