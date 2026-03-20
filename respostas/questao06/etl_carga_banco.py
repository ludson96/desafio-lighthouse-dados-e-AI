import pandas as pd
from sqlalchemy import create_engine
from pathlib import Path

def padronizar_categoria(categoria):
    """Limpa e padroniza as categorias de produtos."""
    cat_limpa = str(categoria).lower().replace(" ", "")
    if cat_limpa.startswith('ele'): return 'eletrônicos'
    elif cat_limpa.startswith('prop'): return 'propulsão'
    elif cat_limpa.startswith('anc') or cat_limpa.startswith('enc'): return 'ancoragem'
    return categoria

def run_etl():
    # Volta 2 níveis para sair de 'respostas/questao06' e chegar na raiz do projeto
    BASE_DIR = Path(__file__).resolve().parents[2]
    vendas_path = BASE_DIR / "data" / "raw" / "vendas_2023_2024.csv"
    produtos_path = BASE_DIR / "data" / "raw" / "produtos_raw.csv"

    print("1. Extraindo e limpando dados de Vendas...")
    df_vendas = pd.read_csv(vendas_path)
    # Remove as linhas vazias corrompidas do CSV (como aquela da linha 1539)
    df_vendas = df_vendas.dropna(subset=['id_client'])
    # Padroniza todas as datas para o formato ISO YYYY-MM-DD
    df_vendas['sale_date'] = pd.to_datetime(df_vendas['sale_date'], format='mixed', dayfirst=True).dt.strftime('%Y-%m-%d')

    print("2. Extraindo e limpando dados de Produtos...")
    df_produtos = pd.read_csv(produtos_path)
    df_produtos['actual_category'] = df_produtos['actual_category'].apply(padronizar_categoria)
    df_produtos['price'] = df_produtos['price'].astype(str).str.replace('R$', '', regex=False).str.strip().astype(float)
    df_produtos = df_produtos.drop_duplicates(ignore_index=True)

    print("3. Conectando ao PostgreSQL no Docker e enviando os dados...")
    # Cria a conexão com o banco de dados via SQLAlchemy
    engine = create_engine('postgresql://postgres:postgres@localhost:5433/source_db')
    
    # O parâmetro if_exists='replace' faz o Pandas criar as tabelas com a tipagem correta sozinho!
    df_vendas.to_sql('vendas_2023_2024', engine, if_exists='replace', index=False)
    df_produtos.to_sql('produtos_raw', engine, if_exists='replace', index=False)
    
    print("🎉 ETL concluído! Os dados estão limpos e prontos no banco.")

if __name__ == "__main__":
    run_etl()