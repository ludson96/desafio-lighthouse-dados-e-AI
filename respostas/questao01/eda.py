""" Questão 1 - EDA
Cenário

Antes de qualquer análise, modelagem ou tomada de decisão, é fundamental entender o que existe nos dados. O Sr. Almir quer uma resposta simples: “Posso confiar nesses dados para tomar decisões?”

Sua missão é realizar uma análise exploratória inicial do dataset vendas_2023_2024.csv e responder perguntas básicas, porém críticas, sobre volume, distribuição e qualidade dos dados.

Premissas obrigatórias
Utilize apenas o dataset vendas_2023_2024.csv
Não faça limpeza nem tratamento dos dados
Apenas observe, agregue e descreva

Tarefas: 
Parte 1 — Visão geral do dataset
Informe:
Quantidade total de linhas
Quantidade total de colunas
Intervalo de datas analisado (data mínima e máxima)
Parte 2 — Análise de valores numéricos
Para a coluna "total", calcule:
Valor mínimo
Valor máximo
Valor médio
Parte 3 — Interpretação
Responda de forma resumida:
Com base na análise exploratória realizada, escreva um breve diagnóstico sobre a confiabilidade do dataset vendas_2023_2024.csv para análises futuras.
Comente sobre:
possíveis outliers em "total",
qualidade dos dados (valores nulos ou inconsistentes),
e se você considera que o dataset está pronto para análises ou se exigiria tratamento prévio. """

import pandas as pd

def realizar_eda():
    # Caminho do dataset fornecido
    caminho_csv = r"c:\Users\Ludso\Desktop\Arquivos do desafio final\vendas_2023_2024.csv"
    
    # Carregar o dataset sem aplicar nenhum tratamento
    df = pd.read_csv(caminho_csv)

    print("--- Parte 1: Visão geral do dataset ---")
    linhas, colunas = df.shape
    print(f"Quantidade total de linhas: {linhas}")
    print(f"Quantidade total de colunas: {colunas}")
    
    # Observação da data (conversão temporária apenas para viabilizar a extração do mínimo e máximo)
    # Nota-se que as datas possuem formatações mistas ('YYYY-MM-DD' e 'DD-MM-YYYY').
    datas_temporarias = pd.to_datetime(df['sale_date'], format='mixed', dayfirst=True)
    print(f"Intervalo de datas analisado: {datas_temporarias.min().date()} a {datas_temporarias.max().date()}")

    print("\n--- Parte 2: Análise de valores numéricos ('total') ---")
    print(f"Valor mínimo: {df['total'].min():.2f}")
    print(f"Valor máximo: {df['total'].max():.2f}")
    print(f"Valor médio: {df['total'].mean():.2f}")

    print("\n--- Parte 3: Interpretação ---")
    interpretacao = """Com base nesta análise exploratória inicial, o dataset NÃO está pronto para modelagens ou análises avançadas e exige tratamento prévio.

- Possíveis outliers em 'total': Existe uma variação extrema e atípica entre o valor mínimo e o máximo. Embora possa ser explicado por produtos com alto valor agregado e quantidades altas, é um forte indício de outliers (reais ou sistêmicos/erros de digitação) que devem ser investigados.
- Qualidade dos dados: A coluna 'sale_date' apresenta nítida inconsistência em sua formatação (padrões YYYY-MM-DD e DD-MM-YYYY convivendo na mesma coluna). A coluna 'id' possui "saltos" (a sequência quebra em vários momentos, como pular do 2 para o 4), o que pode indicar perda de informações ou deleção de registros em etapas anteriores.
- Conclusão: O dataset exige uma etapa de limpeza de dados (Data Cleaning). Precisamos padronizar as datas, verificar a natureza dos valores muito altos na coluna 'total' e tratar tais anomalias e inconsistências antes que o Sr. Almir tome qualquer decisão técnica ou de negócio baseada nestes números."""
    
    print(interpretacao)

if __name__ == "__main__":
    realizar_eda()
