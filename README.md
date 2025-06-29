# 🐾 Top Pet System

Sistema de gestão veterinária moderno e completo para clínicas e hospitais veterinários.

## 🚀 Características Principais

- **Gestão de Pets**: Cadastro completo com fotos, histórico médico e dados do tutor
- **Agendamentos**: Sistema inteligente de agendamento de consultas e procedimentos
- **Prontuários Eletrônicos**: Registros médicos digitais seguros e organizados
- **Gestão de Usuários**: Sistema de permissões para veterinários, atendentes e tutores
- **API REST**: Interface moderna para integração com outros sistemas

## 🛠️ Tecnologias Utilizadas

- **Backend**: Django 4.2 + Django REST Framework
- **Banco de Dados**: PostgreSQL (produção) / SQLite (desenvolvimento)
- **Autenticação**: Token-based authentication
- **Documentação**: Swagger/OpenAPI
- **Testes**: Django TestCase + pytest
- **CI/CD**: GitHub Actions
- **Containerização**: Docker + Docker Compose

## 📊 Status dos Testes

![Tests](https://github.com/seu-usuario/Top_Pet_System/workflows/CI%20Pipeline%20-%20Lint%20e%20Testes/badge.svg)
![Coverage](https://img.shields.io/badge/coverage-85%25-brightgreen)
![Python](https://img.shields.io/badge/python-3.11-blue)
![Django](https://img.shields.io/badge/django-4.2-green)

**56 testes automatizados** executados a cada commit ✅

## 🚀 Instalação e Uso

### Pré-requisitos
- Python 3.11+
- PostgreSQL (opcional para desenvolvimento)
- Docker e Docker Compose (opcional)

### Instalação Local

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/Top_Pet_System.git
cd Top_Pet_System

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
### Realizando Testes Manualmente :

```bash
cd backend
python manage.py test              # Todos os testes
python manage.py test pets         # Apenas app pets
coverage run --source='.' manage.py test  # Com cobertura
```

### Usando Docker-Compose para rodar conteinerizado
### Comandos na pasta do projeto 

```bash
cd Top_Pet_System

# Construir e executar com Docker Compose
docker-compose up --build

# Acessar em http://localhost:8000
```

## 🧪 Executar Testes

### Dentro do docker-compose:
```powershell
cd backend
docker-compose exec web ./run_tests.sh --coverage      # Todos os testes com cobertura
TESTES INDIVIDUAIS
docker-compose exec web python manage.py test pets  #PETS
docker-compose exec web python manage.py test users  #USERS
docker-compose exec web python manage.py test agendamentos #agendamentos
docker-compose exec web python manage.py test prontuarios  #prontuarios
```

### Linux/macOS:
```bash
cd backend
./run_tests.sh --all               # Todos os testes
./run_tests.sh --coverage          # Com cobertura
```



## 📁 Estrutura do Projeto

```
Top_Pet_System/
├── backend/
│   ├── pets/              # App de gestão de pets
│   ├── agendamentos/      # App de agendamentos
│   ├── prontuarios/       # App de prontuários
│   ├── users/             # App de usuários
│   ├── top_pet/           # Configurações Django
│   └── manage.py
├── .github/workflows/     # CI/CD GitHub Actions
├── docker-compose.yml     # Configuração Docker
└── README.md
```

## 🔐 Permissões e Usuários

| Tipo de Usuário | Permissões |
|------------------|------------|
| **Admin** | Acesso total ao sistema |
| **Veterinário** | Gerenciar pets, prontuários, consultas |
| **Atendente** | Agendamentos, cadastros básicos |
| **Tutor** | Visualizar dados dos próprios pets |

## 📚 Documentação da API

A documentação completa da API está disponível em:
- **Swagger UI**: `http://localhost:8000/api/docs/`
- **Django**: `http://localhost:8000/admin/`

### Endpoints Principais:

- `GET /api/pets/` - Listar pets
- `POST /api/pets/` - Criar pet
- `GET /api/agendamentos/` - Listar agendamentos
- `POST /api/agendamentos/` - Criar agendamento
- `GET /api/prontuarios/` - Listar prontuários

## 🤝 Contribuindo

1. Fork o projeto
2. Crie sua branch (`git checkout -b feature/AmazingFeature`)
3. Execute os testes (`.\run_tests.ps1 -TestType all`)
4. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
5. Push para a branch (`git push origin feature/AmazingFeature`)
6. Abra um Pull Request

### Padrões de Código
- Siga PEP 8
- Cobertura de testes mínima: 80%
- Docstrings em funções complexas
- Type hints quando aplicável

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para detalhes.

## 📞 Contato

- **Desenvolvedor**: Seu Nome
- **Email**: seu.email@exemplo.com
- **LinkedIn**: [seu-perfil](https://linkedin.com/in/seu-perfil)

## 📈 Roadmap

- [ ] Interface web (React/Vue.js)
- [ ] Sistema de notificações
- [ ] Relatórios avançados
- [ ] Integração com laboratórios
- [ ] App mobile
- [ ] Sistema de pagamentos

---

⭐ **Se este projeto foi útil para você, considere dar uma estrela!**
