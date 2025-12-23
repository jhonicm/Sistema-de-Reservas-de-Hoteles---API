"""
Repositorio de Cuentas Contables
"""

from typing import Optional
from sqlalchemy.orm import Session
from app.models.cuenta_contable import CuentaContable
from app.repositories.base_repository import BaseRepository


class CuentaContableRepository(BaseRepository[CuentaContable]):
    """
    Repositorio para la entidad CuentaContable
    """
    
    def __init__(self):
        super().__init__(CuentaContable)
    
    def get_by_codigo(self, db: Session, codigo: str) -> Optional[CuentaContable]:
        """Buscar cuenta por código"""
        return db.query(CuentaContable).filter(CuentaContable.codigo == codigo).first()
    
    def get_by_tipo(self, db: Session, tipo: str) -> list[CuentaContable]:
        """Obtener cuentas por tipo"""
        return db.query(CuentaContable).filter(CuentaContable.tipo == tipo).all()
    
    def get_subcuentas(self, db: Session, cuenta_padre_id: int) -> list[CuentaContable]:
        """Obtener subcuentas de una cuenta padre"""
        return db.query(CuentaContable).filter(
            CuentaContable.cuenta_padre_id == cuenta_padre_id
        ).all()
    
    def get_cuentas_principales(self, db: Session) -> list[CuentaContable]:
        """Obtener cuentas principales (sin padre)"""
        return db.query(CuentaContable).filter(
            CuentaContable.cuenta_padre_id == None
        ).all()


# Instancia singleton
cuenta_contable_repository = CuentaContableRepository()
