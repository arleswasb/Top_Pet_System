#!/usr/bin/env python3
"""
Teste rápido das URLs corretas
"""

import requests

def test_correct_urls():
    print("🔍 TESTANDO URLs CORRETAS")
    
    urls_to_test = [
        ("http://localhost:8000/api/schema/", "Schema JSON"),
        ("http://localhost:8000/api/docs/", "Swagger UI"),
        ("http://localhost:8000/api/redoc/", "ReDoc"),
        ("http://localhost:8000/api/users/self-register/", "Self Register"),
        ("http://localhost:8000/api/auth/login/", "Auth Login"),
    ]
    
    for url, description in urls_to_test:
        try:
            response = requests.get(url, timeout=5)
            print(f"✅ {description}: {response.status_code}")
            
            if "schema" in url and response.status_code == 200:
                # Verificar se é JSON
                try:
                    response.json()
                    print("   📋 JSON válido")
                except:
                    print("   ⚠️  Não é JSON válido")
            
        except requests.exceptions.RequestException as e:
            print(f"❌ {description}: Erro - {e}")

if __name__ == "__main__":
    test_correct_urls()
