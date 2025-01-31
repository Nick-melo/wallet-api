# Wallet API - Desafio Back-End

## Descrição
Este projeto implementa uma API para gerenciar carteiras digitais e transações financeiras, desenvolvida com **Django** e **PostgreSQL**, utilizando **JWT** para autenticação.

A API permite aos usuários:
- Criar uma conta.
- Consultar saldo da carteira.
- Adicionar saldo à carteira.
- Criar e listar transferências entre carteiras de usuários.

## Tecnologias Utilizadas
- **Django**: Framework web para desenvolvimento da API.
- **PostgreSQL**: Banco de dados relacional.
- **JWT (JSON Web Token)**: Autenticação segura.
- **Django REST Framework**: Para a criação da API RESTful.
- **CORS Headers**: Para controle de origem de requisições cross-origin.

## Como Rodar o Projeto

### Pré-requisitos
Certifique-se de que você tem o **Python 3.9+** e o **PostgreSQL** instalados. Você também vai precisar de um arquivo `.env` configurado com as variáveis do projeto.

### Passos para Instalação

1. **Clone este repositório:**
    ```bash
    git clone https://github.com/seu_usuario/wallet-api.git
    cd wallet-api
    ```

2. **Crie um ambiente virtual:**
    ```bash
    python -m venv venv
    ```

3. **Ative o ambiente virtual:**
    - **No Windows:**
      ```bash
      venv\Scripts\activate
      ```
    - **No Linux/Mac:**
      ```bash
      source venv/bin/activate
      ```

4. **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

5. **Configure o arquivo `.env`:**
    Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:
    ```env
    DB_NAME=Banco_New
    DB_USER=postgres
    DB_PASSWORD=senha_01
    DB_HOST=localhost
    DB_PORT=5432
    SECRET_KEY=django-insecure-e*wb)y=-9awz1v9^rxm##v%hthdb2nfi0gj4a_r+9u1au*izbn
    DEBUG=False
    CORS_ALLOWED_ORIGINS=http://localhost:3000
    ALLOWED_HOSTS=localhost,127.0.0.1
    ```

6. **Configure o banco de dados:**
    Certifique-se de que o **PostgreSQL** esteja rodando e que o banco de dados mencionado no `.env` seja criado.

    Para criar o banco de dados, execute:
    ```bash
    psql -U postgres
    CREATE DATABASE Banco_New;
    ```

7. **Execute as migrações do banco de dados:**
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

8. **Popule o banco de dados com dados iniciais (se houver script para isso):**
    Caso tenha um script para popular dados fictícios:
    ```bash
    python manage.py loaddata inicial_data.json
    ```

9. **Inicie o servidor Django:**
    ```bash
    python manage.py runserver
    ```

### Uso da API

#### 1. **Autenticação**

Para realizar autenticação, use o **JWT**. O token deve ser enviado no cabeçalho das requisições como **Bearer Token**.

**Exemplo de requisição para login (POST):**

```bash
POST http://127.0.0.1:8000/api/login/
Content-Type: application/json

{
    "username": "usuario_exemplo",
    "password": "senha_exemplo"
}

Resposta:

{
    "access": "JWT_ACCESS_TOKEN",
    "refresh": "JWT_REFRESH_TOKEN"
}

2. Endpoints Principais
Criar Usuário (POST)
Endpoint para criar um novo usuário.


POST /api/users/
Exemplo de corpo:


{
  "username": "novo_usuario",
  "password": "senha_segura"
}
Consultar Saldo (GET)
Endpoint para consultar o saldo da carteira do usuário autenticado.


GET /api/wallets/balance/
Authorization: Bearer JWT_ACCESS_TOKEN
Adicionar Saldo (POST)
Endpoint para adicionar saldo à carteira do usuário.


POST /api/wallets/deposit/
Authorization: Bearer JWT_ACCESS_TOKEN
Exemplo de corpo:

{
  "amount": 100.00
}
Criar Transferência (POST)
Endpoint para criar uma transferência entre carteiras de usuários.


POST /api/transactions/
Authorization: Bearer JWT_ACCESS_TOKEN
Exemplo de corpo:

{
  "recipient": "id_do_destinatario",
  "amount": 50.00
}

Listar Transferências (GET)
Endpoint para listar transferências realizadas por um usuário, com filtro por data.

GET /api/transactions/
Authorization: Bearer JWT_ACCESS_TOKEN

Testes
Caso queira rodar os testes automatizados, execute:


python manage.py test

Arquitetura do Projeto
A API segue os padrões REST para construção de rotas e retornos. A autenticação é realizada utilizando JWT, e o banco de dados é PostgreSQL. A estrutura do projeto foi organizada da seguinte forma:

users: Gerenciamento de usuários.
wallets: Gerenciamento de carteiras.
transactions: Gerenciamento de transferências financeiras.
Melhorias Planejadas
Implementação de verificação de saldo antes da realização de transferências.
Implementação de envio de notificações por email para transferências realizadas.
Licença
Este projeto está licenciado sob a MIT License - veja o arquivo LICENSE para mais detalhes.