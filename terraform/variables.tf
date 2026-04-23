variable "aws_region" {
  description = "AWS region donde desplegar los recursos"
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Nombre del proyecto"
  type        = string
  default     = "aws-cost-optimizer-ai"
}

variable "environment" {
  description = "Entorno de despliegue"
  type        = string
  default     = "production"
}

variable "bedrock_model_id" {
  description = "ID del modelo de Bedrock a usar"
  type        = string
  default     = "anthropic.claude-3-5-sonnet-20241022-v2:0"
}

variable "lambda_zip_path" {
  description = "Ruta al archivo ZIP de Lambda"
  type        = string
  default     = "../lambda_package.zip"
}

variable "schedule_expression" {
  description = "Expresión cron para EventBridge (ejecución semanal por defecto)"
  type        = string
  default     = "cron(0 9 ? * MON *)"  # Lunes a las 9:00 AM UTC
}
