# Desafio Lighthouse - Dados e AI

Repositório com as soluções desenvolvidas para o desafio técnico de Dados e Inteligência Artificial da Lighthouse. O projeto consiste em uma série de scripts Python e análises que abordam problemas de ETL, análise financeira, previsão de demanda e sistemas de recomendação.

## Linguagens e ferramentas usadas

[![Git][Git-logo]][Git-url]
[![Python][Python-logo]][Python-url]
[![Pandas][Pandas-logo]][Pandas-url]
[![Scikit-learn][Scikit-learn-logo]][Scikit-learn-url]
[![PostgreSQL][PostgreSQL-logo]][PostgreSQL-url]
[![Docker][Docker-logo]][Docker-url]

## Soluções Desenvolvidas

O projeto está organizado em pastas, onde cada uma corresponde a uma questão do desafio:

<details>
<summary><strong>📁 Questão 03: Processamento de Dados JSON</strong></summary>
<br>
Script que lê um arquivo JSON aninhado contendo custos de importação, achata a estrutura de dados e o converte para um formato tabular em um arquivo CSV.
<br>
</details>

<details>
<summary><strong>📁 Questão 04: Análise de Prejuízo Relativo</strong></summary>
<br>
Análise que combina dados de vendas, custos de importação (em USD) e cotações históricas do câmbio (BRL) para identificar o produto com o maior prejuízo financeiro relativo. Utiliza junções temporais (`merge_asof`) para garantir a precisão dos cálculos.
<br>
</details>

<details>
<summary><strong>📁 Questão 06: ETL para Banco de Dados e Análise de Vendas</strong></summary>
<br>
Um pipeline ETL (Extração, Transformação e Carga) que limpa, padroniza e carrega dados de vendas e produtos de arquivos CSV para um banco de dados PostgreSQL. A análise textual explica a importância de usar uma tabela calendário para calcular corretamente as médias de vendas, evitando distorções causadas por dias sem faturamento.
<br>
</details>

<details>
<summary><strong>📁 Questão 07: Previsão de Demanda (Baseline)</strong></summary>
<br>
Construção de um modelo de previsão de demanda baseline (Média Móvel de 7 dias) para um produto específico. O script realiza o tratamento da série temporal, calcula a previsão, avalia o modelo usando a métrica MAE (Mean Absolute Error) e discute suas limitações, como a incapacidade de capturar sazonalidade.
<br>
</details>

<details>
<summary><strong>📁 Questão 08: Sistema de Recomendação de Produtos</strong></summary>
<br>
Implementação de um sistema de recomendação de produtos com base em **Filtragem Colaborativa Item-Item**. O script constrói uma matriz de interação cliente-produto, calcula a similaridade de cosseno entre os produtos e gera um ranking de itens recomendados para quem compra um determinado produto.
<br>
</details>

## Estrutura do Projeto

A organização de diretórios e arquivos foi pensada para separar claramente os dados brutos, as soluções desenvolvidas e as configurações de ambiente:

```text
📦 desafio-lighthouse-dados-e-AI
┣ 📂 data
┃ ┗ 📂 raw                 # Arquivos originais fornecidos para o desafio (CSVs e JSONs)
┣ 📂 respostas
┃ ┣ 📂 questao03           # Script de conversão e achatamento de JSON para CSV
┃ ┣ 📂 questao04           # Análise e identificação do produto com maior prejuízo
┃ ┣ 📂 questao06           # Processo de ETL (Python + SQLAlchemy) e explicações
┃ ┣ 📂 questao07           # Previsão de demanda (Baseline) e explicações do modelo
┃ ┗ 📂 questao08           # Motor de recomendação (Filtragem Colaborativa) e explicações
┣ 📜 docker-compose.yml    # Arquivo de orquestração dos contêineres PostgreSQL
┣ 📜 init.sql              # Script SQL para montagem inicial do banco 'source_db'
┣ 📜 README.md             # Documentação principal do projeto
┗ 📜 requirements.txt      # Lista de dependências (pacotes Python)
```

## Instruções para Instalação e Execução

<details>
<summary><strong>📋 Pré-requisitos</strong></summary>
<br>
- Python 3.9+
- Git
- Docker (necessário para a Questão 06)
<br>
</details>

<details>
<summary><strong>🚀 Rodando o projeto</strong></summary>
<br>

1. **Clone o repositório:**

    ```bash
    git clone https://github.com/ludson96/desafio-lighthouse-dados-e-AI.git
    cd desafio-lighthouse-dados-e-AI
    ```

2. **Crie um ambiente virtual e instale as dependências:**

    ```bash
    # Crie e ative o ambiente virtual
    python -m venv .venv
    # No Windows: .\.venv\Scripts\activate
    # No Linux/macOS: source .venv/bin/activate

    # Instale as dependências usando o arquivo requirements.txt
    pip install -r requirements.txt
    ```

3. **Para a Questão 06 (ETL com Banco de Dados):**
    * Inicie os bancos de dados PostgreSQL (source e target) com o Docker Compose:

        ```bash
        docker-compose up -d
        ```

    * Execute o script ETL:

        ```bash
        python respostas/questao06/etl_carga_banco.py
        ```

4. **Para executar as outras questões:**
    Navegue até a pasta da questão desejada e execute o script Python correspondente.

    ```bash
    # Exemplo para a Questão 08
    python respostas/questao08/product_recommendation_system.py
    ```

</details>

[Git-logo]: https://img.shields.io/badge/git-F05033?style=for-the-badge&logo=git&logoColor=white
[Git-url]: https://git-scm.com/
[Python-logo]: https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white
[Python-url]: https://www.python.org/
[Pandas-logo]: https://img.shields.io/badge/pandas-150458?style=for-the-badge&logo=pandas&logoColor=white
[Pandas-url]: https://pandas.pydata.org/
[Scikit-learn-logo]: https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white
[Scikit-learn-url]: https://scikit-learn.org/
[PostgreSQL-logo]: https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white
[PostgreSQL-url]: https://www.postgresql.org/
[Docker-logo]: https://img.shields.io/badge/docker-2496ED?style=for-the-badge&logo=docker&logoColor=white
[Docker-url]: https://www.docker.com/
