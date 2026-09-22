import json
from pathlib import Path

from pydantic import ValidationError

from app.schemas.respostas import RespostaCreate


def carregar_respostas(caminho: str | Path) -> list[RespostaCreate]:
    """
    Carrega e valida respostas armazenadas em um arquivo JSON.

    Registros inválidos são ignorados para que um dado corrompido
    não impeça o processamento das demais respostas.
    """
    caminho = Path(caminho)

    with caminho.open("r", encoding="utf-8") as arquivo:
        dados = json.load(arquivo)

    if not isinstance(dados, list):
        raise ValueError("O arquivo JSON deve conter uma lista de respostas.")

    respostas = []

    for registro in dados:
        try:
            resposta = RespostaCreate.model_validate(registro)
        except ValidationError:
            continue

        respostas.append(resposta)

    return respostas


if __name__ == "__main__":
    pass
