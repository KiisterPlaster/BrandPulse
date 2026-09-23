# Step By Step

Arquivo destinado a registrar, de forma cronológica, as principais etapas, decisões e aprendizados durante o desenvolvimento do projeto.

O objetivo é documentar não apenas o que foi implementado, mas também **por que determinadas decisões foram tomadas**, quais alternativas foram consideradas e quais problemas surgiram ao longo do desenvolvimento.

## Etapas

### 1. Entendimento do problema
- Pesquisa sobre o problema proposto e seus principais conceitos.
- Consulta a projetos semelhantes e referências disponíveis.
- Uso de documentação técnica, pesquisas na internet e ferramentas de IA como apoio.
- Definição do que precisa ser desenvolvido e dos principais requisitos.
- Identificação das decisões técnicas que precisam ser tomadas antes da implementação.

### 2. Configuração inicial do projeto
- Criação da estrutura inicial do repositório.
- Configuração do ambiente de desenvolvimento.
- Definição das ferramentas e dependências iniciais.
- Adição e configuração do Ruff para linting e formatação do código.
- Criação dos arquivos de documentação:
  - `README.md`
  - `SECURITY.md`
  - `STEP_BY_STEP.md`
- Definição das primeiras convenções de organização e qualidade do projeto.

### 3. Modelagem dos dados
- Definição das entidades principais do projeto: `Resposta` e `Menção`.
- Definição dos campos e respectivos tipos para as entidades.
- Definição do relacionamento entre `Resposta` e `Menção`.
- Definição da quantidade de ocorrências de uma determinada marca em uma resposta.
- Definição dos schemas Pydantic para entrada e saída de dados da API.
- Criação dos modelos SQLAlchemy responsáveis pela persistência dos dados.
- Criação de arquivos JSON com diferentes conjuntos de dados para desenvolvimento e testes.
- Criação de uma fixture mínima para utilização nos testes.
- Avaliação inicial das regras de validação dos dados.

### 4. Testes da modelagem e do banco de dados
- Configuração do Pytest como ferramenta de testes automatizados.
- Criação de testes para os modelos `Resposta` e `Mencao`.
- Criação de testes para os schemas Pydantic responsáveis pela validação dos dados.
- Testes da criação de respostas e menções no banco de dados.
- Teste do relacionamento entre `Resposta` e `Mencao`.
- Teste do armazenamento da quantidade de ocorrências de cada menção.
- Criação de um banco SQLite em memória para os testes, evitando alterações no banco utilizado pela aplicação.
- Testes da conexão com o banco de dados.
- Teste da criação das tabelas definidas pelo SQLAlchemy.
- Durante a execução dos testes, foi identificado um `DetachedInstanceError` ao tentar acessar o relacionamento `mencoes` após o encerramento da sessão.
- O problema foi corrigido mantendo o acesso aos relacionamentos dentro da sessão ativa, respeitando o comportamento de carregamento lazy do SQLAlchemy.
- Ao final da etapa, foram executados os testes automatizados e as verificações de qualidade com Ruff.

### 5. Implementação da detecção de menções
- Definição das marcas monitoradas:
  - `Acme`
  - `Zenith`
  - `Nimbus`
- Definição das regras para identificação das marcas nas respostas.
- Implementação da busca case-insensitive.
- Tratamento de variações de escrita das marcas.
- Definição de como evitar falsos positivos em ocorrências de palavras.
- Implementação do serviço responsável por analisar uma resposta.
- Identificação das marcas mencionadas em cada resposta.
- Contagem das ocorrências de cada marca.
- Definição das informações que serão armazenadas em `Mencao`.
- Criação de testes unitários para a detecção de menções.
- Testes de diferentes casos, incluindo:
  - respostas sem marcas;
  - uma única marca;
  - múltiplas marcas;
  - múltiplas ocorrências da mesma marca;
  - diferenças entre letras maiúsculas e minúsculas;
  - variações de escrita;
  - textos com possíveis falsos positivos.

### 6. Implementação da ingestão de dados
- Implementação do serviço responsável pela leitura dos arquivos JSON.
- Utilização do Pydantic para validar os registros durante a ingestão.
- Tratamento de registros inválidos sem interromper o processamento dos demais registros.
- Validação de que os arquivos de entrada possuem uma lista de respostas.
- Integração da ingestão com o schema `RespostaCreate`.
- Criação e organização de fixtures específicas para testar diferentes cenários de entrada:
  - `respostas_minimas.json`
  - `respostas_teste.json`
  - `respostas_validas.json`
  - `respostas_invalidas.json`
- Criação de testes para arquivos válidos e inválidos.
- Teste do comportamento para arquivos inexistentes.
- Teste do comportamento para arquivos que não possuem uma lista de respostas.
- Validação de que os registros carregados pela ingestão são instâncias de `RespostaCreate`.
- Execução dos testes automatizados e das verificações de qualidade com Ruff.

