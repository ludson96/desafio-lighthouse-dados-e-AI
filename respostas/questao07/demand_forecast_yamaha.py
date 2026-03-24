import pandas as pd
from pathlib import Path


def prever_demanda_yamaha():

    # Caminhos dos datasets
    BASE_DIR = Path(__file__).resolve().parents[2]
    vendas_path = BASE_DIR / "data" / "raw" / "vendas_2023_2024.csv"
    produtos_path = BASE_DIR / "data" / "raw" / "produtos_raw.csv"

    print("1. Carregando os dados brutos...")
    df_vendas = pd.read_csv(vendas_path)
    df_produtos = pd.read_csv(produtos_path)

    # Remover registros inválidos e padronizar o formato de datas
    df_vendas = df_vendas.dropna(subset=["id_client"])
    df_vendas["sale_date"] = pd.to_datetime(
        df_vendas["sale_date"], format="mixed", dayfirst=True
    )

    print("2. Identificando o produto alvo...")

    # Como o dataset pode variar, buscamos possíveis nomes de colunas
    colunas_id = ["id_product", "product_id", "id", "code"]
    colunas_nome = ["name", "product_name", "nome", "produto"]

    coluna_id = next((c for c in colunas_id if c in df_produtos.columns), None)
    coluna_nome = next((c for c in colunas_nome if c in df_produtos.columns), None)

    if not coluna_id or not coluna_nome:
        print(
            f"ERRO: Colunas esperadas não encontradas. "
            f"Colunas disponíveis: {list(df_produtos.columns)}"
        )
        return

    produto_alvo = "Motor de Popa Yamaha Evo Dash 155HP"

    try:
        id_yamaha = df_produtos.loc[
            df_produtos[coluna_nome] == produto_alvo, coluna_id
        ].values[0]
    except IndexError:
        print(f"ERRO: Produto '{produto_alvo}' não encontrado.")
        return

    print(f"Produto encontrado! ID do catálogo: {id_yamaha}")

    # Filtrar vendas apenas do produto alvo
    df_vendas_prod = df_vendas[df_vendas["id_product"] == id_yamaha].copy()

    # Agrupar vendas por dia
    vendas_diarias = (
        df_vendas_prod.groupby("sale_date")["qtd"].sum().reset_index()
    )

    print("3. Construindo calendário contínuo...")

    # Criar calendário completo para não perder dias sem venda
    data_min = df_vendas["sale_date"].min()
    data_max = pd.to_datetime("2024-01-31")

    calendario = pd.DataFrame(
        {"sale_date": pd.date_range(start=data_min, end=data_max)}
    )

    df_completo = pd.merge(calendario, vendas_diarias, on="sale_date", how="left")

    # Dias sem venda recebem zero
    df_completo["qtd"] = df_completo["qtd"].fillna(0)

    # Garantir ordenação temporal antes do rolling
    df_completo = df_completo.sort_values("sale_date")

    print("4. Calculando Média Móvel de 7 dias...")

    # shift(1) evita DATA LEAKAGE:
    # a previsão do dia D usa apenas dados de D-7 até D-1
    df_completo["previsao_mm7"] = (
        df_completo["qtd"]
        .shift(1)
        .rolling(window=7)
        .mean()
    )

    print("5. Avaliando modelo (MAE)...")

    # Separação do conjunto de teste
    # Conforme o enunciado:
    # treino -> até 31/12/2023
    # teste  -> Janeiro de 2024
    teste = df_completo[
        (df_completo["sale_date"] >= "2024-01-01")
        & (df_completo["sale_date"] <= "2024-01-31")
    ].copy()

    # Remover dias iniciais que não possuem histórico suficiente
    teste = teste.dropna(subset=["previsao_mm7"])

    # MAE = Mean Absolute Error
    mae = (teste["qtd"] - teste["previsao_mm7"]).abs().mean()

    print("\n" + "=" * 60)
    print("RESULTADO DO MODELO BASELINE (MÉDIA MÓVEL 7 DIAS)")
    print("=" * 60)

    print(f"Produto: {produto_alvo}")
    print("Período de teste: 01/01/2024 até 31/01/2024")
    print(f"MAE: {mae:.2f} unidades de erro médio por dia")
    print("=" * 60)

    print("\nQuestão 5.a - O baseline é adequado para esse produto?")

    print(
        "R: Provavelmente NÃO. Motores de popa são itens de alto valor e "
        "tendem a apresentar demanda intermitente, com vários dias sem "
        "vendas e vendas pontuais esporádicas. A média móvel assume uma "
        "demanda contínua, o que pode gerar previsões fracionadas e "
        "respostas lentas às mudanças de padrão."
    )

    print("\nQuestão 5.b - Cite uma limitação desse método.")

    print(
        "R: A média móvel simples não captura tendências ou sazonalidade. "
        "Ela considera apenas os valores recentes e não consegue aprender "
        "padrões recorrentes, como aumento de vendas no verão ou em "
        "períodos específicos do ano."
    )

    print("\nQuestão 7.2 - Soma da previsão na primeira semana de Janeiro...")

    primeira_semana = teste[
        (teste["sale_date"] >= "2024-01-01")
        & (teste["sale_date"] <= "2024-01-07")
    ].copy()

    soma_previsao = round(primeira_semana["previsao_mm7"].sum())

    print(
        f"Soma total da previsão de vendas (01/01 a 07/01): "
        f"{soma_previsao} unidades"
    )


if __name__ == "__main__":
    prever_demanda_yamaha()