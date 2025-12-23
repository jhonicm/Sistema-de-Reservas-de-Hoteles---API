"""
Servicio de Habitaciones
"""

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List, Optional
from datetime import date

from app.repositories.habitacion_repository import habitacion_repository
from app.schemas.habitacion_schema import (
    HabitacionCreate,
    HabitacionUpdate,
    HabitacionResponse
)


class HabitacionService:
    """
    Servicio de gestión de habitaciones
    """
    
    def create(self, db: Session, habitacion_data: HabitacionCreate) -> HabitacionResponse:
        """
        Crear nueva habitación
        """
        # Verificar número único
        if habitacion_repository.get_by_numero(db, habitacion_data.numero):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ya existe una habitación con ese número"
            )
        
        # Crear habitación
        habitacion = habitacion_repository.create(db, habitacion_data.model_dump())
        return HabitacionResponse.model_validate(habitacion)
    
    def get_all(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100
    ) -> List[HabitacionResponse]:
        """
        Obtener todas las habitaciones
        """
        habitaciones = habitacion_repository.get_all(db, skip, limit)
        return [HabitacionResponse.model_validate(h) for h in habitaciones]
    
    def get_by_id(self, db: Session, habitacion_id: int) -> HabitacionResponse:
        """
        Obtener habitación por ID
        """
        habitacion = habitacion_repository.get_by_id(db, habitacion_id)
        if not habitacion:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Habitación no encontrada"
            )
        return HabitacionResponse.model_validate(habitacion)
    
    def get_disponibles(
        self,
        db: Session,
        fecha_entrada: Optional[date] = None,
        fecha_salida: Optional[date] = None,
        tipo: Optional[str] = None
    ) -> List[HabitacionResponse]:
        """
        Obtener habitaciones disponibles
        """
        if fecha_entrada and fecha_salida:
            # Validar fechas
            if fecha_entrada >= fecha_salida:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="La fecha de entrada debe ser anterior a la fecha de salida"
                )
            
            habitaciones = habitacion_repository.get_disponibles_por_fechas(
                db,
                fecha_entrada,
                fecha_salida,
                tipo
            )
        else:
            # Asegúrate de que la llamada sea así:
            habitaciones = habitacion_repository.get_disponibles(db, tipo)
        
        return [HabitacionResponse.model_validate(h) for h in habitaciones]
    
    def update(
        self,
        db: Session,
        habitacion_id: int,
        habitacion_data: HabitacionUpdate
    ) -> HabitacionResponse:
        """
        Actualizar habitación
        """
        # Verificar que existe
        habitacion = habitacion_repository.get_by_id(db, habitacion_id)
        if not habitacion:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Habitación no encontrada"
            )
        
        # Actualizar
        update_data = habitacion_data.model_dump(exclude_unset=True)
        updated_habitacion = habitacion_repository.update(db, habitacion_id, update_data)
        return HabitacionResponse.model_validate(updated_habitacion)
    
    def delete(self, db: Session, habitacion_id: int) -> bool:
        """
        Eliminar habitación
        """
        habitacion = habitacion_repository.get_by_id(db, habitacion_id)
        if not habitacion:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Habitación no encontrada"
            )
        
        # Verificar que no tenga reservas activas
        if habitacion.reservas:
            reservas_activas = [r for r in habitacion.reservas if r.estado != "Cancelada"]
            if reservas_activas:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="No se puede eliminar una habitación con reservas activas"
                )
        
        # Eliminar
        habitacion_repository.delete(db, habitacion_id)
        return True


# Instancia singleton
habitacion_service = HabitacionService()
