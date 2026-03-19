-- 1. Limpeza das categorias
WITH categorias_limpas AS (
    SELECT
        code AS id_product,
        CASE
            WHEN UPPER(REPLACE(actual_category, ' ', '')) LIKE 'ELETR%' THEN 'ELETRONICOS'
            WHEN UPPER(REPLACE(actual_category, ' ', '')) LIKE 'PROP%' THEN 'PROPULSAO'
            WHEN UPPER(REPLACE(actual_category, ' ', '')) LIKE '%NCOR%' THEN 'ANCORAGEM'
            ELSE 'OUTROS'
        END AS categoria_consolidada
    FROM produtos_raw
),

-- 2. Cálculo do Ticket Médio e Diversidade por cliente
metricas_clientes AS (
    SELECT
        v.id_client,
        SUM(v.total) AS faturamento_total,
        COUNT(v.id) AS frequencia,
        SUM(v.total) / COUNT(v.id) AS ticket_medio,
        COUNT(DISTINCT c.categoria_consolidada) AS diversidade_categorias
    FROM vendas_2023_2024 v
    JOIN categorias_limpas c ON v.id_product = c.id_product
    GROUP BY v.id_client
),

-- 3. Identificação e filtro dos 10 clientes "Fiéis"
clientes_elite AS (
    SELECT
        id_client,
        ticket_medio,
        diversidade_categorias
    FROM metricas_clientes
    WHERE diversidade_categorias >= 3
    ORDER BY ticket_medio DESC, id_client ASC
    LIMIT 10
)

-- 4. A categoria mais vendida considerando o grupo de 10 clientes
SELECT
    c.categoria_consolidada,
    SUM(v.qtd) AS quantidade_total
FROM vendas_2023_2024 v
JOIN categorias_limpas c ON v.id_product = c.id_product
JOIN clientes_elite e ON v.id_client = e.id_client
GROUP BY c.categoria_consolidada
ORDER BY quantidade_total DESC
LIMIT 1;