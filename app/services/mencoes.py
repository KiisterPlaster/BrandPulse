import re

MARCAS_MONITORADAS = ["Acme", "Zenith", "Nimbus"]


def criar_padrao_marca(marca: str) -> str:
    r"""
    Cria uma expressão regular que permite caracteres não alfanuméricos
    entre as letras da marca.

    Exemplo:
        ACME -> A[\W_]*C[\W_]*M[\W_]*E
    """
    letras = list(marca)

    return r"[\W_]*".join(re.escape(letra) for letra in letras if letra.isalnum())


def detectar_mencoes(texto: str) -> dict[str, int]:
    r"""
    Identifica as marcas monitoradas presentes em um texto.

    A busca é case-insensitive e permite separadores como:
        ACME
        A.C.M.E
        A-C-M-E
        A C M E
    """

    mencoes = {}

    for marca in MARCAS_MONITORADAS:
        padrao_marca = criar_padrao_marca(marca)

        padrao = rf"(?<!\w){padrao_marca}(?!\w)"

        ocorrencias = len(
            re.findall(
                padrao,
                texto,
                flags=re.IGNORECASE,
            )
        )

        if ocorrencias > 0:
            mencoes[marca] = ocorrencias

    return mencoes


if __name__ == "__main__":
    pass
