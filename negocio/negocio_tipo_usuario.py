# negocio/negocio_tipo.py
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from modelos.tipo_usuario import Tipo_usuario
from auxiliares.comparar_strings import normalizar_string
from prettytable import PrettyTable

class NegocioTipo:
    """Clase de negocio para manejar tipos de usuario (borrado lógico)."""

    def __init__(self, sesion: Session):
        self.sesion = sesion

    # --- Lectura ---
    def obtener_listado_tipos(self):
        """Devuelve solo tipos de usuario activos."""
        return self.sesion.query(Tipo_usuario).filter(Tipo_usuario.activo == True).all()

    def obtener_tipos_inactivos(self):
        """Devuelve tipos de usuario inactivos (borrados lógicamente)."""
        return self.sesion.query(Tipo_usuario).filter(Tipo_usuario.activo == False).all()

    def buscar_tipos_por_nombre(self, buscar: str):
        """
        Busca tipos por nombre (parcial, insensible a tildes/mayúsculas).
        Solo devuelve tipos activos.
        """
        if not buscar:
            return []
        buscar_norm = normalizar_string(buscar)
        tipos = self.obtener_listado_tipos()
        return [t for t in tipos if buscar_norm in normalizar_string(t.tipo_usuario)]

    # --- Interfaz (tabla) ---
    def mostrar_tipos_tabla(self, tipos):
        tabla = PrettyTable()
        tabla.field_names = ['ID', 'Tipo usuario']
        if tipos:
            for t in tipos:
                tabla.add_row([t.id_tipo_usuario, t.tipo_usuario])
            print(tabla)
        else:
            print("No hay tipos para mostrar.")

    # --- Mutaciones ---
    def agregar_tipo(self, nombre: str):
        """Agrega un tipo si no existe un tipo activo con el mismo nombre (insensible)."""
        nombre = (nombre or "").strip()
        if not nombre:
            return None

        # Evitar duplicados entre activos
        nombre_norm = normalizar_string(nombre)
        activos = self.obtener_listado_tipos()
        if any(normalizar_string(t.tipo_usuario) == nombre_norm for t in activos):
            return None

        nuevo = Tipo_usuario(tipo_usuario=nombre.title())
        try:
            self.sesion.add(nuevo)
            self.sesion.commit()
            return nuevo
        except SQLAlchemyError:
            self.sesion.rollback()
            return None

    def editar_tipo(self, tipo: Tipo_usuario, nuevo_nombre: str | None = None):
        """Edita el nombre del tipo dado (no cambia su estado activo)."""
        if nuevo_nombre:
            tipo.tipo_usuario = nuevo_nombre.strip().title()
            try:
                self.sesion.commit()
                return tipo
            except SQLAlchemyError:
                self.sesion.rollback()
                return None
        return tipo

    def editar_nombre_por_id(self, id_tipo: int, nuevo_nombre: str):
        """
        Método añadido: edita el nombre del tipo identificado por id_tipo.
        - Valida que `nuevo_nombre` no sea vacío.
        - Normaliza y previene duplicados con otros tipos activos.
        - Devuelve el objeto actualizado o None si falla / hay conflicto / no existe.
        """
        if not nuevo_nombre:
            return None

        # Obtener el tipo por id
        tipo = self.sesion.query(Tipo_usuario).get(id_tipo)
        if not tipo:
            return None

        nuevo_nombre_clean = nuevo_nombre.strip()
        if not nuevo_nombre_clean:
            return None

        nuevo_norm = normalizar_string(nuevo_nombre_clean)

        # Comprobar conflicto con otros tipos activos (excepto el mismo registro)
        activos = self.sesion.query(Tipo_usuario).filter(
            Tipo_usuario.activo == True,
            Tipo_usuario.id_tipo_usuario != tipo.id_tipo_usuario
        ).all()
        if any(normalizar_string(t.tipo_usuario) == nuevo_norm for t in activos):
            return None

        # Si todo bien, aplicar cambio y commitear
        tipo.tipo_usuario = nuevo_nombre_clean
        try:
            self.sesion.commit()
            return tipo
        except SQLAlchemyError:
            self.sesion.rollback()
            return None

    def editar_nombre_por_like(self, nombre_actual: str, nuevo_nombre: str):
        """
        Edita el nombre de un tipo de usuario usando coincidencia parcial (LIKE) en el nombre actual.
        - Busca entre tipos activos cuyo nombre contenga `nombre_actual` (insensible a mayúsculas).
        - Si hay más de una coincidencia, no realiza cambios (para evitar ambigüedad).
        - Valida duplicados entre tipos activos con el nuevo nombre.
        - Devuelve el tipo actualizado o None si no se encuentra, hay conflicto o falla.
        """
        if not nombre_actual or not nuevo_nombre:
            return None

        nombre_actual = nombre_actual.strip()
        nuevo_nombre = nuevo_nombre.strip()
        if not nombre_actual or not nuevo_nombre:
            return None

        # Buscar coincidencias parciales (LIKE) entre tipos activos
        tipos_coincidentes = self.sesion.query(Tipo_usuario).filter(
            Tipo_usuario.activo == True,
            Tipo_usuario.tipo_usuario.ilike(f"%{nombre_actual}%")
        ).all()

        if len(tipos_coincidentes) != 1:
            # Ninguno o más de uno: ambigüedad, no editar
            return None

        tipo = tipos_coincidentes[0]

        # Verificar duplicados del nuevo nombre (insensible)
        nuevo_norm = normalizar_string(nuevo_nombre)
        activos = self.obtener_listado_tipos()
        if any(normalizar_string(t.tipo_usuario) == nuevo_norm and t.id_tipo_usuario != tipo.id_tipo_usuario for t in activos):
            return None

        # Aplicar cambio
        tipo.tipo_usuario = nuevo_nombre.title()
        try:
            self.sesion.commit()
            return tipo
        except SQLAlchemyError:
            self.sesion.rollback()
            return None

    def eliminar_tipo(self, tipo_or_nombre):
        """
        Borrado lógico: marca activo=False.
        acepta un objeto Tipo_usuario o un nombre (string).
        No permite desactivar si existen usuarios activos asociados.
        Devuelve el objeto actualizado o None si no pudo.
        """
        # Resolver objeto
        if isinstance(tipo_or_nombre, Tipo_usuario):
            tipo = tipo_or_nombre
        else:
            nombre = (tipo_or_nombre or "").strip()
            if not nombre:
                return None
            tipo = self.sesion.query(Tipo_usuario)\
                             .filter(Tipo_usuario.tipo_usuario.ilike(nombre))\
                             .first()
            if not tipo:
                return None

        # Comprobar usuarios activos asociados (si existe la relación)
        try:
            asociados = getattr(tipo, "usuarios", None)
            if asociados:
                # Si algún usuario asociado está activo, impedimos la desactivación
                for u in asociados:
                    if getattr(u, "usuario_activo", True):
                        # hay un usuario activo: no permitir borrado lógico
                        return None
        except Exception:
            # Si por alguna razón no se puede comprobar, continuamos con cautela
            pass

        tipo.activo = False
        try:
            self.sesion.commit()
            return tipo
        except SQLAlchemyError:
            self.sesion.rollback()
            return None

    def reactivar_tipo(self, tipo_or_nombre):
        """
        Reactiva un tipo (activo=True). acepta objeto o nombre.
        Devuelve el objeto reactivado o None.
        """
        if isinstance(tipo_or_nombre, Tipo_usuario):
            tipo = tipo_or_nombre
        else:
            nombre = (tipo_or_nombre or "").strip()
            if not nombre:
                return None
            tipo = self.sesion.query(Tipo_usuario)\
                             .filter(Tipo_usuario.tipo_usuario.ilike(nombre))\
                             .first()
            if not tipo:
                return None

        tipo.activo = True
        try:
            self.sesion.commit()
            return tipo
        except SQLAlchemyError:
            self.sesion.rollback()
            return None
