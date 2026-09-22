# Brand Mention Analytics

Serviço de análise de menções de marcas em respostas geradas por ferramentas de Inteligência Artificial.

O sistema recebe um conjunto de respostas coletadas de plataformas de IA generativa, como ChatGPT, Gemini e Perplexity, identifica menções às marcas monitoradas e disponibiliza métricas sobre essa presença por meio de uma API HTTP.

O projeto foi desenvolvido com foco em **separação de responsabilidades, testabilidade, persistência, tratamento de dados imperfeitos e facilidade de evolução**.

---

# 1. Objetivo

Ferramentas de Inteligência Artificial generativa podem mencionar diferentes empresas e marcas ao responder perguntas de usuários.

O objetivo deste projeto é transformar um conjunto de respostas coletadas automaticamente em dados estruturados que permitam responder perguntas como:

- Com que frequência uma determinada marca aparece nas respostas?
- Qual é o Share of Voice de uma marca?
- Como a presença da marca varia entre diferentes plataformas?
- Quais respostas mencionam mais marcas?
- Quais respostas apresentam maior concentração de menções?

As marcas monitoradas inicialmente são:

```text
Acme
Zenith
Nimbus
```

O sistema foi projetado de forma que novas marcas possam ser adicionadas posteriormente sem alteração significativa da lógica da aplicação.

---

# 2. Funcionamento geral

O processamento é dividido em algumas etapas principais:

```text
                    respostas.json
                         │
                         ▼
                ┌──────────────────┐
                │     Ingestão     │
                │                  │
                │ Validação        │
                │ Normalização     │
                │ Deduplicação     │
                └────────┬─────────┘
                         │
                         ▼
                ┌──────────────────┐
                │ Detecção de      │
                │ menções          │
                │                  │
                │ Acme             │
                │ Zenith           │
                │ Nimbus           │
                └────────┬─────────┘
                         │
                         ▼
                ┌──────────────────┐
                │    Persistência  │
                │                  │
                │    SQLite        │
                └────────┬─────────┘
                         │
                         ▼
                ┌──────────────────┐
                │     Analytics    │
                │                  │
                │ Share of Voice   │
                │ Top citações     │
                └────────┬─────────┘
                         │
                         ▼
                ┌──────────────────┐
                │     FastAPI      │
                │                  │
                │ HTTP / REST API  │
                └──────────────────┘
```

A API não realiza diretamente a detecção das marcas ou os cálculos analíticos. Essas responsabilidades ficam separadas em serviços próprios.

Essa separação permite testar e alterar cada parte do sistema de forma independente.

---

# 3. Entendendo os conceitos

## Share of Voice (SOV)

Share of Voice (SOV) é uma métrica utilizada para representar a participação de uma marca dentro de um determinado conjunto de menções ou conteúdo analisado.

Neste projeto, o conceito é adaptado para respostas de Inteligência Artificial.

O projeto **não mede participação de mercado**. A métrica responde à seguinte pergunta:

> **Em qual percentual das respostas de IA uma determinada marca é mencionada?**

### Importante

Uma resposta é diferente de uma ocorrência.

Por exemplo:

```text
"Acme é uma ótima ferramenta. A Acme também possui..."
```

Nesse caso:

- a Acme aparece em **1 resposta**;
- a Acme possui **2 ocorrências** dentro dessa resposta.

A fórmula utilizada será:

```text
Share of Voice =
(quantidade de respostas que mencionam a marca / quantidade total de respostas) × 100
```

---

## Citação forte

Para o endpoint `/top-citacoes`, será utilizado um score para identificar respostas com maior concentração de menções às marcas monitoradas.

Neste projeto, uma **citação forte** não representa uma avaliação semântica da importância da marca. O termo representa uma resposta que possui maior concentração de menções, considerando:

- quantidade de marcas distintas;
- frequência total de ocorrências.

O score utilizado será:

```text
score = (3 × marcas_distintas) + frequencia
```

### Diversidade de marcas

A quantidade de marcas distintas aumenta o score.

Por exemplo:

```text
"Acme + Zenith + Nimbus"
```

possui uma diversidade maior do que:

```text
"Acme"
```

Portanto, a primeira resposta terá um score maior.

Foi atribuído peso `3` à diversidade para que a presença de múltiplas marcas tenha maior influência no score do que simples repetições da mesma marca.

### Frequência

A frequência representa quantas vezes as marcas monitoradas aparecem na resposta.

Por exemplo:

```text
"Acme, Acme, Acme"
```

possui 3 ocorrências, enquanto:

```text
"Acme"
```

possui apenas 1 ocorrência.

### Exemplo

Para uma resposta contendo:

