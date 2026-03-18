""" Cenário

Gabriel percebeu que seus dados estão desorganizados e sem um padrão definido e isso pode tornar o trabalho de análise mais trabalhoso. Precisamos melhorar isso utilizando o Python.

Sua missão é realizar uma normalização dos dados presentes no arquivo produtos_raw.csv.

Premissas obrigatórias
Utilize apenas o CSV produtos_raw.csv
Utilize obrigatoriamente Python 3

Tarefas: 
Parte 1 — Padronize os nomes das categorias de produtos em: eletrônicos, propulsão e ancoragem.
Parte 2 — Converta os valores para o tipo numérico.
Parte 3 — Remova as duplicatas. """

import pandas as pd

def padronizar_categoria(categoria):
    """Função auxiliar para padronizar os erros de digitação nas categorias."""
    # Remove espaços e transforma em letras minúsculas
    cat_limpa = str(categoria).lower().replace(" ", "")
    
    # Compara o prefixo para definir a categoria correta
    if cat_limpa.startswith('ele'):
        return 'eletrônicos'
    elif cat_limpa.startswith('prop'):
        return 'propulsão'
    elif cat_limpa.startswith('anc') or cat_limpa.startswith('enc'):
        return 'ancoragem'
    
    return categoria

def normalizar_dados():
    caminho_csv = r"c:\Users\Ludso\Desktop\Arquivos do desafio final\produtos_raw.csv"
    
    # Carregando o dataset original
    df = pd.read_csv(caminho_csv)
    
    # Parte 1 — Padronize os nomes das categorias de produtos
    df['actual_category'] = df['actual_category'].apply(padronizar_categoria)
    
    # Parte 2 — Converta os valores para o tipo numérico
    # Substitui a string 'R$', remove espaços em branco e converte para float
    df['price'] = df['price'].astype(str).str.replace('R$', '', regex=False).str.strip().astype(float)
    
    # Parte 3 — Remova as duplicatas
    # Conta quantas duplicatas exatas existem antes da remoção
    duplicadas_removidas = df.duplicated().sum()
    
    # Usamos keep='first' (padrão) para manter a primeira ocorrência
    df = df.drop_duplicates(ignore_index=True)
    
    # Demonstrando o resultado
    print("--- Dados normalizados com sucesso! ---")
    print(f"Produtos duplicados removidos: {duplicadas_removidas}")
    print(f"Total de linhas após a remoção de duplicatas: {len(df)}")
    print("\nVisualização das primeiras linhas:")
    print(df.head())

if __name__ == "__main__":
    normalizar_dados()
