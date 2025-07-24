{{ config(
    materialized='view',
    description='KPI: Ticket promedio - Valor promedio gastado por orden completada'
) }}

SELECT 
    'ticket_promedio' AS kpi_nombre,
    ROUND(AVG(Total), 2) AS valor,
    'ARS' AS unidad,
    CURRENT_DATE AS fecha_calculo,
    'Valor promedio gastado por orden completada' AS descripcion
FROM {{ ref('mart_ordenes_completadas') }}