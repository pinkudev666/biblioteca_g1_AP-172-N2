from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from .base import Base

class Libro(Base):
    __tablename__ = 'libro'

    id_libro = Column(Integer, primary_key=True, autoincrement=True)
    isbn_libro = Column(String(20), nullable=False, unique=True)
    nombre_libro = Column(String(150), nullable=False)
    autor_libro = Column(String(100), nullable=False)
    copias_disponibles = Column(Integer, default=0)
    activo = Column(Boolean, default=True, nullable=False)

    #Relación con préstamos 1:n
    prestamos = relationship('Prestamo', back_populates='libro')

    def __repr__(self) -> str:
        return f"<Libro(id={self.id_libro}, isbn={self.isbn_libro!r}, nombre={self.nombre_libro!r})>"
