# Questão 7.3 - Explicação do Modelo Baseline

### 1. Como o baseline foi construído?
O baseline foi construído seguindo um processo clássico de manipulação de séries temporais:
1. **Isolamento do Produto:** Buscamos o ID numérico correspondente ao "Motor de Popa Yamaha Evo Dash 155HP" na base de produtos e filtramos o histórico de vendas apenas para ele.
2. **Agregação Diária:** Somamos a quantidade vendida do produto por dia (`GROUP BY sale_date`).
3. **Preenchimento de Lacunas (Resampling):** Criamos um calendário contínuo cobrindo desde a primeira venda até o final do período de teste (31/01/2024). Inserimos o valor `0` para os dias em que a loja operou, mas não vendeu o motor. Isso é fundamental, pois modelos temporais exigem espaçamento constante.
4. **Cálculo da Média Móvel:** Calculamos a média matemática das vendas realizadas na janela dos últimos 7 dias.

### 2. Como evitou *data leakage* (vazamento de dados)?
Na previsão de séries temporais, *data leakage* ocorre quando você acidentalmente usa informações do "futuro" para prever um dado momento. 

No código Pandas, isso foi evitado utilizando o método **`.shift(1)`** imediatamente antes do `.rolling(window=7).mean()`. 
* Sem o `shift(1)`, a média móvel de 7 dias para a data de *hoje* (dia `D`) incluiria as vendas do próprio dia de *hoje* (`D` até `D-6`). Isso passaria a "resposta da prova" para o modelo.
* Com o `shift(1)`, nós "empurramos" a série um dia para baixo. Assim, a previsão para o dia de *hoje* (`D`) olha estritamente e exclusivamente para o que aconteceu de **ontem para trás** (`D-1` até `D-7`), respeitando perfeitamente a linha do tempo do mundo real.

### 3. Uma limitação do modelo proposto.
A Média Móvel de curto prazo (7 dias) tem **"memória curta"** e é puramente reativa, o que a torna incapaz de antecipar **Sazonalidades** ou **Tendências** de longo prazo.

No enunciado da questão, é mencionado que no "verão" o estoque acabou. O modelo de Média Móvel de 7 dias não sabe o que é o "verão" nem se lembra do que ocorreu no ano anterior. Ele só vai começar a prever vendas mais altas depois que a explosão de vendas já tiver começado e inflado os 7 dias imediatamente anteriores, falhando totalmente em ajudar o departamento de compras a se preparar com antecedência.

Além disso, a Média Móvel lida muito mal com **demanda intermitente**. Como motores de popa de alto valor geralmente não vendem todos os dias (muitos zeros seguidos), quando ocorre uma venda isolada, o modelo "espalha" o pico de forma fracionada nos 7 dias seguintes (prevendo coisas como 0.14 motores por dia), o que não é prático para a gestão de estoque do mundo real.