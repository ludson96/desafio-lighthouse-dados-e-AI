# Questão 6.3 - Explicação sobre a Dimensão de Datas

### 1. Por que é necessário utilizar uma tabela de datas (calendário) em vez de agrupar diretamente a tabela de vendas?

Agrupar diretamente a tabela de vendas (`GROUP BY sale_date`) faz com que o banco de dados enxergue **apenas os dias em que houve faturamento**. Dias em que a loja esteve aberta, mas não vendeu absolutamente nada (faturamento = 0), simplesmente não geram registros no arquivo CSV (`vendas_2023_2024.csv`).

Se utilizarmos apenas a tabela de vendas, esses dias "vazios" ficam invisíveis para o motor do banco de dados e são totalmente ignorados nos cálculos. 

A utilização de uma tabela de datas (Calendário) atua como uma "espinha dorsal" temporal contínua e sem buracos. Ao fazermos um `LEFT JOIN` do Calendário com a tabela de Vendas, nós "forçamos" o banco de dados a listar todos os dias do ano. Para os dias em que não houver correspondência na tabela de vendas, o banco gerará um valor nulo (`NULL`), que nós explicitamente convertemos para `0` (usando `COALESCE` no SQL ou `.fillna(0)` no Pandas).

---

### 2. O que aconteceria com a média de vendas se um dia da semana tivesse muitos dias sem nenhuma venda registrada?

Se não usássemos o calendário, a média desse dia da semana seria **artificialmente inflada e geraria uma falsa sensação de sucesso**.

A fórmula matemática da média simples é: `Soma Total / Quantidade de Dias`.

**Exemplo prático:**
Imagine que ao longo de 1 ano (52 domingos), a loja do Sr. Almir vendeu apenas em 2 domingos, faturando R$ 5.000,00 em cada um deles, e não vendeu nada nos outros 50 domingos.
* **Cálculo Errado (Sem calendário):** O estagiário agrupa a tabela de vendas. O banco enxerga apenas 2 domingos. A conta feita é: `R$ 10.000 / 2 = R$ 5.000 de média`. O Sr. Almir acha que o domingo é um dia excelente.
* **Cálculo Correto (Com calendário):** O banco enxerga todos os 52 domingos graças ao `LEFT JOIN`. A conta feita é: `R$ 10.000 / 52 = R$ 192,30 de média`. A realidade é revelada e o Sr. Almir percebe que o Domingo é, de fato, o **pior dia da semana** e que abrir a loja nesse dia dá prejuízo.
