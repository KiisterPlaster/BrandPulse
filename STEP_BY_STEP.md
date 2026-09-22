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