import pandas as pd
import requests
from pathlib import Path

def carregar_cotacoes_bcb(data_inicial, data_final):
    """Busca as cotações de venda do Dólar PTAX na API do Banco Central."""
    # Série 10813: Taxa de câmbio - Livre - Dólar americano (venda) - diário
    url = f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.10813/dados?formato=json&dataInicial={data_inicial}&dataFinal={data_final}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        df_cotacoes = pd.DataFrame(response.json())
        df_cotacoes['data'] = pd.to_datetime(df_cotacoes['data'], format='%d/%m/%Y')
        df_cotacoes['taxa_cambio'] = df_cotacoes['valor'].astype(float)
        return df_cotacoes[['data', 'taxa_cambio']].sort_values('data')
    except requests.exceptions.RequestException as e:
        print(f"Erro ao buscar cotações do BCB: {e}")
        raise

def gerar_tabela_cotacoes():
    BASE_DIR = Path(__file__).resolve().parents[2]
    vendas_path = BASE_DIR / "data" / "raw" / "vendas_2023_2024.csv"
    output_path = BASE_DIR / "data" / "raw" / "cotacoes_bcb.csv"

    # Carregar vendas para descobrir o intervalo de datas necessário
    df_vendas = pd.read_csv(vendas_path)
    df_vendas['sale_date'] = pd.to_datetime(df_vendas['sale_date'], format='mixed', dayfirst=True)
    
    # Começamos em 15/12/2022 para cobrir possíveis vendas nos primeiros dias de 2023
    min_date = "15/12/2022"
    max_date = df_vendas['sale_date'].max().strftime('%d/%m/%Y')
    
    print(f"Buscando cotações do BCB de {min_date} até {max_date}...")
    df_cotacoes = carregar_cotacoes_bcb(min_date, max_date)
    
    # Formatar a data para o padrão ISO (YYYY-MM-DD) adequado para bancos de dados (SQL)
    df_cotacoes['data'] = df_cotacoes['data'].dt.strftime('%Y-%m-%d')
    
    # Salvar para CSV
    df_cotacoes.to_csv(output_path, index=False)
    print(f"Tabela de cotações salva com sucesso em: {output_path}")

if __name__ == "__main__":
    gerar_tabela_cotacoes()