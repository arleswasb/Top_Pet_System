#!/usr/bin/env python3
"""
Script de Configuração e Execução de Testes API
Prepara ambiente e executa simulação completa
"""

import os
import sys
import subprocess
import django
from pathlib import Path


def setup_django():
    """Configura ambiente Django"""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'top_pet.settings')
    django.setup()


def check_dependencies():
    """Verifica dependências necessárias"""
    print("🔍 Verificando dependências...")
    
    required_packages = [
        'django',
        'djangorestframework',
        'python-decouple'
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"  ✅ {package}")
        except ImportError:
            print(f"  ❌ {package}")
            missing.append(package)
    
    if missing:
        print(f"\n⚠️  Dependências faltando: {', '.join(missing)}")
        print("Execute: pip install -r requirements.txt")
        return False
    
    return True


def prepare_database():
    """Prepara banco de dados para testes"""
    print("\n🗄️  Preparando banco de dados...")
    
    try:
        # Aplicar migrações se necessário
        from django.core.management import execute_from_command_line
        
        print("  • Verificando migrações...")
        execute_from_command_line(['manage.py', 'migrate', '--verbosity=0'])
        print("  ✅ Banco de dados preparado")
        
        return True
    except Exception as e:
        print(f"  ❌ Erro ao preparar banco: {e}")
        return False


def create_test_data():
    """Cria dados básicos se necessário"""
    print("\n📝 Verificando dados básicos...")
    
    try:
        setup_django()
        
        from django.contrib.auth.models import User
        from configuracao.models import HorarioFuncionamento
        
        # Criar horários de funcionamento básicos se não existirem
        if not HorarioFuncionamento.objects.exists():
            print("  • Criando horários de funcionamento...")
            horarios = [
                {'dia_semana': 1, 'hora_abertura': '08:00', 'hora_fechamento': '18:00'},
                {'dia_semana': 2, 'hora_abertura': '08:00', 'hora_fechamento': '18:00'},
                {'dia_semana': 3, 'hora_abertura': '08:00', 'hora_fechamento': '18:00'},
                {'dia_semana': 4, 'hora_abertura': '08:00', 'hora_fechamento': '18:00'},
                {'dia_semana': 5, 'hora_abertura': '08:00', 'hora_fechamento': '18:00'},
                {'dia_semana': 6, 'hora_abertura': '08:00', 'hora_fechamento': '12:00'},
            ]
            
            for horario in horarios:
                HorarioFuncionamento.objects.create(**horario)
            
            print("  ✅ Horários criados")
        
        return True
    except Exception as e:
        print(f"  ❌ Erro ao criar dados: {e}")
        return False


def run_simulation():
    """Executa simulação de testes"""
    print("\n🚀 Iniciando simulação CRUD...")
    
    try:
        # Importar e executar simulador
        from test_api_simulation import APISimulator
        
        simulator = APISimulator()
        success = simulator.run_full_simulation()
        
        return success
    except Exception as e:
        print(f"❌ Erro durante simulação: {e}")
        return False


def run_analysis():
    """Executa análise dos resultados"""
    print("\n📊 Executando análise dos resultados...")
    
    try:
        from analyze_test_report import TestReportAnalyzer
        
        analyzer = TestReportAnalyzer()
        success = analyzer.run_analysis()
        
        return success
    except Exception as e:
        print(f"❌ Erro durante análise: {e}")
        return False


def main():
    """Função principal"""
    print("🔧 TOP PET SYSTEM - SETUP E TESTE API")
    print("=" * 50)
    
    # Verificações preliminares
    if not check_dependencies():
        return 1
    
    if not prepare_database():
        return 1
    
    if not create_test_data():
        return 1
    
    # Executar simulação
    print("\n" + "=" * 50)
    if not run_simulation():
        print("❌ Simulação falhou")
        return 1
    
    # Executar análise
    print("\n" + "=" * 50)
    if not run_analysis():
        print("❌ Análise falhou")
        return 1
    
    print("\n✅ PROCESSO COMPLETO FINALIZADO!")
    print("\n📁 Arquivos gerados:")
    print("  • api_test_report.json - Relatório detalhado")
    print("\n💡 Comandos úteis:")
    print("  • python test_api_simulation.py - Executar apenas simulação")
    print("  • python analyze_test_report.py - Executar apenas análise")
    print("  • cat api_test_report.json | python -m json.tool - Ver JSON formatado")
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
