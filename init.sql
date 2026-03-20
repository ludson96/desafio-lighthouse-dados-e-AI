-- Configura o estilo de data do Postgres para aceitar o formato misto do CSV (DD-MM-YYYY e YYYY-MM-DD)
SET DateStyle = 'ISO, DMY';

-- Cria a tabela de vendas
CREATE TABLE IF NOT EXISTS vendas_2023_2024 (
    id INT,
    id_client INT,
    id_product INT,
    qtd INT,
    total NUMERIC,
    sale_date DATE
);

-- Copia os dados de vendas
COPY vendas_2023_2024(id, id_client, id_product, qtd, total, sale_date)
FROM PROGRAM 'grep "[0-9a-zA-Z]" /tmp/vendas_2023_2024.csv'
DELIMITER ','
CSV HEADER;

-- Cria a tabela de produtos (a coluna price entra como texto devido ao "R$ ")
CREATE TABLE IF NOT EXISTS produtos_raw (
    name TEXT,
    price TEXT,
    code INT,
    actual_category TEXT
);

-- Copia os dados de produtos
COPY produtos_raw(name, price, code, actual_category)
FROM '/tmp/produtos_raw.csv'
DELIMITER ','
CSV HEADER;
