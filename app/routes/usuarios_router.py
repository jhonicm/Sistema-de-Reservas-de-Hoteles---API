"""
Controlador de Usuarios
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.config.database import get_db
from app.config.security import get_current_user, require_role
from app.services.usuario_service import usuario_service
from app.schemas.usuario_schema import UsuarioCreate, UsuarioUpdate, UsuarioResponse
from app.schemas.common import ResponseData, ResponseList

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


@router.post(
    "/usuarios",
)
def create_usuario(
    usuario: UsuarioCreate,
    db: Session = Depends(get_db),
    current_user = Depends(require_role(["Administrador"]))
):
    """
    Crear un nuevo usuario (solo Administrador).

    - **username**: Nombre de usuario (string, requerido)
    - **password**: Contraseña (string, requerido)
    - **rol**: Rol del usuario (string, requerido)
    - **activo**: Estado del usuario (booleano, opcional)

    Retorna el usuario creado.
    """
    usuario = usuario_service.create(db, usuario)
    return ResponseData(
        success=True,
        message="Usuario creado correctamente",
        data=usuario
    )


@router.get(
    "/usuarios",
)
def get_usuarios(
    db: Session = Depends(get_db),
    current_user = Depends(require_role(["Administrador"]))
):
    """
    Obtener todos los usuarios
    """
    usuarios = usuario_service.get_all(db)
    return ResponseList(
        success=True,
        message="Usuarios obtenidos correctamente",
        data=usuarios,
        total=len(usuarios)
    )


@router.get(
    "/usuarios/{usuario_id}",
)
def get_usuario(
    usuario_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_role(["Administrador"]))
):
    """
    Obtener usuario por ID
    """
    usuario = usuario_service.get_by_id(db, usuario_id)
    return ResponseData(
        success=True,
        message="Usuario obtenido correctamente",
        data=usuario
    )


@router.put(
    "/usuarios/{usuario_id}",
)
def update_usuario(
    usuario_id: int,
    usuario: UsuarioUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(require_role(["Administrador"]))
):
    """
    Actualizar usuario (solo Administrador)
    """
    usuario = usuario_service.update(db, usuario_id, usuario)
    return ResponseData(
        success=True,
        message="Usuario actualizado correctamente",
        data=usuario
    )


@router.delete(
    "/usuarios/{usuario_id}",
)
def delete_usuario(
    usuario_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_role(["Administrador"]))
):
    """
    Eliminar usuario (soft delete - solo Administrador)
    """
    usuario_service.delete(db, usuario_id)
    return ResponseData(
        success=True,
        message="Usuario eliminado correctamente",
        data={"deleted": True}
    )
