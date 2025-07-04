# Como Resetar o Banco de Dados - Top Pet System

Este documento explica como resetar completamente o banco de dados do projeto Top Pet System usando um script Python simples.

## ⚠️ IMPORTANTE

**ATENÇÃO**: Este script irá **DELETAR PERMANENTEMENTE** todos os dados do banco de dados atual. Certifique-se de fazer backup dos dados importantes antes de proceder.

## Script Python para Reset

Execute o script Python diretamente:

```bash
# Navegue até o diretório backend
cd f:\GitHub\Top_Pet_System\backend

# Execute o script
python reset_db_simple.py
```

**Características do Script:**
- ✅ Interface interativa com confirmações
- ✅ Verificações de segurança
- ✅ Limpeza completa de migrações e cache
- ✅ Criação opcional de superusuário
- ✅ Feedback claro do progresso

## O Que o Script Faz

O script executa as seguintes ações automaticamente:

1. **Remove o banco SQLite**: Deleta o arquivo `db.sqlite3`
2. **Limpa migrações**: Remove arquivos de migração antigos (mantém `__init__.py`)
3. **Limpa cache**: Remove diretórios `__pycache__`
4. **Cria novas migrações**: Gera migrações frescas baseadas nos models atuais
5. **Aplica migrações**: Cria as tabelas no novo banco
6. **Opcionalmente cria superusuário**: Para acessar o admin Django

## Quando Usar

Use o reset do banco de dados quando:

- ✅ Você fez mudanças significativas nos models e quer começar limpo
- ✅ O banco está corrompido ou com dados inconsistentes
- ✅ Você quer resetar para o estado inicial do desenvolvimento
- ✅ Há conflitos de migração que são difíceis de resolver
- ✅ Você quer limpar dados de teste/desenvolvimento

## Não Use Se

- ❌ Você tem dados de produção importantes
- ❌ Você não tem backup dos dados importantes
- ❌ Você só quer fazer pequenos ajustes nas migrações
- ❌ O projeto está em produção

## Após o Reset

Depois de resetar o banco:

1. **Execute o servidor**:
   ```bash
   python manage.py runserver
   ```

2. **Crie dados de teste** se necessário:
   ```bash
   python manage.py loaddata fixtures/inicial.json  # se houver fixtures
   ```

3. **Acesse o admin** (se criou superusuário):
   - URL: http://127.0.0.1:8000/admin/
   - Use as credenciais do superusuário criado

## Estrutura de Apps

O reset afeta os seguintes apps do projeto:
- `agendamentos` - Sistema de agendamentos
- `pets` - Cadastro de pets
- `users` - Usuários e perfis
- `prontuarios` - Prontuários médicos
- `configuracao` - Configurações do sistema

## Arquivos do Reset

O script criado para o reset:

- `reset_db_simple.py` - Script Python para reset do banco

## Troubleshooting

### Erro "Arquivo em uso"
Se aparecer erro dizendo que o arquivo `db.sqlite3` está em uso:
1. Feche o servidor Django (Ctrl+C)
2. Feche o PyCharm/VS Code se estiverem abertos
3. Feche qualquer ferramenta de banco de dados
4. Tente novamente

### Migrações não encontradas
Se algum app não tiver migrações, execute:
```bash
python manage.py makemigrations nome_do_app
```

## Backup Antes do Reset

Se você tem dados importantes, faça backup antes:

```bash
# Backup dos dados
python manage.py dumpdata > backup_dados.json

# Backup apenas de dados específicos
python manage.py dumpdata pets users > backup_principais.json
```

Para restaurar depois:
```bash
python manage.py loaddata backup_dados.json
```
