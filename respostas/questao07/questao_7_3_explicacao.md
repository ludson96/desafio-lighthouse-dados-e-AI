# Questão 7.3 - Explicação da Previsão de Demanda

### 1. Como o baseline foi construído?
O baseline foi construído utilizando um modelo simples de **média móvel de 7 dias** aplicado à série temporal de vendas do produto.

O processo seguiu as seguintes etapas:

1. **Isolamento do Produto:** Foi identificado o ID correspondente ao produto *"Motor de Popa Yamaha Evo Dash 155HP"* na base de produtos e filtrado o histórico de vendas apenas para esse item.
2. **Agregação diária:** As vendas foram agregadas por data, somando a quantidade vendida em cada dia.
3. **Criação de calendário contínuo:** Foi criado um calendário diário contínuo desde o início do histórico de vendas geral da loja até 31/01/2024. Os dias sem venda do produto específico foram preenchidos com valor **0**, garantindo uma série temporal com espaçamento constante entre as observações.
4. **Cálculo da média móvel:** Para cada dia foi calculada a **média das vendas dos 7 dias anteriores**, gerando a previsão diária utilizada como baseline.

---

### 2. Como evitou *data leakage* (vazamento de dados)?
*Data leakage* ocorre quando informações do futuro são usadas para gerar previsões do passado ou do presente.

Para evitar esse problema, foi utilizado o método **`.shift(1)`** antes do cálculo da média móvel:

```python
.shift(1).rolling(window=7).mean()
```

O `shift(1)` desloca a série em um dia, garantindo que a previsão para o dia **D** utilize apenas informações dos dias **D-1 até D-7**.

Sem esse deslocamento, a média móvel incluiria o valor do próprio dia que está sendo previsto, o que significaria utilizar informação que ainda não estaria disponível no momento da previsão.

---

### 3. Uma limitação do modelo proposto

A média móvel é um modelo simples que considera apenas os valores mais recentes da série, sem capturar **tendências ou sazonalidades**.

No contexto do problema, o enunciado menciona aumento de vendas no **verão**, indicando um possível padrão sazonal. A média móvel de 7 dias não consegue antecipar esse tipo de comportamento, pois reage apenas às vendas recentes.

Além disso, o método pode gerar previsões fracionadas (ex.: 0.14 unidades por dia), o que não representa bem a realidade de produtos de alto valor vendidos de forma esporádica.