### 8. Implementação do pipeline de processamento
- Integração do serviço de ingestão com o serviço de detecção de menções.
- Definição do fluxo responsável por processar uma resposta individual.
- Validação da resposta utilizando os schemas Pydantic.
- Detecção das marcas monitoradas presentes no texto da resposta.
- Criação das entidades `Mencao` a partir das marcas identificadas.
- Integração com o `RespostaRepository` para persistência dos dados processados.
- Garantia de que respostas sem menções também possam ser processadas.
- Separação das responsabilidades entre ingestão, detecção de menções e persistência.
- Criação de testes para validar o fluxo completo de processamento.
- Validação do pipeline utilizando os dados presentes nos arquivos de fixtures.

### 9. Implementação da análise de Share of Voice
- Definição da regra de cálculo do Share of Voice.
- Consideração da quantidade de respostas que mencionam uma determinada marca, e não da quantidade total de ocorrências da marca.
- Implementação do cálculo do percentual geral de menções.
- Implementação do cálculo do Share of Voice individual por plataforma.
- Criação dos schemas `PlatformShare` e `ShareOfVoiceResponse` utilizando Pydantic 2.
- Implementação do serviço responsável pelo cálculo do Share of Voice.
- Criação de testes unitários para validar os principais cenários:
  - conjunto sem respostas;
  - nenhuma resposta mencionando a marca;
  - 50% das respostas mencionando a marca;
  - 100% das respostas mencionando a marca;
  - cálculo separado por plataforma;
  - múltiplas ocorrências da mesma marca dentro de uma resposta.
- Utilização de um repository mockado nos testes para manter o foco na regra de negócio, sem depender diretamente do banco de dados.

### 10. Implementação e testes do serviço de Analytics
- Implementação da função `calcular_share_of_voice()`.
- Cálculo do percentual de respostas que mencionam determinada marca.
- Cálculo do Share of Voice geral.
- Cálculo do Share of Voice separado por plataforma.
- Tratamento do cenário em que não existem respostas.
- Implementação da função `calcular_score_citacao()`.
- Definição do critério utilizado para determinar uma citação forte.
- O score considera:
  - quantidade de marcas distintas mencionadas;
  - quantidade total de ocorrências das marcas.
- Implementação da função `obter_top_citacoes()`.
- Filtragem das respostas que possuem pelo menos uma menção.
- Ordenação das respostas de acordo com o score de citação.
- Implementação do limite de resultados utilizando o parâmetro `n`.
- Conversão das respostas para o schema `TopCitacaoResponse`.
- Criação dos testes para o cálculo do Share of Voice.
- Teste do percentual geral de menções.
- Teste do percentual de menções por plataforma.
- Teste de cenários sem respostas e sem menções.
- Testes para o cálculo do score de citação.
- Validação do impacto da quantidade de marcas distintas no score.
- Validação do impacto da quantidade de ocorrências no score.
- Testes da ordenação das Top Citações.
- Teste do limite de resultados retornados.
- Validação de que respostas sem menções são ignoradas.
- Validação dos dados retornados pelo serviço de Top Citações.

### 11. Implementação e testes da API
- Criação da camada de API utilizando FastAPI.
- Criação dos routers para separação das responsabilidades.
- Implementação da rota `GET /share-of-voice`.
- Implementação da rota `GET /top-citacoes`.
- Implementação da rota `POST /respostas`.
- Integração das rotas com os serviços da aplicação.
- Integração dos serviços com o Repository.
- Utilização dos schemas Pydantic para validação das entradas e saídas.
- Validação dos parâmetros das requisições.
- Definição dos códigos de resposta HTTP.
- Integração do fluxo de criação de respostas com a ingestão e detecção de menções.
- Criação dos testes das rotas da API utilizando `TestClient`.
- Teste da rota `/share-of-voice`.
- Teste da rota `/top-citacoes`.
- Teste da rota `/respostas`.
- Teste de parâmetros inválidos.
- Teste de payloads inválidos.
- Teste de criação de respostas válidas.
- Teste de respostas HTTP esperadas para diferentes cenários.

### 12. Documentação e organização do projeto
- Documentação do arquivo principal da aplicação (`main.py`).
- Documentação das rotas da API.
- Documentação dos schemas Pydantic utilizados pela aplicação.
- Documentação dos serviços responsáveis pelas regras de negócio.
- Documentação do serviço de detecção de menções.
- Documentação do serviço de analytics.
- Documentação do Repository responsável pelo acesso aos dados de respostas.
- Documentação dos métodos de criação, consulta e listagem de respostas.
- Documentação dos métodos utilizados para consulta de respostas por marca.
- Inclusão de docstrings nas principais classes e funções.
- Padronização da documentação interna do código.
- Organização da documentação de acordo com a responsabilidade de cada camada da aplicação.
- Revisão da estrutura do projeto após a implementação da API.
- Verificação da qualidade e padronização do código com Ruff.

### 13. Documentação e organização do projeto

