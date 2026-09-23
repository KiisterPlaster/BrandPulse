# Estrutura do Projeto BrandPulse

O BrandPulse utiliza uma arquitetura em camadas para separar HTTP, validação, regras de negócio e persistência.

## Estrutura

```text
BrandPulse/
├── app/
│   ├── api/routes/        # endpoints FastAPI
│   ├── core/              # logging e rate limiting
│   ├── database/          # conexão e criação das tabelas
│   ├── models/            # modelos SQLAlchemy
│   ├── repositories/      # acesso ao banco
│   ├── schemas/           # validação/serialização Pydantic
│   └── services/          # regras de negócio
├── data/                  # SQLite e JSON de exemplo
├── docs/                  # documentação
├── tests/                 # testes e fixtures
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
└── uv.lock
```

## Camadas

### `app/api/routes`

Recebe requisições HTTP e coordena os serviços.

- `analytics.py`: `/share-of-voice` e `/top-citacoes`.
- `respostas.py`: `/respostas`.

### `app/core`

Componentes transversais da aplicação.

- `logging.py`: saída de logs no console e em `logs/app.log`.
- `limiter.py`: configuração do rate limiting.

### `app/database`

Configura o SQLAlchemy, as sessões e a criação das tabelas.

### `app/models`

Representa as entidades persistidas:

- `Resposta` — resposta analisada;
- `Mencao` — marca e quantidade de ocorrências associadas à resposta.

### `app/repositories`

Concentra operações de persistência e consultas sobre respostas e menções.

### `app/schemas`

Define os contratos Pydantic de entrada e saída.

### `app/services`

Contém as regras de negócio:

- `analytics.py` — Share of Voice e Top Citações;
- `ingestao.py` — carregamento e validação de JSON;
- `mencoes.py` — detecção das marcas monitoradas;
- `plataformas.py` — normalização dos nomes de plataformas.

## Fluxo principal

```text
Requisição
   │
   ▼
Router
   │
   ▼
Schema
   │
   ▼
Service
   │
   ▼
Repository
   │
   ▼
SQLAlchemy / SQLite
```

No `POST /respostas`, o service também utiliza `mencoes.py` para detectar marcas e `plataformas.py` para normalizar a plataforma antes da persistência.

## Dados e documentação

- `data/database.db` — banco SQLite local.
- `data/respostas_exemplo.json` — dados de exemplo.
- `docs/documentacoes/` — documentação técnica.
- `docs/STEP_BY_STEP.md` — histórico das etapas do desenvolvimento.

## Testes

A pasta `tests/` acompanha as principais camadas do sistema:

- analytics;
- banco de dados;
- ingestão;
- menções;
- models;
- repositories;
- routes;
- schemas.

`tests/fixtures/` contém entradas válidas, inválidas e cenários mínimos para os testes.

## Execução

Local:

```bash
uv sync
uv run uvicorn app.main:app --reload
```

Docker:

```bash
docker compose up --build
```

O Compose monta `data/` e `logs/`, permitindo compartilhar o banco SQLite e os arquivos de log com o ambiente local.