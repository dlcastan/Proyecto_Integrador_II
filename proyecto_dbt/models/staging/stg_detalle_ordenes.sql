-- models/staging/stg_detalle_ordenes.sql
{{ config(materialized='table') }}
WITH raw_detalle_ordenes AS (
    SELECT *
    FROM {{ source('public', 'detalleordenes') }}
)

SELECT
    DetalleID,
    OrdenID,
    ProductoID,
    Cantidad,
    PrecioUnitario
FROM raw_detalle_ordenes