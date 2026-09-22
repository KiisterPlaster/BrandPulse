from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from app.database.tables import Base
from app.main import app
from app.models.mencao import Mencao
from app.models.resposta import Resposta

# ============================================================
# FIXTURES
# ============================================================


@pytest.fixture
def engine():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    Base.metadata.create_all(bind=engine)

    yield engine

    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client(engine):
    from app.api.routes.analytics import get_repository as analytics_repository
    from app.api.routes.respostas import get_repository as respostas_repository
    from app.repositories.respostas import RespostaRepository

    def override_get_repository():
        with Session(engine) as session:
            yield RespostaRepository(session)

    app.dependency_overrides[analytics_repository] = override_get_repository
    app.dependency_overrides[respostas_repository] = override_get_repository

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest.fixture
def banco_com_respostas(engine):
    with Session(engine) as session:
        resposta_1 = Resposta(
            id="r001",
            pergunta="Qual a melhor ferramenta?",
            plataforma="ChatGPT",
            modelo="gpt-5.1",
            resposta_texto="A Acme é uma boa opção.",
            data_hora=datetime(2026, 1, 15, 10, 0),
            sentimento="positivo",
        )

        resposta_1.mencoes = [
            Mencao(
                marca="Acme",
                ocorrencias=2,
            )
        ]

        resposta_2 = Resposta(
            id="r002",
            pergunta="Quais empresas são conhecidas?",
            plataforma="ChatGPT",
            modelo="gpt-5.1",
            resposta_texto="Acme e Zenith são conhecidas.",
            data_hora=datetime(2026, 1, 16, 10, 0),
            sentimento="neutro",
        )

        resposta_2.mencoes = [
            Mencao(
                marca="Acme",
                ocorrencias=1,
            ),
            Mencao(
                marca="Zenith",
                ocorrencias=1,
            ),
        ]

        resposta_3 = Resposta(
            id="r003",
            pergunta="O que é monitoramento?",
            plataforma="Gemini",
            modelo="gemini-2.5-pro",
            resposta_texto="Zenith é uma opção.",
            data_hora=datetime(2026, 1, 17, 10, 0),
            sentimento="positivo",
        )

        resposta_3.mencoes = [
            Mencao(
                marca="Zenith",
                ocorrencias=3,
            )
        ]

        resposta_4 = Resposta(
            id="r004",
            pergunta="Como funciona análise de dados?",
            plataforma="Perplexity",
            modelo="sonar-pro",
            resposta_texto="Não há marcas citadas.",
            data_hora=datetime(2026, 1, 18, 10, 0),
            sentimento="neutro",
        )

        session.add_all(
            [
                resposta_1,
                resposta_2,
                resposta_3,
                resposta_4,
            ]
        )

        session.commit()


# ============================================================
# GET /share-of-voice
# ============================================================


def test_share_of_voice(client, banco_com_respostas):
    response = client.get(
        "/share-of-voice",
        params={"marca": "Acme"},
    )

    assert response.status_code == 200

    data = response.json()

    assert data["marca"] == "Acme"
    assert data["respostas_com_mencao"] == 2
    assert data["total_respostas"] == 4
    assert data["percentual"] == 50.0


def test_share_of_voice_por_plataforma(
    client,
    banco_com_respostas,
):
    response = client.get(
        "/share-of-voice",
        params={"marca": "Acme"},
    )

    assert response.status_code == 200

    data = response.json()

    plataformas = {item["plataforma"]: item for item in data["por_plataforma"]}

    assert "ChatGPT" in plataformas
    assert "Gemini" in plataformas
    assert "Perplexity" in plataformas

    assert plataformas["ChatGPT"]["total_respostas"] == 2
    assert plataformas["ChatGPT"]["respostas_com_mencao"] == 2
    assert plataformas["ChatGPT"]["percentual"] == 100.0

    assert plataformas["Gemini"]["total_respostas"] == 1
    assert plataformas["Gemini"]["respostas_com_mencao"] == 0
    assert plataformas["Gemini"]["percentual"] == 0.0


def test_share_of_voice_marca_nao_encontrada(
    client,
    banco_com_respostas,
):
    response = client.get(
        "/share-of-voice",
        params={"marca": "MarcaInexistente"},
    )

    assert response.status_code == 200

    data = response.json()

    assert data["marca"] == "MarcaInexistente"
    assert data["respostas_com_mencao"] == 0
    assert data["total_respostas"] == 4
    assert data["percentual"] == 0.0


def test_share_of_voice_sem_marca(client):
    response = client.get("/share-of-voice")

    assert response.status_code == 422


def test_share_of_voice_marca_vazia(client):
    response = client.get(
        "/share-of-voice",
        params={"marca": ""},
    )

    assert response.status_code == 422


# ============================================================
# GET /top-citacoes
# ============================================================


