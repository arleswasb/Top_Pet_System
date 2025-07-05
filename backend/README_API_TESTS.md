# 🚀 Simulação CRUD - Top Pet System API

Este conjunto de scripts permite testar completamente a API do Top Pet System com relatórios detalhados.

## 📁 Arquivos Criados

### 1. `test_api_simulation.py` - Simulador Principal
Script principal que executa todos os testes CRUD da API:
- ✅ Autenticação (registro/login)
- ✅ CRUD de Usuários 
- ✅ CRUD de Pets
- ✅ CRUD de Serviços
- ✅ CRUD de Prontuários
- ✅ CRUD de Agendamentos
- ✅ Endpoints de Configuração
- ✅ Endpoints do Sistema

### 2. `analyze_test_report.py` - Analisador de Resultados
Analisa os resultados dos testes e gera relatórios avançados:
- 📊 Análise de Performance
- 🎯 Cobertura de Testes
- ⏱️ Padrões Temporais
- 🚨 Análise de Erros
- 📋 Resumo Executivo

### 3. `run_api_tests.py` - Script de Configuração
Script que prepara o ambiente e executa tudo automaticamente:
- 🔍 Verificação de dependências
- 🗄️ Preparação do banco de dados
- 📝 Criação de dados básicos
- 🚀 Execução da simulação
- 📊 Análise dos resultados

## 🎯 Como Usar

### Opção 1: Execução Automática (Recomendada)
```bash
python run_api_tests.py
```
Este comando executa todo o processo automaticamente.

### Opção 2: Execução Manual
```bash
# 1. Executar apenas a simulação
python test_api_simulation.py

# 2. Analisar resultados
python analyze_test_report.py

# 3. Ver relatório JSON formatado
cat api_test_report.json | python -m json.tool
```

### Opção 3: Análise de Relatório Específico
```bash
python analyze_test_report.py --file meu_relatorio.json
```

## 📊 Output Esperado

### Console Output
O script mostra em tempo real:
- ✅ Rotas testadas com sucesso (verde)
- ❌ Rotas com erro (vermelho)
- ℹ️ Informações importantes (azul)
- ⚠️ Avisos (amarelo)

### Relatório JSON
Arquivo `api_test_report.json` contém:
```json
{
  "total_tests": 45,
  "passed": 43,
  "failed": 2,
  "routes_tested": [
    {
      "method": "POST",
      "endpoint": "/api/auth/register/",
      "status_code": 201,
      "expected": 201,
      "success": true,
      "duration": 0.156,
      "timestamp": "2025-07-04T14:30:15.123456",
      "data_sent": {...}
    }
  ],
  "errors": [...],
  "total_duration": 12.345
}
```

## 🔍 Análises Disponíveis

### 1. Resumo Executivo
- Taxa de sucesso geral
- Tempo total de execução
- Status geral dos testes
- Recomendações

### 2. Análise de Performance
- Tempo médio por endpoint
- Rotas mais lentas/rápidas
- Estatísticas por método HTTP

### 3. Cobertura de Testes
- Módulos testados
- Endpoints cobertos
- Métodos HTTP utilizados

### 4. Análise de Erros
- Tipos de erro encontrados
- Rotas com problemas
- Frequência de erros

## 🛤️ Rotas Testadas

### Autenticação
- `POST /api/auth/register/` - Registro de usuário
- `POST /api/auth/login/` - Login

### Usuários
- `GET /api/users/` - Listar usuários
- `GET /api/users/{id}/` - Detalhe do usuário
- `PUT /api/users/{id}/` - Atualizar usuário
- `PATCH /api/users/{id}/` - Atualização parcial

### Pets
- `POST /api/pets/` - Criar pet
- `GET /api/pets/` - Listar pets
- `GET /api/pets/{id}/` - Detalhe do pet
- `PUT /api/pets/{id}/` - Atualizar pet
- `PATCH /api/pets/{id}/` - Atualização parcial
- `DELETE /api/pets/{id}/` - Deletar pet

