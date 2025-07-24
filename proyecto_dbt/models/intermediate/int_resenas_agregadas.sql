-- models/intermediate/int_reseñas_agregadas.sql
WITH reseñas_base AS (
    SELECT *
    FROM {{ ref('stg_resenas_productos') }}
),

productos AS (
    SELECT *
    FROM {{ ref('int_productos_enriquecidos') }}
),

usuarios AS (
    SELECT *
    FROM {{ ref('int_usuarios_enriquecidos') }}
),

reseñas_con_contexto AS (
    SELECT
        r.ReseñaID,
        r.UsuarioID,
        r.ProductoID,
        r.Calificacion,
        r.Comentario,
        r.Fecha,
        p.Nombre AS producto_nombre,
        p.categoria_nombre,
        p.Precio AS precio_producto,
        u.nombre_completo AS usuario_nombre,
        u.segmento_antiguedad,
        CASE 
            WHEN r.Calificacion >= 4 THEN 'Positiva'
            WHEN r.Calificacion >= 3 THEN 'Neutral'
            ELSE 'Negativa'
        END AS sentimiento_calificacion,
        CASE 
            WHEN LENGTH(COALESCE(r.Comentario, '')) = 0 THEN 'Sin Comentario'
            WHEN LENGTH(r.Comentario) <= 50 THEN 'Comentario Corto'
            WHEN LENGTH(r.Comentario) <= 200 THEN 'Comentario Medio'
            ELSE 'Comentario Largo'
        END AS tipo_comentario,
        EXTRACT(YEAR FROM r.Fecha) AS año_reseña,
        EXTRACT(MONTH FROM r.Fecha) AS mes_reseña
    FROM reseñas_base r
    LEFT JOIN productos p ON r.ProductoID = p.ProductoID
    LEFT JOIN usuarios u ON r.UsuarioID = u.UsuarioID
)

SELECT
    ReseñaID,
    UsuarioID,
    ProductoID,
    Calificacion,
    Comentario,
    Fecha,
    producto_nombre,
    categoria_nombre,
    precio_producto,
    usuario_nombre,
    segmento_antiguedad,
    sentimiento_calificacion,
    tipo_comentario,
    año_reseña,
    mes_reseña
FROM reseñas_con_contexto