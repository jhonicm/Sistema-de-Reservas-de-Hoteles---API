"""
Servicio de Autenticación
"""

from datetime import timedelta
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.config.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES
)
from app.repositories.usuario_repository import usuario_repository
from app.schemas.auth_schema import LoginRequest, TokenResponse
from app.schemas.usuario_schema import UsuarioResponse


class AuthService:
    """
    Servicio de autenticación
    """
    
    def login(self, db: Session, login_data: LoginRequest) -> TokenResponse:
        """
        Autenticar usuario y generar token
        """
        # Buscar usuario
        user = usuario_repository.get_by_username(db, login_data.username)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuario o contraseña incorrectos"
            )
        
        # Verificar contraseña
        if not verify_password(login_data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuario o contraseña incorrectos"
            )
        
        # Verificar que esté activo
        if not user.activo:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Usuario inactivo"
            )
        
        # Crear token
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username, "rol": user.rol},
            expires_delta=access_token_expires
        )
        
        # Preparar respuesta
        user_data = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "nombre": user.nombre,
            "apellido": user.apellido,
            "rol": user.rol
        }
        
        return TokenResponse(
            access_token=access_token,
            token_type="bearer",
            user=user_data
        )
    
    def change_password(
        self,
        db: Session,
        user_id: int,
        old_password: str,
        new_password: str
    ) -> bool:
        """
        Cambiar contraseña de usuario
        """
        user = usuario_repository.get_by_id(db, user_id)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
            )
        
        # Verificar contraseña actual
        if not verify_password(old_password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Contraseña actual incorrecta"
            )
        
        # Actualizar contraseña
        new_hash = get_password_hash(new_password)
        usuario_repository.update(db, user_id, {"password_hash": new_hash})
        
        return True


# Instancia singleton
auth_service = AuthService()
