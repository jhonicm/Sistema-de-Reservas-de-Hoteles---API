"""
Rutas relacionadas con los usuarios
"""

from fastapi import APIRouter, Depends
from app.config.security import get_current_user, require_role
from app.models.usuario import Usuario
from app.config.database import get_db
from sqlalchemy.orm import Session

router = APIRouter()

@router.get("/usuarios/me")
def leer_usuario_actual(usuario: Usuario = Depends(get_current_user)):
    """Obtener información del usuario actual"""
    return usuario

@router.get("/usuarios/admin")
def solo_admin(usuario: Usuario = Depends(require_role(["admin"]))):
    """Ruta protegida, solo accesible para administradores"""
    return {"msg": "Solo admin"}