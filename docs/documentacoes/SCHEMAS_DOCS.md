# Documentação dos Schemas

Os schemas Pydantic definem os contratos de entrada e saída da API.

## `app/schemas/respostas.py`

### `RespostaCreate`

Entrada utilizada para criação de uma resposta.

| Campo | Tipo | Regra |
|---|---|---|
| `id` | `str` | mínimo de 1 caractere |
| `pergunta` | `str` | mínimo de 1 caractere |
| `plataforma` | `str` | mínimo de 1 caractere |
| `modelo` | `str \| None` | opcional |
| `resposta_texto` | `str` | mínimo de 1 caractere |
| `data_hora` | `datetime` | normalizado antes da validação |
| `sentimento` | `str \| None` | opcional |

O `field_validator` de `data_hora` aceita os formatos:

```text
YYYY-MM-DDTHH:MM:SS
YYYY-MM-DD HH:MM:SS
YYYY-MM-DD
DD/MM/YYYY
YYYY/MM/DD
```

### `RespostasCreate`

Agrupa uma lista de `RespostaCreate`:

```text
respostas: list[RespostaCreate]
```

### `MencaoResponse`

Representa uma menção retornada pela API. Utiliza `from_attributes=True` para permitir conversão a partir de objetos ORM.

| Campo | Tipo |
|---|---|
| `id` | `int` |
| `resposta_id` | `int` |
| `marca` | `str` |
| `ocorrencias` | `int` |

### `RespostaResponse`

Representa uma resposta persistida retornada pela API.

| Campo | Tipo |
|---|---|
| `id` | `int` |
| `resposta_id` | `str` |
| `pergunta` | `str` |
| `plataforma` | `str` |
| `modelo` | `str \| None` |
| `resposta_texto` | `str` |
| `data_hora` | `datetime` |
| `sentimento` | `str \| None` |
| `mencoes` | `list[MencaoResponse]` |

`id` representa o identificador interno do banco; `resposta_id` representa o identificador recebido no dado de origem.

### `StatusResponse`

Estrutura disponível para mensagens de status:

| Campo | Tipo |
|---|---|
| `message` | `str` |
| `respostas_invalidas` | `list[dict]` |

---

## `app/schemas/analytics.py`

### `PlatformShare`

Resultado do Share of Voice em uma plataforma.

| Campo | Tipo | Regra |
|---|---|---|
| `plataforma` | `str` | — |
| `respostas_com_mencao` | `int` | `>= 0` |
| `total_respostas` | `int` | `>= 0` |
| `percentual` | `float` | `0 <= valor <= 100` |

### `ShareOfVoiceResponse`

Resultado completo do Share of Voice.

| Campo | Tipo | Regra |
|---|---|---|
| `marca` | `str` | — |
| `respostas_com_mencao` | `int` | `>= 0` |
| `total_respostas` | `int` | `>= 0` |
| `percentual` | `float` | `0 <= valor <= 100` |
| `por_plataforma` | `list[PlatformShare]` | — |

### `TopCitacaoResponse`

Item retornado pelo ranking de citações.

| Campo | Tipo | Regra |
|---|---|---|
| `resposta_id` | `str` | — |
| `plataforma` | `str` | — |
| `modelo` | `str \| None` | opcional |
| `resposta_texto` | `str` | — |
| `marcas` | `list[str]` | — |
| `score` | `float` | `>= 0` |

## Fluxo

```text
JSON/HTTP
   │
   ▼
RespostaCreate
   │
   ▼
Services
   │
   ▼
SQLAlchemy
   │
   ▼
RespostaResponse
```

Os schemas mantêm a validação e o contrato HTTP separados das regras de negócio e da persistência.