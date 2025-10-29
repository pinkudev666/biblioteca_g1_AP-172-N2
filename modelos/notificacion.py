# modelos/notificacion.py
from sqlalchemy import Column, Integer, String, Date, ForeignKey, text
from sqlalchemy.orm import relationship
from .base import Base

class Notificacion(Base):
    __tablename__ = 'notificacion'

    id_notificacion = Column(Integer, primary_key=True, autoincrement=True)
    mensaje_notificacion = Column(String(255), nullable=False)
    fecha_envio = Column(Date, nullable=False, server_default=text('CURRENT_DATE'))
    id_prestamo = Column(Integer, ForeignKey('prestamo.id_prestamo'), nullable=False)

    prestamo = relationship('Prestamo', back_populates='notificaciones')

    def __repr__(self) -> str:
        return f"<Notificacion(id={self.id_notificacion}, prestamo_id={self.id_prestamo})>"
