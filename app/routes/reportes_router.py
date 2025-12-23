"""
Controlador de Reportes
"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import date

from app.config.database import get_db
from app.config.security import require_role
from app.services.reporte_service import reporte_service
from app.schemas.common import ResponseData

router = APIRouter(prefix="/reportes", tags=["Reportes"])


@router.get("/ocupacion", response_model=ResponseData[dict])
def reporte_ocupacion(
    fecha_desde: date = Query(...),
    fecha_hasta: date = Query(...),
    db: Session = Depends(get_db),
    current_user = Depends(require_role(["Administrador", "Gerencia"]))
):
    """
    Reporte de ocupación hotelera
    """
    reporte = reporte_service.reporte_ocupacion(db, fecha_desde, fecha_hasta)
    return ResponseData(
        success=True,
        message="Reporte de ocupación generado",
        data=reporte
    )


@router.get("/revpar", response_model=ResponseData[dict])
def reporte_revpar(
    fecha_desde: date = Query(...),
    fecha_hasta: date = Query(...),
    db: Session = Depends(get_db),
    current_user = Depends(require_role(["Administrador", "Gerencia"]))
):
    """
    Reporte RevPAR (Revenue Per Available Room)
    """
    reporte = reporte_service.reporte_revpar(db, fecha_desde, fecha_hasta)
    return ResponseData(
        success=True,
        message="Reporte RevPAR generado",
        data=reporte
    )


@router.get("/ingresos", response_model=ResponseData[dict])
def reporte_ingresos(
    fecha_desde: date = Query(...),
    fecha_hasta: date = Query(...),
    db: Session = Depends(get_db),
    current_user = Depends(require_role(["Administrador", "Gerencia", "Contador"]))
):
    """
    Reporte de ingresos
    """
    reporte = reporte_service.reporte_ingresos(db, fecha_desde, fecha_hasta)
    return ResponseData(
        success=True,
        message="Reporte de ingresos generado",
        data=reporte
    )


@router.get("/libro-diario", response_model=ResponseData[dict])
def libro_diario(
    fecha_desde: date = Query(...),
    fecha_hasta: date = Query(...),
    db: Session = Depends(get_db),
    current_user = Depends(require_role(["Administrador", "Contador", "Gerencia"]))
):
    """
    Libro diario contable
    """
    reporte = reporte_service.libro_diario(db, fecha_desde, fecha_hasta)
    return ResponseData(
        success=True,
        message="Libro diario generado",
        data=reporte
    )


@router.get("/habitaciones", response_model=ResponseData[dict])
def reporte_habitaciones(
    db: Session = Depends(get_db),
    current_user = Depends(require_role(["Administrador", "Gerencia"]))
):
    """
    Reporte de estado de habitaciones
    """
    reporte = reporte_service.reporte_habitaciones(db)
    return ResponseData(
        success=True,
        message="Reporte de habitaciones generado",
        data=reporte
    )
