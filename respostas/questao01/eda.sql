-- Questão 1 - EDA (Versão SQL)
-- Cenário: Análise exploratória inicial do dataset vendas_2023_2024

-- ==========================================
-- Parte 1 — Visão geral do dataset
-- ==========================================

-- Quantidade total de linhas
SELECT COUNT(*) AS total_linhas 
FROM vendas_2023_2024;

-- Quantidade total de colunas 
-- (Nota: Consulta ao catálogo de esquemas, padrão em bancos como PostgreSQL, MySQL, SQL Server)
SELECT COUNT(*) AS total_colunas 
FROM information_schema.columns 
WHERE table_name = 'vendas_2023_2024';

-- Intervalo de datas analisado (data mínima e máxima)
-- Atenção: Como a coluna 'sale_date' possui formatações mistas (YYYY-MM-DD e DD-MM-YYYY)
-- gravadas como texto sem tratamento prévio, funções agregadas como MIN e MAX farão 
-- uma ordenação alfabética (lexicográfica), o que não reflete a cronologia real.
SELECT 
    MIN(sale_date) AS data_minima_bruta, 
    MAX(sale_date) AS data_maxima_bruta
FROM vendas_2023_2024;

-- ==========================================
-- Parte 2 — Análise de valores numéricos
-- ==========================================

-- Para a coluna "total", calcular Valor mínimo, Valor máximo e Valor médio
SELECT 
    ROUND(CAST(MIN(total) AS numeric), 2) AS valor_minimo,
    ROUND(CAST(MAX(total) AS numeric), 2) AS valor_maximo,
    ROUND(CAST(AVG(total) AS numeric), 2) AS valor_medio
FROM vendas_2023_2024;

-- ==========================================
-- Parte 3 — Interpretação
-- ==========================================

/*
Com base nesta análise exploratória inicial, o dataset NÃO está pronto para modelagens ou análises avançadas e exige tratamento prévio.

- Possíveis outliers em 'total': Existe uma variação extrema e atípica entre o valor mínimo e o máximo. Embora possa ser explicado por produtos com alto valor agregado e quantidades altas, é um forte indício de outliers (reais ou sistêmicos/erros de digitação) que devem ser investigados.
- Qualidade dos dados: A coluna 'sale_date' apresenta nítida inconsistência em sua formatação (padrões YYYY-MM-DD e DD-MM-YYYY convivendo na mesma coluna). A coluna 'id' possui "saltos" (a sequência quebra em vários momentos, como pular do 2 para o 4), o que pode indicar perda de informações ou deleção de registros em etapas anteriores.
- Conclusão: O dataset exige uma etapa de limpeza de dados (Data Cleaning). Precisamos padronizar as datas, verificar a natureza dos valores muito altos na coluna 'total' e tratar tais anomalias e inconsistências antes que o Sr. Almir tome qualquer decisão técnica ou de negócio baseada nestes números.
*/