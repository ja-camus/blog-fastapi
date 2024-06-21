import os
from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
from dotenv import load_dotenv
from app.database import Base

# Load environment variables from .env
load_dotenv()

# Get environment and database URL
env = os.getenv("ENV", "development")
DATABASE_URL = (
    os.getenv("DATABASE_URL_TEST") if env == "testing" else os.getenv("DATABASE_URL")
)

if not DATABASE_URL:
    raise ValueError("DATABASE_URL not present in .env")

# Configure Alembic
config = context.config
fileConfig(config.config_file_name)
config.set_main_option("sqlalchemy.url", str(DATABASE_URL))

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
