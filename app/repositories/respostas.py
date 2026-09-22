from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.mencao import Mencao
from app.models.resposta import Resposta


class RespostaRepository:
    """
    Repositório responsável pelo acesso aos dados de respostas.

    Centraliza as operações de criação, consulta e listagem de
    respostas e suas respectivas menções no banco de dados.
    """

    def __init__(self, session: Session):
        """
        Inicializa o repositório com uma sessão do SQLAlchemy.
        """
        self.session = session

    def criar(self, resposta: Resposta) -> Resposta:
        """
        Persiste uma resposta no banco de dados.

        Após a confirmação da transação, atualiza o objeto com os
        dados gerados pelo banco e retorna a resposta persistida.
        """
        self.session.add(resposta)
        self.session.commit()
        self.session.refresh(resposta)

        return resposta

    def buscar_por_id(self, resposta_id: str) -> Resposta | None:
        """
        Busca uma resposta pelo seu identificador.

        Retorna a resposta encontrada ou None caso não exista.
        """
        return self.session.get(Resposta, resposta_id)

    def listar(self) -> list[Resposta]:
        """
        Retorna todas as respostas cadastradas no banco de dados.
        """
        statement = select(Resposta)

        return list(self.session.scalars(statement).all())

    def existe(self, resposta_id: str) -> bool:
        """
        Verifica se uma resposta existe pelo seu identificador.

        Retorna True quando a resposta existe e False caso contrário.
        """
        return self.buscar_por_id(resposta_id) is not None

    def listar_por_marca(self, marca: str) -> list[Resposta]:
        """
        Retorna as respostas que possuem menção à marca informada.

        A consulta utiliza o relacionamento entre Resposta e Mencao
        e remove possíveis duplicidades com distinct().
        """
        statement = (
            select(Resposta)
            .join(Resposta.mencoes)
            .where(Mencao.marca == marca)
            .distinct()
        )

        return list(self.session.scalars(statement).all())


if __name__ == "__main__":
    pass
