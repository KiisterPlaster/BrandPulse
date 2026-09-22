import re

MARCAS_MONITORADAS = ["Acme", "Zenith", "Nimbus"]


def detectar_mencoes(texto: str) -> dict[str, int]:
    """
    Identifica as marcas monitoradas presentes em um texto.

    A busca é case-insensitive e considera apenas ocorrências
    da marca como palavra completa.
    """
    mencoes = {}

    for marca in MARCAS_MONITORADAS:
        padrao = rf"\b{re.escape(marca)}\b"
        ocorrencias = len(re.findall(padrao, texto, flags=re.IGNORECASE))

        if ocorrencias > 0:
            mencoes[marca] = ocorrencias

    return mencoes


if __name__ == "__main__":
    pass
