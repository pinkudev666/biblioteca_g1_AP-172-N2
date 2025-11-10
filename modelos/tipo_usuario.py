from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from .base import Base

class Tipo_usuario(Base):
    __tablename__ = 'tipo_usuario'

    id_tipo_usuario = Column(Integer, primary_key=True, autoincrement=True)
    tipo_usuario = Column(String(50), nullable=False)
    activo = Column(Boolean, default=True, nullable=False)

    # relación 1:N hacia Usuario
    usuarios = relationship('Usuario', back_populates='tipo')

    def __repr__(self) -> str:
        return f"<Tipo_usuario(id={self.id_tipo_usuario}, tipo={self.tipo_usuario!r})>"
