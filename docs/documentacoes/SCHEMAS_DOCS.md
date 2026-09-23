# Documentação dos Schemas

Este documento descreve os schemas Pydantic utilizados pelo BrandPulse para validação dos dados de entrada e saída da API.

## `app/schemas/analytics.py`

Define os schemas utilizados pelas rotas de análise, principalmente **Share of Voice** e **Top Citações**.

### `PlatformShare`

Representa os dados de participação de uma marca em uma plataforma específica.

| Campo | Tipo | Validação | Descrição |
|---|---|---|---|
| `plataforma` | `str` | — | Nome da plataforma analisada. |
| `respostas_com_mencao` | `int` | `>= 0` | Quantidade de respostas que mencionaram a marca. |
| `total_respostas` | `int` | `>= 0` | Quantidade total de respostas analisadas. |
| `percentual` | `float` | `0 <= valor <= 100` | Percentual de respostas com menção à marca. |

### `ShareOfVoiceResponse`

Representa o resultado completo da análise de **Share of Voice**.

| Campo | Tipo | Validação | Descrição |
|---|---|---|---|
| `marca` | `str` | — | Marca analisada. |
| `respostas_com_mencao` | `int` | `>= 0` | Quantidade de respostas que mencionaram a marca. |
| `total_respostas` | `int` | `>= 0` | Quantidade total de respostas analisadas. |
| `percentual` | `float` | `0 <= valor <= 100` | Percentual geral de Share of Voice. |
| `por_plataforma` | `list[PlatformShare]` | — | Share of Voice detalhado por plataforma. |

### `TopCitacaoResponse`

Representa um resultado da análise de **Top Citações**.

| Campo | Tipo | Validação | Descrição |
|---|---|---|---|
| `resposta_id` | `str` | — | Identificador da resposta analisada. |
| `plataforma` | `str` | — | Plataforma da resposta. |
| `modelo` | `str \| None` | — | Modelo de IA utilizado, quando disponível. |
| `resposta_texto` | `str` | — | Texto da resposta analisada. |
| `marcas` | `list[str]` | — | Marcas identificadas na resposta. |
| `score` | `float` | `>= 0` | Pontuação utilizada na classificação da citação. |

---

## `app/schemas/respostas.py`

Define os schemas utilizados no fluxo de criação e retorno das respostas.

### `RespostaCreate`

Representa os dados recebidos pela API para criação de uma resposta.

| Campo | Tipo | Validação | Descrição |
|---|---|---|---|
| `id` | `str` | mínimo de 1 caractere | Identificador da resposta. |
| `pergunta` | `str` | mínimo de 1 caractere | Pergunta enviada ao modelo de IA. |
| `plataforma` | `str` | mínimo de 1 caractere | Plataforma de IA utilizada. |
| `modelo` | `str \| None` | opcional | Modelo utilizado para gerar a resposta. |
| `resposta_texto` | `str` | mínimo de 1 caractere | Texto retornado pela plataforma. |
| `data_hora` | `datetime` | — | Data e horário associados à resposta. |
| `sentimento` | `str \| None` | opcional | Sentimento associado à resposta. |

### Normalização de `data_hora`

O campo `data_hora` possui um `field_validator` executado antes da validação padrão do Pydantic.

São aceitos os seguintes formatos:

```text
2026-01-20T10:00:00
2026-01-20 10:00:00
2026-01-20
20/01/2026
2026/01/20
```

Quando o valor corresponde a um desses formatos, ele é convertido para `datetime`.

Valores que não correspondem aos formatos definidos são encaminhados ao Pydantic para validação.

### `RespostasCreate`

Representa uma coleção de respostas.

| Campo | Tipo | Descrição |
|---|---|---|
| `respostas` | `list[RespostaCreate]` | Lista de respostas a serem processadas. |

### `MencaoResponse`

Representa uma menção de marca associada a uma resposta.

O schema utiliza `ConfigDict(from_attributes=True)`, permitindo sua construção a partir de objetos com atributos, como modelos SQLAlchemy.

| Campo | Tipo | Descrição |
|---|---|---|
| `id` | `int` | Identificador da menção. |
| `resposta_id` | `str` | Identificador da resposta associada. |
| `marca` | `str` | Nome da marca mencionada. |
| `ocorrencias` | `int` | Quantidade de ocorrências da marca. |

### `RespostaResponse`

Representa uma resposta retornada pela API.

Também utiliza `ConfigDict(from_attributes=True)` para permitir a conversão dos objetos de persistência para o schema de resposta.

| Campo | Tipo | Descrição |
|---|---|---|
| `id` | `str` | Identificador da resposta. |
| `pergunta` | `str` | Pergunta associada à resposta. |
| `plataforma` | `str` | Plataforma de IA utilizada. |
| `modelo` | `str \| None` | Modelo utilizado, quando disponível. |
| `resposta_texto` | `str` | Texto da resposta. |
| `data_hora` | `datetime` | Data e horário da resposta. |
| `sentimento` | `str \| None` | Sentimento associado à resposta. |
| `mencoes` | `list[MencaoResponse]` | Menções de marcas identificadas na resposta. |

## Fluxo dos Schemas

### Criação de respostas

```text
Requisição HTTP
      │
      ▼
RespostaCreate
      │
      ├── Validação dos campos
      └── Normalização de data_hora
      │
      ▼
Processamento da aplicação
      │
      ▼
RespostaResponse
      │
      └── MencaoResponse
```

### Analytics

```text
Dados processados
      │
      ├── ShareOfVoiceResponse
      │       └── PlatformShare
      │
      └── TopCitacaoResponse
```

Os schemas funcionam, portanto, como a camada responsável por definir e validar o formato dos dados que entram e saem da API.