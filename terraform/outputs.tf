output "vpc_id" {
  description = "VPC ID"
  value       = aws_vpc.main.id
}

output "public_subnet_ids" {
  description = "Public subnet IDs"
  value       = aws_subnet.public[*].id
}

output "private_subnet_ids" {
  description = "Private subnet IDs"
  value       = aws_subnet.private[*].id
}

output "availability_zones" {
  description = "Availability zones"
  value       = data.aws_availability_zones.available.names
}

output "nat_gateway_id" {
  description = "NAT Gateway ID"
  value       = aws_nat_gateway.main.id
}
output "alb_security_group_id" {
  description = "ALB security group ID"
  value       = aws_security_group.alb.id
}

output "ecs_security_group_id" {
  description = "ECS security group ID"
  value       = aws_security_group.ecs.id
}
output "alb_dns_name" {
  description = "Application Load Balancer DNS name"
  value       = aws_lb.main.dns_name
}

output "alb_target_group_arn" {
  description = "ALB target group ARN"
  value       = aws_lb_target_group.app.arn
}
output "ecs_task_execution_role_arn" {
  description = "ECS task execution role ARN"
  value       = aws_iam_role.ecs_task_execution.arn
}
output "ecs_cluster_name" {
  description = "ECS cluster name"
  value       = aws_ecs_cluster.main.name
}

output "ecs_log_group_name" {
  description = "CloudWatch log group name"
  value       = aws_cloudwatch_log_group.app.name
}
output "ecs_task_definition_arn" {
  description = "ECS task definition ARN"
  value       = aws_ecs_task_definition.app.arn
}
output "ecs_service_name" {
  description = "ECS service name"
  value       = aws_ecs_service.app.name
}
