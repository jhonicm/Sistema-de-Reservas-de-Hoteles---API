"""
Servicio de Reservas (Lógica de Negocio Principal)
"""

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List
from datetime import date, datetime
from decimal import Decimal

from app.repositories.reserva_repository import reserva_repository
from app.repositories.habitacion_repository import habitacion_repository
from app.repositories.cliente_repository import cliente_repository
from app.repositories.factura_repository import factura_repository
from app.schemas.reserva_schema import ReservaCreate, ReservaUpdate, ReservaResponse


class ReservaService:
    """
    Servicio de gestión de reservas (núcleo del negocio)
    """
    
    def create(self, db: Session, reserva_data: ReservaCreate) -> ReservaResponse:
        """
        Crear nueva reserva
        """
        # Validar que el cliente existe
        cliente = cliente_repository.get_by_id(db, reserva_data.cliente_id)
        if not cliente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cliente no encontrado"
            )
        
        # Validar que la habitación existe
        habitacion = habitacion_repository.get_by_id(db, reserva_data.habitacion_id)
        if not habitacion:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Habitación no encontrada"
            )
        
        # Verificar disponibilidad
        disponible = reserva_repository.verificar_disponibilidad(
            db,
            reserva_data.habitacion_id,
            reserva_data.fecha_entrada,
            reserva_data.fecha_salida
        )
        
        if not disponible:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La habitación no está disponible para las fechas seleccionadas"
            )
        
        # Calcular precio total
        num_noches = (reserva_data.fecha_salida - reserva_data.fecha_entrada).days
        precio_total = habitacion.precio_noche * num_noches
        
        # Crear reserva
        reserva_dict = reserva_data.model_dump()
        reserva_dict["precio_total"] = precio_total
        reserva_dict["estado"] = "Confirmada"  # Estado inicial
        
        reserva = reserva_repository.create(db, reserva_dict)
        
        # Actualizar estado de habitación
        habitacion_repository.update(db, habitacion.id, {"estado": "Reservada"})
        
        return ReservaResponse.model_validate(reserva)
    
    def get_all(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100
    ) -> List[ReservaResponse]:
        """
        Obtener todas las reservas
        """
        reservas = reserva_repository.get_all(db, skip, limit)
        return [ReservaResponse.model_validate(r) for r in reservas]
    
    def get_by_id(self, db: Session, reserva_id: int) -> ReservaResponse:
        """
        Obtener reserva por ID
        """
        reserva = reserva_repository.get_by_id(db, reserva_id)
        if not reserva:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Reserva no encontrada"
            )
        return ReservaResponse.model_validate(reserva)
    
    def get_by_cliente(self, db: Session, cliente_id: int) -> List[ReservaResponse]:
        """
        Obtener reservas de un cliente
        """
        reservas = reserva_repository.get_by_cliente(db, cliente_id)
        return [ReservaResponse.model_validate(r) for r in reservas]
    
    def check_in(self, db: Session, reserva_id: int) -> ReservaResponse:
        """
        Realizar check-in de una reserva
        """
        reserva = reserva_repository.get_by_id(db, reserva_id)
        if not reserva:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Reserva no encontrada"
            )
        
        # Validar estado
        if reserva.estado != "Confirmada":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"No se puede hacer check-in de una reserva en estado {reserva.estado}"
            )
        
        # Validar fecha
        hoy = date.today()
        if hoy < reserva.fecha_entrada:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No se puede hacer check-in antes de la fecha de entrada"
            )
        
        # Actualizar reserva
        updated_reserva = reserva_repository.update(
            db,
            reserva_id,
            {"estado": "En_Curso"}
        )
        
        # Actualizar habitación
        habitacion_repository.update(
            db,
            reserva.habitacion_id,
            {"estado": "Ocupada"}
        )
        
        return ReservaResponse.model_validate(updated_reserva)
    
    def check_out(self, db: Session, reserva_id: int) -> ReservaResponse:
        """
        Realizar check-out de una reserva (genera factura automáticamente)
        """
        reserva = reserva_repository.get_by_id(db, reserva_id)
        if not reserva:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Reserva no encontrada"
            )
        
        # Validar estado
        if reserva.estado != "En_Curso":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"No se puede hacer check-out de una reserva en estado {reserva.estado}"
            )
        
        # Actualizar reserva
        updated_reserva = reserva_repository.update(
            db,
            reserva_id,
            {"estado": "Completada"}
        )
        
        # Actualizar habitación
        habitacion_repository.update(
            db,
            reserva.habitacion_id,
            {"estado": "Disponible"}
        )
        
        # Generar factura automáticamente si no existe
        factura_existente = factura_repository.get_by_reserva(db, reserva_id)
        if not factura_existente:
            self._generar_factura(db, reserva)
        
        return ReservaResponse.model_validate(updated_reserva)
    
    def cancelar(self, db: Session, reserva_id: int, motivo: str = None) -> ReservaResponse:
        """
        Cancelar una reserva
        """
        reserva = reserva_repository.get_by_id(db, reserva_id)
        if not reserva:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Reserva no encontrada"
            )
        
        # Validar estado
        if reserva.estado in ["Completada", "Cancelada"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"No se puede cancelar una reserva en estado {reserva.estado}"
            )
        
        # Actualizar reserva
        updated_reserva = reserva_repository.update(
            db,
            reserva_id,
            {"estado": "Cancelada"}
        )
        
        # Liberar habitación si estaba reservada
        if reserva.estado == "Confirmada":
            habitacion_repository.update(
                db,
                reserva.habitacion_id,
                {"estado": "Disponible"}
            )
        
        return ReservaResponse.model_validate(updated_reserva)
    
    def _generar_factura(self, db: Session, reserva):
        """
        Generar factura automáticamente (uso interno)
        """
        # Obtener último número de factura
        ultimo_numero = factura_repository.get_ultimo_numero(db)
        nuevo_numero = f"FAC-{int(ultimo_numero.split('-')[1]) + 1:06d}" if ultimo_numero else "FAC-000001"
        
        # Calcular impuestos (15% IVA)
        subtotal = reserva.precio_total
        impuestos = subtotal * Decimal("0.15")
        total = subtotal + impuestos
        
        # Crear factura
        factura_data = {
            "numero_factura": nuevo_numero,
            "reserva_id": reserva.id,
            "subtotal": subtotal,
            "impuestos": impuestos,
            "descuentos": Decimal("0.00"),
            "total": total
        }
        
        factura_repository.create(db, factura_data)


# Instancia singleton
reserva_service = ReservaService()
