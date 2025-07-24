-- models/intermediate/int_detalle_ordenes_enriquecido.sql
WITH detalle_base AS (
    SELECT *
    FROM {{ ref('stg_detalle_ordenes') }}
),

productos AS (
    SELECT *
    FROM {{ ref('int_productos_enriquecidos') }}
),

ordenes AS (
    SELECT *
    FROM {{ ref('stg_ordenes') }}
),

detalle_enriquecido AS (
    SELECT
        d.DetalleID,
        d.OrdenID,
        d.ProductoID,
        d.Cantidad,
        d.PrecioUnitario,
        d.Cantidad * d.PrecioUnitario AS subtotal,
        p.Nombre AS producto_nombre,
        p.categoria_nombre,
        p.segmento_precio,
        o.FechaOrden,
        o.UsuarioID,
        o.Total AS total_orden,
        ROUND(
            (d.Cantidad * d.PrecioUnitario) * 100.0 / NULLIF(o.Total, 0), 2
        ) AS porcentaje_del_total
    FROM detalle_base d
    LEFT JOIN productos p ON d.ProductoID = p.ProductoID
    LEFT JOIN ordenes o ON d.OrdenID = o.OrdenID
)

SELECT
    DetalleID,
    OrdenID,
    ProductoID,
    Cantidad,
    PrecioUnitario,
    subtotal,
    producto_nombre,
    categoria_nombre,
    segmento_precio,
    FechaOrden,
    UsuarioID,
    total_orden,
    porcentaje_del_total
FROM detalle_enriquecido