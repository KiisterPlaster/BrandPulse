import logging
import re

logger = logging.getLogger(__name__)

PLATAFORMAS = {
    "chatgpt": "ChatGPT",
    "gemini": "Gemini",
    "perplexity": "Perplexity",
    "claude": "Claude",
    "copilot": "Copilot",
    "deepseek": "DeepSeek",
}


def normalizar_plataforma(plataforma: str) -> str:
    """
    Normaliza o nome da plataforma.

    Remove diferenças de maiúsculas/minúsculas,
    espaços, hífens e outros caracteres não alfanuméricos.
    """
    logger.debug(
        "Iniciando normalização de plataforma",
    )

    chave = re.sub(r"[\W_]+", "", plataforma.lower())

    plataforma_normalizada = PLATAFORMAS.get(chave, chave)

    logger.info(
        "Plataforma normalizada para '%s'",
        plataforma_normalizada,
    )

    return plataforma_normalizada
