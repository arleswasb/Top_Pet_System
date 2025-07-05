#!/usr/bin/env python3
"""
Analisador de Relatórios de Teste API
Gera análises avançadas dos resultados dos testes
"""

import json
import sys
from collections import defaultdict
from datetime import datetime
import argparse


class TestReportAnalyzer:
    """Analisador de relatórios de teste"""
    
    def __init__(self, report_file='api_test_report.json'):
        self.report_file = report_file
        self.data = None
    
    def load_report(self):
        """Carrega relatório JSON"""
        try:
            with open(self.report_file, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
            return True
        except FileNotFoundError:
            print(f"❌ Arquivo {self.report_file} não encontrado")
            return False
        except json.JSONDecodeError:
            print(f"❌ Erro ao decodificar JSON em {self.report_file}")
            return False
    
    def analyze_performance(self):
        """Analisa performance das rotas"""
        print("\n📊 ANÁLISE DE PERFORMANCE")
        print("=" * 50)
        
        routes = self.data.get('routes_tested', [])
        if not routes:
            print("Nenhuma rota encontrada para análise")
            return
        
        # Agrupar por endpoint base
        endpoint_stats = defaultdict(list)
        for route in routes:
            endpoint_base = route['endpoint'].split('?')[0]
            # Remove IDs numéricos para agrupar
            parts = endpoint_base.split('/')
            clean_parts = []
            for part in parts:
                if part.isdigit():
                    clean_parts.append('{id}')
                else:
                    clean_parts.append(part)
            clean_endpoint = '/'.join(clean_parts)
            
            endpoint_stats[clean_endpoint].append({
                'method': route['method'],
                'duration': route['duration'],
                'success': route['success']
            })
        
        # Calcular estatísticas por endpoint
        for endpoint, stats in sorted(endpoint_stats.items()):
            durations = [s['duration'] for s in stats]
            success_count = sum(1 for s in stats if s['success'])
            
            print(f"\n🛤️  {endpoint}")
            print(f"   Testes: {len(stats)}")
            print(f"   Sucessos: {success_count}/{len(stats)} ({success_count/len(stats)*100:.1f}%)")
            print(f"   Tempo médio: {sum(durations)/len(durations):.3f}s")
            print(f"   Tempo min/max: {min(durations):.3f}s / {max(durations):.3f}s")
            
            # Métodos testados
            methods = defaultdict(int)
            for stat in stats:
                methods[stat['method']] += 1
            print(f"   Métodos: {dict(methods)}")
    
    def analyze_coverage(self):
        """Analisa cobertura de testes"""
        print("\n🎯 ANÁLISE DE COBERTURA")
        print("=" * 50)
        
        routes = self.data.get('routes_tested', [])
        
        # Agrupar por módulo/app
        modules = defaultdict(lambda: defaultdict(set))
        
        for route in routes:
            endpoint = route['endpoint']
            method = route['method']
            
            # Extrair módulo do endpoint
            parts = endpoint.split('/')
            if len(parts) > 2:
                module = parts[2] if parts[2] else 'root'
            else:
                module = 'root'
            
            modules[module]['methods'].add(method)
            modules[module]['endpoints'].add(endpoint)
        
        for module, data in sorted(modules.items()):
            print(f"\n📦 Módulo: {module}")
            print(f"   Endpoints testados: {len(data['endpoints'])}")
            print(f"   Métodos HTTP: {sorted(data['methods'])}")
            
            # Listar endpoints
            for endpoint in sorted(data['endpoints']):
                print(f"     • {endpoint}")
    
    def analyze_errors(self):
        """Analisa erros encontrados"""
        print("\n🚨 ANÁLISE DE ERROS")
        print("=" * 50)
        
        errors = self.data.get('errors', [])
        if not errors:
            print("✅ Nenhum erro encontrado!")
            return
        
        # Agrupar erros por tipo
        error_types = defaultdict(list)
        for error in errors:
            error_types[error['error']].append(error['route'])
        
        for error_type, routes in error_types.items():
            print(f"\n❌ {error_type}")
            print(f"   Ocorrências: {len(routes)}")
            for route in routes:
                print(f"     • {route}")
    
    def analyze_timing_patterns(self):
        """Analisa padrões de tempo"""
        print("\n⏱️  ANÁLISE DE PADRÕES TEMPORAIS")
        print("=" * 50)
        
        routes = self.data.get('routes_tested', [])
        
        # Agrupar por método HTTP
        method_times = defaultdict(list)
        for route in routes:
            method_times[route['method']].append(route['duration'])
        
        for method, times in sorted(method_times.items()):
            print(f"\n🔄 {method}")
            print(f"   Testes: {len(times)}")
            print(f"   Tempo médio: {sum(times)/len(times):.3f}s")
            print(f"   Tempo total: {sum(times):.3f}s")
            print(f"   Min/Max: {min(times):.3f}s / {max(times):.3f}s")
            
            # Classificar performance
            avg_time = sum(times) / len(times)
            if avg_time < 0.1:
                performance = "🟢 Excelente"
            elif avg_time < 0.5:
                performance = "🟡 Boa"
            elif avg_time < 1.0:
                performance = "🟠 Aceitável"
            else:
                performance = "🔴 Lenta"
            
            print(f"   Performance: {performance}")
    
    def generate_summary(self):
        """Gera resumo executivo"""
        print("\n📋 RESUMO EXECUTIVO")
        print("=" * 50)
        
        total_tests = self.data.get('total_tests', 0)
        passed = self.data.get('passed', 0)
        failed = self.data.get('failed', 0)
        total_duration = self.data.get('total_duration', 0)
        
        print(f"Total de testes executados: {total_tests}")
        print(f"Taxa de sucesso: {passed/total_tests*100:.1f}%" if total_tests > 0 else "N/A")
        print(f"Tempo total de execução: {total_duration:.3f}s")
        print(f"Tempo médio por teste: {total_duration/total_tests:.3f}s" if total_tests > 0 else "N/A")
        
        # Status geral
        if failed == 0:
            status = "🟢 TODOS OS TESTES PASSARAM"
        elif failed < total_tests * 0.1:
            status = "🟡 POUCOS ERROS ENCONTRADOS"
        else:
            status = "🔴 MUITOS ERROS ENCONTRADOS"
        
        print(f"\nStatus geral: {status}")
        
        # Recomendações
        print(f"\n💡 RECOMENDAÇÕES:")
        
        routes = self.data.get('routes_tested', [])
        slow_routes = [r for r in routes if r['duration'] > 1.0]
        if slow_routes:
            print(f"   • {len(slow_routes)} rotas estão lentas (>1s)")
        
        if failed > 0:
            print(f"   • Investigar {failed} falhas encontradas")
        
        methods_tested = set(r['method'] for r in routes)
        if 'DELETE' not in methods_tested:
            print("   • Considerar adicionar testes de DELETE")
        
        if total_duration > 30:
            print("   • Otimizar performance geral dos testes")
        
        print("   • Verificar cobertura de casos edge")
        print("   • Adicionar testes de validação de dados")
    
    def run_analysis(self):
        """Executa análise completa"""
        if not self.load_report():
            return False
        
        print("🔍 ANÁLISE AVANÇADA DE TESTES API")
        print("=" * 60)
        
        self.generate_summary()
        self.analyze_performance()
        self.analyze_coverage()
        self.analyze_timing_patterns()
        self.analyze_errors()
        
        return True


def main():
    parser = argparse.ArgumentParser(description='Analisador de relatórios de teste API')
    parser.add_argument('--file', '-f', default='api_test_report.json',
                       help='Arquivo de relatório JSON (padrão: api_test_report.json)')
    
    args = parser.parse_args()
    
    analyzer = TestReportAnalyzer(args.file)
    success = analyzer.run_analysis()
    
    return 0 if success else 1


if __name__ == '__main__':
    sys.exit(main())
