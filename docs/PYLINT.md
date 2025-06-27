# Pipeline de CI/CD - Pylint

## Configuração do Pylint

Este projeto utiliza Pylint para análise estática de código Python, configurado para reportar apenas **erros críticos** e ignorar problemas de formatação e estilo.

### Arquivos de Configuração

1. **`.github/workflows/ci-pylint.yml`** - Pipeline do GitHub Actions
2. **`backend/.pylintrc`** - Configurações do Pylint

### Configurações Ignoradas

O Pylint está configurado para ignorar os seguintes tipos de problemas:

#### Formatação e Estilo
- `line-too-long` - Linhas muito longas
- `trailing-whitespace` - Espaços em branco no final das linhas
- `missing-docstring` - Documentação ausente
- `invalid-name` - Nomes de variáveis inválidos

#### Importações
- `unused-import` - Importações não utilizadas
- `wildcard-import` - Importações com *
- `unused-wildcard-import` - Importações * não utilizadas
- `wrong-import-position` - Posição incorreta de importações
- `imported-auth-user` - Importação do modelo User do Django

#### Complexidade
- `too-many-locals` - Muitas variáveis locais
- `too-many-arguments` - Muitos argumentos
- `too-many-instance-attributes` - Muitos atributos de instância
- `too-many-branches` - Muitas ramificações
- `too-many-statements` - Muitas declarações

#### Django Específico
- `no-member` - Membros não encontrados (Django fields)
- `import-error` - Erros de importação (Django modules)

### O que o Pylint Reporta

O pipeline reporta apenas **erros críticos** que podem causar falhas na execução:

- Erros de sintaxe
- Referências a variáveis não definidas
- Erros de indentação críticos
- Problemas de lógica que impedem execução

### Execução Local

Para executar o Pylint localmente:

```bash
cd backend
pylint --errors-only arquivo.py
```

### Pipeline de CI

O pipeline executa duas verificações:

1. **Verificação Principal** - Falha se encontrar erros críticos
2. **Relatório Completo** - Sempre executa para monitoramento (não falha)

### Benefícios

- ✅ Detecta apenas problemas que realmente importam
- ✅ Não bloqueia desenvolvimento por questões de estilo
- ✅ Foco na qualidade funcional do código
- ✅ Pipeline rápido e eficiente
- ✅ Configuração padronizada para todo o projeto
