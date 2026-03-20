import pandas as pd
from pathlib import Path

def confirmar_pior_dia():
    # 1. Carrega os dados brutos
    BASE_DIR = Path(__file__).resolve().parents[2]
    vendas_path = BASE_DIR / "data" / "raw" / "vendas_2023_2024.csv"
    
    df = pd.read_csv(vendas_path)
    
    # 2. Limpeza básica (igual fizemos no ETL)
    df = df.dropna(subset=['id_client'])
    df['sale_date'] = pd.to_datetime(df['sale_date'], format='mixed', dayfirst=True)
    
    # 3. Agrega as vendas diárias (Soma tudo o que foi vendido em cada data)
    vendas_diarias = df.groupby('sale_date')['total'].sum().reset_index()
    
    # 4. Cria o Calendário Contínuo (A "Dimensão de Datas" do Pandas)
    data_min = vendas_diarias['sale_date'].min()
    data_max = vendas_diarias['sale_date'].max()
    calendario = pd.DataFrame({'sale_date': pd.date_range(start=data_min, end=data_max)})
    
    # 5. Cruza o calendário com as vendas e preenche os dias sem venda com 0
    df_completo = pd.merge(calendario, vendas_diarias, on='sale_date', how='left')
    df_completo['total'] = df_completo['total'].fillna(0)
    
    # 6. Descobre o dia da semana (0 = Segunda, 6 = Domingo) e traduz para Português
    dias_pt = {0: 'Segunda-feira', 1: 'Terça-feira', 2: 'Quarta-feira', 
               3: 'Quinta-feira', 4: 'Sexta-feira', 5: 'Sábado', 6: 'Domingo'}
    df_completo['nome_dia_semana'] = df_completo['sale_date'].dt.dayofweek.map(dias_pt)
    
    # 7. Calcula a média final e ordena
    media_por_dia = df_completo.groupby('nome_dia_semana')['total'].mean().reset_index()
    media_por_dia = media_por_dia.sort_values(by='total', ascending=True).round(2)
    
    print("--- Confirmação: Média de Vendas por Dia da Semana ---")
    print(media_por_dia.to_string(index=False))
    print("\nConclusão: O pior dia é de fato o", media_por_dia.iloc[0]['nome_dia_semana'] + "!")

if __name__ == "__main__":
    confirmar_pior_dia()