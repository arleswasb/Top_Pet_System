# 🚀 Testes Automatizados - Top Pet System

Este diretório contém o workflow do GitHub Actions para automação de testes e CI/CD do projeto Top Pet System.

## 📋 Workflow Principal

### **ci.yml** - Pipeline Completo de CI/CD
**Execução:** A cada push/PR nas branches `main` e `develop`

**Jobs Organizados:**

#### 🔍 **lint** - Análise de Código
- Flake8 (style guide)
- Pylint (qualidade de código)
- Execução: ~2-3 minutos

#### ⚡ **unit-tests** - Testes Rápidos
- Testes unitários (`pets.tests_unidade`)
- Testes de validação (`pets.tests_validacao`)
- Execução: ~3-5 minutos

#### 🌐 **integration-tests** - Testes Completos
- Testes de integração (`pets.tests_integracao`)
- Testes de outros módulos (`users`, `agendamentos`)
- Relatório de cobertura de código
- Upload para Codecov
- Execução: ~5-8 minutos

#### 🔒 **security** - Verificações de Segurança
- Safety (vulnerabilidades de dependências)
- Bandit (vulnerabilidades de código)
- Execução: ~2-3 minutos

#### 🐳 **build** - Build e Deploy
- Build do container Docker
- Teste do container
- Só executa se todos os jobs anteriores passarem
- Execução: ~3-5 minutos

## ⚡ **Vantagens da Nova Estrutura:**

- **Paralelização**: Jobs executam em paralelo
- **Isolamento**: Falhas específicas são fáceis de identificar
- **Cache Otimizado**: Cada job tem cache específico
- **Visibilidade**: Interface clara do GitHub Actions
- **Eficiência**: Falha rápida se um job específico falha

## 📊 **Status dos Testes:**

- **58 testes totais** - Todos passando ✅
- **39 testes do módulo pets** organizados em:
  - 18 testes unitários
  - 13 testes de validação  
  - 16 testes de integração

## 📁 **Estrutura do Projeto:**

```
Top_Pet_System/
├── 📁 .github/                    # Configurações do GitHub
│   ├── 📁 ISSUE_TEMPLATE/         # Templates para issues
│   ├── 📁 workflows/              # GitHub Actions (CI/CD)
│   │   ├── ci.yml                 # Pipeline principal
│   │   └── README.md              # Este arquivo
│   └── pull_request_template.md   # Template para PRs
│
├── 📁 backend/                    # Aplicação Django
│   ├── 📁 agendamentos/           # App de agendamentos
│   │   ├── models.py              # Modelo Agendamento, Serviço
│   │   ├── views.py               # ViewSets da API
│   │   ├── serializers.py         # Serializers DRF
│   │   ├── permissions.py         # Permissões customizadas
│   │   ├── tests_integracao.py    # Testes de API
│   │   └── migrations/            # Migrações do banco
│   │
│   ├── 📁 pets/                   # App de pets (principal)
│   │   ├── models.py              # Modelo Pet
│   │   ├── views.py               # ViewSets da API
│   │   ├── serializers.py         # Serializers DRF
│   │   ├── permissions.py         # Permissões de pets
│   │   ├── tests_unidade.py       # 🧪 Testes unitários (18)
│   │   ├── tests_validacao.py     # ✅ Testes de validação (13)
│   │   ├── tests_integracao.py    # 🌐 Testes de API (16)
│   │   └── migrations/            # Migrações do banco
│   │
│   ├── 📁 prontuarios/            # App de prontuários médicos
│   │   ├── models.py              # Modelo Prontuario
│   │   ├── views.py               # ViewSets da API
│   │   ├── serializers.py         # Serializers DRF
│   │   ├── permissions.py         # Permissões de prontuários
│   │   ├── tests.py               # Testes do módulo
│   │   └── migrations/            # Migrações do banco
│   │
│   ├── 📁 users/                  # App de usuários
│   │   ├── models.py              # Profile (extensão de User)
│   │   ├── views.py               # ViewSets da API
│   │   ├── serializers.py         # Serializers DRF
│   │   ├── permissions.py         # Permissões de usuários
│   │   ├── signals.py             # Signals para Profile
│   │   ├── tests.py               # Testes do módulo
│   │   └── migrations/            # Migrações do banco
│   │
│   ├── 📁 top_pet/                # Configurações Django
│   │   ├── settings.py            # Configurações principais
│   │   ├── urls.py                # URLs principais
│   │   ├── wsgi.py                # WSGI para produção
│   │   └── asgi.py                # ASGI para async
│   │
│   ├── 📁 media/                  # Arquivos de mídia (fotos pets)
│   ├── 📁 logs/                   # Logs da aplicação
│   ├── manage.py                  # Comando principal Django
│   ├── requirements.txt           # Dependências Python
│   ├── dockerfile                # Configuração Docker
│   ├── run_tests.sh              # Script de testes (Linux/macOS)
│   ├── run_tests.ps1             # Script de testes (Windows)
│   ├── .flake8                   # Configuração flake8
│   ├── .coveragerc               # Configuração coverage
│   └── pytest.ini               # Configuração pytest
│
├── 📁 docs/                       # Documentação
│   └── PYLINT.md                 # Guia do Pylint
│
├── README.md                      # Documentação principal
├── TESTES_AUTOMATIZADOS.md       # Guia de testes
├── docker-compose.yml            # Orquestração Docker
├── .gitignore                    # Arquivos ignorados pelo Git
└── Top_Pet_System.code-workspace # Workspace do VS Code
```

