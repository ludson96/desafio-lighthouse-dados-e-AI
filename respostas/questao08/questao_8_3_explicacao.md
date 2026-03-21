# Questão 8.3 - Explicação do Motor de Recomendação

### 1. Como a matriz foi construída?
A matriz de interação foi construída utilizando a técnica de pivotamento de dados (através do método `pivot_table` do Pandas) sobre o histórico limpo de vendas. 
* **Estrutura Base:** Os clientes (`id_client`) foram dispostos como linhas e os itens (`id_product`) como colunas.
* **Binarização (0 e 1):** Como a regra pedia para ignorar a quantidade comprada, criei uma coluna temporária com o valor `1` e utilizei a função de agregação `max`. Assim, se o cliente comprou o produto várias vezes em datas diferentes, o valor se mantém `1`.
* **Preenchimento:** Para as cruzes da matriz onde não houve compra, preenchemos os valores vazios com `0` (`fill_value=0`), resultando em uma matriz binária e esparsa.
* **Transposição:** Para realizar a Filtragem Colaborativa Baseada em Itens (*Item-Based Collaborative Filtering*), a matriz foi transposta (`.T`). Assim, ela passou a ter o formato **Produto × Usuário**, preparando o terreno para compararmos os produtos entre si.

---

### 2. O que significa a Similaridade de Cosseno nesse contexto?
Neste contexto, podemos imaginar que cada Produto é um "vetor" em um espaço multidimensional, onde cada dimensão é um cliente diferente.

A Similaridade de Cosseno mede o ângulo matemático entre dois produtos nesse espaço. 
* Se dois itens (como um GPS e uma Sonda) são comprados frequentemente em conjunto pelos mesmos clientes, seus vetores apontarão para a mesma direção (ângulo próximo a zero) e a similaridade resultante será muito próxima de **`1.0`**. 
* Se eles nunca dividem o mesmo carrinho ou o mesmo cliente, o ângulo será de 90º e a similaridade será **`0.0`**. 

Em resumo, a métrica traduz a "coocorrência" em um score matemático de proximidade de comportamento de consumo.

---

### 3. Uma limitação desse método de recomendação
A principal limitação desse método é o problema conhecido como **Cold Start (Arranque Frio)** aliado à **Esparsidade**.
* **Cold Start:** Como a matemática do cosseno depende inteiramente do histórico de quem já comprou, o sistema é incapaz de recomendar **produtos novos** que acabaram de ser lançados no catálogo da Marina, pois eles não possuem histórico vetorial. O mesmo ocorre para novos clientes que não têm compras passadas registradas.
* **Ignora a temporalidade/sequência:** O algoritmo apenas olha se o Cliente A comprou o Produto X e Y na vida. Ele não compreende a ordem lógica (ex: o fato de que a pessoa geralmente compra a Lancha *antes* de precisar da Defensa).