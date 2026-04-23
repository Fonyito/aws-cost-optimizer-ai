"""
Bedrock Analyzer - Integración con Amazon Bedrock para análisis con IA
"""
import json
import os
from typing import Dict, Any, List
import boto3
from botocore.exceptions import ClientError


class BedrockAnalyzer:
    """Analiza costes usando Amazon Bedrock (Claude 3.5)"""
    
    def __init__(self, demo_mode: bool = True):
        """
        Inicializa el cliente de Bedrock
        
        Args:
            demo_mode: Si es True, simula respuestas de IA
        """
        self.demo_mode = demo_mode
        self.model_id = os.getenv('BEDROCK_MODEL_ID', 'anthropic.claude-3-5-sonnet-20241022-v2:0')
        
        if not demo_mode:
            self.bedrock_client = boto3.client(
                'bedrock-runtime',
                region_name=os.getenv('BEDROCK_REGION', 'us-east-1')
            )
    
    def analyze_costs(self, cost_summary: str, cost_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analiza costes y genera recomendaciones usando IA
        
        Args:
            cost_summary: Resumen textual de costes
            cost_data: Datos completos de costes
            
        Returns:
            Diccionario con análisis y recomendaciones
        """
        if self.demo_mode:
            return self._generate_mock_analysis(cost_data)
        
        return self._analyze_with_bedrock(cost_summary, cost_data)
    
    def _generate_mock_analysis(self, cost_data: Dict[str, Any]) -> Dict[str, Any]:
        """Genera análisis simulado para modo demo"""
        
        recommendations = [
            {
                "priority": "HIGH",
                "category": "Rightsizing EC2",
                "title": "Reducir tamaño de instancias EC2 infrautilizadas",
                "description": "Se detectaron 3 instancias t3.large con uso de CPU < 25% de forma consistente. Estas instancias están sobredimensionadas.",
                "current_cost": 380.19,
                "optimized_cost": 190.10,
                "estimated_savings": 190.09,
                "savings_percentage": 50.0,
                "action": "Cambiar instancias i-0abc123def456, i-0def789ghi012 y i-0jkl901mno234 de t3.large a t3.medium",
                "effort": "LOW",
                "risk": "LOW"
            },
            {
                "priority": "HIGH",
                "category": "Recursos huérfanos",
                "title": "Eliminar volúmenes EBS no adjuntos",
                "description": "2 volúmenes EBS (vol-0def456ghi, vol-0jkl012mno) no están adjuntos a ninguna instancia y están generando costes innecesarios.",
                "current_cost": 35.00,
                "optimized_cost": 0.00,
                "estimated_savings": 35.00,
                "savings_percentage": 100.0,
                "action": "Crear snapshot de respaldo y eliminar volúmenes huérfanos",
                "effort": "LOW",
                "risk": "LOW"
            },
            {
                "priority": "HIGH",
                "category": "Optimización S3",
                "title": "Migrar datos antiguos a S3 Glacier",
                "description": "Los buckets 'company-backups-legacy' y 'company-logs-archive' contienen 7.5TB de datos con acceso infrecuente en clase STANDARD.",
                "current_cost": 172.50,
                "optimized_cost": 30.00,
                "estimated_savings": 142.50,
                "savings_percentage": 82.6,
                "action": "Configurar lifecycle policies para mover datos > 90 días a S3 Glacier Deep Archive",
                "effort": "LOW",
                "risk": "LOW"
            },
            {
                "priority": "MEDIUM",
                "category": "Reserved Instances",
                "title": "Comprar Reserved Instances para RDS",
                "description": "Las instancias RDS prod-mysql-01 y dev-postgres-01 llevan > 6 meses activas 24/7. Reserved Instances de 1 año ofrecen ~40% descuento.",
                "current_cost": 312.45,
                "optimized_cost": 187.47,
                "estimated_savings": 124.98,
                "savings_percentage": 40.0,
                "action": "Comprar 2 Reserved Instances de 1 año con pago parcial adelantado",
                "effort": "LOW",
                "risk": "MEDIUM"
            },
            {
                "priority": "MEDIUM",
                "category": "Recursos huérfanos",
                "title": "Liberar IP elástica no asociada",
                "description": "IP elástica eipalloc-0def456 no está asociada a ninguna instancia y genera coste de $3.60/mes.",
                "current_cost": 3.60,
                "optimized_cost": 0.00,
                "estimated_savings": 3.60,
                "savings_percentage": 100.0,
                "action": "Liberar IP elástica si no se necesita o asociarla a una instancia",
                "effort": "LOW",
                "risk": "LOW"
            },
            {
                "priority": "MEDIUM",
                "category": "Limpieza de snapshots",
                "title": "Eliminar snapshots antiguos",
                "description": "2 snapshots EBS tienen más de 1 año de antigüedad (456 y 523 días). Evaluar si son necesarios.",
                "current_cost": 19.00,
                "optimized_cost": 0.00,
                "estimated_savings": 19.00,
                "savings_percentage": 100.0,
                "action": "Revisar política de retención y eliminar snapshots obsoletos",
                "effort": "LOW",
                "risk": "MEDIUM"
            },
            {
                "priority": "LOW",
                "category": "Consolidación RDS",
                "title": "Evaluar consolidación de base de datos dev",
                "description": "La instancia dev-postgres-01 tiene solo 3 conexiones promedio. Considerar usar RDS Proxy o consolidar con prod.",
                "current_cost": 156.23,
                "optimized_cost": 78.12,
                "estimated_savings": 78.11,
                "savings_percentage": 50.0,
                "action": "Evaluar migrar dev a instancia más pequeña (db.t3.micro) o usar Aurora Serverless v2",
                "effort": "MEDIUM",
                "risk": "LOW"
            },
            {
                "priority": "LOW",
                "category": "Optimización Lambda",
                "title": "Lambda ya está optimizado",
                "description": "El coste de Lambda ($23.45) es razonable para 2.5M invocaciones. No se requiere acción.",
                "current_cost": 23.45,
                "optimized_cost": 23.45,
                "estimated_savings": 0.00,
                "savings_percentage": 0.0,
                "action": "Mantener configuración actual",
                "effort": "NONE",
                "risk": "NONE"
            }
        ]
        
        total_savings = sum(r['estimated_savings'] for r in recommendations)
        
        return {
            "analysis_date": cost_data['analysis_period']['end'],
            "model_used": "mock-demo-mode",
            "total_current_cost": cost_data['total_cost'],
            "total_potential_savings": round(total_savings, 2),
            "savings_percentage": round((total_savings / cost_data['total_cost']) * 100, 1),
            "recommendations": recommendations,
            "summary": f"Se identificaron {len(recommendations)} oportunidades de optimización con un ahorro potencial de ${total_savings:.2f}/mes ({(total_savings / cost_data['total_cost']) * 100:.1f}% del coste actual).",
            "top_priorities": [r for r in recommendations if r['priority'] == 'HIGH']
        }
    
    def _analyze_with_bedrock(self, cost_summary: str, cost_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analiza costes usando Amazon Bedrock real
        
        Args:
            cost_summary: Resumen de costes
            cost_data: Datos completos
            
        Returns:
            Análisis generado por IA
        """
        prompt = f"""Eres un experto AWS Solutions Architect especializado en optimización de costes (FinOps).

Analiza el siguiente informe de costes AWS y genera recomendaciones concretas y accionables:

{cost_summary}

DATOS DETALLADOS:
{json.dumps(cost_data, indent=2, ensure_ascii=False)}

Genera un análisis en formato JSON con esta estructura:
{{
  "recommendations": [
    {{
      "priority": "HIGH|MEDIUM|LOW",
      "category": "Rightsizing|Reserved Instances|Recursos huérfanos|Optimización S3|etc",
      "title": "Título breve",
      "description": "Descripción detallada del problema",
      "current_cost": 100.00,
      "optimized_cost": 60.00,
      "estimated_savings": 40.00,
      "savings_percentage": 40.0,
      "action": "Acción concreta a tomar",
      "effort": "LOW|MEDIUM|HIGH",
      "risk": "LOW|MEDIUM|HIGH"
    }}
  ],
  "summary": "Resumen ejecutivo del análisis"
}}

IMPORTANTE:
- Prioriza recomendaciones por ahorro potencial
- Sé específico con IDs de recursos cuando estén disponibles
- Calcula ahorros realistas basados en precios AWS actuales
- Incluye nivel de esfuerzo y riesgo para cada recomendación
- Responde SOLO con JSON válido, sin texto adicional"""

        try:
            # Preparar request para Claude 3.5
            request_body = {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 4096,
                "temperature": 0.3,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            }
            
            # Invocar Bedrock
            response = self.bedrock_client.invoke_model(
                modelId=self.model_id,
                body=json.dumps(request_body)
            )
            
            # Parsear respuesta
            response_body = json.loads(response['body'].read())
            ai_response = response_body['content'][0]['text']
            
            # Extraer JSON de la respuesta
            analysis = json.loads(ai_response)
            
            # Añadir metadatos
            analysis['analysis_date'] = cost_data['analysis_period']['end']
            analysis['model_used'] = self.model_id
            analysis['total_current_cost'] = cost_data['total_cost']
            
            total_savings = sum(r.get('estimated_savings', 0) for r in analysis['recommendations'])
            analysis['total_potential_savings'] = round(total_savings, 2)
            analysis['savings_percentage'] = round((total_savings / cost_data['total_cost']) * 100, 1)
            analysis['top_priorities'] = [r for r in analysis['recommendations'] if r['priority'] == 'HIGH']
            
            return analysis
            
        except ClientError as e:
            print(f"❌ Error al invocar Bedrock: {e}")
            raise
        except json.JSONDecodeError as e:
            print(f"❌ Error al parsear respuesta de Bedrock: {e}")
            raise


if __name__ == "__main__":
    # Test del módulo
    from cost_analyzer import CostAnalyzer
    
    cost_analyzer = CostAnalyzer(demo_mode=True)
    cost_data = cost_analyzer.get_cost_data()
    cost_summary = cost_analyzer.get_cost_summary(cost_data)
    
    bedrock = BedrockAnalyzer(demo_mode=True)
    analysis = bedrock.analyze_costs(cost_summary, cost_data)
    
    print(json.dumps(analysis, indent=2, ensure_ascii=False))
