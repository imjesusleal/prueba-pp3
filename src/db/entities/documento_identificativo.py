from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class DocumentoIdentificativo(SQLModel, table=True):
    __tablename__ = "documento_identificativo"

    id_documento: int | None = Field(default=None, primary_key=True)
    tipo_documento: str = Field(max_length=10, unique=True)
    descripcion_documento: str | None = Field()
    created_at: datetime | None = Field(default=None)
    modified_at: datetime | None = Field(default=None)