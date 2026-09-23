# BrandPulse

Serviço HTTP para análise de menções de marcas em respostas geradas por ferramentas de IA, como ChatGPT, Gemini e Perplexity.

O projeto foi construído como um serviço modular, com validação, detecção determinística de menções, persistência em SQLite e endpoints para análise.

## Objetivo

A partir de respostas coletadas por scraping, o BrandPulse:

- valida e normaliza os dados recebidos;
- identifica as marcas monitoradas (`Acme`, `Zenith` e `Nimbus`);
- registra as menções e suas ocorrências;
- persiste respostas e menções em SQLite;
- calcula Share of Voice geral e por plataforma;
- ranqueia respostas por score de citação;
- disponibiliza tudo por uma API FastAPI.

A lista de marcas é atualmente fixa, conforme o escopo do desafio.

## Principais decisões

### FastAPI

Escolhido pela validação integrada com Pydantic, tipagem, geração automática de documentação OpenAPI e facilidade de testes com `TestClient`.

### SQLite + SQLAlchemy

SQLite atende ao escopo do desafio e mantém a execução simples, sem exigir um serviço externo de banco. O acesso foi isolado em repositories e models SQLAlchemy, facilitando uma futura migração para PostgreSQL ou outro banco.

### Detecção determinística

As menções são identificadas por expressões regulares, com busca case-insensitive e tolerância a caracteres não alfanuméricos entre as letras da marca. Para o conjunto pequeno e conhecido de marcas, essa abordagem é previsível, barata e facilmente testável.

Exemplos reconhecidos:

```text
Acme
ACME
A.C.M.E.
A-C-M-E
A C M E
```

### Score de citação

Para o ranking de `/top-citacoes`, o score considera diversidade e frequência:

```text
score = (2 × marcas_distintas) + ocorrencias_totais
```

Assim, uma resposta que cita várias marcas recebe peso pela diversidade, enquanto repetições também contribuem para o resultado. O score é uma heurística do projeto, não uma avaliação semântica da qualidade da citação.

### Tratamento de dados imperfeitos

Registros inválidos são descartados durante a ingestão para não impedir o processamento dos demais registros. No `POST /respostas`, cada item também é validado individualmente.

A API ainda normaliza nomes de plataformas e datas aceitas pelo schema e evita inserir respostas já existentes segundo o identificador utilizado pela aplicação.

## Arquitetura

```text
HTTP
 │
 ▼
Routes
 │
 ├── Schemas (validação)
 │
 ├── Services (regras de negócio)
 │
 └── Repositories (persistência)
          │
          ▼
       SQLAlchemy
          │
          ▼
        SQLite
```

Estrutura principal:

```text
BrandPulse/
├── app/
│   ├── api/routes/        # endpoints HTTP
│   ├── core/              # logging e rate limiting
│   ├── database/          # conexão e inicialização do banco
│   ├── models/            # entidades SQLAlchemy
│   ├── repositories/      # acesso aos dados
│   ├── schemas/           # contratos Pydantic
│   └── services/          # regras de negócio
├── data/                  # SQLite e dados de exemplo
├── docs/                  # documentação técnica
├── tests/                 # testes automatizados e fixtures
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
└── uv.lock
```

## API

### `GET /health`

Health check simples da aplicação.

```http
GET /health
```

Resposta:

```json
{"status": "ok"}
```

### `GET /share-of-voice`

Calcula a proporção de respostas que mencionam uma marca, incluindo o detalhamento por plataforma.

```http
GET /share-of-voice?marca=Acme
```

### `GET /top-citacoes`

Retorna as respostas com maior score de citação.

```http
GET /top-citacoes?n=5
```

`n` possui valor padrão `5` e deve ser maior ou igual a `1`.

### `POST /respostas`

Recebe uma lista de respostas, valida cada item, detecta as marcas mencionadas, normaliza a plataforma, verifica duplicidade e persiste os registros válidos.

```http
POST /respostas
Content-Type: application/json
```

Exemplo:

```json
[
  {
    "id": "r001",
    "pergunta": "Qual a melhor ferramenta?",
    "plataforma": "ChatGPT",
    "modelo": "gpt-5",
    "resposta_texto": "A Acme é uma boa opção.",
    "data_hora": "2026-09-22T10:00:00",
    "sentimento": "positivo"
  }
]
```

A documentação interativa pode ser acessada em `/docs` quando a API estiver em execução.

## Executando localmente

Requisitos: Python 3.11+ e `uv`.

```bash
uv sync
uv run uvicorn app.main:app --reload
```

A API ficará disponível em `http://localhost:8000`.

## Executando com Docker

```bash
docker compose up --build
```

O Compose monta `./data` em `/app/data` e `./logs` em `/app/logs`. Dessa forma, o SQLite utilizado pelo container permanece no diretório do projeto e pode ser compartilhado com a execução local.

Para verificar o container:

```bash
docker compose ps
```

O Compose possui health check em `/health`.

## Testes e qualidade

Os testes utilizam `pytest` e o `TestClient` do FastAPI. Os testes de API utilizam banco isolado para não depender dos dados persistidos no ambiente de desenvolvimento.

```bash
uv run pytest
uv run ruff check .
uv run ruff format --check .
```

Também existe `tests/teste_api.http` para testes manuais dos endpoints.

## Logs

O logging é configurado em `app/core/logging.py` e enviado para o console e para `logs/app.log`.

São utilizados principalmente `INFO` para eventos relevantes da aplicação e `DEBUG` para detalhes de diagnóstico. O conteúdo completo das respostas não é registrado nos logs.

## Documentação

- [`docs/documentacoes/API_DOCS.md`](docs/documentacoes/API_DOCS.md) — endpoints, parâmetros, respostas e exemplos.
- [`docs/documentacoes/SCHEMAS_DOCS.md`](docs/documentacoes/SCHEMAS_DOCS.md) — contratos Pydantic.
- [`docs/documentacoes/ESTRUTURA_DOCS.md`](docs/documentacoes/ESTRUTURA_DOCS.md) — organização e responsabilidades das camadas.
- [`docs/STEP_BY_STEP.md`](docs/STEP_BY_STEP.md) — histórico do desenvolvimento.
- [`SECURITY.md`](SECURITY.md) — considerações de segurança.

## O que eu faria com mais tempo

- Migraria o SQLite para PostgreSQL em um ambiente de produção.
- Adicionaria migrações de banco com Alembic.
- Transformaria a lista de marcas monitoradas em configuração persistida, com suporte a aliases.
- Ampliaria a análise semântica de citações, separando frequência de contexto, sentimento e posição da marca na resposta.
- Adicionaria métricas e observabilidade mais completas, como latência por endpoint e métricas de negócio.
- Configuraria CI/CD para executar lint, testes e cobertura a cada alteração.
- Adicionaria autenticação e configuração de CORS/rate limiting adequada ao ambiente de produção.

## Licença

Consulte [`LICENSE`](LICENSE).