### 🎯 **Módulos Principais:**

| Módulo | Responsabilidade | Testes |
|--------|------------------|--------|
| **pets** | Gestão de animais de estimação | 39 testes ✅ |
| **users** | Autenticação e perfis de usuário | 8 testes ✅ |
| **agendamentos** | Agendamentos e serviços | 11 testes ✅ |
| **prontuarios** | Prontuários médicos | Em desenvolvimento |

### 🧪 **Estrutura de Testes:**

```
backend/
├── pets/
│   ├── tests_unidade.py      # Lógica pura, cálculos, validações
│   ├── tests_validacao.py    # Validação de campos, regras
│   └── tests_integracao.py   # API, endpoints, permissões
├── users/
│   └── tests.py              # Testes gerais do módulo
├── agendamentos/
│   └── tests_integracao.py   # Testes de API
└── prontuarios/
    └── tests.py              # Testes básicos
```

## 🔗 **Endpoints da API:**

### 🐾 **Pets** (`/api/pets/`)

| Método | Endpoint | Descrição | Permissão |
|--------|----------|-----------|-----------|
| `GET` | `/api/pets/` | Lista pets do usuário | Autenticado |
| `POST` | `/api/pets/` | Criar novo pet | Cliente/Funcionário |
| `GET` | `/api/pets/{id}/` | Detalhes de um pet | Dono/Admin/Funcionário |
| `PUT` | `/api/pets/{id}/` | Atualizar pet completo | Dono/Admin |
| `PATCH` | `/api/pets/{id}/` | Atualizar pet parcial | Dono/Admin |
| `DELETE` | `/api/pets/{id}/` | Deletar pet | Dono/Admin |

**Campos do Pet:**
- `nome` (obrigatório)
- `especie` (obrigatório)
- `raca` (opcional)
- `sexo` (MACHO/FEMEA/DESCONHECIDO)
- `data_de_nascimento` (opcional)
- `foto` (upload de imagem)
- `observacoes` (opcional)
- `tutor` (auto-definido para clientes)

### 👥 **Usuários** (`/api/`)

| Método | Endpoint | Descrição | Permissão |
|--------|----------|-----------|-----------|
| `POST` | `/api/register/` | Registro de novo usuário | Público |
| `GET` | `/api/admin/users/` | Lista usuários (admin) | Admin |
| `POST` | `/api/admin/users/` | Criar usuário (admin) | Admin |
| `GET` | `/api/admin/users/{id}/` | Detalhes do usuário | Admin |
| `PUT` | `/api/admin/users/{id}/` | Atualizar usuário | Admin |
| `PATCH` | `/api/admin/users/{id}/` | Atualizar parcial | Admin |
| `DELETE` | `/api/admin/users/{id}/` | Deletar usuário | Admin |
| `POST` | `/api/admin/users/{id}/toggle_active/` | Ativar/desativar usuário | Admin |
| `GET` | `/api/logs/` | Visualizar logs do sistema | Admin |

