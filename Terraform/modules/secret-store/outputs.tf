output "secretmanager_id" {
  description = "RDS endpoint"
  value       = aws_secretsmanager_secret.store.id
}

