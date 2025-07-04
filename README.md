# 🐾 Top Pet System

Sistema de gestão veterinária moderno e completo para clínicas e hospitais veterinários.

## 🚀 Características Principais

- **Gestão de Pets**: Cadastro completo com fotos, histórico médico e dados do tutor
- **Agendamentos**: Sistema inteligente de agendamento de consultas e procedimentos
- **Prontuários Eletrônicos**: Registros médicos digitais seguros e organizados
- **Gestão de Usuários**: Sistema de permissões para veterinários, atendentes e tutores
- **API REST**: Interface moderna para integração com outros sistemas
- **Interface Swagger**: Documentação interativa completa da API

## 🛠️ Tecnologias Utilizadas

- **Backend**: Django 4.2 + Django REST Framework
- **Banco de Dados**: PostgreSQL (produção) / SQLite (desenvolvimento)
- **Autenticação**: Token-based authentication
- **Documentação**: Swagger/OpenAPI com drf-spectacular
- **Testes**: Django TestCase + Coverage.py (85%+ cobertura)
- **CI/CD**: GitHub Actions com Pylint
- **Containerização**: Docker + Docker Compose

## 📊 Status dos Testes

![Tests](https://github.com/seu-usuario/Top_Pet_System/workflows/CI%20Pipeline%20-%20Lint%20e%20Testes/badge.svg)
![Coverage](https://img.shields.io/badge/coverage-85%25-brightgreen)
![Python](https://img.shields.io/badge/python-3.11-blue)
![Django](https://img.shields.io/badge/django-4.2-green)

**83 testes automatizados** executados a cada commit ✅

## 🎭 Tipos de Usuário e Permissões

| Tipo de Usuário | Permissões | Funcionalidades |
|------------------|------------|----------------|
| **👑 Admin** | Acesso total ao sistema | Gerenciar todos os usuários, logs, configurações |
| **👨‍💼 Funcionário** | Gerenciar pets de clientes, agendamentos | Criar pets para clientes, visualizar todos os pets |
| **👨‍⚕️ Veterinário** | Gerenciar pets, prontuários, consultas | Criar/editar prontuários, consultas, CRMV obrigatório |
| **👤 Cliente** | Visualizar dados dos próprios pets | Ver pets, agendamentos próprios, auto-cadastro |

## 🚀 Instalação e Uso

### Pré-requisitos
- Python 3.11+
- PostgreSQL (opcional para desenvolvimento)
- Docker e Docker Compose (recomendado)

### 🐳 Usando Docker-Compose (Recomendado)

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/Top_Pet_System.git
cd Top_Pet_System

# Construir e executar com Docker Compose
docker-compose up -d --build

# Criar o super usuário
docker-compose exec web python manage.py createsuperuser

# Acessar em http://localhost:8000
```

### 💻 Instalação Local

```bash
# Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/macOS
# ou
venv\Scripts\activate     # Windows

# Instalar dependências
cd backend
pip install -r requirements.txt

# Configurar banco de dados
python manage.py migrate

# Criar superusuário
python manage.py createsuperuser


# Executar servidor
python manage.py runserver
```

## 🧪 Executar Testes

### Testes Locais

```bash
cd backend

# Todos os testes
python manage.py test

# Testes por app
python manage.py test pets
python manage.py test users
python manage.py test agendamentos
python manage.py test prontuarios

# Testes com cobertura
coverage run --source='.' manage.py test
coverage report
coverage html  # Gera relatório HTML em htmlcov/
```

### Testes no Docker

```bash
# Todos os testes com cobertura
docker-compose exec web coverage run --source='.' manage.py test
docker-compose exec web coverage report

# Testes individuais
docker-compose exec web python manage.py test pets
docker-compose exec web python manage.py test users
docker-compose exec web python manage.py test agendamentos
docker-compose exec web python manage.py test prontuarios
```

### Scripts de Teste

#### Windows PowerShell:
```powershell
.\run_tests.ps1 -TestType all        # Todos os testes
.\run_tests.ps1 -TestType coverage   # Com cobertura
.\run_tests.ps1 -TestType pets       # Apenas pets
```

#### Linux/macOS:
```bash
./run_tests.sh --all                 # Todos os testes
./run_tests.sh --coverage            # Com cobertura
./run_tests.sh --app pets           # Apenas pets
```

## 📚 Documentação da API

### 🌐 URLs Disponíveis:
- **🔥 Swagger UI (Interface Principal)**: http://127.0.0.1:8000/api/docs/
- **📖 ReDoc (Documentação Alternativa)**: http://127.0.0.1:8000/api/redoc/
- **🔧 Schema OpenAPI (JSON)**: http://127.0.0.1:8000/api/schema/
- **⚙️ Django Admin**: http://127.0.0.1:8000/admin/

### 🎫 Credenciais de Teste:

**👑 ADMINISTRADOR:**
- Username: `admin`
- Password: `admin123`
- Token: `297af8e30d64f2cee360713bfecb6e8703ca5232`

**👤 CLIENTE:**
- Username: `testuser`
- Password: `testpass123`
- Token: `0e012c51b22276f49cbb08701af45911cf39f35d`

### 📂 Grupos de Endpoints no Swagger UI:

#### 🔐 **Autenticação** - Login e Registro
- `POST /api/users/register/` - Auto-cadastro como cliente
- `POST /api/auth/token/` - Obter token de autenticação
- `POST /api/auth/password-reset/` - Solicitar reset de senha
- `POST /api/auth/password-reset/confirm/` - Confirmar reset de senha
- `POST /api/auth/password-reset/validate_token/` - Validar token de reset

#### 👥 **Usuários** - Gestão de Usuários
- `GET /api/me/` - Ver próprio perfil
- `GET /api/admin/users/` - Listar usuários (admin)
- `GET /api/funcionario/users/` - Listar clientes (funcionário)
- `POST /api/funcionario/create-user/` - Funcionário criar usuário
- `POST /api/admin/create-user/` - Admin criar usuário
- `GET /api/logs/` - Visualizar logs (admin)

#### 🐕 **Pets** - Gerenciamento de Animais
- `GET /api/pets/` - Listar todos os pets
- `POST /api/pets/` - Criar novo pet
- `GET /api/pets/{id}/` - Detalhes de um pet específico
- `PATCH /api/pets/{id}/` - Atualização parcial
- `DELETE /api/pets/{id}/` - Remover pet

#### 📅 **Agendamentos** - Sistema de Agendamentos
- `GET /api/agendamentos/` - Listar agendamentos
- `POST /api/agendamentos/` - Criar agendamento
- `GET /api/agendamentos/{id}/` - Detalhes do agendamento
- `PATCH /api/agendamentos/{id}/` - Atualização parcial
- `DELETE /api/agendamentos/{id}/` - Cancelar agendamento

#### 📋 **Prontuários** - Prontuários Médicos
- `GET /api/prontuarios/` - Listar prontuários
- `POST /api/prontuarios/` - Criar prontuário
- `GET /api/prontuarios/{id}/` - Detalhes do prontuário
- `PATCH /api/prontuarios/{id}/` - Atualização parcial
- `DELETE /api/prontuarios/{id}/` - Remover prontuário

## 🔐 Regras de Negócio e Segurança

### 🛡️ Validações Implementadas
- **Email único**: Não pode haver emails duplicados
- **Username único**: Não pode haver usernames duplicados
- **CRMV obrigatório**: Para veterinários, o CRMV deve ser informado
- **Senha forte**: Deve atender aos critérios do Django
- **Token único**: Cada usuário tem um token único para API

### 🚫 Restrições de Segurança
- Auto-cadastro público só permite criação de CLIENTES
- Funcionários não podem criar administradores
- Usuários só acessam dados próprios (exceto staff)
- Validação de permissões em cada endpoint
- Tokens obrigatórios para maioria dos endpoints

### 🔄 Fluxos de Trabalho

#### Cliente:
```
Auto-cadastro → Perfil CLIENTE → Gerenciar próprios pets → Fazer agendamentos
```

#### Funcionário:
```
Admin cria funcionário → Pode criar clientes/veterinários → Gerenciar sistema
```

#### Administrador:
```
Controle total → Criar qualquer tipo → Ativar/desativar → Ver logs
```

## 📁 Estrutura do Projeto

```
Top_Pet_System/
├── backend/
│   ├── pets/              # App de gestão de pets
│   │   ├── models.py      # Modelos de dados
│   │   ├── serializers.py # Serializers da API
│   │   ├── views.py       # Views da API
│   │   ├── permissions.py # Permissões customizadas
│   │   └── tests/         # Testes unitários e integração
│   ├── agendamentos/      # App de agendamentos
│   ├── prontuarios/       # App de prontuários
│   ├── users/             # App de usuários e perfis
│   ├── top_pet/           # Configurações Django
│   │   ├── settings.py    # Configurações principais
│   │   ├── urls.py        # URLs principais
│   │   └── wsgi.py        # WSGI para deployment
│   ├── requirements.txt   # Dependências Python
│   └── manage.py
├── .github/workflows/     # CI/CD GitHub Actions
│   └── ci-pylint.yml      # Pipeline de testes e lint
├── docs/                  # Documentação
│   ├── PYLINT.md         # Configurações do Pylint
│   └── API.md            # Documentação da API
├── docker-compose.yml     # Configuração Docker
├── Dockerfile            # Imagem Docker do backend
└── README.md
```

## ⚙️ Configuração de Desenvolvimento

### Variáveis de Ambiente

Crie um arquivo `.env` no diretório `backend/`:

```env
DEBUG=True
SECRET_KEY=sua-chave-secreta-aqui
DATABASE_URL=postgresql://user:password@localhost:5432/top_pet_db
ALLOWED_HOSTS=localhost,127.0.0.1
```

### Configuração do Banco de Dados

#### PostgreSQL (Recomendado para produção)
```bash
# Instalar PostgreSQL
# Criar banco de dados
createdb top_pet_db

# Configurar no settings.py ou .env
DATABASE_URL=postgresql://user:password@localhost:5432/top_pet_db
```

#### SQLite (Padrão para desenvolvimento)
```python
# settings.py - Configuração padrão
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

## 🎨 Qualidade de Código

### Pylint
O projeto usa Pylint configurado para reportar apenas erros críticos:

```bash
cd backend
pylint --errors-only pets/
```

### Coverage
Meta de cobertura de testes: **80%**

```bash
coverage run --source='.' manage.py test
coverage report --fail-under=80
```

### Pre-commit Hooks
```bash
pip install pre-commit
pre-commit install
```

## 🛠️ Comandos Úteis

### 🐳 Docker Commands:
```bash
# Iniciar containers
docker-compose up -d

# Ver logs do backend
docker-compose logs web

# Acessar shell do container
docker-compose exec web bash

# Executar migrações
docker-compose exec web python manage.py migrate

# Backup do banco
docker-compose exec db pg_dump -U postgres postgres > backup.sql
```

### 🔧 Management Commands:
```bash
# Ver migrações pendentes
python manage.py showmigrations

# Executar shell do Django
python manage.py shell

# Executar testes
python manage.py test

# Verificar sistema
python manage.py check
```

### 🔍 Comandos PowerShell para Testes:
```powershell
# Testar endpoint público (registro)
$body = @{
    username = "teste_ps"
    email = "teste@email.com"
    password = "senha123"
    confirm_password = "senha123"
    first_name = "Teste"
    last_name = "PowerShell"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/register/" -Method POST -Body $body -ContentType "application/json"

# Obter token
$loginBody = @{
    username = "admin"
    password = "admin123"
} | ConvertTo-Json

$token = (Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/auth/token/" -Method POST -Body $loginBody -ContentType "application/json").token

# Usar token em requisição
$headers = @{ Authorization = "Token $token" }
Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/me/" -Headers $headers
```

## 🤝 Contribuindo

1. Fork o projeto
2. Crie sua branch (`git checkout -b feature/AmazingFeature`)
3. Execute os testes (`python manage.py test`)
4. Verifique a cobertura (`coverage run --source='.' manage.py test`)
5. Commit suas mudanças (`git commit -m 'Add: nova funcionalidade'`)
6. Push para a branch (`git push origin feature/AmazingFeature`)
7. Abra um Pull Request

### Padrões de Código
- Siga PEP 8 para estilo de código
- Cobertura de testes mínima: 80%
- Docstrings em funções e classes complexas
- Type hints quando aplicável
- Commits semânticos (feat:, fix:, docs:, etc.)

## 🚀 Deploy

### Docker em Produção
```bash
# Build da imagem
docker build -t top-pet-system .

# Run com banco PostgreSQL
docker-compose -f docker-compose.prod.yml up -d
```

### Heroku
```bash
# Instalar Heroku CLI
# Login no Heroku
heroku login

# Criar aplicação
heroku create top-pet-system

# Configurar banco PostgreSQL
heroku addons:create heroku-postgresql:hobby-dev

# Deploy
git push heroku main
```

## 📊 Monitoramento

### Métricas de Qualidade
- **Cobertura de Testes**: 85%+
- **Testes Automatizados**: 83 testes
- **Tempo de Build**: < 3 minutos
- **Pylint Score**: Apenas erros críticos

### Logs
```bash
# Logs do Docker
docker-compose logs -f web

# Logs do Django
tail -f backend/logs/django.log
```

## 🎯 Exemplos de Uso da API

### 📝 Criar um Pet
```json
POST /api/pets/
{
  "nome": "Rex",
  "especie": "Cachorro",
  "raca": "Golden Retriever",
  "data_de_nascimento": "2020-05-15",
  "sexo": "MACHO",
  "observacoes": "Pet muito carinhoso"
}
```

### 🆕 Registrar Novo Cliente
```json
POST /api/register/
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

### 📅 Criar Agendamento
```json
POST /api/agendamentos/
{
  "pet": 1,
  "data_hora": "2024-12-01T14:30:00Z",
  "tipo_servico": "Consulta",
  "observacoes": "Checkup de rotina"
}
```

## 📚 Recursos Adicionais

### 🔗 Links Úteis:
- **Django REST Framework**: https://www.django-rest-framework.org/
- **drf-spectacular**: https://drf-spectacular.readthedocs.io/
- **OpenAPI Specification**: https://swagger.io/specification/
- **PostgreSQL Docs**: https://www.postgresql.org/docs/
- **Docker Compose**: https://docs.docker.com/compose/

### 📖 Documentação Relacionada:
- `docs/PYLINT.md` - Configurações do Pylint e testes com cobertura
- `README2.txt` - Guia completo do Swagger UI
- `backend/requirements.txt` - Dependências Python
- `docker-compose.yml` - Configuração dos containers

### 🎓 Próximos Passos de Aprendizado:
1. **Explorar Swagger UI**: http://127.0.0.1:8000/api/docs/
2. **Estudar modelos de dados**: Arquivos `models.py`
3. **Analisar serializers**: Arquivos `serializers.py`
4. **Entender views**: Arquivos `views.py`
5. **Revisar permissões**: Arquivos `permissions.py`

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para detalhes.

## 📞 Contato

- **Desenvolvedor**: Seu Nome
- **Email**: seu.email@exemplo.com
- **LinkedIn**: [seu-perfil](https://linkedin.com/in/seu-perfil)
- **GitHub**: [seu-usuario](https://github.com/seu-usuario)

## 📈 Roadmap

### Próximas Versões
- [ ] **v2.0**: Interface web (React/Vue.js)
- [ ] **v2.1**: Sistema de notificações em tempo real
- [ ] **v2.2**: Relatórios avançados e dashboards
- [ ] **v2.3**: Integração com laboratórios externos
- [ ] **v3.0**: App mobile (React Native/Flutter)
- [ ] **v3.1**: Sistema de pagamentos e faturas
- [ ] **v3.2**: IA para diagnósticos assistidos

### Funcionalidades em Desenvolvimento
- [ ] Autenticação OAuth2
- [ ] Sistema de backup automático
- [ ] API versioning
- [ ] Cache Redis
- [ ] Monitoramento com Sentry

---

## ✅ ATUALIZAÇÃO - SWAGGER UI TOTALMENTE CONFIGURADO! (30/06/2025)

### 🎯 O QUE FOI IMPLEMENTADO:
✅ **Swagger UI configurado** e acessível em http://127.0.0.1:8000/api/docs/
✅ **Autenticação por token** implementada e testada
✅ **Agrupamento por Tags**: Endpoints organizados logicamente
✅ **Regras de negócio** documentadas (CLIENTE, FUNCIONARIO, VETERINARIO, ADMIN)
✅ **Permissões customizadas** configuradas por tipo de usuário
✅ **Endpoints completos** para pets, agendamentos, prontuários e usuários
✅ **Exemplos práticos** fornecidos para todos os casos de uso
✅ **Troubleshooting** completo para resolução de problemas
✅ **Comandos úteis** para desenvolvimento e manutenção

### 📂 GRUPOS NO SWAGGER UI:
1. **🔐 Autenticação** - Login, registro de clientes
2. **👥 Usuários** - Gestão de perfis e permissões
3. **🐕 Pets** - Cadastro e gestão de animais
4. **🩺 Serviços** - Catálogo de serviços veterinários
5. **📅 Agendamentos** - Sistema de consultas e serviços
6. **📋 Prontuários** - Histórico médico dos pets

**🎉 O sistema está pronto para uso em desenvolvimento e produção!**

---

⭐ **Se este projeto foi útil para você, considere dar uma estrela!**

[![GitHub stars](https://img.shields.io/github/stars/seu-usuario/Top_Pet_System.svg?style=social&label=Star)](https://github.com/seu-usuario/Top_Pet_System)
