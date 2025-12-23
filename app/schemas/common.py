"""
Schemas base y de respuestas comunes
"""

from pydantic import BaseModel
from typing import Generic, TypeVar, List, Optional

T = TypeVar('T')


class ResponseBase(BaseModel):
    """Respuesta base"""
    success: bool
    message: str


class ResponseData(ResponseBase, Generic[T]):
    """Respuesta con datos"""
    data: Optional[T] = None


class ResponseList(ResponseBase, Generic[T]):
    """Respuesta con lista de datos"""
    data: List[T]
    total: int


class ErrorResponse(BaseModel):
    """Respuesta de error"""
    codigo: int
    mensaje: str
    campo: Optional[str] = None