**Perfis de Usuário:**
- `ADMIN` - Acesso total ao sistema
- `FUNCIONARIO` - Visualização e gerenciamento limitado
- `CLIENTE` - Apenas seus próprios pets

### 📅 **Agendamentos** (`/api/agendamentos/`)

| Método | Endpoint | Descrição | Permissão |
|--------|----------|-----------|-----------|
| `GET` | `/api/agendamentos/` | Lista agendamentos | Autenticado |
| `POST` | `/api/agendamentos/` | Criar agendamento | Cliente/Funcionário |
| `GET` | `/api/agendamentos/{id}/` | Detalhes agendamento | Cliente/Funcionário/Admin |
| `PUT` | `/api/agendamentos/{id}/` | Atualizar agendamento | Funcionário/Admin |
| `PATCH` | `/api/agendamentos/{id}/` | Atualizar parcial | Funcionário/Admin |
| `DELETE` | `/api/agendamentos/{id}/` | Cancelar agendamento | Cliente/Funcionário/Admin |

**Campos do Agendamento:**
- `pet` (obrigatório - ID do pet)
- `servico` (obrigatório - ID do serviço)
- `data_hora` (obrigatório - data e hora do agendamento)
- `status` (AGENDADO, CONCLUIDO, CANCELADO)
- `observacoes` (opcional)

### 🛠️ **Serviços** (`/api/servicos/`)

| Método | Endpoint | Descrição | Permissão |
|--------|----------|-----------|-----------|
| `GET` | `/api/servicos/` | Lista serviços | Autenticado |
| `POST` | `/api/servicos/` | Criar serviço | Admin |
| `GET` | `/api/servicos/{id}/` | Detalhes serviço | Autenticado |
| `PUT` | `/api/servicos/{id}/` | Atualizar serviço | Admin |
| `PATCH` | `/api/servicos/{id}/` | Atualizar parcial | Admin |
| `DELETE` | `/api/servicos/{id}/` | Deletar serviço | Admin |

**Campos do Serviço:**
- `nome` (obrigatório - máx 100 chars, único)
- `descricao` (opcional)
- `preco` (obrigatório - decimal)
- `duracao` (opcional - formato HH:MM:SS, padrão 30min)
- `disponivel` (opcional - padrão true)

### 🏥 **Prontuários** (`/api/prontuarios/`)

| Método | Endpoint | Descrição | Permissão |
|--------|----------|-----------|-----------|
| `GET` | `/api/prontuarios/` | Lista prontuários | Autenticado |
| `POST` | `/api/prontuarios/` | Criar prontuário | Funcionário/Admin |
| `GET` | `/api/prontuarios/{id}/` | Detalhes prontuário | Dono/Funcionário/Admin |
| `PUT` | `/api/prontuarios/{id}/` | Atualizar prontuário | Funcionário/Admin |
| `PATCH` | `/api/prontuarios/{id}/` | Atualizar parcial | Funcionário/Admin |
| `DELETE` | `/api/prontuarios/{id}/` | Deletar prontuário | Admin |

**Campos do Prontuário:**
- `pet` (obrigatório - ID do pet)
- `veterinario` (auto-definido ou especificado)
- `data_consulta` (auto-definida)
- `tipo_consulta` (ROTINA, EMERGENCIA, RETORNO, EXAME, CIRURGIA, VACINA)
- `peso` (opcional - em kg)
- `temperatura` (opcional - em °C)
- `motivo_consulta` (obrigatório)
- `exame_fisico` (opcional)
- `diagnostico` (opcional)
- `tratamento` (opcional)
- `medicamentos` (opcional)
- `observacoes` (opcional)
- `proxima_consulta` (opcional)

### 🔐 **Autenticação**

| Método | Endpoint | Descrição | Permissão |
|--------|----------|-----------|-----------|
| `POST` | `/api-token-auth/` | Login (obter token) | Público |
| `POST` | `/api/register/` | Registro de novo usuário | Público |

**Login - Exemplo:**
```json
{
  "username": "usuario@email.com",
  "password": "senha123"
}
```

**Registro - Exemplo:**
```json
{
  "username": "novo@email.com",
  "email": "novo@email.com", 
  "password": "senha123",
  "first_name": "Nome",
  "last_name": "Sobrenome",
  "profile": {
    "role": "CLIENTE"
  }
}
```

