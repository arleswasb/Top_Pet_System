name: Pull Request
description: Template para Pull Requests
title: ""
body:
  - type: markdown
    attributes:
      value: |
        ## 📋 Descrição

        Por favor, inclua um resumo das mudanças e qual issue foi resolvida. Inclua também a motivação e contexto relevante. Liste as dependências necessárias para esta mudança.

  - type: textarea
    id: description
    attributes:
      label: Resumo das Mudanças
      description: Descreva as principais mudanças implementadas
      placeholder: |
        - Implementei funcionalidade X
        - Corrigi bug Y
        - Atualizei documentação Z
    validations:
      required: true

  - type: input
    id: fixes
    attributes:
      label: Fixes Issues
      description: "Este PR resolve qual(is) issue(s)? (ex: Fixes #123)"
      placeholder: "Fixes #"

  - type: dropdown
    id: type
    attributes:
      label: Tipo de Mudança
      description: Que tipo de mudança este PR introduz?
      options:
        - 🐛 Bug fix (correção que resolve um problema)
        - ✨ Nova funcionalidade (mudança que adiciona funcionalidade)
        - 💥 Breaking change (correção ou funcionalidade que quebra funcionalidade existente)
        - 📚 Documentação (mudanças apenas na documentação)
        - 🎨 Refatoração (mudança de código que não corrige bug nem adiciona funcionalidade)
        - ⚡ Performance (mudança que melhora performance)
        - 🧪 Testes (adição ou correção de testes)
        - 🔧 Configuração (mudanças em arquivos de configuração)
    validations:
      required: true

  - type: checkboxes
    id: testing
    attributes:
      label: 🧪 Testes
      description: Como você testou suas mudanças?
      options:
        - label: Testes unitários passando
        - label: Testes de integração passando
        - label: Testes manuais realizados
        - label: Testado em diferentes navegadores (se aplicável)
        - label: Testado em diferentes dispositivos (se aplicável)

  - type: checkboxes
    id: checklist
    attributes:
      label: ✅ Checklist
      description: Confirme que você verificou todos os itens
      options:
        - label: Meu código segue as diretrizes de estilo do projeto
          required: true
        - label: Realizei uma auto-revisão do meu código
          required: true
        - label: Comentei partes complexas do código
          required: true
        - label: Fiz mudanças correspondentes na documentação
          required: true
        - label: Minhas mudanças não geram novos warnings
          required: true
        - label: Adicionei testes que provam que minha correção é efetiva ou que minha funcionalidade funciona
          required: true
        - label: Testes unitários novos e existentes passam localmente com minhas mudanças
          required: true
        - label: Verifiquei que não há dependências conflitantes
          required: true

  - type: textarea
    id: additional_notes
    attributes:
      label: 📝 Notas Adicionais
      description: Adicione qualquer informação adicional sobre este PR
      placeholder: |
        - Considerações especiais
        - Próximos passos
        - Dependências externas

  - type: textarea
    id: screenshots
    attributes:
      label: 📸 Screenshots (se aplicável)
      description: Adicione screenshots para mudanças na UI
