import sqlite3
import pandas as pd
from pathlib import Path

def validate_highest_relative_loss():
    # Definindo a raiz do projeto
    BASE_DIR = Path(__file__).resolve().parents[2]
    
    # Caminhos dos arquivos
    sales_path = BASE_DIR / "data" / "raw" / "vendas_2023_2024.csv"
    costs_path = BASE_DIR / "data" / "raw" / "custos_importacao.csv"
    rates_path = BASE_DIR / "data" / "raw" / "cotacoes_bcb.csv"
    sql_path = BASE_DIR / "respostas" / "questao04" / "analise_prejuizos.sql"
    
    # Carregando datasets
    df_sales = pd.read_csv(sales_path)
    df_costs = pd.read_csv(costs_path)
    df_rates = pd.read_csv(rates_path)
    
    # Tratamento de data exigido pela premissa do SQL
    df_sales['sale_date'] = pd.to_datetime(df_sales['sale_date'], format='mixed', dayfirst=True).dt.strftime('%Y-%m-%d')
    
    # Inicializando banco de dados em memória
    conn = sqlite3.connect(':memory:')
    df_sales.to_sql('vendas_2023_2024', conn, index=False)
    df_costs.to_sql('custos_importacao', conn, index=False)
    df_rates.to_sql('cotacoes_bcb', conn, index=False)
    
    # Lendo e executando o arquivo SQL
    with open(sql_path, 'r', encoding='utf-8') as file:
        query = file.read()
        
    df_result = pd.read_sql_query(query, conn)
    conn.close()
    
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