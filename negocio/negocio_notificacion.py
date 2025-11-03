from modelos.notificacion import Notificacion
from datos.obtener_datos import obtener_listado_objetos
from datos import insertar_objeto
from prettytable import PrettyTable
from datetime import date


def obtener_listado_notificaciones():
    tabla_notificaciones = PrettyTable()
    tabla_notificaciones.field_names = ['N°', 'Mensaje', 'Fecha Envío', 'ID Préstamo']
    listado_notificaciones = obtener_listado_objetos(Notificacion)
    if listado_notificaciones:
        for notif in listado_notificaciones:
            tabla_notificaciones.add_row([notif.id_notificacion, notif.mensaje_notificacion, notif.fecha_envio, notif.id_prestamo])
        print(tabla_notificaciones)


def agregar_notificacion():
    mensaje = input('Ingrese mensaje de notificación: ')
    id_prestamo = int(input('Ingrese ID del préstamo asociado: '))
    nueva_notificacion = Notificacion(mensaje_notificacion=mensaje, id_prestamo=id_prestamo, fecha_envio=date.today())
    insertar_objeto(nueva_notificacion)
    print('Notificación registrada correctamente.')
