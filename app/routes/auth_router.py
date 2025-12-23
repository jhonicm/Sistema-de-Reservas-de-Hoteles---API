"""
Controlador de Autenticación
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.config.security import get_current_user
from app.services.auth_service import auth_service
from app.schemas.auth_schema import LoginRequest, TokenResponse, ChangePasswordRequest
from app.schemas.common import ResponseData, ErrorResponse

router = APIRouter(prefix="/auth", tags=["Autenticación"])


@router.post("/login")
def login(
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):
    """
    Iniciar sesión
    """
    token_response = auth_service.login(db, login_data)
    return ResponseData(
        success=True,
        message="Inicio de sesión exitoso",
        data=token_response
    )


@router.post("/change-password", response_model=ResponseData[dict])
def change_password(
    password_data: ChangePasswordRequest,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Cambiar contraseña
    """
    auth_service.change_password(
        db,
        current_user.id,
        password_data.old_password,
        password_data.new_password
    )
    
    return ResponseData(
        success=True,
        message="Contraseña actualizada correctamente",
        data={"updated": True}
    )


@router.get("/me")
def get_current_user_info(
    current_user = Depends(get_current_user)
):
    """
    Obtener información del usuario actual
    """
    user_data = {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "nombre": current_user.nombre,
        "apellido": current_user.apellido,
        "rol": current_user.rol,
        "activo": current_user.activo
    }
    
    return ResponseData(
        success=True,
        message="Usuario obtenido correctamente",
        data=user_data
    )
