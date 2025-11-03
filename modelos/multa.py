from sqlalchemy import Column, Integer, Date, ForeignKey, text, DECIMAL
from sqlalchemy.orm import relationship
from .base import Base

class Multa(Base):
    __tablename__ = 'multa'

    id_multa = Column(Integer, primary_key=True, autoincrement=True)
    monto_multa = Column(DECIMAL(6, 2), nullable=False)
    fecha_generacion = Column(Date, nullable=False, server_default=text('CURRENT_DATE'))
    id_prestamo = Column(Integer, ForeignKey('prestamo.id_prestamo'), nullable=False)

    prestamo = relationship('Prestamo', back_populates='multas')

    def __repr__(self) -> str:
        return f"<Multa(id={self.id_multa}, monto={self.monto_multa}, prestamo_id={self.id_prestamo})>"