- Organização da documentação do projeto em uma estrutura própria.
- Criação da pasta `docs/` para centralizar a documentação.
- Criação da pasta `docs/documentacoes/` para documentação técnica dos componentes.
- Criação da documentação da API e de seus endpoints.
- Organização e documentação da estrutura de diretórios do projeto.
- Padronização da documentação utilizando arquivos Markdown.
- Inclusão de descrições sobre responsabilidades, entradas, saídas e funcionamento dos componentes.
- Preparação da documentação para facilitar a manutenção e compreensão do projeto.

### 14. Analytics, integração da API e testes automatizados

- Implementação do cálculo de Share of Voice (SOV) de uma marca.
- Implementação do cálculo de Share of Voice por plataforma.
- Implementação do tratamento case insensitive para consultas de marcas.
- Implementação do cálculo de score de citação das respostas.
- Implementação do ranking de Top Citações.
- Suporte a múltiplas marcas e múltiplas ocorrências em uma mesma resposta.
- Tratamento de respostas sem menções e listas vazias.
- Implementação do parâmetro `n` para limitar os resultados do ranking de citações.
- Criação do endpoint `GET /share-of-voice`.
- Criação do endpoint `GET /top-citacoes`.
- Implementação da busca de respostas por marca no `RespostaRepository`.
- Utilização de `distinct()` para evitar respostas duplicadas nas consultas por marca.
- Ajuste dos models `Resposta` e `Mencao` e de seus relacionamentos.
- Ajuste dos schemas Pydantic para respostas, menções e analytics.
- Diferenciação entre o ID interno do banco (`id`) e o identificador externo (`resposta_id`).
- Ajuste da rota de criação de respostas para validação individual dos dados recebidos.
- Implementação da detecção automática de menções de marcas nas respostas.
- Normalização das plataformas antes da persistência.
- Verificação de duplicidade antes da criação das respostas.
- Ampliação dos testes automatizados dos services, repositories, models e routes.
- Criação de testes para Share of Voice, Top Citações e score de citações.
- Criação de testes para consultas de marcas com diferentes capitalizações.
- Criação de banco de dados isolado para execução dos testes.
- Criação de fixtures para os testes automatizados.
- Criação de arquivo `.http` para testes manuais dos endpoints da API.
- Atualização das dependências de desenvolvimento no `pyproject.toml`.
- Atualização do `uv.lock`.

### 15. Dockerização
- Criação do `Dockerfile` para definir o ambiente de execução da aplicação.
- Criação do `.dockerignore` para evitar o envio de arquivos desnecessários para o contexto de build.
- Configuração da imagem Python 3.11.
- Configuração da execução da API utilizando Uvicorn dentro do container.
- Criação do `docker-compose.yml` para facilitar a inicialização da aplicação.
- Configuração do container da API com exposição da porta `8000`.
- Configuração do acesso ao banco SQLite através do diretório `data/`.
- Configuração para que a execução via `uv run` e via Docker Compose utilize os mesmos dados persistidos.
- Configuração do volume `./data:/app/data` para compartilhar o banco entre o ambiente local e o container.
- Teste da construção da imagem Docker.
- Teste da execução da API dentro do container.
- Teste da comunicação entre a aplicação e o banco de dados.
- Validação da persistência dos dados entre execuções locais e em container.

### 16. Implementação de logs nos serviços

- Adição de logging nos serviços responsáveis pelo processamento da aplicação.
- Configuração de logs no serviço de analytics.
- Registro do início e término dos cálculos de Share of Voice.
- Registro da quantidade de respostas analisadas e respostas com menções.
- Registro dos resultados de Share of Voice por plataforma.
- Registro do processamento do ranking de Top Citações.
- Adição de logs no serviço de detecção de menções.
- Registro das marcas detectadas e suas respectivas quantidades de ocorrências.
- Adição de logs no serviço de normalização de plataformas.
- Registro das plataformas após a normalização.
- Utilização de diferentes níveis de log (`INFO` e `DEBUG`) de acordo com a relevância da informação.
- Evitada a exposição do conteúdo completo das respostas nos arquivos de log.
- Padronização dos logs para facilitar o acompanhamento e diagnóstico da aplicação.

### 17. Finalizaçao de detalhes do projeto
- Atualização da documentação da estrutura do projeto conforme a organização atual dos diretórios.
- Revisão da documentação dos endpoints da API.
- Atualização da documentação dos schemas Pydantic.
- Inclusão dos schemas PlatformShare, ShareOfVoiceResponse e TopCitacaoResponse.
- Atualização das descrições dos campos, tipos e regras de validação dos schemas.
- Documentação da normalização do campo data_hora e dos formatos aceitos.
- Atualização da documentação dos fluxos de entrada e saída de dados da API.
- Revisão dos exemplos de requisições e respostas dos endpoints.
- Remoção de informações desatualizadas e redução de repetições entre as documentações.
- Padronização da linguagem e da estrutura dos arquivos Markdown.
- Atualização da documentação para refletir as funcionalidades atuais de analytics, ingestão, menções e respostas.