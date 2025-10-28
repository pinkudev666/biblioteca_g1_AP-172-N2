from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Herramientas necesarias para trabajar con DB
# pip install sqlalchemy
# pip install mysql-connector-python

# Definir cadena de conexion
# mysql+mysqlconnector://user:password@host:port/database_name

DATABASE_URL = "mysql+mysqlconnector://root:@localhost:3306/biblioteca_db"
motor_db = create_engine(DATABASE_URL)
Session = sessionmaker(bind=motor_db)
sesion = Session()