terraform {
  required_version = ">= 1.0"
  
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# S3 Bucket para almacenar resultados
resource "aws_s3_bucket" "cost_optimizer_results" {
  bucket = "${var.project_name}-results-${data.aws_caller_identity.current.account_id}"
  
  tags = {
    Name        = "AWS Cost Optimizer Results"
    Environment = var.environment
    ManagedBy   = "Terraform"
  }
}

resource "aws_s3_bucket_versioning" "results_versioning" {
  bucket = aws_s3_bucket.cost_optimizer_results.id
  
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "results_encryption" {
  bucket = aws_s3_bucket.cost_optimizer_results.id
  
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

# IAM Role para Lambda
resource "aws_iam_role" "lambda_role" {
  name = "${var.project_name}-lambda-role"
  
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
  
  tags = {
    Name = "Cost Optimizer Lambda Role"
  }
}

# Policy para Lambda - CloudWatch Logs
resource "aws_iam_role_policy_attachment" "lambda_basic" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

# Policy para Cost Explorer
resource "aws_iam_role_policy" "cost_explorer_policy" {
  name = "${var.project_name}-cost-explorer-policy"
  role = aws_iam_role.lambda_role.id
  
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "ce:GetCostAndUsage",
          "ce:GetCostForecast"
        ]
        Resource = "*"
      }
    ]
  })
}

# Policy para Bedrock
resource "aws_iam_role_policy" "bedrock_policy" {
  name = "${var.project_name}-bedrock-policy"
  role = aws_iam_role.lambda_role.id
  
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "bedrock:InvokeModel"
        ]
        Resource = "arn:aws:bedrock:${var.aws_region}::foundation-model/${var.bedrock_model_id}"
      }
    ]
  })
}

# Policy para S3
resource "aws_iam_role_policy" "s3_policy" {
  name = "${var.project_name}-s3-policy"
  role = aws_iam_role.lambda_role.id
  
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:PutObject",
          "s3:GetObject"
        ]
        Resource = "${aws_s3_bucket.cost_optimizer_results.arn}/*"
      }
    ]
  })
}

# Lambda Function
resource "aws_lambda_function" "cost_optimizer" {
  filename         = var.lambda_zip_path
  function_name    = var.project_name
  role            = aws_iam_role.lambda_role.arn
  handler         = "main.lambda_handler"
  source_code_hash = fileexists(var.lambda_zip_path) ? filebase64sha256(var.lambda_zip_path) : null
  runtime         = "python3.11"
  timeout         = 300
  memory_size     = 512
  
  environment {
    variables = {
      BEDROCK_MODEL_ID = var.bedrock_model_id
      BEDROCK_REGION   = var.aws_region
      S3_BUCKET        = aws_s3_bucket.cost_optimizer_results.id
      DEMO_MODE        = "false"
    }
  }
  
  tags = {
    Name        = "AWS Cost Optimizer"
    Environment = var.environment
  }
}

# EventBridge Rule - Ejecución semanal
resource "aws_cloudwatch_event_rule" "weekly_schedule" {
  name                = "${var.project_name}-weekly"
  description         = "Ejecuta análisis de costes semanalmente"
  schedule_expression = var.schedule_expression
  
  tags = {
    Name = "Cost Optimizer Weekly Schedule"
  }
}

resource "aws_cloudwatch_event_target" "lambda_target" {
  rule      = aws_cloudwatch_event_rule.weekly_schedule.name
  target_id = "CostOptimizerLambda"
  arn       = aws_lambda_function.cost_optimizer.arn
}

resource "aws_lambda_permission" "allow_eventbridge" {
  statement_id  = "AllowExecutionFromEventBridge"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.cost_optimizer.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.weekly_schedule.arn
}

# Data sources
data "aws_caller_identity" "current" {}
