1. Como você realizou a limpeza das categorias?

A limpeza foi realizada diretamente no SQL através da normalização e padronização dos nomes das categorias presentes na tabela produtos_raw.

Primeiramente, foi aplicada uma normalização textual utilizando UPPER() para converter todos os caracteres para maiúsculas e REPLACE() para remover espaços internos, reduzindo inconsistências causadas por diferenças de formatação.

Após essa normalização, foi utilizado um CASE WHEN com padrões (LIKE) para consolidar variações de escrita em uma única categoria padronizada:

Valores iniciados por "ELETR" foram classificados como ELETRONICOS
Valores iniciados por "PROP" foram classificados como PROPULSAO
Valores contendo "NCOR" foram classificados como ANCORAGEM

Qualquer categoria que não atendesse a esses padrões foi classificada como OUTROS, evitando perda de registros.

2. Qual lógica utilizou para filtrar os clientes com diversidade mínima?

Após a padronização das categorias, foi realizada uma junção entre a tabela de vendas (vendas_2023_2024) e a tabela de categorias limpas.

Em seguida, os dados foram agregados por cliente (GROUP BY id_client) para calcular as métricas exigidas:

Faturamento Total: SUM(total)
Frequência de compra: COUNT(id)
Ticket Médio: SUM(total) / COUNT(id)
Diversidade de Categorias: COUNT(DISTINCT categoria_consolidada)

A diversidade foi calculada utilizando COUNT(DISTINCT ...), garantindo que apenas categorias diferentes fossem consideradas.

Por fim, foi aplicado um filtro para selecionar apenas clientes que compraram em três ou mais categorias distintas, utilizando a condição:

diversidade_categorias >= 3
3. Como garantiu que a contagem de itens refletisse apenas os Top 10?

Após o cálculo das métricas por cliente, foi criada uma CTE chamada clientes_elite, responsável por armazenar os 10 clientes com maior Ticket Médio, respeitando também o critério de desempate por id_client em ordem crescente.

Esse ranking foi obtido através da ordenação:

ticket_medio DESC
id_client ASC

seguido da limitação do resultado com LIMIT 10.

Na etapa final, as vendas foram filtradas utilizando um INNER JOIN entre a tabela de vendas e a CTE clientes_elite. Dessa forma, apenas as transações pertencentes aos clientes do Top 10 foram consideradas na agregação final.

Com os dados já restritos a esse grupo, foi realizada a soma da quantidade de itens vendidos (SUM(qtd)) por categoria, permitindo identificar qual categoria concentrou o maior volume de produtos adquiridos pelos clientes de elite.