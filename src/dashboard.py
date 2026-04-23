"""
Dashboard Generator - Genera dashboard HTML interactivo con Chart.js
"""
import json
import os
from datetime import datetime
from typing import Dict, Any


class DashboardGenerator:
    """Genera dashboard visual HTML con gráficos"""
    
    def __init__(self):
        """Inicializa el generador de dashboard"""
        self.template_dir = os.path.join(os.path.dirname(__file__), '..', 'templates')
        self.output_dir = os.path.join(os.path.dirname(__file__), '..', 'output')
    
    def generate(self, analysis_file: str = None):
        """
        Genera dashboard HTML desde archivo de análisis
        
        Args:
            analysis_file: Ruta al archivo JSON de análisis (opcional)
        """
        # Cargar datos de análisis
        if analysis_file and os.path.exists(analysis_file):
            with open(analysis_file, 'r', encoding='utf-8') as f:
                analysis = json.load(f)
        else:
            # Usar datos de ejemplo
            analysis = self._load_demo_analysis()
        
        # Generar HTML
        html = self._generate_html(analysis)
        
        # Guardar dashboard
        output_file = os.path.join(self.template_dir, 'dashboard.html')
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"✅ Dashboard generado: {output_file}")
        print(f"🌐 Abre el archivo en tu navegador para visualizarlo")
        
        return output_file
    
    def _load_demo_analysis(self) -> Dict[str, Any]:
        """Carga análisis de ejemplo para demo"""
        from cost_analyzer import CostAnalyzer
        from bedrock_analyzer import BedrockAnalyzer
        
        cost_analyzer = CostAnalyzer(demo_mode=True)
        cost_data = cost_analyzer.get_cost_data()
        cost_summary = cost_analyzer.get_cost_summary(cost_data)
        
        bedrock = BedrockAnalyzer(demo_mode=True)
        analysis = bedrock.analyze_costs(cost_summary, cost_data)
        
        # Añadir datos de costes para gráficos
        analysis['cost_data'] = cost_data
        
        return analysis
    
    def _generate_html(self, analysis: Dict[str, Any]) -> str:
        """Genera HTML completo del dashboard"""
        
        cost_data = analysis.get('cost_data', {})
        services = cost_data.get('services', [])[:10]
        recommendations = analysis.get('recommendations', [])
        
        # Preparar datos para Chart.js
        service_labels = json.dumps([s['service'].replace('Amazon ', '').replace('AWS ', '') for s in services])
        service_costs = json.dumps([s['cost'] for s in services])
        
        # Top 5 recomendaciones
        top_recs = sorted(recommendations, 
                         key=lambda x: x.get('estimated_savings', 0), 
                         reverse=True)[:5]
        
        rec_labels = json.dumps([r['title'][:40] + '...' if len(r['title']) > 40 else r['title'] for r in top_recs])
        rec_savings = json.dumps([r['estimated_savings'] for r in top_recs])
        
        # Generar HTML
        html = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AWS Cost Optimizer AI - Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            color: #333;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
        }}
        
        header {{
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            margin-bottom: 30px;
            text-align: center;
        }}
        
        h1 {{
            color: #667eea;
            font-size: 2.5em;
            margin-bottom: 10px;
        }}
        
        .subtitle {{
            color: #666;
            font-size: 1.1em;
        }}
        
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        
        .stat-card {{
            background: white;
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            transition: transform 0.3s ease;
        }}
        
        .stat-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 10px 25px rgba(0,0,0,0.15);
        }}
        
        .stat-label {{
            color: #666;
            font-size: 0.9em;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 10px;
        }}
        
        .stat-value {{
            font-size: 2.5em;
            font-weight: bold;
            color: #667eea;
        }}
        
        .stat-value.savings {{
            color: #10b981;
        }}
        
        .stat-value.percentage {{
            color: #f59e0b;
        }}
        
        .charts-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
            gap: 30px;
            margin-bottom: 30px;
        }}
        
        .chart-card {{
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }}
        
        .chart-title {{
            font-size: 1.5em;
            color: #333;
            margin-bottom: 20px;
            text-align: center;
        }}
        
        .recommendations {{
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }}
        
        .rec-item {{
            padding: 20px;
            margin-bottom: 15px;
            border-left: 4px solid #667eea;
            background: #f9fafb;
            border-radius: 8px;
            transition: all 0.3s ease;
        }}
        
        .rec-item:hover {{
            background: #f3f4f6;
            transform: translateX(5px);
        }}
        
        .rec-item.high {{
            border-left-color: #ef4444;
        }}
        
        .rec-item.medium {{
            border-left-color: #f59e0b;
        }}
        
        .rec-item.low {{
            border-left-color: #10b981;
        }}
        
        .rec-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
        }}
        
        .rec-title {{
            font-size: 1.2em;
            font-weight: bold;
            color: #333;
        }}
        
        .rec-savings {{
            font-size: 1.3em;
            font-weight: bold;
            color: #10b981;
        }}
        
        .rec-description {{
            color: #666;
            margin-bottom: 10px;
            line-height: 1.6;
        }}
        
        .rec-action {{
            color: #667eea;
            font-weight: 500;
            padding: 10px;
            background: #eef2ff;
            border-radius: 5px;
            margin-top: 10px;
        }}
        
        .priority-badge {{
            display: inline-block;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.8em;
            font-weight: bold;
            text-transform: uppercase;
        }}
        
        .priority-badge.high {{
            background: #fee2e2;
            color: #dc2626;
        }}
        
        .priority-badge.medium {{
            background: #fef3c7;
            color: #d97706;
        }}
        
        .priority-badge.low {{
            background: #d1fae5;
            color: #059669;
        }}
        
        footer {{
            text-align: center;
            color: white;
            margin-top: 40px;
            padding: 20px;
        }}
        
        @media (max-width: 768px) {{
            .charts-grid {{
                grid-template-columns: 1fr;
            }}
            
            h1 {{
                font-size: 1.8em;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>💰 AWS Cost Optimizer AI</h1>
            <p class="subtitle">Dashboard de Análisis y Optimización de Costes</p>
            <p style="color: #999; margin-top: 10px;">Generado: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</p>
        </header>
        
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-label">💵 Coste Actual</div>
                <div class="stat-value">${analysis.get('total_current_cost', 0):.2f}</div>
                <div style="color: #999; margin-top: 5px;">USD/mes</div>
            </div>
            
            <div class="stat-card">
                <div class="stat-label">💡 Ahorro Potencial</div>
                <div class="stat-value savings">${analysis.get('total_potential_savings', 0):.2f}</div>
                <div style="color: #999; margin-top: 5px;">USD/mes</div>
            </div>
            
            <div class="stat-card">
                <div class="stat-label">📊 Porcentaje de Ahorro</div>
                <div class="stat-value percentage">{analysis.get('savings_percentage', 0):.1f}%</div>
                <div style="color: #999; margin-top: 5px;">del coste total</div>
            </div>
            
            <div class="stat-card">
                <div class="stat-label">🎯 Recomendaciones</div>
                <div class="stat-value">{len(recommendations)}</div>
                <div style="color: #999; margin-top: 5px;">oportunidades</div>
            </div>
        </div>
        
        <div class="charts-grid">
            <div class="chart-card">
                <h2 class="chart-title">📊 Costes por Servicio AWS</h2>
                <canvas id="servicesChart"></canvas>
            </div>
            
            <div class="chart-card">
                <h2 class="chart-title">💰 Top 5 Ahorros Potenciales</h2>
                <canvas id="savingsChart"></canvas>
            </div>
        </div>
        
        <div class="recommendations">
            <h2 class="chart-title">🔥 Recomendaciones Prioritarias</h2>
            
            {self._generate_recommendations_html(recommendations[:8])}
        </div>
        
        <footer>
            <p>Desarrollado con ❤️ usando Amazon Bedrock (Claude 3.5) y AWS Cost Explorer</p>
            <p style="margin-top: 10px; opacity: 0.8;">AWS Cost Optimizer AI © 2026</p>
        </footer>
    </div>
    
    <script>
        // Gráfico de costes por servicio
        const servicesCtx = document.getElementById('servicesChart').getContext('2d');
        new Chart(servicesCtx, {{
            type: 'doughnut',
            data: {{
                labels: {service_labels},
                datasets: [{{
                    data: {service_costs},
                    backgroundColor: [
                        '#667eea', '#764ba2', '#f093fb', '#4facfe',
                        '#43e97b', '#fa709a', '#fee140', '#30cfd0',
                        '#a8edea', '#fed6e3'
                    ],
                    borderWidth: 2,
                    borderColor: '#fff'
                }}]
            }},
            options: {{
                responsive: true,
                plugins: {{
                    legend: {{
                        position: 'bottom',
                        labels: {{
                            padding: 15,
                            font: {{
                                size: 12
                            }}
                        }}
                    }},
                    tooltip: {{
                        callbacks: {{
                            label: function(context) {{
                                return context.label + ': $' + context.parsed.toFixed(2);
                            }}
                        }}
                    }}
                }}
            }}
        }});
        
        // Gráfico de ahorros potenciales
        const savingsCtx = document.getElementById('savingsChart').getContext('2d');
        new Chart(savingsCtx, {{
            type: 'bar',
            data: {{
                labels: {rec_labels},
                datasets: [{{
                    label: 'Ahorro USD/mes',
                    data: {rec_savings},
                    backgroundColor: 'rgba(16, 185, 129, 0.8)',
                    borderColor: 'rgba(16, 185, 129, 1)',
                    borderWidth: 2
                }}]
            }},
            options: {{
                responsive: true,
                plugins: {{
                    legend: {{
                        display: false
                    }}
                }},
                scales: {{
                    y: {{
                        beginAtZero: true,
                        ticks: {{
                            callback: function(value) {{
                                return '$' + value;
                            }}
                        }}
                    }}
                }}
            }}
        }});
    </script>
</body>
</html>"""
        
        return html
    
    def _generate_recommendations_html(self, recommendations: list) -> str:
        """Genera HTML para lista de recomendaciones"""
        html = ""
        
        for rec in recommendations:
            priority = rec.get('priority', 'LOW').lower()
            priority_emoji = {'high': '🔴', 'medium': '🟡', 'low': '🟢'}.get(priority, '⚪')
            
            html += f"""
            <div class="rec-item {priority}">
                <div class="rec-header">
                    <div>
                        <span class="priority-badge {priority}">{priority_emoji} {rec.get('priority', 'LOW')}</span>
                        <span style="color: #999; margin-left: 10px;">{rec.get('category', 'General')}</span>
                    </div>
                    <div class="rec-savings">${rec.get('estimated_savings', 0):.2f}/mes</div>
                </div>
                <div class="rec-title">{rec.get('title', 'Sin título')}</div>
                <div class="rec-description">{rec.get('description', 'Sin descripción')}</div>
                <div class="rec-action">
                    <strong>✅ Acción:</strong> {rec.get('action', 'No especificada')}
                </div>
                <div style="margin-top: 10px; color: #999; font-size: 0.9em;">
                    Esfuerzo: {rec.get('effort', 'N/A')} | Riesgo: {rec.get('risk', 'N/A')} | 
                    Ahorro: {rec.get('savings_percentage', 0):.1f}%
                </div>
            </div>
            """
        
        return html


def main():
    """Función principal para generar dashboard"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Genera dashboard HTML de análisis de costes')
    parser.add_argument('--input', type=str, help='Archivo JSON de análisis (opcional)')
    args = parser.parse_args()
    
    generator = DashboardGenerator()
    output_file = generator.generate(args.input)
    
    print(f"\n✨ Dashboard listo!")
    print(f"🌐 Abre este archivo en tu navegador: {output_file}")


if __name__ == "__main__":
    main()
