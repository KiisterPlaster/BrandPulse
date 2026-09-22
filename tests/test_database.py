from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from app.database.tables import Base


def create_test_engine():
    return create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )


def test_database_connection():
    engine = create_test_engine()

    with Session(engine) as session:
        resultado = session.execute(text("SELECT 1")).scalar()

    assert resultado == 1


def test_create_tables():
    engine = create_test_engine()

    Base.metadata.create_all(bind=engine)

    inspector = inspect(engine)
    tabelas = inspector.get_table_names()

    assert "respostas" in tabelas
    assert "mencoes" in tabelas