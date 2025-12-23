"""
Servicio de Usuarios
"""

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List, Optional

from app.config.security import get_password_hash, verify_password
from app.repositories.usuario_repository import usuario_repository
from app.schemas.usuario_schema import UsuarioCreate, UsuarioUpdate, UsuarioResponse


class UsuarioService:
    """
    Servicio de gestión de usuarios
    """
    
    def create(self, db: Session, usuario_data: UsuarioCreate) -> UsuarioResponse:
        """
        Crear nuevo usuario
        """
        # Verificar username único
        if usuario_repository.get_by_username(db, usuario_data.username):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El nombre de usuario ya existe"
            )
        
        # Verificar email único
        if usuario_repository.get_by_email(db, usuario_data.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El email ya está registrado"
            )
        
        # Encriptar contraseña
        password_hash = get_password_hash(usuario_data.password)
        
        # Preparar datos
        usuario_dict = usuario_data.model_dump(exclude={"password"})
        usuario_dict["password_hash"] = password_hash
        
        # Crear usuario
        usuario = usuario_repository.create(db, usuario_dict)
        return UsuarioResponse.model_validate(usuario)
    
    def get_all(self, db: Session, skip: int = 0, limit: int = 100) -> List[UsuarioResponse]:
        """
        Obtener todos los usuarios
        """
        usuarios = usuario_repository.get_all(db, skip, limit)
        return [UsuarioResponse.model_validate(u) for u in usuarios]
    
    def get_by_id(self, db: Session, usuario_id: int) -> UsuarioResponse:
        """
        Obtener usuario por ID
        """
        usuario = usuario_repository.get_by_id(db, usuario_id)
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
            )
        return UsuarioResponse.model_validate(usuario)
    
    def update(
        self,
        db: Session,
        usuario_id: int,
        usuario_data: UsuarioUpdate
    ) -> UsuarioResponse:
        """
        Actualizar usuario
        """
        # Verificar que existe
        usuario = usuario_repository.get_by_id(db, usuario_id)
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
            )
        
        # Verificar email único si se está cambiando
        if usuario_data.email:
            existing = usuario_repository.get_by_email(db, usuario_data.email)
            if existing and existing.id != usuario_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El email ya está registrado"
                )
        
        # Actualizar
        update_data = usuario_data.model_dump(exclude_unset=True)
        updated_usuario = usuario_repository.update(db, usuario_id, update_data)
        return UsuarioResponse.model_validate(updated_usuario)
    
    def delete(self, db: Session, usuario_id: int) -> bool:
        """
        Eliminar usuario (soft delete - marcar como inactivo)
        """
        usuario = usuario_repository.get_by_id(db, usuario_id)
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
            )
        
        # Soft delete
        usuario_repository.update(db, usuario_id, {"activo": False})
        return True
    
    def autenticar_usuario(db: Session, username: str, password: str):
        usuario = usuario_repository.get_by_username(db, username)
        if usuario and verify_password(password, usuario.hashed_password):
            return usuario
        return None


# Instancia singleton
usuario_service = UsuarioService()
