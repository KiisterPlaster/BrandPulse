from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.database.tables import Base
from app.models.mencao import Mencao
from app.models.resposta import Resposta
from app.repositories.respostas import RespostaRepository


def create_test_engine():
    return create_engine("sqlite:///:memory:")


def test_listar_por_marca_case_insensitive():
    engine = create_test_engine()
    Base.metadata.create_all(engine)

    resposta = Resposta(
        resposta_id="1",
        pergunta="Qual a melhor marca?",
        plataforma="ChatGPT",
        modelo="gpt-5",
        resposta_texto="A Acme é excelente.",
        data_hora=datetime(2026, 9, 22, 10, 0),
        sentimento=None,
        mencoes=[
            Mencao(
                marca="Acme",
                ocorrencias=1,
            )
        ],
    )

    with Session(engine) as session:
        repository = RespostaRepository(session)

        repository.criar(resposta)

        assert len(repository.listar_por_marca("Acme")) == 1
        assert len(repository.listar_por_marca("acme")) == 1
        assert len(repository.listar_por_marca("ACME")) == 1
        assert len(repository.listar_por_marca("AcMe")) == 1


def test_criar_resposta():
    engine = create_test_engine()
    Base.metadata.create_all(engine)

    resposta = Resposta(
        resposta_id="resposta-001",
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

        assert resultado is not None
        assert resultado.resposta_id == "resposta-001"
        assert resultado.id is not None


def test_buscar_resposta_por_id():
    engine = create_test_engine()
    Base.metadata.create_all(engine)

    resposta = Resposta(
        resposta_id="resposta-002",
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

        resultado = repository.buscar_por_resposta_id("resposta-002")

        assert resultado is not None
        assert resultado.resposta_id == "resposta-002"
        assert resultado.id is not None


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
        resposta_id="resposta-003",
        pergunta="Pergunta 1",
        plataforma="ChatGPT",
        modelo="gpt-5",
        resposta_texto="Resposta 1",
        data_hora=datetime(2026, 9, 22, 12, 0),
        sentimento=None,
    )

    resposta_2 = Resposta(
        resposta_id="resposta-004",
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

        ids = {resposta.resposta_id for resposta in resultados}

        assert ids == {
            "resposta-003",
            "resposta-004",
        }


def test_resposta_existe():
    engine = create_test_engine()
    Base.metadata.create_all(engine)

    resposta = Resposta(
        resposta_id="resposta-005",
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

        assert repository.existe_duplicata(resposta) is True

        outra_resposta = Resposta(
            resposta_id="resposta-006",
            pergunta="Outra pergunta",
            plataforma="ChatGPT",
            modelo="gpt-5",
            resposta_texto="Outra resposta",
            data_hora=datetime(2026, 9, 22, 15, 0),
            sentimento=None,
        )

        assert repository.existe_duplicata(outra_resposta) is False
