import logging
import re

logger = logging.getLogger(__name__)

MARCAS_MONITORADAS = ["Acme", "Zenith", "Nimbus"]


def criar_padrao_marca(marca: str) -> str:
    r"""
    Cria uma expressão regular que permite caracteres não alfanuméricos
    entre as letras da marca.

    Exemplo:
        ACME -> A[\W_]*C[\W_]*M[\W_]*E
    """
    logger.debug(
        "Criando padrão de busca para a marca '%s'",
        marca,
    )

    letras = list(marca)

    padrao = r"[\W_]*".join(re.escape(letra) for letra in letras if letra.isalnum())

    logger.debug(
        "Padrão criado para a marca '%s'",
        marca,
    )

    return padrao


def detectar_mencoes(texto: str) -> dict[str, int]:
    r"""
    Identifica as marcas monitoradas presentes em um texto.

    A busca é case-insensitive e permite separadores como:
        ACME
        A.C.M.E
        A-C-M-E
        A C M E
    """
    logger.debug(
        "Iniciando detecção de menções em texto com %d caracteres",
        len(texto),
    )

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

            logger.info(
                "Marca '%s' detectada: %d ocorrência(s)",
                marca,
                ocorrencias,
            )

    logger.debug(
        "Detecção de menções finalizada: %d marca(s) encontrada(s)",
        len(mencoes),
    )

    return mencoes


if __name__ == "__main__":
    pass
