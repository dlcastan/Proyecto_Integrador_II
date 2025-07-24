-- Calculo los KPIS definidos para controlar y optimizar el rendimiento del ecommerce.

-- 1. Valor total de ventas

SELECT 
    SUM(Total) AS valor_total_ventas
FROM 
    Ordenes
WHERE 
    Estado = 'Completado';

--  2. Ticket promedio

SELECT 
    AVG(Total) AS ticket_promedio
FROM 
    Ordenes
WHERE 
    Estado = 'Completado';


-- 3. Índice de satisfacción de productos

SELECT 
    AVG(Calificacion) AS promedio_calificaciones
FROM 
    ReseñasProductos;

--  4. Recompra de clientes

WITH ordenes_por_usuario AS (
    SELECT UsuarioID, COUNT(*) AS cantidad_ordenes
    FROM Ordenes
    GROUP BY UsuarioID
),
usuarios_con_1_orden AS (
    SELECT COUNT(*) AS total
    FROM ordenes_por_usuario
),
usuarios_con_mas_de_una AS (
    SELECT COUNT(*) AS con_recompra
    FROM ordenes_por_usuario
    WHERE cantidad_ordenes > 1
)

SELECT 
    ROUND(100.0 * con_recompra / total, 2) AS porcentaje_recompra
FROM 
    usuarios_con_mas_de_una, usuarios_con_1_orden;