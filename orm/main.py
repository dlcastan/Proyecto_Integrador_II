import os
from sqlalchemy import text
from db_conector import get_db_engine

SCRIPTS_DIR = "scripts_postgresql"

# Orden de ejecución para evitar errores por claves foráneas
SCRIPT_ORDER = [
    "2.usuarios_postgres.sql",
    "3.categorias_postgress.sql",
    "4.Productos_postgres.sql",
    "5.ordenes_postgres.sql",
    "6.detalles_ordenes.sql",
    "7.direcciones_envio_postgres.sql",
    "8.carrito_postgres.sql",
    "9.metodos_pago_postgres.sql",
    "10.ordenes_metodospago_postgres.sql",
    "11.resenas_productos_postgres.sql",
    "12.historial_pagos_postgres.sql"
]

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
    print(f"✅ Script ejecutado correctamente: {filepath}")

def drop_all_tables_and_indexes(engine):
    print("\nEliminando índices y tablas (con CASCADE)...")
    with engine.connect() as conn:
        # Iniciar una transacción explícita
        with conn.begin() as transaction:
            # Eliminar índices no primarios ni únicos de sistema
            indexes_result = conn.execute(text("""
                SELECT indexname, schemaname
                FROM pg_indexes
                WHERE schemaname NOT IN ('pg_catalog', 'information_schema')
                  AND indexname NOT LIKE 'pg_%';
            """))
            indexes = [(row.schemaname, row.indexname) for row in indexes_result]

            for schema, index in indexes:
                print(f"Eliminando índice: {schema}.{index}")
                try:
                    conn.execute(text(f'DROP INDEX IF EXISTS "{schema}"."{index}"'))
                except Exception as e:
                    print(f"Error eliminando índice {schema}.{index}: {e}")

            # Eliminar tablas
            tables_result = conn.execute(text("""
                SELECT table_schema, table_name 
                FROM information_schema.tables 
                WHERE table_type = 'BASE TABLE' 
                AND table_schema NOT IN ('pg_catalog', 'information_schema');
            """))
            tables = [(row.table_schema, row.table_name) for row in tables_result]

            for schema, table in tables:
                print(f"Eliminando tabla: {schema}.{table}")
                conn.execute(text(f'DROP TABLE IF EXISTS "{schema}"."{table}" CASCADE'))

    print("Todos los índices y tablas fueron eliminados correctamente.")

def main():
    print("Selecciona una opción:")
    print("1. Crear tablas")
    print("2. Cargar datos (insertar en tablas)")
    print("3. Borrar todas las tablas")
    choice = input("Opción: ").strip()

    engine = get_db_engine()
    print(f"\nConectando a la base de datos: {engine.url}")

    if choice == "1":
        ddl_path = os.path.join(SCRIPTS_DIR, "1.Create_ddl_postgres.sql")
        if os.path.isfile(ddl_path):
            run_sql_script(engine, ddl_path)
        else:
            print("❌ Error: No se encontró 1.Create_ddl_postgres.sql")

    elif choice == "2":
        print("\n🔄 Ejecutando scripts en orden lógico...")
        for script in SCRIPT_ORDER:
            filepath = os.path.join(SCRIPTS_DIR, script)
            if os.path.isfile(filepath):
                try:
                    run_sql_script(engine, filepath)
                except Exception as e:
                    print(f"❌ Error en {script}: {e}\n→ Continuando con el siguiente script...")
            else:
                print(f"⚠️ Archivo no encontrado: {script}")

    elif choice == "3":
        drop_all_tables_and_indexes(engine)

    else:
        print("Opción no válida.")

if __name__ == "__main__":
    main()
