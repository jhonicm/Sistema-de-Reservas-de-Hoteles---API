"""
Controlador de Habitaciones
"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date

from app.config.database import get_db
from app.config.security import require_role
from app.services.habitacion_service import habitacion_service
from app.schemas.habitacion_schema import HabitacionCreate, HabitacionUpdate, HabitacionResponse
from app.schemas.common import ResponseData, ResponseList

router = APIRouter(prefix="/habitaciones", tags=["Habitaciones"])


@router.post(
    "/habitaciones",
)
def create_habitacion(
    habitacion_data: HabitacionCreate,
    db: Session = Depends(get_db),
    current_user = Depends(require_role(["Administrador"]))
):
    """
    Crear nueva habitación (solo Administrador)

    - **habitacion_data**: Datos de la habitación a crear
    - **db**: Sesión de base de datos inyectada por FastAPI
    - **current_user**: Usuario actual, debe tener rol de Administrador

    Retorna:
        Objeto de la habitación creada
    """
    habitacion = habitacion_service.create(db, habitacion_data)
    return ResponseData(
        success=True,
        message="Habitación creada correctamente",
        data=habitacion
    )


@router.get(
    "/habitaciones",
)
def get_habitaciones(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(require_role(["Administrador", "Recepcionista", "Gerencia"]))
):
    """
    Obtener todas las habitaciones

    - **skip**: Número de habitaciones a omitir (paginación)
    - **limit**: Número máximo de habitaciones a retornar
    - **db**: Sesión de base de datos inyectada por FastAPI
    - **current_user**: Usuario actual, debe tener uno de los roles permitidos

    Retorna:
        Listado de todas las habitaciones registradas
    """
    habitaciones = habitacion_service.get_all(db, skip, limit)
    return ResponseList(
        success=True,
        message="Habitaciones obtenidas correctamente",
        data=habitaciones,
        total=len(habitaciones)
    )


@router.get(
    "/habitaciones/disponibles",
)
def get_habitaciones_disponibles(
    fecha_entrada: Optional[date] = Query(None),
    fecha_salida: Optional[date] = Query(None),
    tipo: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user = Depends(require_role(["Administrador", "Recepcionista"]))
):
    """
    Obtener habitaciones disponibles (con o sin fechas)

    - **fecha_entrada**: Fecha de entrada para filtrar habitaciones disponibles
    - **fecha_salida**: Fecha de salida para filtrar habitaciones disponibles
    - **tipo**: Tipo de habitación a filtrar (opcional)
    - **db**: Sesión de base de datos inyectada por FastAPI
    - **current_user**: Usuario actual, debe tener uno de los roles permitidos

    Retorna:
        Lista de habitaciones con estado 'Disponible'. Si se especifica 'tipo', filtra por tipo de habitación
    """
    habitaciones = habitacion_service.get_disponibles(
        db,
        fecha_entrada,
        fecha_salida,
        tipo
    )
    return ResponseList(
        success=True,
        message="Habitaciones disponibles obtenidas",
        data=habitaciones,
        total=len(habitaciones)
    )


@router.get(
    "/habitaciones/{habitacion_id}",
)
def get_habitacion(
    habitacion_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_role(["Administrador", "Recepcionista", "Gerencia"]))
):
    """
    Obtener habitación por ID

    - **habitacion_id**: ID de la habitación a obtener
    - **db**: Sesión de base de datos inyectada por FastAPI
    - **current_user**: Usuario actual, debe tener uno de los roles permitidos

    Retorna:
        Objeto de la habitación solicitada
    """
    habitacion = habitacion_service.get_by_id(db, habitacion_id)
    return ResponseData(
        success=True,
        message="Habitación obtenida correctamente",
        data=habitacion
    )


@router.put(
    "/habitaciones/{habitacion_id}",
)
def update_habitacion(
    habitacion_id: int,
    habitacion_data: HabitacionUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(require_role(["Administrador"]))
):
    """
    Actualizar habitación (solo Administrador)

    - **habitacion_id**: ID de la habitación a actualizar
    - **habitacion_data**: Nuevos datos de la habitación
    - **db**: Sesión de base de datos inyectada por FastAPI
    - **current_user**: Usuario actual, debe tener rol de Administrador

    Retorna:
        Objeto de la habitación actualizada
    """
    habitacion = habitacion_service.update(db, habitacion_id, habitacion_data)
    return ResponseData(
        success=True,
        message="Habitación actualizada correctamente",
        data=habitacion
    )


@router.delete(
    "/habitaciones/{habitacion_id}",
)
def delete_habitacion(
    habitacion_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_role(["Administrador"]))
):
    """
    Eliminar habitación (solo Administrador)

    - **habitacion_id**: ID de la habitación a eliminar
    - **db**: Sesión de base de datos inyectada por FastAPI
    - **current_user**: Usuario actual, debe tener rol de Administrador

    Retorna:
        Mensaje de éxito o error
    """
    habitacion_service.delete(db, habitacion_id)
    return ResponseData(
        success=True,
        message="Habitación eliminada correctamente",
        data={"deleted": True}
    )
