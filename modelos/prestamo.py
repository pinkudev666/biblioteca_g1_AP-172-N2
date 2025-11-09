from sqlalchemy import Column, Integer, Date, ForeignKey, Enum, String
from sqlalchemy.orm import relationship
from .base import Base

estado_enum = Enum(
    'Pendiente', 'Devuelto a tiempo', 'Devuelto atrasado',
    name='estado_prestamo_enum'
)

class Prestamo(Base):
    __tablename__ = 'prestamo'

    id_prestamo = Column(Integer, primary_key=True, autoincrement=True)
    fecha_inicio = Column(Date, nullable=False)
    fecha_vencimiento = Column(Date, nullable=False)
    fecha_devolucion = Column(Date, nullable=True)
    rut_usuario = Column(String(15), ForeignKey('usuario.rut_usuario'), nullable=False)
    id_libro = Column(Integer, ForeignKey('libro.id_libro'), nullable=False)
    estado = Column(estado_enum, nullable=False, server_default='Pendiente')

    usuario = relationship('Usuario', back_populates='prestamos')
    libro = relationship('Libro', back_populates='prestamos')
    multas = relationship('Multa', back_populates='prestamo', cascade='all, delete-orphan')
    notificaciones = relationship('Notificacion', back_populates='prestamo', cascade='all, delete-orphan')

    def __repr__(self) -> str:
        return f"<Prestamo(id={self.id_prestamo}, usuario={self.rut_usuario!r}, libro_id={self.id_libro})>"
