from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class RespostaCreate(BaseModel):
    id: str = Field(min_length=1)
    pergunta: str = Field(min_length=1)
    plataforma: str = Field(min_length=1)
    modelo: str | None = None
    resposta_texto: str = Field(min_length=1)
    data_hora: datetime
    sentimento: str | None = None


class RespostaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    pergunta: str
    plataforma: str
    modelo: str | None
    resposta_texto: str
    data_hora: datetime
    sentimento: str | None
    mencoes: list[str]
