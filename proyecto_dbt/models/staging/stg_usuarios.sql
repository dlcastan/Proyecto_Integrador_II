-- models/staging/stg_usuarios.sql

WITH raw_usuarios AS (
    SELECT *
    FROM {{ source('public', 'usuarios') }}
)

SELECT
    UsuarioID,
    Nombre,
    Apellido,
    Email,
    FechaRegistro
FROM raw_usuarios
