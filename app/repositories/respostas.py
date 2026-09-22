from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.resposta import Resposta


class RespostaRepository:
    def __init__(self, session: Session):
        self.session = session

    def criar(self, resposta: Resposta) -> Resposta:
        self.session.add(resposta)
        self.session.commit()
        self.session.refresh(resposta)

        return resposta

    def buscar_por_id(self, resposta_id: str) -> Resposta | None:
        return self.session.get(Resposta, resposta_id)

    def listar(self) -> list[Resposta]:
        statement = select(Resposta)

        return list(self.session.scalars(statement).all())

    def existe(self, resposta_id: str) -> bool:
        return self.buscar_por_id(resposta_id) is not None


if __name__ == "__main__":
    pass
