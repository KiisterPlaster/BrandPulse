from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


class RespostaCreate(BaseModel):
    id: str = Field(min_length=1)
    pergunta: str = Field(min_length=1)
    plataforma: str = Field(min_length=1)
    modelo: str | None = None
    resposta_texto: str = Field(min_length=1)
    data_hora: datetime
    sentimento: str | None = None

    @field_validator("data_hora", mode="before")
    @classmethod
    def normalizar_data_hora(cls, valor):
        if isinstance(valor, datetime):
            return valor

        if not isinstance(valor, str):
            return valor

        valor = valor.strip()

        formatos = [
            "%Y-%m-%dT%H:%M:%S",
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%d",
            "%d/%m/%Y",
            "%Y/%m/%d",
        ]

        for formato in formatos:
            try:
                return datetime.strptime(valor, formato)
            except ValueError:
                continue

        return valor


class RespostasCreate(BaseModel):
    respostas: list[RespostaCreate]


class MencaoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    resposta_id: int
    marca: str
    ocorrencias: int


class RespostaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    resposta_id: str
    pergunta: str
    plataforma: str
    modelo: str | None
    resposta_texto: str
    data_hora: datetime
    sentimento: str | None
    mencoes: list[MencaoResponse]
