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