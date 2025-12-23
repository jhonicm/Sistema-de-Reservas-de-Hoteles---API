"""
Servicio de Pagos
"""

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List
from decimal import Decimal

from app.repositories.pago_repository import pago_repository
from app.repositories.factura_repository import factura_repository
from app.schemas.pago_schema import PagoCreate, PagoResponse


class PagoService:
    """
    Servicio de gestión de pagos
    """
    
    def create(self, db: Session, pago_data: PagoCreate) -> PagoResponse:
        """
        Registrar nuevo pago
        """
        # Validar que la factura existe
        factura = factura_repository.get_by_id(db, pago_data.factura_id)
        if not factura:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Factura no encontrada"
            )
        
        # Verificar que no se pague más del total
        total_pagado = pago_repository.get_total_pagado(db, pago_data.factura_id)
        total_pendiente = factura.total - total_pagado
        
        if pago_data.monto > total_pendiente:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"El monto excede el saldo pendiente de {total_pendiente}"
            )
        
        # Crear pago
        pago = pago_repository.create(db, pago_data.model_dump())
        return PagoResponse.model_validate(pago)
    
    def get_all(self, db: Session, skip: int = 0, limit: int = 100) -> List[PagoResponse]:
        """
        Obtener todos los pagos
        """
        pagos = pago_repository.get_all(db, skip, limit)
        return [PagoResponse.model_validate(p) for p in pagos]
    
    def get_by_id(self, db: Session, pago_id: int) -> PagoResponse:
        """
        Obtener pago por ID
        """
        pago = pago_repository.get_by_id(db, pago_id)
        if not pago:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Pago no encontrado"
            )
        return PagoResponse.model_validate(pago)
    
    def get_by_factura(self, db: Session, factura_id: int) -> List[PagoResponse]:
        """
        Obtener todos los pagos de una factura
        """
        pagos = pago_repository.get_by_factura(db, factura_id)
        return [PagoResponse.model_validate(p) for p in pagos]
    
    def get_saldo_pendiente(self, db: Session, factura_id: int) -> Decimal:
        """
        Obtener saldo pendiente de una factura
        """
        # Validar factura
        factura = factura_repository.get_by_id(db, factura_id)
        if not factura:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Factura no encontrada"
            )
        
        total_pagado = pago_repository.get_total_pagado(db, factura_id)
        return factura.total - total_pagado


# Instancia singleton
pago_service = PagoService()
