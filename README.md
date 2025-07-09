# Proyecto Integrador de Henry

Carrera: Data Engineer  
Alumno: Diego Lopez Castan

## EcommerceDB - Generación de Esquema con SQLAlchemy y PostgreSQL

Este proyecto en Python permite crear las tablas necesarias para una base de datos de comercio electrónico (`EcommerceDB`) utilizando SQLAlchemy y PostgreSQL. También incluye la opción de ejecutar directamente un script `.sql` si preferís trabajar con SQL puro.

---

## Requisitos

- Python 3.8 o superior
- PostgreSQL (con una base de datos ya creada)
- pip (gestor de paquetes de Python)

---

## Instalación

1. Cloná el repositorio o descargá el proyecto.
2. Creá y activá un entorno virtual (opcional pero recomendado):

```bash
python -m venv venv
source venv/bin/activate      # En Linux/macOS
venv\\Scripts\\activate         # En Windows
```

## Instalá las dependencias:

```bash
pip install -r requirements.txt
```

## Configuración

Editá el archivo db_conector.py para configurar tu conexión a PostgreSQL:

```bash
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base

Base = declarative_base()

def get_db_engine():
    return create_engine("postgresql+psycopg2://usuario:contraseña@localhost:5432/EcommerceDB")
```

## Despliegue con Docker

Este proyecto incluye un archivo docker-compose.yml que permite levantar fácilmente una base de datos PostgreSQL y una instancia de PgAdmin para administración visual.

### Pasos para iniciar los contenedores:

Copiá el siguiente archivo como docker-compose.yml en la raíz del proyecto (o en mi_proyecto_pg/).

Crea un archivo .env con tus variables de entorno:

```bash
POSTGRES_DB=EcommerceDB
POSTGRES_USER=admin
POSTGRES_PASSWORD=admin123
PGADMIN_DEFAULT_EMAIL=admin@admin.com
PGADMIN_DEFAULT_PASSWORD=admin123
```

Ejecutá Docker Compose:

```bash
docker-compose up -d
```

### Puertos expuestos:

```bash
PostgreSQL: localhost:5432
PgAdmin: http://localhost:8080
```

### Volúmenes:

./data: Datos persistentes de PostgreSQL

./pgadmin-data: Configuración persistente de PgAdmin

./init-scripts: Scripts .sql que se ejecutan automáticamente al iniciar la base de datos

##  Uso
### Opción A: Crear tablas con SQLAlchemy

```bash
python main.py
```

Esto usará los modelos definidos en modelos.py y creará automáticamente las tablas en la base de datos.

### Opción B: Ejecutar script SQL directamente

Podés ejecutar un script SQL completo editando main.py para usar la función run_sql_script("Create_ddl_postgres.sql").


## Estructura del Proyecto



├── scripts/    # Scripts SQL para crear tablas directamente

├── main.py 

├── main.py

├── docker-compose.yml

├── modelos.py

├── db_conector.py

├── requirements.txt

└── README.md                   


## Ver la base de datos en PgAdmin

Una vez que la base de datos `EcommerceDB` ha sido creada exitosamente, puede que **no la veas automáticamente en PgAdmin**. Esto es normal. PgAdmin requiere que registres el servidor manualmente.

### Pasos para agregar la base de datos en PgAdmin

1. Abrí tu navegador y andá a:
http://localhost:8080

2. Iniciá sesión con los datos definidos en el archivo `.env`:

3. En el panel izquierdo de PgAdmin:

Hacé clic derecho en "Servers"

Seleccioná "Register" → "Server..."

4. Completá el formulario:

🔹 Tab "General"
Name: Postgres

🔹 Tab "Connection"
Host name/address: db

Port: 5432

Maintenance database: EcommerceDB

Username: tu_usuario

Password: tu_pass

Hacé clic en "Save"



##  🙌 Créditos (opcional)
Desarrollado por Diego Lopez Castan como ejercicio de integración entre SQLAlchemy y PostgreSQL.

##   📝 Licencia
Este proyecto se entrega sin licencia explícita. Podés usarlo y modificarlo libremente con fines educativos o personales.
