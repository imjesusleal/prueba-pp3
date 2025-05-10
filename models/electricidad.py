from sqlmodel import Field, SQLModel


class Electricidad(SQLModel, table = True):
    id_electricidad: int = Field(primary_key=True)
    id_mes: int = Field()
    monto: float | None = Field(default = None)
    nro_factura: str | None = Field(default = None)