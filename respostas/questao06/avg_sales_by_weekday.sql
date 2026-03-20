-- Questão 6.1 - Análise de pior média de vendas por dia da semana

WITH RECURSIVE Limites_Data AS (
    -- 1. Descobre a menor e a maior data de venda registradas na tabela
    SELECT 
        MIN(sale_date::DATE) AS data_min,
        MAX(sale_date::DATE) AS data_max
    FROM vendas_2023_2024
),
Calendario AS (
    -- 2. Constrói o Calendário contínuo (Dimensão de Datas) usando recursividade
    SELECT data_min AS data_ref
    FROM Limites_Data
    
    UNION ALL
    
    SELECT (data_ref + INTERVAL '1 day')::DATE
    FROM Calendario
    WHERE data_ref < (SELECT data_max FROM Limites_Data)
),
Calendario_Dias_Semana AS (
    -- 3. Mapeia o dia da semana para o idioma Português
    SELECT 
        data_ref,
        EXTRACT(ISODOW FROM data_ref) AS id_dia_semana, -- 1 = Segunda, 7 = Domingo (ISO 8601)
        CASE EXTRACT(ISODOW FROM data_ref)
            WHEN 1 THEN 'Segunda-feira'
            WHEN 2 THEN 'Terça-feira'
            WHEN 3 THEN 'Quarta-feira'
            WHEN 4 THEN 'Quinta-feira'
            WHEN 5 THEN 'Sexta-feira'
            WHEN 6 THEN 'Sábado'
            WHEN 7 THEN 'Domingo'
        END AS nome_dia_semana
    FROM Calendario
),
Vendas_Diarias AS (
    -- 4. LEFT JOIN: Cruza o calendário com as vendas
    -- Isso garante que os dias sem vendas (NULL) sejam preenchidos com 0 através do COALESCE
    SELECT 
        c.data_ref,
        c.nome_dia_semana,
        c.id_dia_semana,
        COALESCE(SUM(v.total), 0) AS valor_venda_diaria
    FROM Calendario_Dias_Semana c
    LEFT JOIN vendas_2023_2024 v 
        ON c.data_ref = v.sale_date::DATE
    GROUP BY 
        c.data_ref,
        c.nome_dia_semana,
        c.id_dia_semana
)
-- 5. Agregação Final: Média de vendas por dia da semana
SELECT 
    nome_dia_semana,
    ROUND(AVG(valor_venda_diaria)::NUMERIC, 2) AS media_vendas
FROM Vendas_Diarias
GROUP BY 
    nome_dia_semana,
    id_dia_semana
ORDER BY 
    media_vendas ASC; -- Ordena do pior para o melhor dia
