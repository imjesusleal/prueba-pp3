from logging.config import fileConfig
import os

from sqlalchemy import create_engine, engine_from_config
from sqlalchemy import pool

from alembic import context
from dotenv import load_dotenv
from db.entities.users_roles import UsersRoles
from db.entities.refresh_token import RefreshToken
from db.entities.users import Users
from db.entities.pacientes import Pacientes
from db.entities.medicos import Medicos
from db.entities.especialidades import Especialidades
from db.entities.consultas import Consulta
from db.entities.documento_identificativo import DocumentoIdentificativo
from db.entities.reviews import Reviews
from db.entities.turnos import Turnos

from sqlmodel import SQLModel


dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
load_dotenv(dotenv_path)

HOST_URL = os.getenv('DATABASE_URL')
HOST_SYNC = HOST_URL.replace("mssql+aioodbc", "mssql+pyodbc")


# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config
config.set_main_option('sqlalchemy.url',HOST_SYNC)

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata

target_metadata = SQLModel.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata,
            compare_type=True
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
