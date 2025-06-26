# Top Pet System

Este é um sistema de gerenciamento para um pet shop, desenvolvido com Django e Docker.

## Pré-requisitos

- Docker
- Docker Compose

## Configuração do Ambiente

1. **Clone o repositório:**
   ```bash
   git clone <URL_DO_REPOSITORIO>
   cd Top_Pet_System
   ```

2. **Construa e inicie os contêineres:**

   Para iniciar todos os serviços em segundo plano, execute:
   ```bash
   docker compose up -d --build
   ```

   Isso irá construir as imagens e iniciar os contêineres do `backend` e do `db`.

3. **Execute as migrações do banco de dados:**

   Para criar as tabelas no banco de dados, execute o seguinte comando:
   ```bash
   docker compose exec backend python manage.py migrate
   ```

4. **Crie um superusuário (opcional):**

   Para acessar o painel de administração do Django, crie um superusuário:
   ```bash
   docker compose exec backend python manage.py createsuperuser
   ```

## Executando os Testes

O projeto está configurado para rodar testes de unidade e integração usando `pytest`.

### Executando todos os testes

Para rodar todos os conjuntos de testes e verificar a cobertura, execute:
```bash
docker compose run --rm backend pytest
```

### Executando conjuntos de testes específicos

Você também pode executar cada conjunto de testes individualmente:

- **Testes de Agendamentos:**
  ```bash
  docker compose run --rm backend pytest agendamentos/tests.py
  ```

- **Testes de Integração de Pets:**
  ```bash
  docker compose run --rm backend pytest pets/tests.py
  ```

- **Testes de Unidade de Pets:**
  ```bash
  docker compose run --rm backend pytest pets/tests_unidade.py
  ```

- **Testes de Usuários:**
  ```bash
  docker compose run --rm backend pytest users/tests.py
  ```

## Acessando a Aplicação

- A API estará disponível em `http://localhost:8000/`.
- O painel de administração do Django estará em `http://localhost:8000/admin/`.
