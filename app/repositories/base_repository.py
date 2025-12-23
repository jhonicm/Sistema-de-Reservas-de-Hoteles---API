"""
Repositorio Base - Operaciones CRUD genéricas
Similar a CrudRepository de Spring
"""

from typing import Generic, TypeVar, Type, List, Optional
from sqlalchemy.orm import Session
from app.config.database import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    """
    Repositorio base con operaciones CRUD
    """
    
    def __init__(self, model: Type[ModelType]):
        self.model = model
    
    def create(self, db: Session, obj_in: dict) -> ModelType:
        """Crear un nuevo registro"""
        db_obj = self.model(**obj_in)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def get_by_id(self, db: Session, id: int) -> Optional[ModelType]:
        """Obtener por ID"""
        return db.query(self.model).filter(self.model.id == id).first()
    
    def get_all(self, db: Session, skip: int = 0, limit: int = 100) -> List[ModelType]:
        """Obtener todos los registros"""
        return db.query(self.model).offset(skip).limit(limit).all()
    
    def update(self, db: Session, id: int, obj_in: dict) -> Optional[ModelType]:
        """Actualizar un registro"""
        db_obj = self.get_by_id(db, id)
        if db_obj:
            for key, value in obj_in.items():
                setattr(db_obj, key, value)
            db.commit()
            db.refresh(db_obj)
        return db_obj
    
    def delete(self, db: Session, id: int) -> bool:
        """Eliminar un registro"""
        db_obj = self.get_by_id(db, id)
        if db_obj:
            db.delete(db_obj)
            db.commit()
            return True
        return False
    
    def count(self, db: Session) -> int:
        """Contar registros"""
        return db.query(self.model).count()
