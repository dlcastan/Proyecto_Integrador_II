import os
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine


load_dotenv()


DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432") 
DB_NAME = os.getenv("POSTGRES_DB")

DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

print(f"Conectando a: {DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

try:
    engine = create_engine(DATABASE_URL, echo=False, client_encoding='utf8')
    print("Conexion creada exitosamente.")
except Exception as e:
    print(f"Error al crear la conexión: {e}")
    raise


Base = declarative_base()
DBSession = sessionmaker(bind=engine)

def get_db_engine():
    return engine

def get_db_session():
    return DBSession()

def get_db_connection():
    return engine.connect()
