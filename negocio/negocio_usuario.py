from config_rutas import ROOT
from datos.conexion import Session
from modelos.usuario import Usuario
from auxiliares.comparar_strings import normalizar_string
from prettytable import PrettyTable

class UsuarioNegocio:
    def __init__(self):
        self.session = Session()

    def crear_usuario(self, rut, nombre, correo, id_tipo_usuario):
        try:
            correo_norm = normalizar_string(correo)
            usuarios_activos = self.session.query(Usuario).filter(Usuario.usuario_activo == True).all()
            for u in usuarios_activos:
                if normalizar_string(u.correo_usuario) == correo_norm:
                    raise Exception("El correo ya está en uso por otro usuario activo.")

            usuario = Usuario(
                rut_usuario=rut,
                nombre_usuario=nombre,
                correo_usuario=correo,
                id_tipo_usuario=id_tipo_usuario,
                usuario_activo=True
            )
            self.session.add(usuario)
            self.session.commit()
            return usuario
        except Exception as e:
            self.session.rollback()
            raise Exception(f"Error al crear usuario: {e}")

    def obtener_usuario(self, rut):
        return self.session.query(Usuario).filter(
            Usuario.rut_usuario == rut,
            Usuario.usuario_activo == True
        ).first()

    def obtener_usuarios(self):
        return self.session.query(Usuario).filter(
            Usuario.usuario_activo == True
        ).all()

    def buscar_usuarios(self, texto_busqueda):
        texto_norm = normalizar_string(texto_busqueda)
        resultados = []
        for u in self.session.query(Usuario).filter(Usuario.usuario_activo == True).all():
            if (texto_norm in normalizar_string(u.nombre_usuario) or
                texto_norm in normalizar_string(u.correo_usuario)):
                resultados.append(u)
        return resultados

    def actualizar_usuario(self, rut, **kwargs):
        try:
            usuario = self.session.query(Usuario).filter(Usuario.rut_usuario == rut).first()
            if not usuario:
                return None

            if 'correo_usuario' in kwargs:
                correo_norm = normalizar_string(kwargs['correo_usuario'])
                usuarios_activos = self.session.query(Usuario).filter(Usuario.rut_usuario != rut).all()
                for u in usuarios_activos:
                    if normalizar_string(u.correo_usuario) == correo_norm and u.usuario_activo:
                        raise Exception("El correo ya está en uso por otro usuario activo.")

            for key, value in kwargs.items():
                if hasattr(usuario, key):
                    setattr(usuario, key, value)

            self.session.commit()
            return usuario
        except Exception as e:
            self.session.rollback()
            raise Exception(f"Error al actualizar usuario: {e}")

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
            return usuario
        except Exception as e:
            self.session.rollback()
            raise Exception(f"Error al eliminar usuario: {e}")

# ----------------- Helpers -----------------
def mostrar_tabla_usuarios(usuarios):
    if not usuarios:
        print("No hay usuarios para mostrar.")
        return

    tabla = PrettyTable()
    tabla.field_names = ["RUT", "Nombre", "Correo", "ID Tipo Usuario", "Activo"]

    for u in usuarios:
        tabla.add_row([
            u.rut_usuario,
            u.nombre_usuario,
            u.correo_usuario,
            u.id_tipo_usuario,
            "Sí" if u.usuario_activo else "No"
        ])

    print(tabla)

def menu_usuario():
    print("\n=== MENÚ DE PRUEBA USUARIO ===")
    print("1. Crear usuario")
    print("2. Obtener usuario por RUT")
    print("3. Buscar usuarios por texto")
    print("4. Actualizar usuario")
    print("5. Eliminar usuario (borrado lógico)")
    print("6. Listar todos los usuarios activos")
    print("0. Salir")
    return input("Selecciona una opción: ").strip()

# ----------------- CLI -----------------
def main():
    negocio = UsuarioNegocio()

    while True:
        opcion = menu_usuario()

        if opcion == "1":
            rut = input("RUT: ").strip()
            nombre = input("Nombre: ").strip()
            correo = input("Correo: ").strip()
            tipo = int(input("ID tipo usuario: ").strip())
            try:
                u = negocio.crear_usuario(rut, nombre, correo, tipo)
                print("Usuario creado:")
                mostrar_tabla_usuarios([u])
            except Exception as e:
                print(e)

        elif opcion == "2":
            rut = input("RUT del usuario a obtener: ").strip()
            u = negocio.obtener_usuario(rut)
            if u:
                mostrar_tabla_usuarios([u])
            else:
                print("Usuario no encontrado.")

        elif opcion == "3":
            texto = input("Texto para buscar: ").strip()
            resultados = negocio.buscar_usuarios(texto)
            if resultados:
                mostrar_tabla_usuarios(resultados)
            else:
                print("No se encontraron usuarios.")

        elif opcion == "4":
            rut = input("RUT del usuario a actualizar: ").strip()
            print("Deja en blanco los campos que no quieras cambiar.")
            nombre = input("Nuevo nombre: ").strip()
            correo = input("Nuevo correo: ").strip()
            tipo_str = input("Nuevo ID tipo usuario: ").strip()
            activo_str = input("¿El usuario estará activo? (s/n): ").strip()

            cambios = {}
            if nombre:
                cambios["nombre_usuario"] = nombre
            if correo:
                cambios["correo_usuario"] = correo
            if tipo_str:
                cambios["id_tipo_usuario"] = int(tipo_str)
            if activo_str.lower() == 's':
                cambios["usuario_activo"] = True
            elif activo_str.lower() == 'n':
                cambios["usuario_activo"] = False

            try:
                u = negocio.actualizar_usuario(rut, **cambios)
                if u:
                    print("Usuario actualizado:")
                    mostrar_tabla_usuarios([u])
                else:
                    print("Usuario no encontrado.")
            except Exception as e:
                print(e)

        elif opcion == "5":
            rut = input("RUT del usuario a eliminar: ").strip()
            u = negocio.eliminar_usuario(rut)
            if u:
                print("Usuario eliminado (borrado lógico):")
                mostrar_tabla_usuarios([u])
            else:
                print("Usuario no encontrado.")

        elif opcion == "6":
            usuarios = negocio.obtener_usuarios()
            mostrar_tabla_usuarios(usuarios)

        elif opcion == "0":
            print("Saliendo...")
            break

        else:
            print("Opción inválida, intenta de nuevo.")

if __name__ == "__main__":
    main()
