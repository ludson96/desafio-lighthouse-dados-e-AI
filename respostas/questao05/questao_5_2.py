import pandas as pd
from pathlib import Path

def clean_category(cat):
    """Padroniza a categoria com as mesmas regras do SQL"""
    cat_upper = str(cat).upper().replace(' ', '')
    if cat_upper.startswith('ELETR'):
        return 'ELETRONICOS'
    elif cat_upper.startswith('PROP'):
        return 'PROPULSAO'
    elif 'NCOR' in cat_upper:
        return 'ANCORAGEM'
    else:
        return 'OUTROS'

def validar_questao_5():
    # Resolve o caminho de forma relativa ao local do script
    BASE_DIR = Path(__file__).resolve().parents[2]
    
    produtos_path = BASE_DIR / "data" / "raw" / "produtos_raw.csv"
    vendas_path = BASE_DIR / "data" / "raw" / "vendas_2023_2024.csv"
    
    df_produtos = pd.read_csv(produtos_path)
    df_vendas = pd.read_csv(vendas_path)
    
    # 1. Limpeza das categorias
    df_produtos['categoria_consolidada'] = df_produtos['actual_category'].apply(clean_category)
    
    # 2. Junção dos dados (trazendo a categoria limpa para as vendas)
    df_merged = df_vendas.merge(
        df_produtos[['code', 'categoria_consolidada']], 
        left_on='id_product', 
        right_on='code', 
        how='inner'
    )
    
    # 3. Métricas por cliente
    metricas = df_merged.groupby('id_client').agg(
        faturamento_total=('total', 'sum'),
        frequencia=('id', 'count'),
        diversidade_categorias=('categoria_consolidada', 'nunique')
    ).reset_index()
    
    metricas['ticket_medio'] = metricas['faturamento_total'] / metricas['frequencia']
    
    # 4. Filtrar Elite (3+ categorias) e selecionar Top 10
    elite = metricas[metricas['diversidade_categorias'] >= 3]
    top_10 = elite.sort_values(by=['ticket_medio', 'id_client'], ascending=[False, True]).head(10)
    top_10_ids = top_10['id_client'].tolist()
    
    # 5. Filtrar histórico desses 10 clientes e agregar
    vendas_elite = df_merged[df_merged['id_client'].isin(top_10_ids)]
    vendas_por_categoria = vendas_elite.groupby('categoria_consolidada')['qtd'].sum().reset_index()
    categoria_top = vendas_por_categoria.sort_values(by='qtd', ascending=False).iloc[0]
    
    # 6. Exibição de resultados
    print("--- Top 10 Clientes (Fiéis) ---")
    print(top_10[['id_client', 'ticket_medio', 'diversidade_categorias']].to_string(index=False))
    
    print("\n--- Vendas por Categoria (Apenas Top 10 Clientes) ---")
    print(vendas_por_categoria.sort_values(by='qtd', ascending=False).to_string(index=False))
    
    print(f"\n=> A categoria de produtos mais vendida para eles foi: {categoria_top['categoria_consolidada']} com {categoria_top['qtd']} itens comprados.")

if __name__ == "__main__":
    validar_questao_5()