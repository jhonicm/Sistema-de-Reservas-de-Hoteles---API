"""
Repositorio de Usuarios
"""

from typing import Optional
from sqlalchemy.orm import Session
from app.models.usuario import Usuario
from app.repositories.base_repository import BaseRepository


class UsuarioRepository(BaseRepository[Usuario]):
    """
    Repositorio para la entidad Usuario
    """
    
    def __init__(self):
        super().__init__(Usuario)
    
    def get_by_username(self, db: Session, username: str):
        """Buscar usuario por username"""
        return db.query(Usuario).filter(Usuario.username == username).first()

    def create(self, db: Session, usuario: Usuario):
        """Crear un nuevo usuario"""
        db.add(usuario)
        db.commit()
        db.refresh(usuario)
        return usuario
    
    def get_by_email(self, db: Session, email: str) -> Optional[Usuario]:
        """Buscar usuario por email"""
        return db.query(Usuario).filter(Usuario.email == email).first()
    
    def get_by_rol(self, db: Session, rol: str) -> list[Usuario]:
        """Obtener usuarios por rol"""
        return db.query(Usuario).filter(Usuario.rol == rol).all()
    
    def get_activos(self, db: Session) -> list[Usuario]:
        """Obtener usuarios activos"""
        return db.query(Usuario).filter(Usuario.activo == True).all()


# Instancia singleton
usuario_repository = UsuarioRepository()