### 📊 **Exemplos de Uso:**

#### 🔐 Fazer Login:
```bash
curl -X POST http://localhost:8000/api-token-auth/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "usuario@email.com",
    "password": "senha123"
  }'
```

#### 👤 Registrar Usuário:
```bash
curl -X POST http://localhost:8000/api/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "novo@email.com",
    "email": "novo@email.com",
    "password": "senha123",
    "first_name": "João",
    "last_name": "Silva"
  }'
```

#### 🐾 Criar um Pet:
```bash
curl -X POST http://localhost:8000/api/pets/ \
  -H "Authorization: Token seu_token_aqui" \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "Rex",
    "especie": "Cachorro",
    "raca": "Labrador",
    "sexo": "MACHO",
    "data_de_nascimento": "2020-05-15",
    "observacoes": "Pet muito dócil"
  }'
```

#### 📋 Listar Pets:
```bash
curl -X GET http://localhost:8000/api/pets/ \
  -H "Authorization: Token seu_token_aqui"
```

#### 📅 Criar Agendamento:
```bash
curl -X POST http://localhost:8000/api/agendamentos/ \
  -H "Authorization: Token seu_token_aqui" \
  -H "Content-Type: application/json" \
  -d '{
    "pet": 1,
    "servico": 1,
    "data_hora": "2025-07-01T10:00:00Z",
    "observacoes": "Consulta de rotina"
  }'
```

#### 🛠️ Criar Serviço (Admin):
```bash
curl -X POST http://localhost:8000/api/servicos/ \
  -H "Authorization: Token admin_token_aqui" \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "Consulta Veterinária",
    "descricao": "Consulta geral com veterinário",
    "preco": "150.00",
    "duracao": "00:30:00",
    "disponivel": true
  }'
```

#### 🏥 Criar Prontuário (Funcionário/Admin):
```bash
curl -X POST http://localhost:8000/api/prontuarios/ \
  -H "Authorization: Token funcionario_token_aqui" \
  -H "Content-Type: application/json" \
  -d '{
    "pet": 1,
    "tipo_consulta": "ROTINA",
    "peso": "25.5",
    "temperatura": "38.5",
    "motivo_consulta": "Consulta de rotina e vacinação",
    "exame_fisico": "Animal saudável, sem alterações",
    "diagnostico": "Saudável",
    "tratamento": "Manter cuidados regulares",
    "medicamentos": "Nenhum prescrito"
  }'
```

#### 📊 Verificar Logs (Admin):
```bash
curl -X GET http://localhost:8000/api/logs/ \
  -H "Authorization: Token admin_token_aqui"
```

### 📨 **Códigos de Resposta HTTP:**

| Código | Descrição | Exemplo de Uso |
|--------|-----------|----------------|
| `200` | Sucesso (OK) | Listagem, atualização bem-sucedida |
| `201` | Criado | Pet/agendamento criado com sucesso |
| `204` | Sem conteúdo | Exclusão bem-sucedida |
| `400` | Requisição inválida | Dados faltando ou formato incorreto |
| `401` | Não autorizado | Token inválido ou expirado |
| `403` | Proibido | Sem permissão para a operação |
| `404` | Não encontrado | Pet/usuário não existe |
| `500` | Erro interno | Erro no servidor |

### 🔑 **Headers Obrigatórios:**

```bash
# Para endpoints autenticados
Authorization: Token seu_token_aqui

# Para requisições POST/PUT/PATCH (JSON)
Content-Type: application/json

# Para upload de arquivos (multipart)
Content-Type: multipart/form-data
```

### 📷 **Upload de Fotos de Pets:**

Para fazer upload de foto junto com dados do pet:

```bash
curl -X POST http://localhost:8000/api/pets/ \
  -H "Authorization: Token seu_token_aqui" \
  -F "nome=Rex" \
  -F "especie=Cachorro" \
  -F "raca=Labrador" \
  -F "sexo=MACHO" \
  -F "foto=@/caminho/para/foto.jpg"
```

**Formatos aceitos:** JPG, JPEG, PNG  
**Tamanho máximo:** Configurável (padrão: alguns MB)  
**Localização:** `/media/pets/` no servidor

