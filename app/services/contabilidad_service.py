"""
Servicio de Contabilidad
"""

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List, Optional
from datetime import date, datetime
from decimal import Decimal

from app.repositories.cuenta_contable_repository import cuenta_contable_repository
from app.repositories.transaccion_repository import transaccion_repository
from app.schemas.cuenta_contable_schema import (
    CuentaContableCreate,
    CuentaContableUpdate,
    CuentaContableResponse
)
from app.schemas.transaccion_schema import TransaccionCreate, TransaccionResponse


class ContabilidadService:
    """
    Servicio de gestión contable
    """
    
    # ========== Cuentas Contables ==========
    
    def create_cuenta(
        self,
        db: Session,
        cuenta_data: CuentaContableCreate
    ) -> CuentaContableResponse:
        """
        Crear nueva cuenta contable
        """
        # Verificar código único
        if cuenta_contable_repository.get_by_codigo(db, cuenta_data.codigo):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ya existe una cuenta con ese código"
            )
        
        # Validar cuenta padre si se especifica
        if cuenta_data.cuenta_padre_id:
            cuenta_padre = cuenta_contable_repository.get_by_id(db, cuenta_data.cuenta_padre_id)
            if not cuenta_padre:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Cuenta padre no encontrada"
                )
        
        # Crear cuenta
        cuenta = cuenta_contable_repository.create(db, cuenta_data.model_dump())
        return CuentaContableResponse.model_validate(cuenta)
    
    def get_cuentas(
        self,
        db: Session,
        tipo: Optional[str] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[CuentaContableResponse]:
        """
        Obtener cuentas contables
        """
        if tipo:
            cuentas = cuenta_contable_repository.get_by_tipo(db, tipo)
        else:
            cuentas = cuenta_contable_repository.get_all(db, skip, limit)
        
        return [CuentaContableResponse.model_validate(c) for c in cuentas]
    
    def get_cuenta_by_id(self, db: Session, cuenta_id: int) -> CuentaContableResponse:
        """
        Obtener cuenta por ID
        """
        cuenta = cuenta_contable_repository.get_by_id(db, cuenta_id)
        if not cuenta:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cuenta no encontrada"
            )
        return CuentaContableResponse.model_validate(cuenta)
    
    def update_cuenta(
        self,
        db: Session,
        cuenta_id: int,
        cuenta_data: CuentaContableUpdate
    ) -> CuentaContableResponse:
        """
        Actualizar cuenta contable
        """
        cuenta = cuenta_contable_repository.get_by_id(db, cuenta_id)
        if not cuenta:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cuenta no encontrada"
            )
        
        update_data = cuenta_data.model_dump(exclude_unset=True)
        updated_cuenta = cuenta_contable_repository.update(db, cuenta_id, update_data)
        return CuentaContableResponse.model_validate(updated_cuenta)
    
    # ========== Transacciones ==========
    
    def create_transaccion(
        self,
        db: Session,
        transaccion_data: TransaccionCreate
    ) -> TransaccionResponse:
        """
        Registrar nueva transacción contable
        """
        # Validar que la cuenta existe
        cuenta = cuenta_contable_repository.get_by_id(db, transaccion_data.cuenta_id)
        if not cuenta:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cuenta contable no encontrada"
            )
        
        # Validar tipo de transacción según tipo de cuenta
        if cuenta.tipo == "Activo":
            # Débito aumenta, Crédito disminuye
            pass
        elif cuenta.tipo == "Pasivo" or cuenta.tipo == "Patrimonio":
            # Crédito aumenta, Débito disminuye
            pass
        elif cuenta.tipo == "Ingreso":
            # Crédito aumenta ingresos
            pass
        elif cuenta.tipo == "Egreso":
            # Débito aumenta egresos
            pass
        
        # Crear transacción
        transaccion_dict = transaccion_data.model_dump()
        transaccion_dict["fecha_transaccion"] = datetime.now()
        
        transaccion = transaccion_repository.create(db, transaccion_dict)
        return TransaccionResponse.model_validate(transaccion)
    
    def get_transacciones(
        self,
        db: Session,
        cuenta_id: Optional[int] = None,
        fecha_desde: Optional[date] = None,
        fecha_hasta: Optional[date] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[TransaccionResponse]:
        """
        Obtener transacciones
        """
        if cuenta_id:
            transacciones = transaccion_repository.get_by_cuenta(db, cuenta_id)
        elif fecha_desde and fecha_hasta:
            transacciones = transaccion_repository.get_by_fecha_rango(
                db,
                fecha_desde,
                fecha_hasta
            )
        else:
            transacciones = transaccion_repository.get_all(db, skip, limit)
        
        return [TransaccionResponse.model_validate(t) for t in transacciones]
    
    def get_balance(
        self,
        db: Session,
        fecha_desde: Optional[date] = None,
        fecha_hasta: Optional[date] = None
    ) -> dict:
        """
        Obtener balance general
        """
        total_ingresos = transaccion_repository.get_total_ingresos(
            db,
            fecha_desde,
            fecha_hasta
        )
        
        total_egresos = transaccion_repository.get_total_egresos(
            db,
            fecha_desde,
            fecha_hasta
        )
        
        utilidad = total_ingresos - total_egresos
        
        return {
            "total_ingresos": total_ingresos,
            "total_egresos": total_egresos,
            "utilidad_neta": utilidad,
            "periodo": {
                "desde": fecha_desde.isoformat() if fecha_desde else None,
                "hasta": fecha_hasta.isoformat() if fecha_hasta else None
            }
        }
    
    def registrar_ingreso_reserva(
        self,
        db: Session,
        reserva_id: int,
        monto: Decimal,
        concepto: str
    ):
        """
        Registrar automáticamente ingreso por reserva
        """
        # Buscar cuenta de ingresos por hospedaje
        cuenta = cuenta_contable_repository.get_by_codigo(db, "4.1.01")  # Ingresos por hospedaje
        
        if not cuenta:
            # Si no existe, crearla
            cuenta_data = {
                "codigo": "4.1.01",
                "nombre": "Ingresos por Hospedaje",
                "tipo": "Ingreso",
                "cuenta_padre_id": None
            }
            cuenta = cuenta_contable_repository.create(db, cuenta_data)
        
        # Registrar transacción
        transaccion_data = {
            "cuenta_id": cuenta.id,
            "tipo": "Crédito",
            "concepto": f"{concepto} - Reserva #{reserva_id}",
            "monto": monto,
            "fecha_transaccion": datetime.now()
        }
        
        transaccion_repository.create(db, transaccion_data)


# Instancia singleton
contabilidad_service = ContabilidadService()
