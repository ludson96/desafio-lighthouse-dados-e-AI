import pandas as pd
import json
from pathlib import Path

def processar_custos_importacao():
    # Definir os caminhos baseados na estrutura do projeto
    BASE_DIR = Path(__file__).resolve().parents[2]
    json_path = BASE_DIR / "data" / "raw" / "custos_importacao.json"
    csv_output_path = BASE_DIR / "data" / "raw" / "custos_importacao.csv"
    
    # Carregar o arquivo JSON
    with open(json_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        
    # Achatar (flatten) os dados aninhados da chave 'historic_data'
    df = pd.json_normalize(
        data,
        record_path=['historic_data'],
        meta=['product_id', 'product_name', 'category']
    )
    
    # Reordenar as colunas para o formato esperado
    df = df[['product_id', 'product_name', 'category', 'start_date', 'usd_price']]
    
    # Converter os tipos de dados conforme especificado
    df['product_id'] = df['product_id'].astype(int)
    df['product_name'] = df['product_name'].astype(str)
    df['category'] = df['category'].astype(str)
    # Converter start_date do padrão DD/MM/YYYY para date puro (YYYY-MM-DD)
    df['start_date'] = pd.to_datetime(df['start_date'], format='%d/%m/%Y').dt.date
    df['usd_price'] = df['usd_price'].astype(float)
    
    # Salvar em CSV sem o índice do Pandas
    df.to_csv(csv_output_path, index=False, encoding='utf-8-sig')
    print(f"--- Sucesso! Arquivo CSV gerado em: {csv_output_path} ---")

if __name__ == "__main__":
    processar_custos_importacao()