from sqlalchemy import text
from db_conector import get_db_engine

import os

# Scripts SQL para ejecutar
SQL_SCRIPTS = [
    "scripts/Create_ddl_postgres.sql",
    "scripts/categorias_postgress.sql",
    "scripts/Productos_postgres.sql",
    "scripts/usuarios_postgres.sql",
    "scripts/direcciones_envio_postgres.sql",
    "scripts/carrito_postgres.sql",
    "scripts/metodos_pago_postgres.sql",
    "scripts/ordenes_postgres.sql",
    "scripts/ordenes_metodospago_postgres.sql",
    "scripts/historial_pagos_postgres.sql",
    "scripts/resenas_productos_postgres.sql"
]

def run_sql_script(engine, filename):
    print(f"\nEjecutando script: {filename}")
    with engine.connect() as conn:
        with conn.begin():
            with open(filename, 'r', encoding='utf-8') as file:
                sql_script = file.read()
                for statement in sql_script.split(';'):
                    statement = statement.strip()
                    if statement:
                        conn.execute(text(statement))
            print(f"Script ejecutado correctamente: {filename}")

def main():
    engine = get_db_engine()
    print(f"Conectando a la base de datos: {engine.url}")
    
    for script_path in SQL_SCRIPTS:
        if os.path.isfile(script_path):
            run_sql_script(engine, script_path)
        else:
            print(f"Error: Archivo no encontrado: {script_path}")
    
    print("\nProceso corrido correctamente.")

if __name__ == "__main__":
    main()