```text
"Acme, Zenith e Nimbus são ferramentas conhecidas. Acme possui grande presença no mercado."
```

temos:

```text
marcas_distintas = 3
frequencia = 4

score = (3 × 3) + 4
score = 13
```

O score será utilizado para ordenar as respostas no endpoint:

```http
GET /top-citacoes?n=5
```

---

# 4. Tratamento de dados

O arquivo de entrada representa dados provenientes de scraping automático e, portanto, não é considerado completamente confiável.

O sistema deve ser tolerante a inconsistências sem comprometer a integridade dos dados.

Entre os problemas esperados estão:

- plataformas com diferentes capitalizações;
- formatos diferentes de data;
- campos opcionais;
- respostas vazias;
- registros duplicados;
- modelos ausentes;
- diferentes formas de escrever uma mesma marca.

Por exemplo, o conjunto de dados pode conter:

```text
ChatGPT
chatgpt
Chat-GPT
```

que representam a mesma plataforma.

Da mesma forma, uma marca pode aparecer como:

```text
Acme
ACME
A.C.M.E.
```

Essas variações serão tratadas durante a normalização.

---

# 5. Detecção de menções

A detecção será inicialmente baseada em processamento determinístico de texto.

O fluxo será:

```text
Texto original
      │
      ▼
Normalização
      │
      ├── case-insensitive
      ├── normalização Unicode
      ├── remoção de pontuação relevante
      └── normalização de espaços
      │
      ▼
Aplicação de aliases
      │
      ▼
Busca das marcas
      │
      ▼
Menções identificadas
```

A estratégia foi escolhida em vez de utilizar um modelo de Inteligência Artificial porque o problema inicial é bem definido e possui um conjunto pequeno e conhecido de marcas.

Uma solução determinística possui algumas vantagens:

- comportamento previsível;
- baixo custo computacional;
- fácil reprodução;
- facilidade para escrever testes;
- facilidade para explicar por que uma menção foi detectada.

Por exemplo:

```text
"A.C.M.E. é uma empresa conhecida"
```

poderá ser normalizado antes da busca para permitir que seja reconhecido como uma menção à marca `Acme`.

---

# 6. Persistência das menções

Além de armazenar a resposta original, o sistema armazenará as menções identificadas.

Conceitualmente:

```text
Resposta
   │
   ├── Acme
   │     └── 2 ocorrências
   │
   └── Zenith
         └── 1 ocorrência
```

Isso evita a necessidade de executar novamente a detecção das marcas sempre que uma métrica for solicitada.

Também permite futuras análises sobre a quantidade de ocorrências de cada marca.

O texto original da resposta será preservado para possibilitar a auditoria do resultado da detecção.

---

# 7. Deduplicação

Os registros possuem um identificador próprio (`id`).

Esse identificador será tratado como único.

A ingestão será idempotente: caso o mesmo registro seja processado novamente, ele não deverá ser duplicado no banco.

Isso é importante porque arquivos provenientes de scraping podem conter registros repetidos ou podem ser processados mais de uma vez.

A decisão também permite executar novamente o processo de ingestão sem alterar incorretamente os resultados.

---

# 8. Share of Voice

O endpoint:

```http
GET /share-of-voice?marca=Acme
```

retornará o percentual de respostas que mencionam a marca.

A fórmula utilizada será:

```text
Share of Voice =
(respostas que mencionam a marca / total de respostas) × 100
```

O resultado também será dividido por plataforma.

Exemplo conceitual:

```json
{
  "marca": "Acme",
  "total_respostas": 100,
  "respostas_com_mencao": 35,
  "share_of_voice": 35.0,
  "por_plataforma": {
    "chatgpt": {
      "total_respostas": 40,
      "respostas_com_mencao": 20,
      "share_of_voice": 50.0
    },
    "gemini": {
      "total_respostas": 35,
      "respostas_com_mencao": 10,
      "share_of_voice": 28.57
    }
  }
}
```

A métrica representa a presença da marca no conjunto de respostas analisado, e não a participação em um mercado real.

---

# 9. API

A primeira versão da API terá os seguintes endpoints:

## `GET /share-of-voice`

Consulta a presença de uma marca.

```http
GET /share-of-voice?marca=Acme
```

O resultado apresentará o Share of Voice geral e a distribuição da métrica por plataforma.

---

## `GET /top-citacoes`

Retorna as respostas com maior Citation Strength Score.

```http
GET /top-citacoes?n=5
```

O parâmetro `n` define a quantidade de respostas retornadas.

---

## `POST /respostas`

Adiciona uma nova resposta ao conjunto de dados.

```http
POST /respostas
```

Exemplo:

