# Estrutura do Projeto BrandPulse

## 1. Visão geral

O BrandPulse é organizado em camadas, separando as responsabilidades da aplicação entre API, schemas, serviços, repositórios, modelos e banco de dados.

Essa organização facilita a manutenção do código, a realização de testes e a evolução da aplicação.

---

## 2. Estrutura de diretórios

```text
BrandPulse/
├── app/
│   ├── api/
│   │   └── routes/
│   ├── core/
│   ├── database/
│   ├── models/
│   ├── repositories/
│   ├── schemas/
│   └── services/
│
├── data/
├── docs/
│   ├── documentacoes/
│   └── STEP_BY_STEP.md
│
├── tests/
│   └── fixtures/
│
├── LICENSE
├── README.md
├── SECURITY.md
├── pyproject.toml
└── uv.lock
```

---

## 3. Diretório `app`

Contém o código principal da aplicação.

### `app/api`

Responsável pela camada de API da aplicação.

As rotas são organizadas dentro do diretório `routes`.

#### `app/api/routes/analytics.py`

Contém as rotas relacionadas às análises da aplicação:

- `GET /share-of-voice`
- `GET /top-citacoes`

#### `app/api/routes/respostas.py`

Contém a rota responsável pela criação de respostas:

- `POST /respostas`

As rotas recebem as requisições HTTP, validam os dados através dos schemas e encaminham o processamento para as camadas responsáveis.

---

## 4. Diretório `app/core`

Contém componentes centrais da aplicação.

### `app/core/limiter.py`

Contém a configuração relacionada ao controle de requisições da aplicação.

---

## 5. Diretório `app/database`

Responsável pela configuração e inicialização do banco de dados.

### `connection.py`

Responsável pela configuração da conexão com o banco de dados e pela criação das sessões utilizadas pela aplicação.

### `init_db.py`

Responsável pela inicialização do banco de dados.

### `tables.py`

Contém a configuração da base declarativa utilizada pelos modelos SQLAlchemy.

---

## 6. Diretório `app/models`

Contém os modelos ORM utilizados para representar as entidades persistidas no banco de dados.

### `resposta.py`

Define o modelo `Resposta`.

Representa as respostas analisadas pelo BrandPulse.

### `mencao.py`

Define o modelo `Mencao`.

Representa as marcas identificadas dentro das respostas.

---

## 7. Diretório `app/repositories`

Responsável pelo acesso aos dados persistidos.

### `respostas.py`

Contém o `RespostaRepository`, responsável pelas operações relacionadas às respostas.

Entre as operações disponíveis estão:

- criação de respostas;
- busca de resposta por ID;
- listagem de respostas;
- verificação de existência;
- listagem de respostas que mencionam determinada marca.

O repository concentra as operações de acesso ao banco, evitando que essa responsabilidade fique diretamente nas rotas ou nos serviços.

---

## 8. Diretório `app/schemas`

Contém os schemas Pydantic utilizados para validação e serialização dos dados.

### `analytics.py`

Define os schemas utilizados pelas rotas de análise:

- `PlatformShare`
- `ShareOfVoiceResponse`
- `TopCitacaoResponse`

### `respostas.py`

Define os schemas relacionados às respostas:

- `RespostaCreate`
- `RespostasCreate`
- `MencaoResponse`
- `RespostaResponse`

Os schemas são utilizados para validar os dados recebidos pela API e definir o formato das respostas retornadas pelos endpoints.

---

## 9. Diretório `app/services`

Contém as regras de negócio da aplicação.

### `analytics.py`

Implementa as regras utilizadas pelas análises do BrandPulse.

Entre as funcionalidades estão:

- cálculo do Share of Voice;
- cálculo do score de citação;
- obtenção das respostas com maior número de citações.

### `ingestao.py`

Contém a lógica relacionada à ingestão das respostas utilizadas pela aplicação.

### `mencoes.py`

Contém a lógica responsável pela identificação das marcas monitoradas dentro dos textos.

---

## 10. `app/main.py`

É o ponto de entrada da aplicação FastAPI.

É responsável pela criação e configuração da aplicação e pelo registro das rotas.

---

## 11. Diretório `data`

Contém os dados utilizados pela aplicação.

### `database.db`

Banco de dados utilizado localmente pela aplicação.

### `respostas_exemplo.json`

Arquivo contendo respostas utilizadas como dados de exemplo.

---

## 12. Diretório `docs`

Concentra a documentação do projeto.

### `docs/documentacoes/`

Contém documentações específicas dos componentes da aplicação.

Atualmente estão documentados:

- `API_DOCS.md` — documentação dos endpoints da API;
- `SCHEMAS_DOCS.md` — documentação dos schemas Pydantic;
- `ESTRUTURA_PROJETO.md` — documentação da organização do projeto.

### `docs/STEP_BY_STEP.md`

