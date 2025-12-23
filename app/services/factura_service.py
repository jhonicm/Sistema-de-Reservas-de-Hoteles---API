"""
Servicio de Facturación
"""

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List
from decimal import Decimal

from app.repositories.factura_repository import factura_repository
from app.repositories.reserva_repository import reserva_repository
from app.schemas.factura_schema import FacturaCreate, FacturaResponse


class FacturaService:
    """
    Servicio de gestión de facturas
    """
    
    def create(self, db: Session, factura_data: FacturaCreate) -> FacturaResponse:
        """
        Crear nueva factura manualmente
        """
        # Validar que la reserva existe
        reserva = reserva_repository.get_by_id(db, factura_data.reserva_id)
        if not reserva:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Reserva no encontrada"
            )
        
        # Verificar que no exista ya una factura para esta reserva
        factura_existente = factura_repository.get_by_reserva(db, factura_data.reserva_id)
        if factura_existente:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ya existe una factura para esta reserva"
            )
        
        # Generar número de factura consecutivo
        ultimo_numero = factura_repository.get_ultimo_numero(db)
        if ultimo_numero:
            numero_int = int(ultimo_numero.split("-")[1]) + 1
            nuevo_numero = f"FAC-{numero_int:06d}"
        else:
            nuevo_numero = "FAC-000001"
        
        # Calcular totales
        subtotal = reserva.precio_total
        subtotal = Decimal(str(subtotal))  # Asegura que subtotal sea Decimal
        impuestos = subtotal * Decimal("0.15")  # 15% IVA
        descuentos = factura_data.descuentos if factura_data.descuentos else Decimal("0.00")
        total = subtotal + impuestos - descuentos
        
        # Crear factura
        factura_dict = {
            "numero_factura": nuevo_numero,
            "reserva_id": factura_data.reserva_id,
            "subtotal": subtotal,
            "impuestos": impuestos,
            "descuentos": descuentos,
            "total": total
        }
        
        factura = factura_repository.create(db, factura_dict)
        return FacturaResponse.model_validate(factura)
    
    def get_all(self, db: Session, skip: int = 0, limit: int = 100) -> List[FacturaResponse]:
        """
        Obtener todas las facturas
        """
        facturas = factura_repository.get_all(db, skip, limit)
        return [FacturaResponse.model_validate(f) for f in facturas]
    
    def get_by_id(self, db: Session, factura_id: int) -> FacturaResponse:
        """
        Obtener factura por ID
        """
        factura = factura_repository.get_by_id(db, factura_id)
        if not factura:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Factura no encontrada"
            )
        return FacturaResponse.model_validate(factura)
    
    def get_by_numero(self, db: Session, numero_factura: str) -> FacturaResponse:
        """
        Obtener factura por número
        """
        factura = factura_repository.get_by_numero(db, numero_factura)
        if not factura:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Factura no encontrada"
            )
        return FacturaResponse.model_validate(factura)


# Instancia singleton
factura_service = FacturaService()
