import re

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
    chave = re.sub(r"[\W_]+", "", plataforma.lower())

    return PLATAFORMAS.get(chave, chave)
