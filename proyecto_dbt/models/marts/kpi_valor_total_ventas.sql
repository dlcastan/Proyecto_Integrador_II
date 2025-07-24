{{ config(
    materialized='view',
    description='KPI: Valor total de ventas - Monto total facturado en órdenes completadas'
) }}

SELECT 
    'valor_total_ventas' AS kpi_nombre,
    SUM(Total) AS valor,
    'ARS' AS unidad,
    CURRENT_DATE AS fecha_calculo,
    'Monto total facturado en órdenes completadas' AS descripcion
FROM {{ ref('mart_ordenes_completadas') }}