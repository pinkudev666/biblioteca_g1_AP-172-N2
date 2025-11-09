from config_rutas import ROOT
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError

from datos.conexion import Session
from modelos.usuario import Usuario
from auxiliares.comparar_strings import *
from modelos.tipo_usuario import Tipo_usuario
from typing import List, Dict

class UsuarioNegocio:
    def __init__(self):
        self.session = Session()

    # 1. Función para crear un nuevo usuario
    def crear_usuario(self, rut, nombre, correo, id_tipo_usuario):
        try:
            correo_norm = (normalizar_string(correo) or "").lower()

            # Buscamos en la BD (no traer todo a memoria)
            existe = self.session.query(Usuario).filter(
                func.lower(Usuario.correo_usuario) == correo_norm
            ).first()
            if existe:
                raise Exception("El correo ya está en uso por otro usuario.")

            usuario = Usuario(
                rut_usuario=rut,
                nombre_usuario=nombre,
                correo_usuario=correo_norm,  # guardamos normalizado
                id_tipo_usuario=int(id_tipo_usuario),
                usuario_activo=True
            )
            self.session.add(usuario)
            try:
                self.session.commit()
            except IntegrityError:
                self.session.rollback()
                raise Exception("El correo ya está en uso por otro usuario (conflicto en BD).")
            # refrescar para evitar expired attrs
            self.session.refresh(usuario)
            return usuario
        except Exception as e:
            # ya hicimos rollback en errores de commit; en otros casos aseguramos rollback
            try:
                self.session.rollback()
            except Exception:
                pass
            raise Exception(f"Error al crear usuario: {e}")

    # 2. Función para obtener un usuario por su RUT independientemente de su estado
    def obtener_usuario(self, rut, solo_activos=False):
        q = self.session.query(Usuario).filter(Usuario.rut_usuario == rut)
        if solo_activos:
            q = q.filter(Usuario.usuario_activo == True)
        return q.first()
    
    # 3. Función para listar usuarios por tipo de usuario (nombre_tipo)
    def listar_usuarios_por_tipo(self, nombre_tipo_usuario: str):
        tipo = self.session.query(Tipo_usuario).filter_by(tipo_usuario=nombre_tipo_usuario).first()
        if not tipo:
            return None  # None = tipo no existe
        usuarios = self.session.query(Usuario).filter_by(id_tipo_usuario=tipo.id_tipo_usuario).all()
        return usuarios  # [] = tipo existe pero sin usuarios


    # 4. Función para actualizar datos de un usuario existente
    def actualizar_usuario(self, rut, **kwargs):
        try:
            rut_normalizado = normalizar_rut(rut)
            usuario = (
                self.session.query(Usuario)
                .filter(func.replace(func.replace(func.upper(Usuario.rut_usuario), '.', ''), '-', '') == rut_normalizado)
                .first()
            )

            if not usuario:
                return None  # no se encontró el usuario

            # Solo usuarios activos pueden ser modificados
            if not usuario.usuario_activo:
                raise Exception("El usuario está inactivo y no puede ser modificado.")

            # Si se cambia correo, normalizamos y validamos unicidad
            if 'correo_usuario' in kwargs:
                correo_norm = normalizar_string(kwargs['correo_usuario'])
                existe = (
                    self.session.query(Usuario)
                    .filter(Usuario.rut_usuario != rut)
                    .filter(func.lower(Usuario.correo_usuario) == correo_norm)
                    .first()
                )
                if existe:
                    raise Exception("El correo ya está en uso por otro usuario.")
                kwargs['correo_usuario'] = correo_norm

            # Normalizamos id_tipo_usuario si viene como string
            if 'id_tipo_usuario' in kwargs:
                try:
                    kwargs['id_tipo_usuario'] = int(kwargs['id_tipo_usuario'])
                except ValueError:
                    raise Exception("El tipo de usuario debe ser numérico.")

            # Actualizamos solo los campos válidos del modelo
            campos_validos = {'nombre_usuario', 'correo_usuario', 'id_tipo_usuario', 'usuario_activo'}
            for key, value in kwargs.items():
                if key in campos_validos:
                    setattr(usuario, key, value)

            try:
                self.session.commit()
            except IntegrityError:
                self.session.rollback()
                raise Exception("Error de integridad al actualizar el usuario (posible duplicado).")

            self.session.refresh(usuario)
            return usuario

        except Exception as e:
            try:
                self.session.rollback()
            except Exception:
                pass
            raise Exception(f"Error al actualizar usuario: {e}")

    # 5. Borrar usuario mediante borrado lógico (cambiar estado a inactivo)
    def eliminar_usuario(self, rut):
        try:
            usuario = self.session.query(Usuario).filter(
                Usuario.rut_usuario == rut,
                Usuario.usuario_activo == True
            ).first()
            if not usuario:
                return None
            usuario.usuario_activo = False
            self.session.commit()
            self.session.refresh(usuario)
            return usuario
        except Exception as e:
            try:
                self.session.rollback()
            except Exception:
                pass
            raise Exception(f"Error al eliminar usuario: {e}")

    def cerrar(self):
        try:
            self.session.close()
        except Exception:
            pass

    # 6. Activar usuario (cambiar estado a activo)
    def activar_usuario(self, rut):
        try:
            usuario = self.session.query(Usuario).filter(
                Usuario.rut_usuario == rut,
                Usuario.usuario_activo == False
            ).first()
            if not usuario:
                return None
            usuario.usuario_activo = True
            self.session.commit()
            self.session.refresh(usuario)
            return usuario
        except Exception as e:
            try:
                self.session.rollback()
            except Exception:
                pass
            raise Exception(f"Error al activar usuario: {e}")


    # 7. Función para obtener lista de usuarios ACTIVOS
    def obtener_usuarios(self, solo_activos=True):
        q = self.session.query(Usuario)
        if solo_activos:
            q = q.filter(Usuario.usuario_activo == True)
        return q.order_by(Usuario.nombre_usuario).all()

    