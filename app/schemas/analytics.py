from pydantic import BaseModel, Field


class PlatformShare(BaseModel):
    plataforma: str
    respostas_com_mencao: int = Field(ge=0)
    total_respostas: int = Field(ge=0)
    percentual: float = Field(ge=0, le=100)


class ShareOfVoiceResponse(BaseModel):
    marca: str
    respostas_com_mencao: int = Field(ge=0)
    total_respostas: int = Field(ge=0)
    percentual: float = Field(ge=0, le=100)
    por_plataforma: list[PlatformShare]


class TopCitacaoResponse(BaseModel):
    resposta_id: str
    plataforma: str
    modelo: str | None
    resposta_texto: str
    marcas: list[str]
    score: float = Field(ge=0)
