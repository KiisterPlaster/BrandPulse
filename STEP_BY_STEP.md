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

