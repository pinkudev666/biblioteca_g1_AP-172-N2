# modelos/tipo_usuario.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import Base

class Tipo_usuario(Base):
    __tablename__ = 'tipo_usuario'

    id_tipo_usuario = Column(Integer, primary_key=True, autoincrement=True)
    tipo_usuario = Column(String(50), nullable=False)

    # relación 1:N hacia Usuario
    usuarios = relationship('Usuario', back_populates='tipo', cascade='all, delete-orphan')

    def __repr__(self) -> str:
        return f"<Tipo_usuario(id={self.id_tipo_usuario}, tipo={self.tipo_usuario!r})>"
