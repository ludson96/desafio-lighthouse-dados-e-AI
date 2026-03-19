-- Questão 4.1 - Código SQL (Análise de Prejuízos Reais)

-- NOTA ARQUITETURAL SOBRE A COTAÇÃO DO BCB:
-- Como a linguagem SQL não realiza requisições HTTP nativas para APIs externas (Banco Central),
-- é uma premissa obrigatória de arquitetura de dados que essa informação seja previamente extraída
-- (ex: via script Python) e carregada no banco de dados. 
-- Portanto, este script assume a existência da tabela `cotacoes_bcb` (data, taxa_cambio) como 
-- resultado dessa etapa de ingestão (Pipeline ELT). Também assume-se que a coluna `sale_date`
-- foi previamente padronizada para o tipo DATE.

WITH Vendas_Com_Custo AS (
    -- Passo 1: Encontrar o custo (usd_price) mais recente em relação à data da venda
    SELECT 
        v.id AS id_venda,
        v.id_product,
        v.qtd,
        v.total,
        v.sale_date,
        c.product_name,
        c.usd_price,
        ROW_NUMBER() OVER(
            PARTITION BY v.id 
            ORDER BY c.start_date DESC
        ) AS rn_custo
    FROM vendas_2023_2024 v
    LEFT JOIN custos_importacao c 
        ON v.id_product = c.product_id 
        AND c.start_date <= v.sale_date
),
Vendas_Com_Cotacao AS (
    -- Passo 2: Encontrar a taxa de câmbio mais recente em relação à data da venda (cobrindo finais de semana)
    SELECT 
        vc.id_venda,
        vc.id_product,
        vc.product_name,
        vc.qtd,
        vc.total,
        vc.sale_date,
        vc.usd_price,
        cb.taxa_cambio,
        ROW_NUMBER() OVER(
            PARTITION BY vc.id_venda 
            ORDER BY cb.data DESC
        ) AS rn_cotacao
    FROM Vendas_Com_Custo vc
    LEFT JOIN cotacoes_bcb cb 
        ON cb.data <= vc.sale_date
    WHERE vc.rn_custo = 1 -- Filtra apenas o último custo válido de importação
),
Calculo_Prejuizo AS (
    -- Passo 3: Calcular custo em reais e identificar as perdas (apenas transações onde Custo > Receita)
    SELECT 
        id_product,
        product_name,
        total AS receita_venda,
        (qtd * usd_price * taxa_cambio) AS custo_total_brl,
        CASE 
            WHEN (qtd * usd_price * taxa_cambio) > total THEN (qtd * usd_price * taxa_cambio) - total 
            ELSE 0 
        END AS prejuizo_transacao
    FROM Vendas_Com_Cotacao
    WHERE rn_cotacao = 1 -- Filtra apenas a última taxa de câmbio válida
)
-- Passo 4: Agregação por id_produto conforme os requisitos (Foco: Maior prejuízo absoluto)
SELECT 
    id_product,
    SUM(receita_venda) AS receita_total,
    SUM(prejuizo_transacao) AS prejuizo_total,
    (SUM(prejuizo_transacao) / NULLIF(SUM(receita_venda), 0)) AS percentual_perda
FROM Calculo_Prejuizo
GROUP BY 
    id_product
ORDER BY 
    prejuizo_total DESC;


-- ====================================================================================
-- Questão 4.2 - Validação (Maior porcentagem de perda financeira relativa)
-- ====================================================================================

SELECT 
    id_product,
    SUM(receita_venda) AS receita_total,
    SUM(prejuizo_transacao) AS prejuizo_total,
    (SUM(prejuizo_transacao) / NULLIF(SUM(receita_venda), 0)) AS percentual_perda
FROM Calculo_Prejuizo
GROUP BY 
    id_product
ORDER BY 
    percentual_perda DESC
LIMIT 1;