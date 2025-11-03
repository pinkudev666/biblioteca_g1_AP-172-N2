from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

# Cadena de conexión
DATABASE_URL = "mysql+mysqlconnector://root:@localhost:3306/biblioteca_db"

try:
    motor_db = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=motor_db)
    #print("Conexión establecida correctamente con la base de datos")

    #Prueba de conexión: obtener el nombre de la base de datos actual
    #with Session() as sesion:
        #resultado = sesion.execute(text("SELECT DATABASE();"))
        #print("Base de datos actual:", resultado.scalar())

except SQLAlchemyError as e:
    print("Error al conectar con la base de datos:")
    print(e)
