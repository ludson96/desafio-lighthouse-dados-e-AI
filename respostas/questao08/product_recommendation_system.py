"""
Questão 8.1 - Motor de Recomendação
Cenário: Identificar produtos recomendados para acompanhar o item 
"GPS Garmin Vortex Maré Drift" baseado no histórico de compras dos clientes.
"""

import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from pathlib import Path

def recomendacao_produtos():
    # Definindo os caminhos para os arquivos do projeto
    BASE_DIR = Path(__file__).resolve().parents[2]
    
    vendas_path = BASE_DIR / "data" / "raw" / "vendas_2023_2024.csv"
    produtos_path = BASE_DIR / "data" / "raw" / "produtos_raw.csv"
    clientes_path = BASE_DIR / "data" / "raw" / "clientes_crm.json"
    
    print("1. Carregando os dados brutos...")
    df_vendas = pd.read_csv(vendas_path)
    df_produtos = pd.read_csv(produtos_path)
    df_clientes = pd.read_json(clientes_path)
    
    # -------------------------------------------------------------
    # 1. Limpeza e Filtros Iniciais
    # -------------------------------------------------------------
    # Garantir que estamos utilizando apenas vendas de clientes válidos no CRM
    clientes_validos = df_clientes['code'].unique()
    df_vendas = df_vendas[df_vendas['id_client'].isin(clientes_validos)].copy()
    
    # Remover registros que não tenham produto ou cliente identificados
    df_vendas = df_vendas.dropna(subset=['id_client', 'id_product'])
    
    print("2. Construindo a Matriz de Interação (Usuário x Produto)...")
    
    # Criar uma coluna binária indicando que a compra existiu (ignora a quantidade)
    df_vendas['comprou'] = 1
    
    # Pivotar a tabela: Linhas = id_client, Colunas = id_product
    # aggfunc='max' garante que, se o cliente comprou o produto várias vezes, o valor continue 1
    matriz_interacao = df_vendas.pivot_table(
        index='id_client', 
        columns='id_product', 
        values='comprou', 
        aggfunc='max', 
        fill_value=0
    )
    
    print("3. Calculando a Similaridade de Cosseno (Produto x Produto)...")
    
    # Transpor a matriz para que as linhas sejam Produtos e as colunas sejam Usuários
    matriz_produto_usuario = matriz_interacao.T
    
    # Calcular a similaridade de cosseno
    sim_matrix = cosine_similarity(matriz_produto_usuario)
    
    # Transformar a matriz de similaridade em um DataFrame para facilitar a busca
    df_similaridade = pd.DataFrame(
        sim_matrix, 
        index=matriz_produto_usuario.index, 
        columns=matriz_produto_usuario.index
    )
    
    print("4. Gerando Ranking de Recomendações...\n")
    
    # Definir o produto de referência
    produto_alvo = "GPS Garmin Vortex Maré Drift"
    
    # Encontrar o ID correspondente ao produto na base de catálogo
    id_alvo = df_produtos.loc[df_produtos['name'] == produto_alvo, 'code'].values
    
    if len(id_alvo) == 0:
        print(f"ERRO: Produto '{produto_alvo}' não encontrado no catálogo.")
        return
        
    id_alvo = id_alvo[0]
    
    # Extrair os scores de similaridade do produto alvo com todos os outros
    similaridades_alvo = df_similaridade[id_alvo]
    
    # Remover o próprio produto alvo da recomendação e ordenar as similaridades do maior para o menor
    similaridades_alvo = similaridades_alvo.drop(id_alvo).sort_values(ascending=False)
    
    # Selecionar os top 5 produtos mais similares
    top_5 = similaridades_alvo.head(5)
    
    print(f"="*60)
    print(f"TOP 5 RECOMENDAÇÕES PARA: {produto_alvo}")
    print(f"="*60)
    
    for rank, (prod_id, score) in enumerate(top_5.items(), start=1):
        nome_prod = df_produtos.loc[df_produtos['code'] == prod_id, 'name'].values[0]
        print(f"{rank}. {nome_prod} (ID: {prod_id})")
        print(f"   Score de Similaridade: {score:.4f}\n")

if __name__ == "__main__":
    recomendacao_produtos()