Contém o acompanhamento do desenvolvimento do BrandPulse e a descrição dos steps do projeto.

---

## 13. Diretório `tests`

Contém os testes automatizados da aplicação.

Os testes são separados de acordo com a camada ou funcionalidade testada.

### Arquivos de teste

- `test_analytics.py` — testes dos serviços de analytics;
- `test_database.py` — testes relacionados ao banco de dados;
- `test_ingestao.py` — testes da ingestão;
- `test_mencoes.py` — testes da detecção de menções;
- `test_models.py` — testes dos modelos;
- `test_repositories.py` — testes dos repositories;
- `test_routes.py` — testes das rotas da API;
- `test_schemas.py` — testes dos schemas.

### `tests/fixtures/`

Contém arquivos utilizados como dados de teste.

Atualmente estão presentes:

- `respostas_invalidas.json`;
- `respostas_minimas.json`;
- `respostas_teste.json`;
- `respostas_validas.json`.

---

## 14. Arquivos de configuração e documentação

### `pyproject.toml`

Contém as configurações do projeto Python, incluindo dependências e ferramentas utilizadas no desenvolvimento.

### `uv.lock`

Registra as versões das dependências utilizadas pelo projeto.

### `README.md`

Contém a documentação principal do projeto.

### `SECURITY.md`

Contém informações relacionadas à segurança do projeto.

### `LICENSE`

Define os termos de licenciamento do projeto.

---

## 15. Fluxo da aplicação

O fluxo principal da aplicação segue a separação entre as diferentes camadas:

```text
                    Requisição HTTP
                           │
                           ▼
                    ┌─────────────┐
                    │    Router   │
                    └──────┬──────┘
                           │
                           ▼
                    ┌─────────────┐
                    │   Schema    │
                    └──────┬──────┘
                           │
                           ▼
                    ┌─────────────┐
                    │   Service   │
                    └──────┬──────┘
                           │
                           ▼
                    ┌─────────────┐
                    │ Repository  │
                    └──────┬──────┘
                           │
                           ▼
                    ┌─────────────┐
                    │    Model    │
                    └──────┬──────┘
                           │
                           ▼
                    ┌─────────────┐
                    │  Database   │
                    └─────────────┘
```

### Responsabilidade de cada camada

| Camada | Responsabilidade |
|---|---|
| Router | Receber e responder às requisições HTTP |
| Schema | Validar e serializar os dados |
| Service | Executar as regras de negócio |
| Repository | Realizar operações de acesso aos dados |
| Model | Representar as entidades do banco |
| Database | Persistir os dados |

Essa separação permite que cada componente tenha uma responsabilidade específica e reduz o acoplamento entre as diferentes partes da aplicação.

---

## 16. Fluxo de criação de uma resposta

Para o endpoint `POST /respostas`, o fluxo principal é:

```text
POST /respostas
       │
       ▼
RespostaCreate
       │
       ▼
Router de respostas
       │
       ▼
Detecção de menções
       │
       ▼
Criação de Resposta + Mencao
       │
       ▼
RespostaRepository
       │
       ▼
Banco de dados
       │
       ▼
RespostaResponse
       │
       ▼
Resposta HTTP 201
```

Durante esse processo, os dados recebidos são validados pelo Pydantic e as marcas presentes no texto da resposta são identificadas antes da persistência.

---

## 17. Fluxo das análises

As rotas de análise utilizam os dados armazenados para produzir informações agregadas.

### Share of Voice

```text
GET /share-of-voice
       │
       ▼
Router
       │
       ▼
Repository
       │
       ▼
Respostas armazenadas
       │
       ▼
Service de Analytics
       │
       ▼
ShareOfVoiceResponse
       │
       ▼
Resposta HTTP
```

### Top Citações

```text
GET /top-citacoes
       │
       ▼
Router
       │
       ▼
Repository
       │
       ▼
Respostas armazenadas
       │
       ▼
Service de Analytics
       │
       ▼
TopCitacaoResponse
       │
       ▼
Resposta HTTP
```

---

## 18. Testes

Os testes utilizam `pytest` e `TestClient` para validar o comportamento da aplicação.

A estrutura dos testes acompanha a estrutura das funcionalidades da aplicação, permitindo testar separadamente:

- modelos;
- banco de dados;
- repositories;
- services;
- schemas;
- ingestão;
- detecção de menções;
- rotas da API.

Os testes das rotas utilizam um banco SQLite em memória para evitar dependência do banco de dados utilizado em produção ou desenvolvimento.

---

## 19. Organização arquitetural

A organização atual do BrandPulse segue uma separação de responsabilidades entre:

```text
API
 │
 ├── Schemas
 │
 ├── Services
 │
 ├── Repositories
 │
 └── Models
        │
        ▼
     Database
```

Essa estrutura permite evoluir cada camada de maneira independente, mantendo as regras de negócio nos services e as operações de persistência nos repositories.