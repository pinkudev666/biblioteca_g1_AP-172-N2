from sqlalchemy import Column, String, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from .base import Base

class Usuario(Base):
    __tablename__ = 'usuario'

    rut_usuario = Column(String(15), primary_key=True)  
    nombre_usuario = Column(String(100), nullable=False)
    correo_usuario = Column(String(100), nullable=False, unique=True)
    id_tipo_usuario = Column(Integer, ForeignKey('tipo_usuario.id_tipo_usuario'), nullable=False)
    usuario_activo = Column(Boolean, default=True)  

    # relaciones
    tipo = relationship('Tipo_usuario', back_populates='usuarios')
    prestamos = relationship('Prestamo', back_populates='usuario', cascade='all, delete-orphan')

    def __repr__(self) -> str:
        return f"<Usuario(rut={self.rut_usuario!r}, nombre={self.nombre_usuario!r})>"
