# 📚 TOP PET SYSTEM - GUIA COMPLETO DA API

## 📋 ÍNDICE RÁPIDO
1. [🎯 Visão Geral](#-visão-geral)
2. [🚀 Configuração Inicial](#-configuração-inicial)
3. [🔐 Autenticação](#-autenticação)
4. [📋 Estrutura da API](#-estrutura-da-api)
5. [🎯 Regras de Negócio](#-regras-de-negócio-e-permissões)
6. [🧪 Exemplos Práticos](#-exemplos-práticos)
7. [🎨 Interface Swagger](#-interface-swagger)
8. [🚨 Troubleshooting](#-troubleshooting)
9. [🛠️ Comandos Úteis](#️-comandos-úteis)
10. [📚 Recursos Adicionais](#-recursos-adicionais)

---

## 🎯 VISÃO GERAL

O **Top Pet System** é uma API REST completa para gerenciamento de clínicas veterinárias, desenvolvida com Django REST Framework. Este guia demonstra como utilizar o Swagger UI para interagir com todos os endpoints da API.

### 🌟 Principais Funcionalidades
- **Interface web interativa** para testar APIs via Swagger UI
- **Documentação automática** dos endpoints com OpenAPI 3.0
- **Autenticação por token** com diferentes níveis de permissão
- **Gestão completa** de usuários, pets, agendamentos e prontuários
- **Validação em tempo real** com exemplos práticos
- **Suporte multi-usuário** com 4 tipos de perfil distintos

### 🎭 Tipos de Usuário
- **👤 CLIENTE**: Dono de pet (auto-cadastro permitido)
- **👨‍💼 FUNCIONARIO**: Funcionário da clínica
- **👨‍⚕️ VETERINARIO**: Profissional veterinário (requer CRMV)
- **👑 ADMIN**: Administrador do sistema (acesso total)

---

## 🚀 CONFIGURAÇÃO INICIAL

### 📋 Pré-requisitos
- **Docker** e **Docker Compose** instalados
- Projeto clonado em: `f:\GitHub\Top_Pet_System`

### 🐳 Iniciando com Docker (Recomendado)

```bash
### Navegue até o projeto
cd f:\GitHub\Top_Pet_System

### Inicie os containers
docker-compose up -d

### Aguarde a inicialização (30-60 segundos)
docker-compose ps

### Criar superusuário
docker-compose exec web python manage.py createsuperuser
### Exemplo: username=admin, password=admin123

### Configure o perfil de administrador
### Acesse: http://127.0.0.1:8000/admin/
### Login com as credenciais criadas
### Vá em USERS/Profiles > Selecione seu usuário
### Em Role Settings/Role > Selecione "Admin" > SAVE
```

### 🌐 URLs Principais
- **🔖 Swagger UI**: http://127.0.0.1:8000/api/docs/
- **📖 ReDoc**: http://127.0.0.1:8000/api/redoc/
- **📄 Schema OpenAPI**: http://127.0.0.1:8000/api/schema/
- **⚙️ Admin Django**: http://127.0.0.1:8000/admin/

### 🛠️ Desenvolvimento Local (Opcional)

```bash
### Navegue até o backend
cd f:\GitHub\Top_Pet_System\backend

### Configure ambiente virtual (opcional)
python -m venv venv
venv\Scripts\activate  # Windows

### Instale dependências
pip install -r requirements.txt

### Execute migrações
python manage.py migrate

### Criar superusuário
python manage.py createsuperuser

### Iniciar servidor
python manage.py runserver
```
### Configure o perfil de administrador
### Acesse: http://127.0.0.1:8000/admin/
### Login com as credenciais criadas
### Vá em USERS/Profiles > Selecione seu usuário
### Em Role Settings/Role > Selecione "Admin" > SAVE

### ✅ Verificação
1. Acesse http://127.0.0.1:8000/api/docs/
2. A interface do Swagger UI deve carregar
3. Se houver erro: `docker-compose logs web`

---

## 🔐 AUTENTICAÇÃO

### 🎫 Credenciais Padrão
```
👑 ADMIN
Username: admin
Password: admin123
```

### 🔑 Métodos de Autenticação

#### Método 1: Auto-cadastro de Cliente
```json
POST /api/users/register/
{
  "username": "cliente_teste",
  "password": "cliente123",
  "email": "cliente@teste.com",
  "first_name": "João",
  "last_name": "Silva"
}
```

#### Método 2: Obter Token via API
```json
POST /api/auth/token/
{
  "username": "admin",
  "password": "admin123"
}
```

#### Método 3: Autorizar no Swagger
1. Clique no botão **🔒 Authorize** no topo
2. No campo **TokenAuthentication**, digite:
   ```
   Token SEU_TOKEN_AQUI
   ```
3. Clique **Authorize** → **Close**

---

## 📋 ESTRUTURA DA API

### 🏷️ Endpoints por Categoria

####  **USUÁRIOS**
- `GET /api/users/me/` - Ver próprio perfil
- `POST /api/users/register/` - Auto-cadastro como cliente
- `GET /api/users/admin/users/` - Listar usuários (admin)
- `POST /api/users/admin/users/` - Admin criar usuário
- `GET /api/users/funcionario/users/` - Listar clientes (funcionário)
- `POST /api/users/funcionario/users/` - Funcionário criar usuário
- `GET /api/users/logs/` - Visualizar logs (admin)

#### 🔐 **AUTENTICAÇÃO**
- `POST /api/auth/token/` - Obter token de autenticação
- `POST /api/auth/password-reset/` - Solicitar reset de senha
- `POST /api/auth/password-reset/confirm/` - Confirmar reset de senha
- `POST /api/auth/password-reset/validate_token/` - Validar token de reset

#### 🐕 **PETS**
- `GET /api/pets/` - Listar pets
- `POST /api/pets/` - Criar novo pet
- `GET /api/pets/{id}/` - Detalhes de um pet
- `PATCH /api/pets/{id}/` - Atualizar pet
- `DELETE /api/pets/{id}/` - Remover pet

#### 📅 **AGENDAMENTOS**
- `GET /api/agendamentos/agendamentos/` - Listar agendamentos
- `POST /api/agendamentos/agendamentos/` - Criar agendamento
- `GET /api/agendamentos/agendamentos/{id}/` - Detalhes do agendamento
- `PATCH /api/agendamentos/agendamentos/{id}/` - Atualizar agendamento
- `DELETE /api/agendamentos/agendamentos/{id}/` - Cancelar agendamento
- `GET /api/agendamentos/horarios-disponiveis/` - Consultar horários disponíveis

#### 🩺 **SERVIÇOS**
- `GET /api/agendamentos/servicos/` - Listar serviços
- `POST /api/agendamentos/servicos/` - Criar serviço
- `GET /api/agendamentos/servicos/{id}/` - Detalhes do serviço
- `PATCH /api/agendamentos/servicos/{id}/` - Atualizar serviço
- `DELETE /api/agendamentos/servicos/{id}/` - Remover serviço

#### 📋 **PRONTUÁRIOS**
- `GET /api/prontuarios/` - Listar prontuários
- `POST /api/prontuarios/` - Criar prontuário
- `GET /api/prontuarios/{id}/` - Detalhes do prontuário
- `PATCH /api/prontuarios/{id}/` - Atualizar prontuário
- `DELETE /api/prontuarios/{id}/` - Remover prontuário

#### 🔧 **SISTEMA**
- `GET /api/` - Página inicial da API
- `GET /api/status/` - Status do sistema
- `GET /api/info/` - Informações da API

---

## 🎯 REGRAS DE NEGÓCIO E PERMISSÕES

### 📋 Hierarquia de Usuários
```
👑 ADMIN
├── Acesso total ao sistema
├── Pode criar qualquer tipo de usuário
└── Pode ativar/desativar usuários

👨‍💼 FUNCIONARIO
├── Pode criar: CLIENTE, FUNCIONARIO, VETERINARIO
├── Pode gerenciar todos os pets
└── Não pode criar ADMIN

👨‍⚕️ VETERINARIO
├── Mesmas permissões de FUNCIONARIO
├── Pode criar prontuários
└── Requer CRMV obrigatório

👤 CLIENTE
├── Pode gerenciar apenas próprios pets
├── Pode fazer agendamentos
└── Auto-cadastro permitido
```

### 🔐 Regras de Cadastro

#### Auto-cadastro Público (`/api/users/register/`)
- ✅ **Permitido**: Apenas tipo **CLIENTE**
- ❌ **Bloqueado**: FUNCIONARIO, VETERINARIO, ADMIN
- 🔓 **Acesso**: Público (sem autenticação)

#### Criação por Funcionários (`/api/users/funcionario/users/`)
- ✅ **Permitido**: CLIENTE, FUNCIONARIO, VETERINARIO
- ❌ **Bloqueado**: ADMIN
- 🔐 **Acesso**: Funcionários e Admins

#### Criação por Administradores (`/api/users/admin/users/`)
- ✅ **Permitido**: Qualquer tipo de usuário
- 🔐 **Acesso**: Apenas administradores

### 🛡️ Validações Especiais
- **VETERINARIO**: Campo `crmv` obrigatório
- **Senhas**: Confirmação obrigatória (`confirm_password`)
- **Email/Username**: Devem ser únicos
- **Profiles**: Um por usuário, criação automática

---

## 🧪 EXEMPLOS PRÁTICOS

### 📝 1. Criar um Pet
```json
POST /api/pets/
{
  "nome": "Rex",
  "especie": "Cachorro",
  "raca": "Golden Retriever", 
  "data_de_nascimento": "2020-05-15",
  "sexo": "MACHO",
  "observacoes": "Pet muito carinhoso",
  "tutor": 1
}
```

### 📊 2. Listar Pets
```
GET /api/pets/
```

### 👤 3. Ver Próprio Perfil
```
GET /api/users/me/
```

### 🆕 4. Registrar Novo Cliente
```json
POST /api/users/register/
{
  "username": "novocliente",
  "password": "minhasenha123",
  "confirm_password": "minhasenha123",
  "email": "cliente@email.com",
  "first_name": "João",
  "last_name": "Silva",
  "telefone": "(11) 99999-9999",
  "endereco": "Rua das Flores, 123"
}
```

### 📅 5. Consultar Horários Disponíveis
```
GET /api/agendamentos/horarios-disponiveis/?data=2025-07-10

Resposta:
["08:00", "09:00", "10:00", "11:00", "14:00", "15:00", "16:00"]
```

### 📅 6. Criar Agendamento
```json
POST /api/agendamentos/agendamentos/
{
  "pet_id": 1,
  "servico_id": 1,
  "data_hora": "2025-07-10T14:00:00Z",
  "observacoes": "Checkup de rotina"
}
```

### 🩺 7. Criar Serviço (Funcionário/Admin)
```json
POST /api/agendamentos/servicos/
{
  "nome": "Consulta Veterinária",
  "descricao": "Consulta geral para avaliação da saúde do pet",
  "preco": "80.00",
  "duracao": "01:00:00",
  "disponivel": true
}
```

### 🏥 8. Criar Prontuário (Veterinário/Admin)
```json
POST /api/prontuarios/
{
  "pet": 1,
  "veterinario": 2,
  "data_consulta": "2025-07-10T14:30:00Z",
  "motivo_consulta": "Consulta de rotina",
  "diagnostico": "Pet saudável",
  "tratamento": "Vacinação atualizada",
  "observacoes": "Retorno em 6 meses"
}
```

### 👨‍💼 9. Funcionário Criando Usuários

**Cliente:**
```json
POST /api/users/funcionario/users/
{
  "username": "cliente_func",
  "password": "cliente123",
  "confirm_password": "cliente123",
  "email": "cliente.func@toppet.com",
  "first_name": "Maria",
  "last_name": "Cliente",
  "role": "CLIENTE"
}
```

**Veterinário:**
```json
POST /api/users/funcionario/users/
{
  "username": "dr_silva",
  "password": "veterinario123",
  "confirm_password": "veterinario123",
  "email": "dr.silva@toppet.com",
  "first_name": "Dr. Carlos",
  "last_name": "Silva",
  "role": "VETERINARIO",
  "crmv": "12345-SP"
}
```

### 👑 10. Admin Criando Usuários
```json
POST /api/users/admin/users/
{
  "username": "admin2",
  "password": "admin456",
  "confirm_password": "admin456",
  "email": "admin2@toppet.com",
  "first_name": "Admin",
  "last_name": "Secundário",
  "role": "ADMIN"
}
```

---

## 🎨 INTERFACE SWAGGER

### 🔍 Elementos da Interface
- **🟢 Verde (200-299)**: Sucesso
- **🔵 Azul (201)**: Criado
- **🟡 Amarelo (400)**: Erro do cliente
- **🔴 Vermelho (500)**: Erro do servidor

### 🛠️ Funcionalidades
- **Try it out**: Ativa modo de teste
- **Execute**: Executa requisição real
- **Schemas**: Estrutura de dados expandível
- **Copy as cURL**: Copia comando curl
- **Download**: Baixa resposta JSON

---

## 🚨 TROUBLESHOOTING

### ❌ Erro 401 Unauthorized
**Problema**: "Authentication credentials were not provided"

**Solução**:
- Verifique se está autenticado
- Token deve ter formato: `Token SEU_TOKEN_AQUI`
- Certifique-se do espaço após "Token"

### ❌ Erro 403 Forbidden
**Problema**: Usuário sem permissão

**Solução**:
- Use conta com privilégios adequados
- Verifique tipo de usuário necessário

### ❌ Erro 400 Bad Request
**Problema**: Dados inválidos

**Solução**:
- Verifique formato JSON
- Confira campos obrigatórios
- Valide tipos de dados

### ⚠️ Erros Específicos

#### "This field is required: crmv"
- **Causa**: Criando VETERINARIO sem CRMV
- **Solução**: Sempre incluir `"crmv": "12345-SP"` para veterinários

#### "You don't have permission to create ADMIN users"
- **Causa**: Funcionário tentando criar ADMIN
- **Solução**: Use endpoint `/api/users/admin/users/` com credenciais de admin

#### "Password and confirm_password do not match"
- **Causa**: Senhas diferentes no cadastro
- **Solução**: Garantir que ambas sejam idênticas

---
## 🛠️ COMANDOS ÚTEIS

### 🐳 Docker
```bash
# Iniciar containers
docker-compose up -d

# Parar containers  
docker-compose down

# Ver logs
docker-compose logs web

# Acessar shell do container
docker-compose exec web bash

# Executar migrações
docker-compose exec web python manage.py migrate

# Criar superusuário
docker-compose exec web python manage.py createsuperuser

# Backup do banco
docker-compose exec db pg_dump -U postgres postgres > backup.sql
```

### 🔧 Django Management
```bash
# Ver migrações pendentes
python manage.py showmigrations

# Criar migrações
python manage.py makemigrations

# Shell do Django
python manage.py shell

# Executar testes
python manage.py test

# Verificar sistema
python manage.py check
```

### 🔍 PowerShell - Testes de API
```powershell
# Testar registro de cliente
$body = @{
    username = "teste_ps"
    email = "teste@email.com" 
    password = "senha123"
    confirm_password = "senha123"
    first_name = "Teste"
    last_name = "PowerShell"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/users/register/" -Method POST -Body $body -ContentType "application/json"

# Obter token
$loginBody = @{
    username = "admin"
    password = "admin123"
} | ConvertTo-Json

$token = (Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/auth/token/" -Method POST -Body $loginBody -ContentType "application/json").token

# Usar token em requisição
$headers = @{ Authorization = "Token $token" }
Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/users/me/" -Headers $headers
```

---

## 📚 RECURSOS ADICIONAIS

### 🔗 Links Úteis
- **Django REST Framework**: https://www.django-rest-framework.org/
- **drf-spectacular**: https://drf-spectacular.readthedocs.io/
- **OpenAPI Specification**: https://swagger.io/specification/
- **PostgreSQL Docs**: https://www.postgresql.org/docs/
- **Docker Compose**: https://docs.docker.com/compose/

### 📖 Documentação do Projeto
- `README.md` - Este guia completo
- `backend/requirements.txt` - Dependências Python  
- `docker-compose.yml` - Configuração dos containers
- `backend/schema.yml` - Schema OpenAPI

---

## 🎯 RESUMO FINAL

### ✅ Status do Sistema
- **Swagger UI**: Configurado e funcional
- **Autenticação**: Token-based implementada
- **Permissões**: Sistema hierárquico completo
- **Endpoints**: CRUD completo para todas as entidades
- **Validações**: Regras de negócio implementadas
- **Documentação**: OpenAPI 3.0 atualizada

### 🚀 URLs Principais
- **API Docs**: http://127.0.0.1:8000/api/docs/
- **ReDoc**: http://127.0.0.1:8000/api/redoc/
- **Admin**: http://127.0.0.1:8000/admin/

### 💡 Próximos Passos
1. Pratique com os exemplos fornecidos
2. Explore diferentes tipos de usuário
3. Teste cenários de erro
4. Integre com aplicações frontend
5. Use para documentação de equipe

---

📅 **Última Atualização**: Julho 2025  
🔧 **Versão da API**: 1.0.0  
👨‍💻 **Sistema**: Top Pet System API  
🚀 **Status**: Totalmente Funcional  

🎉 **O sistema está pronto para uso em desenvolvimento e produção!**