### 🔍 **Filtros e Consultas:**

#### Filtrar pets por espécie:
```bash
curl -X GET "http://localhost:8000/api/pets/?especie=Cachorro" \
  -H "Authorization: Token seu_token_aqui"
```

#### Filtrar agendamentos por status:
```bash
curl -X GET "http://localhost:8000/api/agendamentos/?status=AGENDADO" \
  -H "Authorization: Token seu_token_aqui"
```

#### Buscar prontuários por pet:
```bash
curl -X GET "http://localhost:8000/api/prontuarios/?pet=1" \
  -H "Authorization: Token seu_token_aqui"
```

### 📄 **Paginação:**

A API suporta paginação automática. Exemplo de resposta:

```json
{
  "count": 25,
  "next": "http://localhost:8000/api/pets/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "nome": "Rex",
      "especie": "Cachorro"
    }
  ]
}
```

**Funcionalidades:**
- 🧪 Execução completa de testes
- 📊 Comentário automático com cobertura de código
- ⚡ Feedback rápido para desenvolvedores

## 🛠️ Scripts Locais

### Para Linux/macOS:
```bash
cd backend
chmod +x run_tests.sh
./run_tests.sh --all
```

### Para Windows:
```powershell
cd backend
.\run_tests.ps1 -TestType all
```

## 📊 Opções de Teste

| Comando | Descrição |
|---------|-----------|
| `--all` | Executa todos os testes e verificações |
| `--unit` | Apenas testes unitários |
| `--integration` | Apenas testes de integração |
| `--coverage` | Testes com relatório de cobertura |
| `--pytest` | Executa com pytest |
| `--lint` | Apenas verificação de código |

## 🔧 Configuração Local

### Pré-requisitos:
1. Python 3.11+
2. PostgreSQL (para testes de integração)
3. Docker (opcional, para testes completos)

### Instalação:
```bash
cd backend
pip install -r requirements.txt
```

### Configuração do Banco de Dados:
```bash
# Criar banco de teste
createdb top_pet_test

# Executar migrações
python manage.py migrate
```

## 📈 Métricas e Relatórios

### Cobertura de Código:
- **Meta mínima:** 80%
- **Meta para novos códigos:** 90%
- **Relatórios:** `htmlcov/index.html`

### Qualidade do Código:
- **Linter:** flake8
- **Complexidade máxima:** 10
- **Tamanho de linha:** 127 caracteres

### Segurança:
- **Safety:** Verificação de vulnerabilidades em dependências
- **Bandit:** Análise de segurança do código Python

## 🚨 Troubleshooting

### Erro: "Database connection failed"
```bash
# Verificar se PostgreSQL está rodando
pg_isready

# Criar banco de teste se não existir
createdb top_pet_test
```

### Erro: "Module not found"
```bash
# Reinstalar dependências
pip install -r requirements.txt
```

### Erro: "Permission denied" (Linux/macOS)
```bash
# Dar permissão de execução ao script
chmod +x run_tests.sh
```

## 🔄 Integração Contínua

O workflow `ci.yml` é executado automaticamente quando:

1. **Push para main/develop:** Executa pipeline completo com todos os jobs
2. **Abertura de PR:** Executa testes e análise de cobertura
3. **Manual:** Pode ser executado a qualquer momento via GitHub Actions

### Fluxo de Execução:
```
Push/PR → lint → unit-tests → integration-tests → security → build
           ↓         ↓              ↓              ↓         ↓
        flake8   testes      API/cobertura     safety   Docker
        pylint   rápidos                       bandit   
```

## 📝 Contribuindo

Ao contribuir com o projeto:

1. ✅ Execute os testes localmente antes do commit
2. 📊 Mantenha a cobertura de testes acima de 80%
3. 🔍 Garanta que o código passa no flake8
4. 🔒 Verifique se não há vulnerabilidades de segurança

## 🔗 Links Úteis

- [Documentação do pytest](https://docs.pytest.org/)
- [Documentação do Django Testing](https://docs.djangoproject.com/en/stable/topics/testing/)
- [GitHub Actions](https://docs.github.com/en/actions)
- [Coverage.py](https://coverage.readthedocs.io/)