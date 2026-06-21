output "instance_id" {
  description = "The EC2 instance ID"
  value       = aws_instance.app.id
}

output "public_ip" {
  description = "The public IP address (Elastic IP) of the application"
  value       = aws_eip.app.public_ip
}

output "public_dns" {
  description = "The public DNS of the EC2 instance"
  value       = aws_instance.app.public_dns
}

output "app_url" {
  description = "The application URL"
  value       = "http://${aws_eip.app.public_ip}:8000"
}

output "app_docs_url" {
  description = "The Swagger documentation URL"
  value       = "http://${aws_eip.app.public_ip}:8000/docs"
}

output "ssh_command" {
  description = "The command to connect to the EC2 instance via SSH"
  value       = "ssh -i ~/.ssh/${var.key_pair_name}.pem ec2-user@${aws_eip.app.public_ip}"
}

output "vpc_id" {
  description = "The VPC ID"
  value       = aws_vpc.main.id
}

output "security_group_id" {
  description = "The Security Group ID"
  value       = aws_security_group.app.id
}