import os
from sqlalchemy import text
from db_conector import get_db_engine

SCRIPTS_DIR = "scripts"
DDL_FILE = "1.Create_ddl.sql"

def run_sql_script(engine, filepath):
    print(f"\nEjecutando script: {filepath}")
    with engine.connect() as conn:
        with conn.begin():
            with open(filepath, 'r', encoding='utf-8') as file:
                raw_sql = file.read()

            # 1. Eliminar líneas que contienen solo "GO" o "USE ..."
            cleaned_lines = []
            for line in raw_sql.splitlines():
                stripped = line.strip().upper()
                if stripped == "GO" or stripped.startswith("USE "):
                    continue
                if "CREATE DATABASE" in stripped:
                    print("CREATE DATABASE omitido.")
                    continue
                cleaned_lines.append(line)

            cleaned_script = "\n".join(cleaned_lines)

            # 2. Ejecutar cada sentencia separada por punto y coma
            for statement in cleaned_script.split(';'):
                statement = statement.strip()
                if statement:
                    conn.execute(text(statement))
    print("Script ejecutado correctamente.")


def main():
    engine = get_db_engine()
    ddl_path = os.path.join(SCRIPTS_DIR, DDL_FILE)
    
    if os.path.isfile(ddl_path):
        print(f"Conectando a la base de datos: {engine.url}")
        run_sql_script(engine, ddl_path)
    else:
        print(f"Error: No se encontró el archivo {DDL_FILE}")

if __name__ == "__main__":
    main()
