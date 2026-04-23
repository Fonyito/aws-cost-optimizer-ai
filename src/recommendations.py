"""
Recommendations - Lógica de procesamiento y priorización de recomendaciones
"""
import json
from typing import Dict, Any, List
from datetime import datetime


class RecommendationProcessor:
    """Procesa y prioriza recomendaciones de optimización"""
    
    PRIORITY_WEIGHTS = {
        'HIGH': 3,
        'MEDIUM': 2,
        'LOW': 1
    }
    
    def __init__(self):
        """Inicializa el procesador de recomendaciones"""
        pass
    
    def prioritize_recommendations(self, recommendations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Ordena recomendaciones por prioridad y ahorro potencial
        
        Args:
            recommendations: Lista de recomendaciones
            
        Returns:
            Lista ordenada de recomendaciones
        """
        def sort_key(rec):
            priority_weight = self.PRIORITY_WEIGHTS.get(rec.get('priority', 'LOW'), 1)
            savings = rec.get('estimated_savings', 0)
            return (priority_weight * 1000 + savings, -priority_weight)
        
        return sorted(recommendations, key=sort_key, reverse=True)
    
    def filter_by_priority(self, recommendations: List[Dict[str, Any]], priority: str) -> List[Dict[str, Any]]:
        """
        Filtra recomendaciones por nivel de prioridad
        
        Args:
            recommendations: Lista de recomendaciones
            priority: Nivel de prioridad (HIGH, MEDIUM, LOW)
            
        Returns:
            Lista filtrada
        """
        return [r for r in recommendations if r.get('priority') == priority]
    
    def filter_by_category(self, recommendations: List[Dict[str, Any]], category: str) -> List[Dict[str, Any]]:
        """
        Filtra recomendaciones por categoría
        
        Args:
            recommendations: Lista de recomendaciones
            category: Categoría a filtrar
            
        Returns:
            Lista filtrada
        """
        return [r for r in recommendations if r.get('category') == category]
    
    def get_quick_wins(self, recommendations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Obtiene 'quick wins': alto ahorro, bajo esfuerzo, bajo riesgo
        
        Args:
            recommendations: Lista de recomendaciones
            
        Returns:
            Lista de quick wins
        """
        quick_wins = []
        for rec in recommendations:
            if (rec.get('effort') == 'LOW' and 
                rec.get('risk') == 'LOW' and 
                rec.get('estimated_savings', 0) > 10):
                quick_wins.append(rec)
        
        return sorted(quick_wins, key=lambda x: x.get('estimated_savings', 0), reverse=True)
    
    def generate_summary_report(self, analysis: Dict[str, Any]) -> str:
        """
        Genera un informe resumen en texto plano
        
        Args:
            analysis: Análisis completo con recomendaciones
            
        Returns:
            Informe en texto
        """
        recommendations = analysis.get('recommendations', [])
        total_savings = analysis.get('total_potential_savings', 0)
        current_cost = analysis.get('total_current_cost', 0)
        
        report = f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    AWS COST OPTIMIZATION REPORT                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

📅 Fecha de análisis: {analysis.get('analysis_date', 'N/A')}
💰 Coste actual: ${current_cost:.2f} USD/mes
💡 Ahorro potencial: ${total_savings:.2f} USD/mes ({analysis.get('savings_percentage', 0):.1f}%)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔥 TOP 5 RECOMENDACIONES PRIORITARIAS:

"""
        
        # Top 5 recomendaciones
        top_recs = sorted(recommendations, 
                         key=lambda x: (self.PRIORITY_WEIGHTS.get(x.get('priority', 'LOW'), 1) * 1000 + 
                                       x.get('estimated_savings', 0)), 
                         reverse=True)[:5]
        
        for i, rec in enumerate(top_recs, 1):
            priority_emoji = {'HIGH': '🔴', 'MEDIUM': '🟡', 'LOW': '🟢'}.get(rec.get('priority'), '⚪')
            report += f"{i}. {priority_emoji} [{rec.get('priority')}] {rec.get('title')}\n"
            report += f"   💵 Ahorro: ${rec.get('estimated_savings', 0):.2f}/mes\n"
            report += f"   📋 {rec.get('description')}\n"
            report += f"   ✅ Acción: {rec.get('action')}\n\n"
        
        # Quick wins
        quick_wins = self.get_quick_wins(recommendations)
        if quick_wins:
            report += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            report += f"⚡ QUICK WINS (bajo esfuerzo, bajo riesgo):\n\n"
            for i, rec in enumerate(quick_wins[:3], 1):
                report += f"{i}. {rec.get('title')} - ${rec.get('estimated_savings', 0):.2f}/mes\n"
        
        # Resumen por categoría
        categories = {}
        for rec in recommendations:
            cat = rec.get('category', 'Otros')
            if cat not in categories:
                categories[cat] = {'count': 0, 'savings': 0}
            categories[cat]['count'] += 1
            categories[cat]['savings'] += rec.get('estimated_savings', 0)
        
        report += "\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        report += "📊 RESUMEN POR CATEGORÍA:\n\n"
        
        for cat, data in sorted(categories.items(), key=lambda x: x[1]['savings'], reverse=True):
            report += f"• {cat}: {data['count']} recomendaciones - ${data['savings']:.2f}/mes\n"
        
        report += "\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        report += f"\n✨ {analysis.get('summary', '')}\n"
        
        return report
    
    def export_to_json(self, analysis: Dict[str, Any], output_file: str):
        """
        Exporta análisis completo a JSON
        
        Args:
            analysis: Análisis completo
            output_file: Ruta del archivo de salida
        """
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(analysis, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Análisis exportado a: {output_file}")


if __name__ == "__main__":
    # Test del módulo
    from cost_analyzer import CostAnalyzer
    from bedrock_analyzer import BedrockAnalyzer
    
    cost_analyzer = CostAnalyzer(demo_mode=True)
    cost_data = cost_analyzer.get_cost_data()
    cost_summary = cost_analyzer.get_cost_summary(cost_data)
    
    bedrock = BedrockAnalyzer(demo_mode=True)
    analysis = bedrock.analyze_costs(cost_summary, cost_data)
    
    processor = RecommendationProcessor()
    print(processor.generate_summary_report(analysis))
