"""
Schemas para autenticación
"""

from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):
    """Request para login"""
    username: str
    password: str


class TokenResponse(BaseModel):
    """Respuesta de token"""
    access_token: str
    token_type: str = "bearer"
    user: dict


class ChangePasswordRequest(BaseModel):
    """Request para cambiar contraseña"""
    old_password: str
    new_password: str
