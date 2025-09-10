from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker


SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://admin:admin@localhost:5432/ml_automatization"

# Creates an engine that manages connections to the database.
engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=False)

# Factory for creating sessions
SessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)

# Creates a base class for all ORM models.
Base = declarative_base()
