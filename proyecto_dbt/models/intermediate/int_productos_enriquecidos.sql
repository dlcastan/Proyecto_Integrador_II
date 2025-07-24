-- models/intermediate/int_productos_enriquecidos.sql
WITH productos_base AS (
    SELECT *
    FROM {{ ref('stg_productos') }}
),

categorias_base AS (
    SELECT *
    FROM {{ ref('stg_categorias') }}
),

productos_con_categoria AS (
    SELECT
        p.*,
        c.Nombre AS categoria_nombre,
        c.Descripcion AS categoria_descripcion
    FROM productos_base p
    LEFT JOIN categorias_base c ON p.CategoriaID = c.CategoriaID
),

productos_enriquecidos AS (
    SELECT
        *,
        CASE 
            WHEN Stock = 0 THEN 'Sin Stock'
            WHEN Stock <= 10 THEN 'Stock Bajo'
            WHEN Stock <= 50 THEN 'Stock Normal'
            ELSE 'Stock Alto'
        END AS estado_stock,
        CASE 
            WHEN Precio <= 100 THEN 'Económico'
            WHEN Precio <= 500 THEN 'Medio'
            WHEN Precio <= 1000 THEN 'Premium'
            ELSE 'Lujo'
        END AS segmento_precio
    FROM productos_con_categoria
)

SELECT
    ProductoID,
    Nombre,
    Descripcion,
    Precio,
    Stock,
    CategoriaID,
    categoria_nombre,
    categoria_descripcion,
    estado_stock,
    segmento_precio
FROM productos_enriquecidos