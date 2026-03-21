# Questão 5.3 - Explicação da Lógica

### 1. Como você realizou a limpeza das categorias?
A limpeza foi baseada na padronização de texto e busca por padrões fonéticos/escritos (substrings). O processo seguiu estas etapas:
- **Normalização preliminar:** Primeiro, removi todos os espaços em branco no meio das palavras e converti os textos inteiros para letras maiúsculas (no SQL usando `UPPER(REPLACE(coluna, ' ', ''))` e no Python com `.upper().replace(' ', '')`). Isso neutralizou erros como "E L E T R Ô N I C O S" ou "eLeTrÔnIcOs".
- **Regras de Associação Categórica:** Em vez de tentar mapear todas as variações incorretas uma a uma, busquei a raiz das palavras:
  - Tudo que iniciava com o radical `"ELETR"` virou **"ELETRONICOS"** (corrigindo "Eletrunicos", "Eletronicoz", etc).
  - Tudo que iniciava com o radical `"PROP"` virou **"PROPULSAO"** (corrigindo "Propulção", "Propulssão", etc).
  - Tudo que continha o miolo `"NCOR"` virou **"ANCORAGEM"** (isso foi crucial para capturar tanto as variáveis que começam com 'A' como "Ancorajen" e "Ancoraguem", quanto as que começavam com 'E', como "Encoragem").
  - Qualquer outro valor residual cairia em um grupo genérico ("OUTROS").

### 2. Qual lógica utilizou para filtrar os clientes com diversidade mínima?
Após juntar o histórico de vendas com a base de categorias padronizadas, realizei um agrupamento (`GROUP BY`) focado no identificador do cliente (`id_client`). 

Dentro desse agrupamento, além de somar o faturamento e contar a frequência, apliquei uma **contagem distinta de categorias** que apareceram no histórico do cliente. 
- No SQL: utilizei a função agregadora `COUNT(DISTINCT categoria_consolidada)`. 
- No Python (Pandas): utilizei a função agregadora `.nunique()`. 

Isso gerou uma coluna numérica para cada cliente representando quantas categorias diferentes ele experimentou. A lógica final foi simplesmente isolar essa métrica por meio de um filtro clássico (cláusula `WHERE` no SQL ou filtro booleano no Python), exigindo que a "diversidade_categorias" fosse `>= 3`.

### 3. Como garantiu que a contagem de itens refletisse apenas os Top 10?
O processo exigiu isolar os 10 clientes ("Fiéis") do resto da base antes da agregação final. Fizemos isso em duas etapas:

1. **Criação da Lista VIP:** Peguei os clientes já filtrados pela diversidade, calculei o Ticket Médio (Total Gasto / Frequência) e os ordenei do maior para o menor. Utilizei o ID em ordem crescente para critério de desempate e cortei a lista no décimo registro (`LIMIT 10` no SQL e `.head(10)` no Pandas).
2. **Garantia de Unicidade dos Produtos:** Antes de calcular os volumes, garanti que o catálogo de produtos possuísse apenas IDs únicos. Se fizéssemos a junção (`Merge`/`JOIN`) com produtos duplicados no catálogo, ocorrerá uma "explosão cartesiana", multiplicando transações e inflando a contagem de itens de forma irreal.
3. **Filtro Estrito no Dataset Principal:** Com essa pequena "lista" contendo apenas os 10 IDs VIPs em mãos, voltei ao dataset bruto de vendas e fiz uma triagem. 
   - No SQL, isso se deu através de um `INNER JOIN` entre as transações de venda e a tabela virtual (`CTE`) dos clientes de elite. 
   
Essa operação atua como um funil: qualquer venda registrada que não pertencesse a um dos 10 IDs da lista VIP era imediatamente descartada. Só com os dados perfeitamente isolados e deduplicados para esse grupo é que agrupei novamente pela categoria do produto e realizei a soma da quantidade comprada (`SUM(qtd)`).