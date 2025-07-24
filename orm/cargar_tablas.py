import os
from sqlalchemy import text
from db_conector import get_db_engine

SCRIPTS_DIR = "scripts"

def run_sql_script(engine, filepath):
    print(f"\nEjecutando script: {filepath}")
    with engine.connect() as conn:
        with conn.begin():
            with open(filepath, 'r', encoding='utf-8') as file:
                sql_script = file.read()
                for statement in sql_script.split(';'):
                    statement = statement.strip()
                    if statement:
                        conn.execute(text(statement))
    print("Script ejecutado correctamente.")

def main():
    engine = get_db_engine()
    print(f"Conectando a la base de datos: {engine.url}")

    for filename in sorted(os.listdir(SCRIPTS_DIR)):
        if filename.endswith(".sql") and filename != "1.Create_ddl.sql":
            filepath = os.path.join(SCRIPTS_DIR, filename)
            run_sql_script(engine, filepath)

    print("Carga de datos finalizada.")

if __name__ == "__main__":
    main()
