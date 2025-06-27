# Sistema de Proteção de Arquivos de Teste

## 🛡️ Sobre
Este sistema protege os arquivos de teste do projeto contra apagamento ou modificação não autorizada.

## 📁 Arquivos Protegidos
- `users/tests.py`
- `pets/tests.py`
- `pets/tests_unidade.py`
- `agendamentos/tests.py`
- `agendamentos/tests_integracao.py`
- `prontuarios/tests.py`
- `prontuarios/models.py`
- `prontuarios/serializers.py`
- `prontuarios/urls.py`
- `prontuarios/permissions.py`

## 🔧 Como Usar

### Criar Backup
```bash
cd backend
python protect_tests.py backup
```

### Verificar Integridade
```bash
cd backend
python protect_tests.py verify
```

### Restaurar Arquivos
```bash
cd backend
python protect_tests.py restore
```

## ⚡ Proteção Automática
- **Hook Pre-commit**: Verifica arquivos antes de cada commit
- **Backups**: Armazenados em `backend/test_backups/`
- **Checksums**: Salvos em `backend/test_checksums.json`

## 🚨 Em Caso de Problema
Se os arquivos de teste forem apagados:

1. Restaurar: `python protect_tests.py restore`
2. Verificar: `python protect_tests.py verify`
3. Criar novo backup: `python protect_tests.py backup`

## 📋 Status Atual
- ✅ Arquivos de teste restaurados
- ✅ Modelos de prontuários restaurados
- ✅ Serializers de prontuários restaurados
- ✅ URLs de prontuários restauradas
- ✅ Permissões de prontuários restauradas
- ✅ App prontuários adicionado ao settings.py
- ✅ Sistema de backup ativo
- ✅ Hook do Git configurado
- ✅ Checksums verificados

## 🔍 Investigação do Problema
O apagamento dos arquivos de teste pode ter sido causado por:
- Execução de comandos Django `startapp` que recriam templates
- Scripts de CI/CD mal configurados
- Conflitos de merge no Git
- Comandos de reset acidentais

## 🛠️ Prevenção
- Execute `python protect_tests.py verify` regularmente
- Sempre faça backup antes de grandes mudanças
- O hook do Git rejeitará commits que modifiquem os testes sem autorização