```json
{
  "id": "r011",
  "pergunta": "Qual ferramenta você recomenda?",
  "plataforma": "ChatGPT",
  "modelo": "gpt-5.1",
  "resposta_texto": "A Acme é uma opção bastante conhecida.",
  "data_hora": "2026-01-23T10:00:00",
  "sentimento": "positivo"
}
```

A resposta será validada, processada, analisada e persistida.

---

# 10. Fluxo de uma nova resposta

Quando uma nova resposta é enviada para a API:

```text
POST /respostas
       │
       ▼
Validação Pydantic
       │
       ▼
Normalização
       │
       ▼
Detecção de menções
       │
       ▼
Cálculo dos dados derivados
       │
       ▼
Persistência
       │
       ▼
Resposta HTTP
```

A API não precisa executar manualmente nenhuma etapa adicional.

---

# 11. Decisões arquiteturais

As principais decisões deste projeto foram tomadas buscando equilíbrio entre simplicidade e possibilidade de evolução.

## Por que não um único arquivo?

Porque a aplicação possui responsabilidades diferentes:

```text
HTTP
Business Logic
Persistence
Ingestion
Validation
Analytics
```

Mantê-las separadas facilita testes, manutenção e evolução.

A estrutura final de diretórios e a responsabilidade de cada módulo serão documentadas após a implementação.

---

## Por que não microsserviços?

O problema possui escopo pequeno e não apresenta necessidade de distribuição independente dos componentes.

Um monólito modular oferece menor complexidade operacional, mantendo uma boa separação de responsabilidades.

---

## Por que não utilizar um LLM para detectar as marcas?

As marcas monitoradas são conhecidas e a tarefa inicial consiste em identificar ocorrências textuais.

Uma solução determinística é suficiente e apresenta comportamento mais previsível.

Além disso, ela possui menor custo computacional, facilita a reprodução dos resultados e permite testar de forma mais objetiva a detecção das menções.

---

## Por que SQLite?

O SQLite atende ao volume esperado para o desafio e não exige infraestrutura externa.

Além disso, permite manter a execução do projeto simples durante o desenvolvimento.

Em um ambiente de produção com maior volume de dados ou múltiplas instâncias da aplicação, a persistência poderia ser migrada para PostgreSQL.

---

# 12. Possíveis evoluções

Com mais tempo e um volume de produção maior, algumas evoluções seriam consideradas.

## PostgreSQL

Substituir o SQLite por PostgreSQL para cenários com maior concorrência e volume de dados.

---

## Alembic

Adicionar migrations para controlar a evolução do schema do banco de dados.

---

## Processamento assíncrono

Para grandes volumes de respostas, a ingestão poderia ser desacoplada da API através de uma fila:

```text
API
 │
 ▼
Queue
 │
 ▼
Workers
 │
 ├── Normalização
 ├── Detecção
 └── Persistência
```

Isso permitiria processar grandes quantidades de respostas sem bloquear as requisições da API.

---

## Detecção semântica

Uma evolução futura seria utilizar modelos de linguagem ou modelos especializados para identificar menções mais complexas.

Por exemplo, uma resposta poderia mencionar uma empresa indiretamente, sem utilizar exatamente seu nome.

Essa abordagem, porém, aumentaria a complexidade, o custo computacional e a necessidade de avaliação da qualidade dos resultados.

Por isso, não faz parte da primeira versão do projeto.

---

# 13. Testes

Os testes serão concentrados principalmente nas partes que possuem regras de negócio ou maior possibilidade de apresentar comportamentos incorretos, como:

- normalização dos dados;
- detecção de menções;
- reconhecimento de variações das marcas;
- cálculo do Share of Voice;
- cálculo do Citation Strength Score;
- validação das respostas recebidas pela API;
- deduplicação e idempotência da ingestão.

A cobertura e a estrutura definitiva dos testes serão documentadas após a implementação.

---

# 14. Qualidade de código

O projeto utiliza **Ruff** para linting e formatação do código Python.

Para verificar problemas:

```bash
ruff check .
```

Para formatar o código:

```bash
ruff format .
```

Para verificar se o código já está formatado, sem modificar os arquivos:

```bash
ruff format --check .
```

Os testes serão executados com:

```bash
pytest
```

---

# 15. Próximos passos

A implementação será realizada de forma incremental:

```text
1. Configuração do projeto
        ↓
2. Modelagem dos dados
        ↓
3. Persistência
        ↓
4. Ingestão do JSON
        ↓
5. Normalização
        ↓
6. Detecção de menções
        ↓
7. Cálculo das métricas
        ↓
8. API
        ↓
9. Testes
        ↓
10. Documentação final
```

A documentação da estrutura de diretórios, instalação, execução e exemplos reais da API será adicionada após a implementação para refletir a arquitetura efetivamente utilizada.