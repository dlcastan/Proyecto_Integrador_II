{{ config(
    materialized='view',
    description='KPI: Recompra clientes - Porcentaje de clientes que realizaron más de una compra'
) }}

WITH ordenes_por_usuario AS (
    SELECT 
        UsuarioID, 
        COUNT(*) AS cantidad_ordenes
    FROM {{ ref('mart_ordenes_completadas') }}
    GROUP BY UsuarioID
),

metricas_recompra AS (
    SELECT 
        COUNT(*) AS total_usuarios,
        COUNT(CASE WHEN cantidad_ordenes > 1 THEN 1 END) AS usuarios_recompra
    FROM ordenes_por_usuario
)

SELECT 
    'recompra_clientes' AS kpi_nombre,
    ROUND(100.0 * usuarios_recompra / NULLIF(total_usuarios, 0), 2) AS valor,
    'porcentaje' AS unidad,
    CURRENT_DATE AS fecha_calculo,
    'Porcentaje de clientes que realizaron más de una compra' AS descripcion
FROM metricas_recompra