### Serviços
- `POST /api/servicos/` - Criar serviço
- `GET /api/servicos/` - Listar serviços
- `GET /api/servicos/{id}/` - Detalhe do serviço
- `PUT /api/servicos/{id}/` - Atualizar serviço
- `PATCH /api/servicos/{id}/` - Atualização parcial
- `DELETE /api/servicos/{id}/` - Deletar serviço

### Prontuários
- `POST /api/prontuarios/` - Criar prontuário
- `GET /api/prontuarios/` - Listar prontuários
- `GET /api/prontuarios/{id}/` - Detalhe do prontuário
- `GET /api/pets/{id}/prontuarios/` - Prontuários por pet
- `PUT /api/prontuarios/{id}/` - Atualizar prontuário
- `PATCH /api/prontuarios/{id}/` - Atualização parcial
- `DELETE /api/prontuarios/{id}/` - Deletar prontuário

### Agendamentos
- `POST /api/agendamentos/` - Criar agendamento
- `GET /api/agendamentos/` - Listar agendamentos
- `GET /api/agendamentos/{id}/` - Detalhe do agendamento
- `GET /api/agendamentos/?data=YYYY-MM-DD` - Por data
- `GET /api/horarios-disponiveis/?data=YYYY-MM-DD` - Horários disponíveis
- `PUT /api/agendamentos/{id}/` - Atualizar agendamento
- `PATCH /api/agendamentos/{id}/` - Atualização parcial
- `DELETE /api/agendamentos/{id}/` - Deletar agendamento

### Configuração
- `GET /api/configuracao/horarios/` - Horários funcionamento
- `GET /api/configuracao/feriados/` - Feriados
- `POST /api/configuracao/horarios/` - Criar horário
- `POST /api/configuracao/feriados/` - Criar feriado

### Sistema
- `GET /api/` - Status do sistema
- `GET /api/docs/` - Documentação
- `GET /api/schema/` - Schema OpenAPI

## 🎛️ Configurações

### Variáveis de Ambiente
O script usa as configurações do arquivo `.env`:
- Banco PostgreSQL para API
- SQLite em memória para testes

### Dados de Teste
Objetos criados automaticamente:
- Usuário: `teste_api` / `senha123`
- Pets: Rex (Labrador), Mia (Siamês)
- Serviços: Consulta, Banho e Tosa, Vacinação
- Prontuários e Agendamentos conforme necessário

### Cleanup Automático
Todos os objetos criados são removidos ao final dos testes.

## 🔧 Troubleshooting

### Erro: "Django não configurado"
```bash
# Certifique-se de estar no diretório backend
cd backend
python run_api_tests.py
```

### Erro: "Módulo não encontrado"
```bash
# Instalar dependências
pip install -r requirements.txt
```

### Erro: "Token de autenticação inválido"
- Verificar se o endpoint de registro/login está funcionando
- Verificar configurações de autenticação no Django

### Performance Lenta
- Verificar se está usando SQLite em memória para testes
- Verificar conexão com PostgreSQL

## 📈 Interpretando Resultados

### Taxa de Sucesso
- **95-100%**: Excelente ✅
- **85-94%**: Boa 🟡
- **< 85%**: Precisa atenção 🔴

### Performance
- **< 0.1s**: Excelente 🟢
- **0.1-0.5s**: Boa 🟡
- **0.5-1.0s**: Aceitável 🟠
- **> 1.0s**: Lenta 🔴

### Próximos Passos
1. Corrigir erros encontrados
2. Otimizar rotas lentas
3. Adicionar testes de casos edge
4. Implementar testes de carga
5. Configurar CI/CD com estes testes

## 🚀 Desenvolvimento Contínuo

Este conjunto de scripts pode ser:
- Integrado ao CI/CD
- Executado antes de deploys
- Usado para monitoramento de performance
- Estendido com novos testes
- Customizado para diferentes ambientes

---

**Desenvolvido para Top Pet System API** 🐾
*Script criado para desenvolvedores seniores*
