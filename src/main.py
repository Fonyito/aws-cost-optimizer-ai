#!/usr/bin/env python3
"""
AWS Cost Optimizer AI - Main Entry Point
Analiza costes de AWS y genera recomendaciones usando IA
"""
import argparse
import json
import os
import sys
from datetime import datetime
from dotenv import load_dotenv

from cost_analyzer import CostAnalyzer
from bedrock_analyzer import BedrockAnalyzer
from recommendations import RecommendationProcessor


def main():
    """Función principal"""
    # Cargar variables de entorno
    load_dotenv()
    
    # Parsear argumentos
    parser = argparse.ArgumentParser(
        description='AWS Cost Optimizer AI - Analiza y optimiza costes de AWS con IA'
    )
    parser.add_argument(
        '--demo',
        action='store_true',
        help='Ejecutar en modo demo con datos de ejemplo'
    )
    parser.add_argument(
        '--days',
        type=int,
        default=30,
        help='Número de días a analizar (default: 30)'
    )
    parser.add_argument(
        '--output',
        type=str,
        default='output',
        help='Directorio de salida para resultados (default: output)'
    )
    parser.add_argument(
        '--format',
        choices=['json', 'text', 'both'],
        default='both',
        help='Formato de salida (default: both)'
    )
    
    args = parser.parse_args()
    
    # Determinar modo de ejecución
    demo_mode = args.demo or os.getenv('DEMO_MODE', 'true').lower() == 'true'
    
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║                    AWS COST OPTIMIZER AI                                     ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝\n")
    
    if demo_mode:
        print("🎭 Modo DEMO activado - usando datos de ejemplo")
    else:
        print("☁️  Modo AWS REAL - conectando a Cost Explorer y Bedrock")
    
    print(f"📅 Analizando últimos {args.days} días\n")
    
    try:
        # Paso 1: Obtener datos de costes
        print("📊 [1/4] Obteniendo datos de costes...")
        cost_analyzer = CostAnalyzer(demo_mode=demo_mode)
        cost_data = cost_analyzer.get_cost_data(days=args.days)
        print(f"✅ Coste total: ${cost_data['total_cost']:.2f} USD")
        print(f"✅ Servicios analizados: {len(cost_data['services'])}\n")
        
        # Paso 2: Generar resumen para IA
        print("📝 [2/4] Generando resumen de costes...")
        cost_summary = cost_analyzer.get_cost_summary(cost_data)
        print("✅ Resumen generado\n")
        
        # Paso 3: Analizar con Bedrock
        print("🧠 [3/4] Analizando con IA (Amazon Bedrock)...")
        bedrock = BedrockAnalyzer(demo_mode=demo_mode)
        analysis = bedrock.analyze_costs(cost_summary, cost_data)
        print(f"✅ {len(analysis['recommendations'])} recomendaciones generadas")
        print(f"✅ Ahorro potencial: ${analysis['total_potential_savings']:.2f} USD/mes\n")
        
        # Paso 4: Procesar y exportar resultados
        print("💾 [4/4] Procesando y exportando resultados...")
        processor = RecommendationProcessor()
        
        # Crear directorio de salida
        os.makedirs(args.output, exist_ok=True)
        
        # Exportar JSON
        if args.format in ['json', 'both']:
            json_file = os.path.join(args.output, f'analysis_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json')
            processor.export_to_json(analysis, json_file)
        
        # Exportar texto
        if args.format in ['text', 'both']:
            text_file = os.path.join(args.output, f'report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt')
            report = processor.generate_summary_report(analysis)
            with open(text_file, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"✅ Informe exportado a: {text_file}")
        
        # Mostrar resumen en consola
        print("\n" + "="*80 + "\n")
        print(processor.generate_summary_report(analysis))
        
        print("\n" + "="*80)
        print("✨ Análisis completado exitosamente")
        print(f"📁 Resultados guardados en: {args.output}/")
        print("\n💡 Siguiente paso: Ejecuta 'python src/dashboard.py' para ver el dashboard visual")
        
    except FileNotFoundError as e:
        print(f"\n❌ Error: {e}")
        print("💡 Asegúrate de que el archivo data/sample_cost_data.json existe")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
