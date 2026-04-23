# Guía de Configuración - AWS Cost Optimizer AI

## 📋 Requisitos Previos

### Software necesario
- Python 3.11 o superior
- pip (gestor de paquetes Python)
- Git
- AWS CLI (opcional, solo para despliegue real)
- Terraform 1.0+ (opcional, solo para despliegue IaC)

### Cuenta AWS (opcional para demo)
- Acceso a AWS Cost Explorer
- Acceso a Amazon Bedrock (región us-east-1 recomendada)
- Permisos IAM necesarios

---

## 🚀 Instalación Local

### 1. Clonar el repositorio

\`\`\`bash
git clone https://github.com/tu-usuario/aws-cost-optimizer-ai.git
cd aws-cost-optimizer-ai
\`\`\`

### 2. Crear entorno virtual

\`\`\`bash
# Crear entorno virtual
python3 -m venv venv

# Activar entorno virtual
# En macOS/Linux:
source venv/bin/activate

# En Windows:
venv\\Scripts\\activate
\`\`\`

### 3. Instalar dependencias

\`\`\`bash
pip install -r requirements.txt
\`\`\`

### 4. Configurar variables de entorno (opcional)

\`\`\`bash
cp .env.example .env
# Editar .env con tus valores si usas AWS real
\`\`\`

---

## 🎭 Modo DEMO (sin AWS)

Perfecto para probar el proyecto sin cuenta AWS:

\`\`\`bash
# Ejecutar análisis con datos de ejemplo
python src/main.py --demo

# Generar dashboard visual
python src/dashboard.py

# Abrir dashboard en navegador
open templates/dashboard.html  # macOS
xdg-open templates/dashboard.html  # Linux
start templates/dashboard.html  # Windows
\`\`\`

---

## ☁️ Configuración AWS Real

### 1. Configurar AWS CLI

\`\`\`bash
aws configure
# Ingresar:
# - AWS Access Key ID
# - AWS Secret Access Key
# - Default region: us-east-1
# - Default output format: json
\`\`\`

### 2. Habilitar Cost Explorer

1. Ir a AWS Console → Cost Management → Cost Explorer
2. Clic en "Enable Cost Explorer"
3. Esperar 24 horas para que se generen datos

### 3. Solicitar acceso a Bedrock

1. Ir a AWS Console → Amazon Bedrock
2. Seleccionar región us-east-1
3. Ir a "Model access"
4. Solicitar acceso a "Claude 3.5 Sonnet"
5. Esperar aprobación (usualmente instantánea)

### 4. Configurar permisos IAM

Crear una política IAM con estos permisos:

\`\`\`json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ce:GetCostAndUsage",
        "ce:GetCostForecast"
      ],
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "bedrock:InvokeModel"
      ],
      "Resource": "arn:aws:bedrock:us-east-1::foundation-model/anthropic.claude-3-5-sonnet-20241022-v2:0"
    }
  ]
}
\`\`\`

### 5. Ejecutar con AWS real

\`\`\`bash
# Editar .env y cambiar DEMO_MODE=false
python src/main.py --days 30

# Generar dashboard
python src/dashboard.py --input output/analysis_*.json
\`\`\`

---

## 🏗️ Despliegue en AWS (Serverless)

### Opción 1: Terraform (recomendado)

\`\`\`bash
# 1. Crear paquete Lambda
cd src
pip install -r ../requirements.txt -t package/
cp *.py package/
cd package
zip -r ../../lambda_package.zip .
cd ../..

# 2. Desplegar con Terraform
cd terraform
terraform init
terraform plan
terraform apply

# 3. Verificar despliegue
aws lambda invoke --function-name aws-cost-optimizer-ai output.json
cat output.json
\`\`\`

### Opción 2: Manual (AWS Console)

1. **Crear S3 Bucket**
   - Nombre: \`aws-cost-optimizer-results-{account-id}\`
   - Habilitar versionado
   - Habilitar cifrado

2. **Crear IAM Role**
   - Servicio: Lambda
   - Adjuntar políticas (ver sección anterior)

3. **Crear Lambda Function**
   - Runtime: Python 3.11
   - Memoria: 512 MB
   - Timeout: 5 minutos
   - Variables de entorno:
     - \`BEDROCK_MODEL_ID\`: anthropic.claude-3-5-sonnet-20241022-v2:0
     - \`BEDROCK_REGION\`: us-east-1
     - \`S3_BUCKET\`: nombre del bucket creado
     - \`DEMO_MODE\`: false

4. **Crear EventBridge Rule**
   - Schedule: \`cron(0 9 ? * MON *)\` (lunes 9 AM)
   - Target: Lambda function creada

---

## 🧪 Testing

\`\`\`bash
# Ejecutar tests unitarios
pytest tests/ -v

# Con cobertura
pytest --cov=src tests/

# Test de integración (modo demo)
python src/main.py --demo
\`\`\`

---

## 🐛 Troubleshooting

### Error: "ModuleNotFoundError"
\`\`\`bash
# Asegúrate de estar en el entorno virtual
source venv/bin/activate
pip install -r requirements.txt
\`\`\`

### Error: "FileNotFoundError: sample_cost_data.json"
\`\`\`bash
# Verifica que el archivo existe
ls data/sample_cost_data.json

# Si no existe, verifica que clonaste el repo completo
\`\`\`

### Error: "Access Denied" en AWS
\`\`\`bash
# Verifica credenciales
aws sts get-caller-identity

# Verifica permisos IAM
aws iam get-user-policy --user-name tu-usuario --policy-name tu-politica
\`\`\`

### Error: "Model not found" en Bedrock
- Verifica que solicitaste acceso al modelo en Bedrock Console
- Verifica que estás en la región correcta (us-east-1)
- Espera unos minutos después de solicitar acceso

---

## 📚 Recursos Adicionales

- [Documentación AWS Cost Explorer](https://docs.aws.amazon.com/cost-management/latest/userguide/ce-what-is.html)
- [Documentación Amazon Bedrock](https://docs.aws.amazon.com/bedrock/)
- [Guía de Terraform AWS](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)

---

## 💬 Soporte

¿Problemas con la configuración?

- 📧 Email: tu@email.com
- 💼 Malt: [Tu perfil](https://www.malt.es/profile/tu-perfil)
- 🐛 Issues: [GitHub Issues](https://github.com/tu-usuario/aws-cost-optimizer-ai/issues)
