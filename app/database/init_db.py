import app.models  # noqa: F401
from app.database.connection import engine
from app.database.tables import Base


def create_tables() -> None:
    Base.metadata.create_all(bind=engine)
