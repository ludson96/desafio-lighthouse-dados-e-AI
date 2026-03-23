import pandas as pd
from pathlib import Path

def validate_highest_relative_loss():
    # Definindo a raiz do projeto
    BASE_DIR = Path(__file__).resolve().parents[2]
    
    # Caminhos dos arquivos
    sales_path = BASE_DIR / "data" / "raw" / "vendas_2023_2024.csv"
    costs_path = BASE_DIR / "data" / "raw" / "custos_importacao.csv"
    rates_path = BASE_DIR / "data" / "raw" / "cotacoes_bcb.csv"
    
    # Carregando datasets
    df_sales = pd.read_csv(sales_path)
    df_costs = pd.read_csv(costs_path)
    df_rates = pd.read_csv(rates_path)
    
    # 1. Transformar em datetime real (necessário para o merge temporal do Pandas)
    # Voltando ao modo correto (Padrão BR) para garantir o cálculo preciso (62.80%)
    df_sales['sale_date'] = pd.to_datetime(df_sales['sale_date'], format='mixed', dayfirst=True).dt.normalize()
    df_costs['start_date'] = pd.to_datetime(df_costs['start_date'], format='mixed', dayfirst=True).dt.normalize()
    df_rates['data'] = pd.to_datetime(df_rates['data'], format='mixed', dayfirst=True).dt.normalize()
    
    # 2. Ordenar pelas datas (exigência do merge_asof para séries temporais)
    df_sales = df_sales.sort_values('sale_date')
    df_costs = df_costs.sort_values('start_date')
    df_rates = df_rates.sort_values('data')
    
    # 3. Join de Custos (Pega o custo mais recente <= data da venda, correspondente ao id do produto)
    df_sales_costs = pd.merge_asof(
        df_sales, df_costs, 
        left_on='sale_date', right_on='start_date', 
        left_by='id_product', right_by='product_id', 
        direction='backward'
    )
    
    # 4. Join de Cotações (Pega a cotação mais recente <= data da venda)
    df_final = pd.merge_asof(
        df_sales_costs, df_rates, 
        left_on='sale_date', right_on='data', 
        direction='backward'
    )
    
    # 5. Cálculo do custo total e extração do prejuízo (com clip(lower=0) fazendo o papel do CASE WHEN)
    df_final['custo_total_brl'] = df_final['qtd'] * df_final['usd_price'] * df_final['taxa_cambio']
    df_final['prejuizo_transacao'] = (df_final['custo_total_brl'] - df_final['total']).clip(lower=0)
    
    # 6. Agregação do resultado
    df_result = df_final.groupby('id_product').agg(
        receita_total=('total', 'sum'),
        prejuizo_total=('prejuizo_transacao', 'sum')
    ).reset_index()
    
    df_result['percentual_perda'] = df_result['prejuizo_total'] / df_result['receita_total']

    # Encontrar a linha com a maior porcentagem de perda
    # A coluna 'percentual_perda' foi gerada pelo script SQL
    highest_loss_row = df_result.loc[df_result['percentual_perda'].idxmax()]
    
    product_id = int(highest_loss_row['id_product'])
    loss_percentage = highest_loss_row['percentual_perda'] * 100
    
    print("--- Questão 4.2 - Validação ---")
    print("Qual é o id_produto que apresentou a maior porcentagem de perda financeira relativa?")
    print(f"Resposta: O id_produto é {product_id}")
    print(f"Ele apresentou um prejuízo equivalente a {loss_percentage:.2f}% sobre a sua receita total.")

if __name__ == "__main__":
    validate_highest_relative_loss()