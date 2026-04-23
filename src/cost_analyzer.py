"""
AWS Cost Analyzer - Obtiene datos de costes de AWS Cost Explorer
"""
import json
import os
from datetime import datetime, timedelta
from typing import Dict, Any
import boto3
from botocore.exceptions import ClientError


class CostAnalyzer:
    """Analiza costes de AWS usando Cost Explorer API"""
    
    def __init__(self, demo_mode: bool = True):
        """
        Inicializa el analizador de costes
        
        Args:
            demo_mode: Si es True, usa datos de ejemplo en lugar de AWS real
        """
        self.demo_mode = demo_mode
        if not demo_mode:
            self.ce_client = boto3.client('ce', region_name=os.getenv('AWS_REGION', 'us-east-1'))
    
    def get_cost_data(self, days: int = 30) -> Dict[str, Any]:
        """
        Obtiene datos de costes de los últimos N días
        
        Args:
            days: Número de días a analizar
            
        Returns:
            Diccionario con datos de costes
        """
        if self.demo_mode:
            return self._load_sample_data()
        
        return self._fetch_from_cost_explorer(days)
    
    def _load_sample_data(self) -> Dict[str, Any]:
        """Carga datos de ejemplo desde archivo JSON"""
        sample_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'sample_cost_data.json')
        
        try:
            with open(sample_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            print("✅ Datos de ejemplo cargados correctamente")
            return data
        except FileNotFoundError:
            raise FileNotFoundError(f"No se encontró el archivo de datos de ejemplo: {sample_file}")
    
    def _fetch_from_cost_explorer(self, days: int) -> Dict[str, Any]:
        """
        Obtiene datos reales de AWS Cost Explorer
        
        Args:
            days: Número de días a analizar
            
        Returns:
            Diccionario con datos de costes formateados
        """
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=days)
        
        try:
            # Obtener costes por servicio
            response = self.ce_client.get_cost_and_usage(
                TimePeriod={
                    'Start': start_date.strftime('%Y-%m-%d'),
                    'End': end_date.strftime('%Y-%m-%d')
                },
                Granularity='MONTHLY',
                Metrics=['UnblendedCost'],
                GroupBy=[
                    {
                        'Type': 'DIMENSION',
                        'Key': 'SERVICE'
                    }
                ]
            )
            
            # Formatear respuesta
            services = []
            total_cost = 0.0
            
            for result in response['ResultsByTime']:
                for group in result['Groups']:
                    service_name = group['Keys'][0]
                    cost = float(group['Metrics']['UnblendedCost']['Amount'])
                    
                    if cost > 0:
                        services.append({
                            'service': service_name,
                            'cost': round(cost, 2)
                        })
                        total_cost += cost
            
            # Ordenar por coste descendente
            services.sort(key=lambda x: x['cost'], reverse=True)
            
            return {
                'analysis_period': {
                    'start': start_date.strftime('%Y-%m-%d'),
                    'end': end_date.strftime('%Y-%m-%d')
                },
                'total_cost': round(total_cost, 2),
                'currency': 'USD',
                'services': services[:10]  # Top 10 servicios
            }
            
        except ClientError as e:
            print(f"❌ Error al obtener datos de Cost Explorer: {e}")
            raise
    
    def get_cost_summary(self, cost_data: Dict[str, Any]) -> str:
        """
        Genera un resumen textual de los costes para enviar a Bedrock
        
        Args:
            cost_data: Datos de costes obtenidos
            
        Returns:
            Resumen en texto plano
        """
        summary = f"""
ANÁLISIS DE COSTES AWS
Período: {cost_data['analysis_period']['start']} a {cost_data['analysis_period']['end']}
Coste total: ${cost_data['total_cost']:.2f} USD

SERVICIOS CON MAYOR COSTE:
"""
        
        for i, service in enumerate(cost_data['services'][:10], 1):
            percentage = (service['cost'] / cost_data['total_cost']) * 100
            summary += f"{i}. {service['service']}: ${service['cost']:.2f} ({percentage:.1f}%)\n"
        
        # Añadir detalles adicionales si están disponibles
        if 'resource_summary' in cost_data:
            summary += f"\nRECURSOS DETECTADOS:\n"
            rs = cost_data['resource_summary']
            summary += f"- Instancias EC2: {rs.get('ec2_instances', 0)}\n"
            summary += f"- Instancias RDS: {rs.get('rds_instances', 0)}\n"
            summary += f"- Buckets S3: {rs.get('s3_buckets', 0)}\n"
            summary += f"- Volúmenes EBS: {rs.get('ebs_volumes', 0)}\n"
            summary += f"- Volúmenes huérfanos: {rs.get('orphaned_volumes', 0)}\n"
            summary += f"- IPs elásticas sin usar: {rs.get('unattached_eips', 0)}\n"
            summary += f"- Snapshots antiguos: {rs.get('old_snapshots', 0)}\n"
        
        return summary


if __name__ == "__main__":
    # Test del módulo
    analyzer = CostAnalyzer(demo_mode=True)
    data = analyzer.get_cost_data()
    print(json.dumps(data, indent=2, ensure_ascii=False))
    print("\n" + "="*80 + "\n")
    print(analyzer.get_cost_summary(data))
