{{ config(
    materialized='view',
    description='KPI: Satisfacción productos - Promedio de calificaciones de productos'
) }}

SELECT 
    'satisfaccion_productos' AS kpi_nombre,
    ROUND(AVG(Calificacion), 2) AS valor,
    'puntos' AS unidad,
    CURRENT_DATE AS fecha_calculo,
    'Promedio de calificaciones de productos' AS descripcion
FROM {{ ref('int_resenas_agregadas') }}
