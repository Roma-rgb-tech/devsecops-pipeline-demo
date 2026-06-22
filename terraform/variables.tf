variable "aws_region" {
  description = "AWS region for deploy infastructure "
  type        = string
  default     = "eu-central-1"
}

variable "project_name" {
  description = "Name of project"
  type        = string
  default     = "devsecops-demo"
}

variable "environment" {
  description = "Environment (dev, staging, prod)"
  type        = string
  default     = "prod"

  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment would be : dev, staging or prod."
  }
}

variable "vpc_cidr" {
  description = "CIDR for VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "public_subnet_cidr" {
  description = "CIDR block for public subnet"
  type        = string
  default     = "10.0.1.0/24"
}

variable "instance_type" {
  description = "Type EC2 instance"
  type        = string
  default     = "t2.micro"
}

variable "ami_id" {
  description = "AMI ID for EC2 (Amazon Linux 2023, eu-central-1)"
  type        = string
  default     = "ami-0faab6bdbac9486fb"
}

variable "key_pair_name" {
  description = "Name SSH key pair for connections to  EC2"
  type        = string
  default     = "devsecops-demo-key"
}

variable "app_port" {
  description = "Port where FastApi is starting"
  type        = number
  default     = 8000
}

variable "my_ip" {
  description = "Your IP address for SSH access"
  type        = string
}

variable "grafana_endpoint" {
  description = "Grafana Cloud OTLP endpoint"
  type        = string
  default     = "https://otlp-gateway-prod-eu-north-0.grafana.net/otlp"
}

variable "grafana_instance_id" {
  description = "Grafana Cloud instance ID"
  type        = string
}

variable "grafana_api_key" {
  description = "Grafana Cloud API key"
  type        = string
  sensitive   = true
}