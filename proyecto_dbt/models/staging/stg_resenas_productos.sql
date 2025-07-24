-- models/staging/stg_reseñas_productos.sql
WITH raw_reseñas_productos AS (
    SELECT *
    FROM {{ source('public', 'reseñasproductos') }}
)

SELECT
    ReseñaID,
    UsuarioID,
    ProductoID,
    Calificacion,
    Comentario,
    Fecha
FROM raw_reseñas_productos