-- models/intermediate/int_metricas_productos.sql
WITH productos AS (
    SELECT *
    FROM {{ ref('int_productos_enriquecidos') }}
),

detalle_ordenes AS (
    SELECT *
    FROM {{ ref('int_detalle_ordenes_enriquecido') }}
),

reseñas AS (
    SELECT *
    FROM {{ ref('int_resenas_agregadas') }}
),

metricas_ventas AS (
    SELECT
        ProductoID,
        COUNT(DISTINCT OrdenID) AS total_ordenes,
        SUM(Cantidad) AS total_vendido,
        AVG(Cantidad) AS promedio_cantidad_por_orden,
        SUM(subtotal) AS ingresos_totales,
        AVG(subtotal) AS ingreso_promedio_por_orden,
        MIN(FechaOrden) AS primera_venta,
        MAX(FechaOrden) AS ultima_venta
    FROM detalle_ordenes
    GROUP BY ProductoID
),

metricas_reseñas AS (
    SELECT
        ProductoID,
        COUNT(*) AS total_reseñas,
        AVG(Calificacion) AS calificacion_promedio,
        COUNT(CASE WHEN sentimiento_calificacion = 'Positiva' THEN 1 END) AS reseñas_positivas,
        COUNT(CASE WHEN sentimiento_calificacion = 'Negativa' THEN 1 END) AS reseñas_negativas,
        COUNT(CASE WHEN tipo_comentario != 'Sin Comentario' THEN 1 END) AS reseñas_con_comentario
    FROM reseñas
    GROUP BY ProductoID
),

productos_con_metricas AS (
    SELECT
        p.*,
        COALESCE(v.total_ordenes, 0) AS total_ordenes,
        COALESCE(v.total_vendido, 0) AS total_vendido,
        COALESCE(v.promedio_cantidad_por_orden, 0) AS promedio_cantidad_por_orden,
        COALESCE(v.ingresos_totales, 0) AS ingresos_totales,
        COALESCE(v.ingreso_promedio_por_orden, 0) AS ingreso_promedio_por_orden,
        v.primera_venta,
        v.ultima_venta,
        COALESCE(r.total_reseñas, 0) AS total_reseñas,
        COALESCE(r.calificacion_promedio, 0) AS calificacion_promedio,
        COALESCE(r.reseñas_positivas, 0) AS reseñas_positivas,
        COALESCE(r.reseñas_negativas, 0) AS reseñas_negativas,
        COALESCE(r.reseñas_con_comentario, 0) AS reseñas_con_comentario,
        CASE 
            WHEN COALESCE(v.total_vendido, 0) = 0 THEN 'Sin Ventas'
            WHEN v.total_vendido <= 10 THEN 'Pocas Ventas'
            WHEN v.total_vendido <= 100 THEN 'Ventas Moderadas'
            ELSE 'Altas Ventas'
        END AS categoria_ventas,
        CASE 
            WHEN COALESCE(r.calificacion_promedio, 0) = 0 THEN 'Sin Calificar'
            WHEN r.calificacion_promedio >= 4 THEN 'Excelente'
            WHEN r.calificacion_promedio >= 3 THEN 'Bueno'
            ELSE 'Mejorable'
        END AS categoria_calificacion
    FROM productos p
    LEFT JOIN metricas_ventas v ON p.ProductoID = v.ProductoID
    LEFT JOIN metricas_reseñas r ON p.ProductoID = r.ProductoID
)

SELECT *
FROM productos_con_metricas