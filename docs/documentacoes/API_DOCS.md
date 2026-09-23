# Documentação da API

## 5. Códigos de resposta HTTP

A API utiliza códigos de status HTTP para indicar o resultado do processamento de cada requisição.

### GET /share-of-voice

| Código | Descrição |
|---|---|
| `200 OK` | Requisição processada com sucesso. |
| `422 Unprocessable Content` | Parâmetro `marca` ausente, vazio ou inválido. |

### GET /top-citacoes

| Código | Descrição |
|---|---|
| `200 OK` | Requisição processada com sucesso. |
| `422 Unprocessable Content` | Parâmetro `n` inválido ou menor que `1`. |

### POST /respostas

| Código | Descrição |
|---|---|
| `201 Created` | Respostas criadas e persistidas com sucesso. |
| `422 Unprocessable Content` | Dados enviados não atendem aos schemas de validação. |

### Código 422 — Erro de validação

O código `422 Unprocessable Content` é utilizado quando os dados recebidos não atendem às regras de validação definidas pelos schemas Pydantic ou pelos parâmetros dos endpoints.

Entre os casos tratados estão:

- parâmetros obrigatórios ausentes;
- parâmetros com valores inválidos;
- `n` menor que `1`;
- `id` vazio;
- `pergunta` ausente;
- `plataforma` ausente;
- `resposta_texto` ausente ou vazio;
- payload incompleto;
- payload em formato incompatível;
- `data_hora` em formato não reconhecido.

---

## 6. Exemplos de requisições e respostas

### 6.1 GET /share-of-voice

Calcula a participação de uma marca entre as respostas cadastradas.

#### Requisição

```http
GET /share-of-voice?marca=Acme
```

#### Resposta — 200 OK

```json
{
  "marca": "Acme",
  "respostas_com_mencao": 2,
  "total_respostas": 4,
  "percentual": 50.0,
  "por_plataforma": [
    {
      "plataforma": "ChatGPT",
      "respostas_com_mencao": 2,
      "total_respostas": 2,
      "percentual": 100.0
    },
    {
      "plataforma": "Gemini",
      "respostas_com_mencao": 0,
      "total_respostas": 1,
      "percentual": 0.0
    }
  ]
}
```

#### Exemplo de erro — 422

```http
GET /share-of-voice
```

```json
{
  "detail": [
    {
      "type": "missing",
      "loc": ["query", "marca"],
      "msg": "Field required"
    }
  ]
}
```

### 6.2 GET /top-citacoes

Retorna as respostas com maior score de citação.

#### Requisição

```http
GET /top-citacoes?n=2
```

#### Resposta — 200 OK

```json
[
  {
    "resposta_id": "r002",
    "plataforma": "ChatGPT",
    "modelo": "gpt-5.1",
    "resposta_texto": "Acme e Zenith são conhecidas.",
    "marcas": ["Acme", "Zenith"],
    "score": 6.0
  },
  {
    "resposta_id": "r003",
    "plataforma": "Gemini",
    "modelo": "gemini-2.5-pro",
    "resposta_texto": "Zenith é uma opção.",
    "marcas": ["Zenith"],
    "score": 5.0
  }
]
```

O parâmetro `n` determina a quantidade máxima de resultados retornados. Quando não informado, o valor padrão é `5`.

#### Exemplo de erro — 422

```http
GET /top-citacoes?n=0
```

```json
{
  "detail": [
    {
      "type": "greater_than_equal",
      "loc": ["query", "n"],
      "msg": "Input should be greater than or equal to 1"
    }
  ]
}
```

### 6.3 POST /respostas

Cria uma ou mais respostas e realiza automaticamente a detecção das menções presentes no texto.

#### Requisição

```http
POST /respostas
Content-Type: application/json
```

```json
[
  {
    "id": "r100",
    "pergunta": "Qual a melhor ferramenta de monitoramento?",
    "plataforma": "ChatGPT",
    "modelo": "gpt-5.1",
    "resposta_texto": "A Acme é uma boa opção. A Zenith também é conhecida.",
    "data_hora": "2026-01-20T10:00:00",
    "sentimento": "positivo"
  }
]
```

#### Resposta — 201 Created

```json
[
  {
    "id": "r100",
    "pergunta": "Qual a melhor ferramenta de monitoramento?",
    "plataforma": "ChatGPT",
    "modelo": "gpt-5.1",
    "resposta_texto": "A Acme é uma boa opção. A Zenith também é conhecida.",
    "data_hora": "2026-01-20T10:00:00",
    "sentimento": "positivo",
    "mencoes": [
      {
        "id": 1,
        "resposta_id": "r100",
        "marca": "Acme",
        "ocorrencias": 1
      },
      {
        "id": 2,
        "resposta_id": "r100",
        "marca": "Zenith",
        "ocorrencias": 1
      }
    ]
  }
]
```

### 6.4 Criando múltiplas respostas

O endpoint também aceita uma lista contendo várias respostas.

#### Requisição

```http
POST /respostas
Content-Type: application/json
```

```json
[
  {
    "id": "r101",
    "pergunta": "Qual ferramenta é recomendada?",
    "plataforma": "ChatGPT",
    "modelo": "gpt-5.1",
    "resposta_texto": "A Acme é uma boa opção.",
    "data_hora": "2026-01-20T10:00:00",
    "sentimento": "positivo"
  },
  {
    "id": "r102",
    "pergunta": "Qual empresa é conhecida?",
    "plataforma": "Gemini",
    "modelo": "gemini-2.5-pro",
    "resposta_texto": "A Zenith é uma empresa conhecida.",
    "data_hora": "2026-01-20T11:00:00",
    "sentimento": "neutro"
  }
]
```

#### Resposta — 201 Created

A API retorna uma lista contendo as respostas criadas e as respectivas menções detectadas.

### 6.5 Formatos de data aceitos

O campo `data_hora` possui normalização durante a validação da entrada.

Os formatos atualmente aceitos são:

```text
YYYY-MM-DDTHH:MM:SS
YYYY-MM-DD HH:MM:SS
YYYY-MM-DD
DD/MM/YYYY
YYYY/MM/DD
```

Valores que não correspondem a nenhum dos formatos suportados resultam em erro de validação `422`.