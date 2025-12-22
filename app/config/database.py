"""
Configuración de la base de datos
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

# URL de la base de datos
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./hotel_reservas.db")

# Crear motor de base de datos
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

# Crear sesión
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base declarativa para los modelos
Base = declarative_base()


# Dependencia para obtener la sesión de BD
def get_db():
    """
    Generador de sesión de base de datos
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
