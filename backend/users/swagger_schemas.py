# users/swagger_schemas.py

from drf_spectacular.utils import OpenApiExample

# Exemplos para o endpoint de auto-cadastro
USER_SELF_REGISTER_EXAMPLES = [
    OpenApiExample(
        'Cadastro Completo',
        description='Exemplo com todos os campos (obrigatórios e opcionais) preenchidos',
        value={
            "username": "joao_silva",
            "password": "minhasenha123",
            "confirm_password": "minhasenha123", 
            "email": "joao@email.com",
            "first_name": "João",
            "last_name": "Silva",
            "telefone": "(11) 99999-9999",
            "endereco": "Rua das Flores, 123 - São Paulo/SP"
        }
    ),
    OpenApiExample(
        'Cadastro Mínimo',
        description='Apenas campos obrigatórios - telefone e endereço são OPCIONAIS',
        value={
            "username": "maria_santos", 
            "password": "senha123",
            "confirm_password": "senha123",
            "email": "maria@email.com",
            "first_name": "Maria",
            "last_name": "Santos"
        }
    ),
    OpenApiExample(
        'Apenas com Telefone',
        description='Campos obrigatórios + telefone (endereço continua opcional)',
        value={
            "username": "carlos_oliveira", 
            "password": "novasenha456",
            "confirm_password": "novasenha456",
            "email": "carlos@email.com",
            "first_name": "Carlos",
            "last_name": "Oliveira",
            "telefone": "(21) 88888-8888"
        }
    )
]

# Descrições detalhadas para campos
FIELD_DESCRIPTIONS = {
    'username': 'Nome de usuário único no sistema (obrigatório)',
    'password': 'Senha com no mínimo 8 caracteres (obrigatório)',
    'confirm_password': 'Confirmação da senha - deve ser idêntica ao campo password (obrigatório)',
    'email': 'Email válido para contato e comunicações (obrigatório)',
    'first_name': 'Primeiro nome do usuário (obrigatório)',
    'last_name': 'Sobrenome do usuário (obrigatório)',
    'telefone': 'Telefone de contato - pode ficar em branco (OPCIONAL)',
    'endereco': 'Endereço residencial completo - pode ficar em branco (OPCIONAL)'
}

# Schema personalizado para auto-cadastro
SELF_REGISTER_SCHEMA = {
    'summary': 'Auto-cadastro de cliente',
    'description': """
    **🔓 Endpoint público para auto-cadastro** de novos usuários como CLIENTE.
    
    **✅ CAMPOS OBRIGATÓRIOS:**
    - `username`: Nome de usuário único
    - `password`: Senha com no mínimo 8 caracteres  
    - `confirm_password`: Confirmação da senha
    - `email`: Email válido para contato
    - `first_name`: Primeiro nome
    - `last_name`: Sobrenome
    
    **⚪ CAMPOS OPCIONAIS:**
    - `telefone`: Telefone de contato (pode ficar vazio)
    - `endereco`: Endereço residencial (pode ficar vazio)
    
    **ℹ️ Observações importantes:**
    - ✅ Não requer autenticação (endpoint público)
    - 🔒 O tipo de usuário é automaticamente definido como CLIENTE
    - ❌ Campos CRMV e especialidade NÃO se aplicam a este endpoint
    - 📧 Email deve ser único no sistema
    - 👤 Username deve ser único no sistema
    - 🔐 Senhas devem ter pelo menos 8 caracteres
    
    **💡 Dica:** Os campos telefone e endereço podem ser preenchidos posteriormente no perfil do usuário.
    """,
    'tags': ['Autenticação'],
    'examples': USER_SELF_REGISTER_EXAMPLES
}

# Schemas para os endpoints de reset de senha
PASSWORD_RESET_REQUEST_SCHEMA = {
    'summary': 'Solicitar reset de senha',
    'description': """
    **📧 Endpoint público para solicitar reset de senha.**
    
    **Como funciona:**
    1. 📤 Envie o email do usuário
    2. 📬 Um token será enviado por email
    3. 🔐 Use o token nos próximos endpoints para definir nova senha
    
    **✅ CAMPO OBRIGATÓRIO:**
    - `email`: Email do usuário cadastrado no sistema
    
    **ℹ️ Observações importantes:**
    - ✅ Não requer autenticação (endpoint público)
    - 📧 Email deve estar cadastrado no sistema
    - ⏰ Token tem validade limitada
    - 🔒 Apenas um token ativo por vez por usuário
    """,
    'tags': ['Autenticação']
}

PASSWORD_RESET_CONFIRM_SCHEMA = {
    'summary': 'Confirmar reset de senha',
    'description': """
    **🔐 Confirma o reset de senha com o token recebido por email.**
    
    **Como usar:**
    1. 📧 Use o token recebido por email
    2. 🔑 Defina a nova senha
    3. ✅ Senha será alterada imediatamente
    
    **✅ CAMPOS OBRIGATÓRIOS:**
    - `token`: Token recebido por email
    - `password`: Nova senha (mínimo 8 caracteres)
    
    **ℹ️ Observações importantes:**
    - ✅ Não requer autenticação (endpoint público) 
    - 🔐 Token deve ser válido e não expirado
    - 🔑 Nova senha deve atender aos critérios de segurança
    - ⚡ Token é consumido após uso (não pode ser reutilizado)
    """,
    'tags': ['Autenticação']
}

PASSWORD_RESET_VALIDATE_SCHEMA = {
    'summary': 'Validar token de reset',
    'description': """
    **✅ Valida se um token de reset de senha é válido.**
    
    **Uso recomendado:**
    - 🔍 Verificar se token é válido antes de mostrar tela de nova senha
    - ⏰ Verificar se token não expirou
    - 🛡️ Validação de segurança adicional
    
    **✅ CAMPO OBRIGATÓRIO:**
    - `token`: Token a ser validado
    
    **ℹ️ Observações importantes:**
    - ✅ Não requer autenticação (endpoint público)
    - 🔍 Apenas valida, não consome o token
    - ⏰ Retorna informações sobre validade
    """,
    'tags': ['Autenticação']
}