def test_top_citacoes(client, banco_com_respostas):
    response = client.get(
        "/top-citacoes",
        params={"n": 2},
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2

    assert data[0]["resposta_id"] == "r002"
    assert data[0]["marcas"] == ["Acme", "Zenith"]

    assert data[1]["resposta_id"] == "r003"
    assert data[1]["marcas"] == ["Zenith"]


def test_top_citacoes_respeita_quantidade(
    client,
    banco_com_respostas,
):
    response = client.get(
        "/top-citacoes",
        params={"n": 1},
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["resposta_id"] == "r002"


def test_top_citacoes_ignora_respostas_sem_mencao(
    client,
    banco_com_respostas,
):
    response = client.get(
        "/top-citacoes",
        params={"n": 10},
    )

    assert response.status_code == 200

    data = response.json()

    ids = [item["resposta_id"] for item in data]

    assert "r004" not in ids


def test_top_citacoes_retorna_score(
    client,
    banco_com_respostas,
):
    response = client.get(
        "/top-citacoes",
        params={"n": 10},
    )

    assert response.status_code == 200

    data = response.json()

    resultados = {item["resposta_id"]: item for item in data}

    assert resultados["r002"]["score"] == 6
    assert resultados["r003"]["score"] == 5


# ============================================================
# POST /respostas
# ============================================================


def criar_payload_resposta(
    id_resposta="r100",
    resposta_texto="A Acme é uma boa opção de monitoramento, junto com a Zenith.",
    data_hora="2026-01-20T10:00:00",
):
    return {
        "id": id_resposta,
        "pergunta": "Qual a melhor ferramenta de monitoramento?",
        "plataforma": "ChatGPT",
        "modelo": "gpt-5.1",
        "resposta_texto": resposta_texto,
        "data_hora": data_hora,
        "sentimento": "positivo",
    }


def test_criar_resposta(client):
    payload = [criar_payload_resposta()]

    response = client.post(
        "/respostas",
        json=payload,
    )

    assert response.status_code == 201

    data = response.json()

    assert isinstance(data, list)
    assert len(data) == 1

    resposta = data[0]

    assert resposta["id"] == "r100"
    assert resposta["pergunta"] == payload[0]["pergunta"]
    assert resposta["plataforma"] == "ChatGPT"
    assert resposta["modelo"] == "gpt-5.1"
    assert resposta["resposta_texto"] == payload[0]["resposta_texto"]
    assert resposta["sentimento"] == "positivo"


def test_criar_resposta_retorna_mencoes(client):
    payload = [criar_payload_resposta()]

    response = client.post(
        "/respostas",
        json=payload,
    )

    assert response.status_code == 201

    data = response.json()

    assert isinstance(data[0]["mencoes"], list)


def test_criar_resposta_detecta_mencoes(client):
    payload = [
        criar_payload_resposta(
            resposta_texto=(
                "A Acme é uma boa opção. A Zenith também é bastante conhecida."
            ),
        )
    ]

    response = client.post(
        "/respostas",
        json=payload,
    )

    assert response.status_code == 201

    data = response.json()

    marcas = [mencao["marca"] for mencao in data[0]["mencoes"]]

    assert "Acme" in marcas
    assert "Zenith" in marcas


def test_criar_resposta_persiste_resposta(
    client,
    engine,
):
    payload = [criar_payload_resposta()]

    response = client.post(
        "/respostas",
        json=payload,
    )

    assert response.status_code == 201

    with Session(engine) as session:
        resposta = session.get(
            Resposta,
            "r100",
        )

    assert resposta is not None
    assert resposta.id == "r100"
    assert resposta.pergunta == payload[0]["pergunta"]
    assert resposta.plataforma == "ChatGPT"


def test_criar_resposta_persiste_mencoes(
    client,
    engine,
):
    payload = [
        criar_payload_resposta(
            resposta_texto="Acme e Zenith são marcas conhecidas.",
        )
    ]

    response = client.post(
        "/respostas",
        json=payload,
    )

    assert response.status_code == 201

    with Session(engine) as session:
        resposta = session.get(
            Resposta,
            "r100",
        )

        assert resposta is not None

        mencoes = session.query(Mencao).filter(Mencao.resposta_id == "r100").all()

    marcas = [mencao.marca for mencao in mencoes]

    assert "Acme" in marcas
    assert "Zenith" in marcas


def test_criar_multiplas_respostas(client, engine):
    payload = [
        criar_payload_resposta(
            id_resposta="r101",
            resposta_texto="A Acme é uma boa opção.",
        ),
        criar_payload_resposta(
            id_resposta="r102",
            resposta_texto="A Zenith é uma boa opção.",
        ),
    ]

    response = client.post(
        "/respostas",
        json=payload,
    )

    assert response.status_code == 201

    data = response.json()

    assert len(data) == 2
    assert data[0]["id"] == "r101"
    assert data[1]["id"] == "r102"

    with Session(engine) as session:
        resposta_1 = session.get(
            Resposta,
            "r101",
        )

        resposta_2 = session.get(
            Resposta,
            "r102",
        )

    assert resposta_1 is not None
    assert resposta_2 is not None


# ============================================================
# POST /respostas
# Datas
# ============================================================


@pytest.mark.parametrize(
    "data_hora",
    [
        "2026-01-20T10:00:00",
        "2026-01-20",
        "20/01/2026",
        "2026/01/20",
    ],
)
def test_criar_resposta_aceita_diferentes_formatos_de_data(
    client,
    data_hora,
):
    payload = [
        criar_payload_resposta(
            data_hora=data_hora,
        )
    ]

    response = client.post(
        "/respostas",
        json=payload,
    )

    assert response.status_code == 201

    data = response.json()

    assert len(data) == 1
    assert data[0]["id"] == "r100"
    assert data[0]["data_hora"] is not None


def test_criar_resposta_retorna_data_formatada(client):
    payload = [
        criar_payload_resposta(
            data_hora="2026-01-20",
        )
    ]

    response = client.post(
        "/respostas",
        json=payload,
    )

    assert response.status_code == 201

    data = response.json()

    assert data[0]["data_hora"] is not None


def test_criar_resposta_data_invalida(client):
    payload = [
        criar_payload_resposta(
            data_hora="data-invalida",
        )
    ]

    response = client.post(
        "/respostas",
        json=payload,
    )

    assert response.status_code == 422


# ============================================================
# POST /respostas
# Validação
# ============================================================


def test_criar_resposta_sem_id(client):
    payload = criar_payload_resposta()
    del payload["id"]

    response = client.post(
        "/respostas",
        json=[payload],
    )

    assert response.status_code == 422


def test_criar_resposta_sem_pergunta(client):
    payload = criar_payload_resposta()
    del payload["pergunta"]

    response = client.post(
        "/respostas",
        json=[payload],
    )

    assert response.status_code == 422


def test_criar_resposta_sem_plataforma(client):
    payload = criar_payload_resposta()
    del payload["plataforma"]

    response = client.post(
        "/respostas",
        json=[payload],
    )

    assert response.status_code == 422


def test_criar_resposta_sem_texto(client):
    payload = criar_payload_resposta()
    del payload["resposta_texto"]

    response = client.post(
        "/respostas",
        json=[payload],
    )

    assert response.status_code == 422


def test_criar_resposta_texto_vazio(client):
    payload = criar_payload_resposta()
    payload["resposta_texto"] = ""

    response = client.post(
        "/respostas",
        json=[payload],
    )

    assert response.status_code == 422


def test_criar_resposta_id_vazio(client):
    payload = criar_payload_resposta()
    payload["id"] = ""

    response = client.post(
        "/respostas",
        json=[payload],
    )

    assert response.status_code == 422


def test_criar_resposta_payload_incompleto(client):
    response = client.post(
        "/respostas",
        json=[
            {
                "id": "r200",
                "pergunta": "Pergunta incompleta",
            }
        ],
    )

    assert response.status_code == 422


def test_criar_resposta_payload_nao_lista(client):
    payload = criar_payload_resposta()

    response = client.post(
        "/respostas",
        json=payload,
    )

    assert response.status_code == 422


def test_criar_resposta_lista_vazia(client):
    response = client.post(
        "/respostas",
        json=[],
    )

    assert response.status_code == 201

    data = response.json()

    assert data == []


@pytest.mark.parametrize(
    "data_hora",
    [
        "2026-01-20T10:00:00",
        "2026-01-20",
        "20/01/2026",
        "2026/01/20",
    ],
)
def test_criar_resposta_normaliza_data(
    client,
    data_hora,
):
    payload = [
        criar_payload_resposta(
            data_hora=data_hora,
        )
    ]

    response = client.post(
        "/respostas",
        json=payload,
    )

    assert response.status_code == 201

    data = response.json()[0]

    assert data["data_hora"].startswith("2026-01-20")


# ============================================================
# GET /share-of-voice
# ============================================================


@pytest.mark.parametrize(
    "valor",
    [
        "0",
        "-1",
    ],
)
def test_top_citacoes_n_invalido(
    client,
    banco_com_respostas,
    valor,
):
    response = client.get(
        "/top-citacoes",
        params={"n": valor},
    )

    assert response.status_code == 422


def test_top_citacoes_n_nao_numerico(
    client,
    banco_com_respostas,
):
    response = client.get(
        "/top-citacoes",
        params={"n": "abc"},
    )

    assert response.status_code == 422


def test_top_citacoes_banco_vazio(client):
    response = client.get(
        "/top-citacoes",
        params={"n": 5},
    )

    assert response.status_code == 200

    data = response.json()

    assert data == []
