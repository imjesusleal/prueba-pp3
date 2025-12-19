from datetime import datetime
from sqlalchemy import select
from db.entities.estado_turnos_opciones import EstadoTurnosOpciones
from db.db import db

ESTADOS_DEFAULT = [
    {"valor": "PE", "descripcion": "Pendiente", "created_at": datetime.now(), "modified_at":datetime.now()},
    {"valor": "CO", "descripcion": "Confirmado","created_at": datetime.now(), "modified_at":datetime.now()},
    {"valor": "CA", "descripcion": "Cancelado", "created_at": datetime.now(), "modified_at":datetime.now()},
]

async def seed_estados_turnos() -> None:
    async with db.session() as session:
        result = await session.execute(
            select(EstadoTurnosOpciones.valor)
        )

        existentes = set(result.scalars().all())

        nuevos = [
            EstadoTurnosOpciones(
                valor=estado["valor"],
                descripcion=estado["descripcion"],
                created_at= estado["created_at"],
                modified_at= estado["modified_at"]
            )
            for estado in ESTADOS_DEFAULT
            if estado["valor"] not in existentes
        ]

        if nuevos:
            session.add_all(nuevos)
            await session.commit()
