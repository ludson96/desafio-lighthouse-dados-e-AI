import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

def gerar_grafico():
    BASE_DIR = Path(__file__).resolve().parents[2]
    
    # Caminhos dos arquivos
    vendas_path = BASE_DIR / "data" / "raw" / "vendas_2023_2024.csv"
    custos_path = BASE_DIR / "data" / "raw" / "custos_importacao.csv"
    cotacoes_path = BASE_DIR / "data" / "raw" / "cotacoes_bcb.csv"
    sql_path = BASE_DIR / "respostas" / "questao04" / "analise_prejuizos.sql"
    
    print("Carregando datasets...")
    df_vendas = pd.read_csv(vendas_path)
    df_custos = pd.read_csv(custos_path)
    df_cotacoes = pd.read_csv(cotacoes_path)
    
    # Tratamento de data exigido pela premissa do SQL (conforme comentado no seu .sql)
    df_vendas['sale_date'] = pd.to_datetime(df_vendas['sale_date'], format='mixed', dayfirst=True).dt.strftime('%Y-%m-%d')
    
    print("Executando a query SQL em memória...")
    conn = sqlite3.connect(':memory:')
    df_vendas.to_sql('vendas_2023_2024', conn, index=False)
    df_custos.to_sql('custos_importacao', conn, index=False)
    df_cotacoes.to_sql('cotacoes_bcb', conn, index=False)
    
    # Ler e executar o seu arquivo SQL
    with open(sql_path, 'r', encoding='utf-8') as f:
        query = f.read()
        
    df_resultado = pd.read_sql_query(query, conn)
    conn.close()
    
    # Filtrar apenas produtos que tiveram prejuízo (maior que zero)
    df_prejuizo = df_resultado[df_resultado['prejuizo_total'] > 0].copy()
    df_prejuizo['id_product'] = df_prejuizo['id_product'].astype(str) # Transformar em string para o eixo Y ficar categórico
    
    print("Gerando o gráfico...")
    plt.figure(figsize=(10, 6))
    sns.barplot(
        data=df_prejuizo.sort_values('prejuizo_total', ascending=False), 
        x='prejuizo_total', 
        y='id_product', 
        palette='Reds_r'
    )
    
    plt.title('Prejuízo Total por Produto (BRL)', fontsize=14, pad=15)
    plt.xlabel('Prejuízo Total (R$)', fontsize=12)
    plt.ylabel('ID do Produto', fontsize=12)
    plt.tight_layout()
    
    plt.show()

if __name__ == "__main__":
    gerar_grafico()