"""
Servicio de Reportes
"""

from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from typing import List, Optional, Dict, Any
from datetime import date, datetime, timedelta
from decimal import Decimal

from app.models.reserva import Reserva
from app.models.habitacion import Habitacion
from app.models.factura import Factura
from app.models.pago import Pago
from app.models.transaccion import Transaccion
from app.models.cuenta_contable import CuentaContable


class ReporteService:
    """
    Servicio de generación de reportes
    """
    
    def reporte_ocupacion(
        self,
        db: Session,
        fecha_desde: date,
        fecha_hasta: date
    ) -> Dict[str, Any]:
        """
        Reporte de ocupación hotelera
        """
        # Total de habitaciones
        total_habitaciones = db.query(func.count(Habitacion.id)).scalar()
        
        # Habitaciones ocupadas en el periodo
        reservas = db.query(Reserva).filter(
            and_(
                Reserva.fecha_entrada <= fecha_hasta,
                Reserva.fecha_salida >= fecha_desde,
                Reserva.estado.in_(["Confirmada", "En_Curso"])
            )
        ).all()
        
        # Calcular días de ocupación
        dias_periodo = (fecha_hasta - fecha_desde).days + 1
        total_habitaciones_dia = total_habitaciones * dias_periodo
        
        dias_ocupados = 0
        for reserva in reservas:
            inicio = max(reserva.fecha_entrada, fecha_desde)
            fin = min(reserva.fecha_salida, fecha_hasta)
            dias = (fin - inicio).days
            dias_ocupados += dias
        
        # Porcentaje de ocupación
        porcentaje_ocupacion = (dias_ocupados / total_habitaciones_dia * 100) if total_habitaciones_dia > 0 else 0
        
        return {
            "periodo": {
                "desde": fecha_desde.isoformat(),
                "hasta": fecha_hasta.isoformat()
            },
            "total_habitaciones": total_habitaciones,
            "dias_periodo": dias_periodo,
            "dias_ocupados": dias_ocupados,
            "porcentaje_ocupacion": round(porcentaje_ocupacion, 2),
            "total_reservas": len(reservas)
        }
    
    def reporte_revpar(
        self,
        db: Session,
        fecha_desde: date,
        fecha_hasta: date
    ) -> Dict[str, Any]:
        """
        Revenue Per Available Room (RevPAR)
        """
        # Total de habitaciones
        total_habitaciones = db.query(func.count(Habitacion.id)).scalar()
        
        # Ingresos por habitaciones en el periodo
        reservas = db.query(Reserva).filter(
            and_(
                Reserva.fecha_entrada >= fecha_desde,
                Reserva.fecha_salida <= fecha_hasta,
                Reserva.estado.in_(["Completada", "En_Curso"])
            )
        ).all()
        
        ingresos_totales = sum(r.precio_total for r in reservas)
        
        # Calcular días
        dias_periodo = (fecha_hasta - fecha_desde).days + 1
        
        # RevPAR = Ingresos totales / (Total habitaciones * días)
        habitaciones_disponibles = total_habitaciones * dias_periodo
        revpar = (ingresos_totales / habitaciones_disponibles) if habitaciones_disponibles > 0 else 0
        
        # ADR (Average Daily Rate) = Ingresos / Habitaciones vendidas
        habitaciones_vendidas = len(reservas)
        adr = (ingresos_totales / habitaciones_vendidas) if habitaciones_vendidas > 0 else 0
        
        return {
            "periodo": {
                "desde": fecha_desde.isoformat(),
                "hasta": fecha_hasta.isoformat()
            },
            "ingresos_totales": float(ingresos_totales),
            "total_habitaciones": total_habitaciones,
            "habitaciones_vendidas": habitaciones_vendidas,
            "dias_periodo": dias_periodo,
            "revpar": round(float(revpar), 2),
            "adr": round(float(adr), 2)
        }
    
    def reporte_ingresos(
        self,
        db: Session,
        fecha_desde: date,
        fecha_hasta: date
    ) -> Dict[str, Any]:
        """
        Reporte de ingresos
        """
        # Facturas del periodo
        facturas = db.query(Factura).join(Reserva).filter(
            and_(
                Reserva.fecha_entrada >= fecha_desde,
                Reserva.fecha_salida <= fecha_hasta
            )
        ).all()
        
        # Totales
        subtotal = sum(f.subtotal for f in facturas)
        impuestos = sum(f.impuestos for f in facturas)
        descuentos = sum(f.descuentos for f in facturas)
        total = sum(f.total for f in facturas)
        
        # Pagos recibidos
        pagos = db.query(Pago).join(Factura).join(Reserva).filter(
            and_(
                Reserva.fecha_entrada >= fecha_desde,
                Reserva.fecha_salida <= fecha_hasta
            )
        ).all()
        
        total_pagado = sum(p.monto for p in pagos)
        
        # Métodos de pago
        pagos_efectivo = sum(p.monto for p in pagos if p.metodo_pago == "Efectivo")
        pagos_tarjeta = sum(p.monto for p in pagos if p.metodo_pago == "Tarjeta")
        pagos_transferencia = sum(p.monto for p in pagos if p.metodo_pago == "Transferencia")
        
        return {
            "periodo": {
                "desde": fecha_desde.isoformat(),
                "hasta": fecha_hasta.isoformat()
            },
            "facturacion": {
                "subtotal": float(subtotal),
                "impuestos": float(impuestos),
                "descuentos": float(descuentos),
                "total": float(total)
            },
            "pagos": {
                "total_pagado": float(total_pagado),
                "saldo_pendiente": float(total - total_pagado),
                "por_metodo": {
                    "efectivo": float(pagos_efectivo),
                    "tarjeta": float(pagos_tarjeta),
                    "transferencia": float(pagos_transferencia)
                }
            },
            "total_facturas": len(facturas)
        }
    
    def libro_diario(
        self,
        db: Session,
        fecha_desde: date,
        fecha_hasta: date
    ) -> List[Dict[str, Any]]:
        """
        Libro diario contable
        """
        # Obtener transacciones del periodo
        transacciones = db.query(Transaccion).join(CuentaContable).filter(
            and_(
                func.date(Transaccion.fecha_transaccion) >= fecha_desde,
                func.date(Transaccion.fecha_transaccion) <= fecha_hasta
            )
        ).order_by(Transaccion.fecha_transaccion).all()
        
        # Formatear para libro diario
        libro = []
        for t in transacciones:
            libro.append({
                "fecha": t.fecha_transaccion.isoformat(),
                "cuenta_codigo": t.cuenta.codigo,
                "cuenta_nombre": t.cuenta.nombre,
                "concepto": t.concepto,
                "tipo": t.tipo,
                "debe": float(t.monto) if t.tipo == "Débito" else 0.00,
                "haber": float(t.monto) if t.tipo == "Crédito" else 0.00
            })
        
        # Totales
        total_debe = sum(item["debe"] for item in libro)
        total_haber = sum(item["haber"] for item in libro)
        
        return {
            "periodo": {
                "desde": fecha_desde.isoformat(),
                "hasta": fecha_hasta.isoformat()
            },
            "transacciones": libro,
            "totales": {
                "debe": round(total_debe, 2),
                "haber": round(total_haber, 2),
                "balance": round(total_debe - total_haber, 2)
            }
        }
    
    def reporte_habitaciones(
        self,
        db: Session
    ) -> Dict[str, Any]:
        """
        Reporte de estado de habitaciones
        """
        # Habitaciones por estado
        disponibles = db.query(func.count(Habitacion.id)).filter(
            Habitacion.estado == "Disponible"
        ).scalar()
        
        ocupadas = db.query(func.count(Habitacion.id)).filter(
            Habitacion.estado == "Ocupada"
        ).scalar()
        
        reservadas = db.query(func.count(Habitacion.id)).filter(
            Habitacion.estado == "Reservada"
        ).scalar()
        
        mantenimiento = db.query(func.count(Habitacion.id)).filter(
            Habitacion.estado == "Mantenimiento"
        ).scalar()
        
        # Habitaciones por tipo
        habitaciones_tipo = db.query(
            Habitacion.tipo,
            func.count(Habitacion.id)
        ).group_by(Habitacion.tipo).all()
        
        return {
            "por_estado": {
                "disponibles": disponibles,
                "ocupadas": ocupadas,
                "reservadas": reservadas,
                "mantenimiento": mantenimiento,
                "total": disponibles + ocupadas + reservadas + mantenimiento
            },
            "por_tipo": [
                {"tipo": tipo, "cantidad": cantidad}
                for tipo, cantidad in habitaciones_tipo
            ]
        }


# Instancia singleton
reporte_service = ReporteService()
