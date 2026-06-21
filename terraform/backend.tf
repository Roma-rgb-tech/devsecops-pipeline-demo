
terraform {
  backend "s3" {
    bucket         = "devsecops-demo-terraform-state-20260615-roman"
    key            = "prod/terraform.tfstate"
    region         = "eu-central-1"
    encrypt        = true
    dynamodb_table = "terraform-state-lock"
  }
}

