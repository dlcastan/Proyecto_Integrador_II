{{ config(materialized='table') }}

SELECT
    DATE_TRUNC('month', o.FechaOrden) AS Mes,
    SUM(o.Total) AS TotalVentas
FROM {{ source('public', 'ordenes') }} o
GROUP BY 1
ORDER BY 1
