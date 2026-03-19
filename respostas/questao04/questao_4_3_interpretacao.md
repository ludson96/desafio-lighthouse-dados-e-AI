# Questão 4.3 - Interpretação

### 1. Qual data de câmbio você utilizou?
Utilizei a **data exata da venda**. Para contornar o problema de dias não úteis (finais de semana e feriados), nos quais o Banco Central não emite cotações, utilizei a cotação do **último dia útil imediatamente anterior** à data da transação. Isso foi garantido no SQL através de um `LEFT JOIN` com a cláusula analítica `ROW_NUMBER()`, ordenando as datas de câmbio de forma decrescente para selecionar a mais recente válida.

### 2. Como definiu o prejuízo?
O prejuízo foi definido exclusivamente pelas **transações onde o custo superou a receita**. 
Primeiro, calculei o custo total da transação em BRL aplicando a fórmula: `(quantidade_vendida * custo_unitario_usd * taxa_cambio_do_dia)`. 
Em seguida, utilizei uma condicional `CASE WHEN` para avaliar se esse Custo BRL era maior que a Receita da venda (coluna `total`). Caso verdadeiro, o prejuízo registrado foi a diferença exata (`Custo BRL - Receita BRL`). Transações lucrativas receberam valor `0`, garantindo que eventuais lucros não abatessem o somatório das perdas ("prejuízo_total") na etapa de agregação.

### 3. Alguma suposição relevante?
Sim, algumas suposições e tratamentos foram fundamentais para a modelagem:

* **Vigência dos Custos:** Como o catálogo de fornecedores possui datas de início (`start_date`), assumiu-se que o custo aplicável a uma venda é sempre o registro mais recente cuja `start_date` seja menor ou igual à data da venda.
* **Tratamento de Datas (Data Quality):** Assumiu-se a necessidade de um pré-processamento (ELT) das datas de venda. Como a coluna `sale_date` apresentava formatos mistos, ela foi padronizada em Python para o formato ISO 8601 (`YYYY-MM-DD`) antes da inserção no banco de dados, permitindo que os operadores lógicos de data do SQL funcionassem corretamente.
* **Isolamento de Variáveis:** Conforme a premissa de negócio estipulada no enunciado, impostos, taxas e custos logísticos (frete) não compuseram o preço de custo unitário, isolando assim o impacto estrito da variação cambial e do erro de precificação.