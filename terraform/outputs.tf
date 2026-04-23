output "lambda_function_name" {
  description = "Nombre de la función Lambda"
  value       = aws_lambda_function.cost_optimizer.function_name
}

output "lambda_function_arn" {
  description = "ARN de la función Lambda"
  value       = aws_lambda_function.cost_optimizer.arn
}

output "s3_bucket_name" {
  description = "Nombre del bucket S3 para resultados"
  value       = aws_s3_bucket.cost_optimizer_results.id
}

output "s3_bucket_arn" {
  description = "ARN del bucket S3"
  value       = aws_s3_bucket.cost_optimizer_results.arn
}

output "eventbridge_rule_name" {
  description = "Nombre de la regla EventBridge"
  value       = aws_cloudwatch_event_rule.weekly_schedule.name
}

output "iam_role_arn" {
  description = "ARN del rol IAM de Lambda"
  value       = aws_iam_role.lambda_role.arn
}
