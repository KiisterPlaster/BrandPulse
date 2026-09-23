# Documentação da API

A API do BrandPulse é construída com FastAPI e disponibiliza ingestão, análise e health check.

## Endpoints

| Método | Endpoint | Finalidade |
|---|---|---|
| `GET` | `/health` | Verificar se a aplicação está disponível. |
| `GET` | `/share-of-voice` | Calcular a presença de uma marca nas respostas. |
| `GET` | `/top-citacoes` | Retornar as respostas com maior score de citação. |
| `POST` | `/respostas` | Validar, processar e persistir novas respostas. |

A documentação OpenAPI interativa é disponibilizada pelo FastAPI em `/docs`.

---

## `GET /health`

Retorna o estado básico da aplicação.

### Resposta `200`

```json
{"status": "ok"}
```

---

## `GET /share-of-voice`

Calcula o percentual de respostas que mencionam a marca informada e apresenta o resultado também por plataforma.

### Parâmetro

| Parâmetro | Tipo | Regra |
|---|---|---|
| `marca` | `string` | obrigatório e não vazio |

### Exemplo

```http
GET /share-of-voice?marca=Acme
```

### Resposta `200`

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
    }
  ]
}
```

O cálculo considera respostas, e não o número de ocorrências da marca dentro de uma resposta:

```text
SOV = (respostas com menção / total de respostas) × 100
```

### Erros

`422 Unprocessable Content` quando `marca` está ausente, vazia ou inválida.

---

## `GET /top-citacoes`

Retorna até `n` respostas com maior score de citação.

### Parâmetro

| Parâmetro | Tipo | Padrão | Regra |
|---|---|---:|---|
| `n` | `integer` | `5` | deve ser `>= 1` |

### Exemplo

```http
GET /top-citacoes?n=2
```

### Resposta `200`

```json
[
  {
    "resposta_id": "r002",
    "plataforma": "ChatGPT",
    "modelo": "gpt-5.1",
    "resposta_texto": "Acme e Zenith são conhecidas.",
    "marcas": ["Acme", "Zenith"],
    "score": 6.0
  }
]
```

O score utilizado atualmente é:

```text
score = (2 × marcas_distintas) + ocorrencias_totais
```

Apenas respostas com pelo menos uma menção participam do ranking.

### Erros

`422 Unprocessable Content` quando `n < 1` ou possui formato inválido.

---

## `POST /respostas`

Recebe uma lista de respostas. Cada item é validado individualmente.

O processamento inclui:

1. validação pelo `RespostaCreate`;
2. normalização da data;
3. detecção das marcas monitoradas;
4. normalização da plataforma;
5. criação das entidades de menção;
6. verificação de duplicidade;
7. persistência no SQLite.

### Exemplo

```http
POST /respostas
Content-Type: application/json
```

```json
[
  {
    "id": "r100",
    "pergunta": "Qual ferramenta é recomendada?",
    "plataforma": "ChatGPT",
    "modelo": "gpt-5.1",
    "resposta_texto": "A Acme é uma boa opção. A Zenith também é conhecida.",
    "data_hora": "2026-09-22T10:00:00",
    "sentimento": "positivo"
  }
]
```

### Resposta `201`

A API retorna as respostas criadas, incluindo as menções detectadas.

### Validação parcial

Um item inválido não impede o processamento dos demais. Se nenhuma resposta válida for criada, a API retorna `422` com a relação de dados inválidos.

### Duplicidade

Registros identificados como duplicados são ignorados. Se houver ao menos uma nova resposta válida, o endpoint mantém o status `201` e retorna as respostas criadas.

---

## Códigos HTTP

| Código | Uso |
|---|---|
| `200` | Consulta ou health check concluído. |
| `201` | Novas respostas persistidas. |
| `404` | Rota inexistente. |
| `422` | Parâmetros ou payload inválidos, ou nenhuma nova resposta criada. |
| `429` | Limite de requisições excedido. |

A aplicação possui tratamento próprio para rotas inexistentes e para exceder o rate limit.

---

## Datas aceitas

O campo `data_hora` aceita:

```text
YYYY-MM-DDTHH:MM:SS
YYYY-MM-DD HH:MM:SS
YYYY-MM-DD
DD/MM/YYYY
YYYY/MM/DD
```

Após a validação, o valor é representado como `datetime`.