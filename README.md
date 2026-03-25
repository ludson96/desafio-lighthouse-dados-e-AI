# Repositório do projeto `Agrix - Final` 🚜

Repositório possuí projeto desenvolvido abordando conceitos
de `autenticação`, `JWT`, `autorização` e `SpEL`.

## Informações de aprendizados

- Primeiro projeto usando `autenticação` e `autorização`.

## Linguagens e ferramentas usadas

[![Git][Git-logo]][Git-url]
[![Java][Java-logo]][Java-url]
[![Apache Maven][Apache Maven-logo]][Apache Maven-url]
[![Docker][Docker-logo]][Docker-url]
[![MySQL][MySQL-logo]][MySQL-url]
[![Spring][Spring-logo]][Spring-url]
[![Spring Boot][Spring boot-logo]][Spring boot-url]
[![Spring Security][Spring Security-logo]][Spring Security-url]
[![Hibernate][Hibernate-logo]][Hibernate-url]

## O que foi desenvolvido

Desenvolvi o Agrix, um sistema que permitirá a gestão e o monitoramento de fazendas, com login, autenticação e autorização de usuários.

Esse produto foi desenvolvido em fases:
- [Fase A](https://github.com/ludson96/agrix-fase-a)
- [Fase B](https://github.com/ludson96/agrix-fase-b)
- [Fase C (Final) - Este](https://github.com/ludson96/agrix)



## Habilidades trabalhadas
- Implementar gerenciamento de erros no Spring Web.
- Utilizar campos de data nas rotas da API e no banco de dados
- Aplicar o conhecimento do ecossistema Spring para criar rotas da API.
- Criar o Dockerfile para configurar a aplicação para execução no Docker.
- Garantir que diferentes rotas atenda a regras específicas de autorização.
- Aplicar o conhecimento sobre Spring Security para adicionar autenticação ao projeto.
- Aplicar a injeção de dependência para conectar as camadas de controle, serviço e persistência.
- Criar testes unitários para garantir a qualidade e funcionamento correto da implementação, com cobertura de código adequada.
- Utilizar o Spring Data JPA para implementar entidades e repositórios para a persistência em banco de dados, bem como implementar buscas customizadas.

## Instruções para instalar e rodar

<details>

1. Clone o repositório (recomendado usar em SSH) e entre na pasta:

    ```bash
    git clone git@github.com:ludson96/agrix.git
    cd agrix
    ```

1. Instale as dependências:

    ```bash
    mvn install
    ```

1. Caso não tenha jdk ou maven instalados, basta executar o `Docker` com o comando abaixo:

   ```bash
   #Comando para gerar imagem.
   docker build . -t multi-stage-image
   
   #Comando para executar o container usando a imagem gerada anteriormente. Irá executar o servidor Spring automaticamente e podendo ignorar o passo abaixo.
   docker run -p 8080:8080 --name multi-stage-container multi-stage-image
   ```
1. Para executar o servidor spring:

    ```bash
   mvn clean package
   java -jar target/agrix-1.0-SNAPSHOT.jar
    ```

</details>

## Detalhamento do projeto

### Banco de dados

<details>
<summary><strong>🗄️ Descrição </strong></summary><br>

![Modelo de tabelas](images/agrix-tabelas-fase-b.png)

Nesse modelo, temos as seguintes tabelas:
- `farm`: representa uma fazenda
- `crop`: representa uma plantação, e está em relacionamento `n:1` ("muitos para um") com a tabela `farm`
- `fertilizer`: representa um fertilizante, e está em um relacionamento `n:n` ("muitos para muitos") com a tabela `crop`. Esse relacionamento é realizado através da tabela `crop_fertilizer`.

</details>

### Autenticação no projeto

<details>
  <summary><strong>Instruções para autenticação</strong></summary><br />

### 1. `Endpoints de acesso público`:
- POST `/persons` (cadastra novas pessoas, instruções abaixo)
- POST `/auth/login` (realiza o login)
- Rotas possuem limitações de Acesso, conforme abaixo:
  - `GET /farms` role `USER`, `MANAGER` ou `ADMIN`;
  - `GET /crops` role `MANAGER` ou `ADMIN`;
  - `GET /fertilizers` role `ADMIN`.

### 2. `POST /auth/login`:

<details>
  <summary>Realiza o login</summary><br />

Funciona da seguinte forma:

- `/auth/login` (`POST`)
    - deve receber via corpo do POST `username` e `password` da requisição.
        - Exemplo de requisição:
            ```json
            {
              "username": "zerocool",
              "password": "senhasecreta"
            }
            ```
    - em caso de sucesso:
    - caso os dados estejam corretos, retorna um campo `token` contendo um JWT gerado
      - Exemplo de resposta:

        ```json
        {
          "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJhZ3JpeCIsInN1YiI6Im1ycm9ib3QiLCJleHAiOjE2ODk5ODY2NTN9.lyha4rMcMhFd_ij-farGCXuJy-1Tun1IpJd5Ot6z_5w"
        }
        ```
    - caso os dados estejam incorretos, retorna status 403 

</details>

---

</details>



<details>

  <summary><strong>/farms</strong></summary>

### 1. `POST /farms`

<details>
  <summary>Cria uma nova fazenda</summary><br />

Funciona da seguinte forma:

- `/farms` (`POST`)
    - deve receber via corpo do POST os dados de uma fazenda.
        - Exemplo de requisição:
           ```json
           {
             "name": "Fazendinha",
             "size": 5
           }
           ```
    - em caso de sucesso:
        - retornar o status HTTP 201 (CREATED)
        - retornar os dados da fazenda criada. O `id` da fazenda esta incluso na resposta.
            - Exemplo de resposta:

          ```json
          {
            "id": 1,
            "name": "Fazendinha",
            "size": 5
          }
          ```

</details>

### 2. `GET /farms`

<details>
  <summary>Retorna todas as fazendas cadastradas </summary><br />

Funciona da seguinte forma:

- `/farms` (`GET`)
    - retorna uma lista de todas as fazendas. O `id` da fazenda esta
      incluso na resposta.
        - Exemplo de resposta:

           ```json
           [
             {
               "id": 1,
               "name": "Fazendinha",
               "size": 5.0
             },
             {
               "id": 2,
               "name": "Fazenda do Júlio",
               "size": 2.5
             }
           ]
           ```

</details>

### 3. `GET /farms/{id}`

<details>
  <summary>Retorna informações de uma fazenda especifica</summary><br />

Funciona da seguinte forma:

- `/farms/{id}` (`GET`):
    - recebe um `id` pelo caminho da rota e retorna a fazenda com esse `id`. O `id` da
      fazenda esta incluso na resposta.
        - Exemplo de resposta para a rota `/farms/3` (supondo que exista uma fazenda com `id = 3`):

           ```json
           {
             "id": 3,
             "name": "My Cabbages!",
             "size": 3.49
           }
           ```
    - caso não exista uma fazenda com esse `id`, a rota retorna o status HTTP 404 com a
      mensagem `Fazenda não encontrada!` no corpo da resposta.

</details>

### 4. `POST /farms/{farmId}/crops`

<details>
  <summary>Cria uma nova plantação</summary><br />

Funciona da seguinte forma:

- `/farms/{farmId}/crops` (`POST`)
    - recebe o `id` da fazenda pelo caminho da rota (representado aqui por `farmId` apenas para diferenciar da plantação)
        - recebe via corpo do POST os dados da plantação e salva a nova plantação a partir dos dados recebidos, associada à fazenda com o ID
            - Exemplo de requisição na rota `/farms/1/crops` (supondo que exista uma fazenda com `id = 1`):

              ```json
              {
                "name": "Couve-flor",
                "plantedArea": 5.43,
                "plantedDate": "2022-12-05",
                "harvestDate": "2023-06-08"
              }
              ```
    - em caso de sucesso:
        - retorna o status HTTP 201 (CREATED)
        - retorna os dados da plantação criada. A resposta inclui o `id` da plantação e
          o `id` da fazenda.
            - caso não exista uma fazenda com o `id` passado, retorna o status HTTP 404 com a
              mensagem `Fazenda não encontrada!` no corpo da resposta.
            - Exemplo de resposta:

                ```json
                {
                  "id": 1,
                  "name": "Couve-flor",
                  "plantedArea": 5.43,
                  "plantedDate": "2022-12-05",
                  "harvestDate": "2023-06-08",
                  "farmId": 1
                }
                ```

</details>

### 5. `GET /farms/{farmId}/crops`

<details>
  <summary>Lista as plantações de uma fazenda específica</summary><br />

Funciona da seguinte forma:
- `/farms/{farmId}/crops` (`GET`):
    - recebe o `id` de uma fazenda pelo caminho
    - retorna uma lista com todas as plantações associadas à fazenda
        - Exemplo de resposta para a rota `/farms/1/crops` (supondo que exista uma fazenda com `id = 1`):

        ```json
        [
          {
            "id": 1,
            "name": "Couve-flor",
            "plantedArea": 5.43,
            "plantedDate": "2022-12-05",
            "harvestDate": "2023-06-08",
            "farmId": 1
          },
          {
            "id": 2,
            "name": "Alface",
            "plantedArea": 21.3,
            "plantedDate": "2022-02-15",
            "harvestDate": "2023-02-20",
            "farmId": 1
          }
        ]
        ```
    - caso não exista uma fazenda com esse `id`, retorna o status HTTP 404 com a
      mensagem `Fazenda não encontrada!` no corpo da resposta.

</details>

---
</details>

<details>

  <summary><strong>/crops</strong></summary>

### 1. `GET /crops`

<details>
  <summary>Lista todas as plantações cadastradas</summary><br />

Funciona da seguinte forma:
- `/crops` (`GET`)
    - retorna uma lista de todas as plantações cadastradas. A resposta inclui o `id` de
      cada plantação e o `id` da fazenda associada.
        - Exemplo de resposta:

            ```json
            [
              {
                "id": 1,
                "name": "Couve-flor",
                "plantedArea": 5.43,
                "plantedDate": "2022-02-15",
                "harvestDate": "2023-02-20",
                "farmId": 1
              },
              {
                "id": 2,
                "name": "Alface",
                "plantedArea": 21.3,
                "plantedDate": "2022-02-15",
                "harvestDate": "2023-02-20",
                "farmId": 1
              },
              {
                "id": 3,
                "name": "Tomate",
                "plantedArea": 1.9,
                "plantedDate": "2023-05-22",
                "harvestDate": "2024-01-10",
                "farmId": 2
              }
            ]
            ```

</details>

### 2. `GET /crops/{id}`

<details>
  <summary>Retorna as informações de plantações de uma fazenda especifica</summary><br />

Funciona da seguinte forma:
- `/crops/{id}` (`GET`):
    - recebe o `id` de uma plantação pelo caminho da rota
    - caso exista a plantação com o `id` recebido, retorna os dados da plantação. A resposta
      inclui o `id` de cada plantação e o `id` da fazenda associada.
        - Exemplo de resposta para a rota `/crops/3` (supondo que exista uma plantação com `id = 3`:

        ```json
        {
          "id": 3,
          "name": "Tomate",
          "plantedArea": 1.9,
          "plantedDate": "2023-05-22",
          "harvestDate": "2024-01-10",
          "farmId": 2
        }
        ```

    - caso não exista uma plantação com o `id` passado, retorna o status HTTP 404 com a
      mensagem `Plantação não encontrada!` no corpo da resposta.

</details>

### 3. `GET /crops/search`

<details>
  <summary>Busca plantações a partir da data de colheita</summary><br />

Funciona da seguinte forma:
- `/crops/search` (`GET`)
    - recebe dois parâmetros por query string para busca:
        - `start`: data de início
        - `end`: data de fim
    - retorna uma lista com as plantações nas quais o campo `harvestDate` esteja entre as data de início e de fim.
        - a comparação das datas são inclusiva (ou seja, deve incluir datas que sejam iguais à de início ou à de fim)
    - a resposta inclui o `id` de cada plantação e o `id` da fazenda associada, mas inclui os dados da fazenda.
        - Exemplo de resposta para a rota `/crops/search?start=2023-01-07&end=2024-01-10`:

          ```json
          [
            {
              "id": 1,
              "name": "Couve-flor",
              "plantedArea": 5.43,
              "plantedDate": "2022-02-15",
              "harvestDate": "2023-02-20",
              "farmId": 1
            },
            {
              "id": 3,
              "name": "Tomate",
              "plantedArea": 1.9,
              "plantedDate": "2023-05-22",
              "harvestDate": "2024-01-10",
              "farmId": 2
            }
          ]
          ```

</details>

### 4. `POST /crops/{cropId}/fertilizers/{fertilizerId}`

<details>
  <summary>Associa uma plantação a um fertilizante</summary><br />

A rota a ser criada é:
- `/crops/{cropId}/fertilizers/{fertilizerId}` (`POST`)
    - recebe tanto o `id` da plantação quanto o `id` do fertilizante pelo caminho da rota
    - o corpo da requisição será vazio
    - faz a associação entre o fertilizante e a plantação
    - em caso de sucesso, retorna o status HTTP 201 (CREATED) com a mensagem `Fertilizante e plantação associados com sucesso!` no corpo da resposta
    - caso não exista uma plantação com o `id` recebido, a rota retorna o status HTTP 404 com a mensagem `Plantação não encontrada!` no corpo da resposta.
    - caso não exista um fertilizante com o `id` recebido, a rota retorna o status HTTP 404 com a mensagem `Fertilizante não encontrado!` no corpo da resposta.
        - Exemplo de resposta para a rota `/crops/1/fertilizers/2` (supondo que exista uma plantação com `id = 1` e um fertilizante com `id = 2`):

          ```text
          Fertilizante e plantação associados com sucesso!
          ```

</details>

### 5. `GET /crops/{cropId}/fertilizers`

<details>
  <summary>Lista os fertilizante associados a uma plantação</summary><br />

A rota a ser criada é:
- `/crops/{cropId}/fertilizers` (`GET`):
    - recebe o `id` de uma plantação pelo caminho
    - retorna uma lista com todas os fertilizantes associados à plantação
    - caso não exista uma plantação com o `id` recebido, a rota retorna o status HTTP 404 com a mensagem `Plantação não encontrada!` no corpo da resposta.
        - Exemplo de resposta para a rota `/crops/2/fertilizers` (supondo que exista uma plantação com `id = 2`):

          ```json
          [
            {
              "id": 2,
              "name": "Húmus",
              "brand": "Feito pelas minhocas",
              "composition": "Muitos nutrientes"
            },
            {
              "id": 3,
              "name": "Adubo",
              "brand": "Feito pelas vaquinhas",
              "composition": "Esterco"
            }
          ]
          ```

</details>

---

</details>

<details>
  <summary><strong>/fertilizers</strong></summary>

### 1. `POST /fertilizers`

<details>
  <summary>Cria um novo fertilizante</summary><br />

A rota a ser criada é:
- `/fertilizers` (`POST`)
    - recebe via corpo do POST os dados de um fertilizante
    - salva um novo fertilizante a partir dos dados recebidos
        - em caso de sucesso:
            - retorna o status HTTP 201 (CREATED)
            - retorna os dados do fertilizante criado, incluindo seu `id`
            - Exemplo de requisição:

                ```json
                {
                "name": "Compostagem",
                "brand": "Feita em casa",
                "composition": "Restos de alimentos"
                }
                ```

            - Exemplo de resposta:

              ```json
              {
                "id": 1,
                "name": "Compostagem",
                "brand": "Feita em casa",
                "composition": "Restos de alimentos"
              }
              ```

</details>

### 2. `GET /fertilizers`

<details>
  <summary>Lista todos os fertilizantes cadastrados</summary><br />

A rota a ser criada é:
- `/fertilizers` (`GET`):
    - retorna uma lista de todos os fertilizantes cadastrados, incluindo o `id` de cada.
    - Exemplo de resposta:

        ```json
        [
          {
            "id": 1,
            "name": "Compostagem",
            "brand": "Feita em casa",
            "composition": "Restos de alimentos"
          },
          {
            "id": 2,
            "name": "Húmus",
            "brand": "Feito pelas minhocas",
            "composition": "Muitos nutrientes"
          },
          {
            "id": 3,
            "name": "Adubo",
            "brand": "Feito pelas vaquinhas",
            "composition": "Esterco"
          }
        ]
        ```
</details>

### 3. `GET /fertilizers/{id}`

<details>
  <summary>Retorna informações de um fertilizante</summary><br />

A rota a ser criada é:
- `/fertilizers/{fertilizerId}` (`GET`):
    - recebe o `id` de um fertilizante pelo caminho da rota
    - caso exista o fertilizante com o `id` recebido, retorna seus dados, incluindo seu `id`
    - caso não exista um fertilizante com o `id` passado, a rota retorna o status HTTP 404 com a
      mensagem `Fertilizante não encontrado!` no corpo da resposta.
    - Exemplo de resposta da rota `/fertilizers/3` (supondo que exista um fertilizante com `id = 3`):

        ```json
        {
          "id": 3,
          "name": "Adubo",
          "brand": "Feito pelas vaquinhas",
          "composition": "Esterco"
        }
        ```

</details>

</details>

[Git-logo]: https://img.shields.io/badge/git-%23F05033.svg?style=for-the-badge&logo=git&logoColor=white
[Git-url]: https://git-scm.com

[Java-logo]: https://img.shields.io/badge/java-%23ED8B00.svg?style=for-the-badge&logo=openjdk&logoColor=white
[Java-url]: https://www.java.com/pt-BR/

[Apache Maven-logo]: https://img.shields.io/badge/Apache%20Maven-C71A36?style=for-the-badge&logo=Apache%20Maven&logoColor=white
[Apache Maven-url]: https://maven.apache.org/

[Docker-logo]: https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white
[Docker-url]: https://www.docker.com

[Spring-logo]: https://img.shields.io/badge/Spring-6DB33F.svg?style=for-the-badge&logo=Spring&logoColor=white
[Spring-url]: https://spring.io/

[Spring boot-logo]:https://img.shields.io/badge/Spring%20Boot-6DB33F.svg?style=for-the-badge&logo=Spring-Boot&logoColor=white
[Spring boot-url]: https://spring.io/projects/spring-boot

[Spring Security-logo]: https://img.shields.io/badge/Spring%20Security-6DB33F.svg?style=for-the-badge&logo=Spring-Security&logoColor=white
[Spring Security-url]: https://spring.io/projects/spring-security

[Hibernate-logo]: https://img.shields.io/badge/Hibernate-59666C?style=for-the-badge&logo=Hibernate&logoColor=white
[Hibernate-url]: https://hibernate.org/

[MySQL-logo]: https://img.shields.io/badge/mysql-%2300f.svg?style=for-the-badge&logo=mysql&logoColor=white
[MySQL-url]: https://www.mysql.com
