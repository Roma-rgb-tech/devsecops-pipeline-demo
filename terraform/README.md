# 🏗️ Terraform — AWS Infrastructure

> Infrastructure as Code for deploying the FastAPI application on AWS EC2.
> Uses S3 remote backend for state storage and DynamoDB for state locking.

---

## 📐 Architecture

```
Internet
    │
Internet Gateway
    │
┌───▼──────────────────────────────────┐
│           VPC (10.0.0.0/16)          │
│  ┌────────────────────────────────┐  │
│  │       Public Subnet            │  │
│  │       (10.0.1.0/24)            │  │
│  │                                │  │
│  │  ┌──────────────────────────┐  │  │
│  │  │  EC2 t2.micro            │  │  │
│  │  │  Amazon Linux 2023       │  │  │
│  │  │  Docker + FastAPI :8000  │  │  │
│  │  │  Elastic IP (static)     │  │  │
│  │  └──────────────────────────┘  │  │
│  └────────────────────────────────┘  │
└──────────────────────────────────────┘

S3 Bucket    → stores terraform.tfstate (remote backend)
DynamoDB     → state locking (prevents concurrent apply)
```

---

## 📁 File Structure

```
terraform/
├── versions.tf              # Terraform and provider version pins
├── backend.tf               # S3 remote backend + DynamoDB locking
├── variables.tf             # All input variables with descriptions
├── vpc.tf                   # VPC, Subnet, IGW, Route Table, Security Group
├── main.tf                  # EC2 instance + Elastic IP
├── outputs.tf               # Outputs: URL, IP, SSH command
├── user_data.sh             # EC2 bootstrap: installs Docker, runs app
├── terraform.tfvars.example # Example variable values
└── .gitignore               # Excludes state files and secrets from Git
```

---

## 🚀 Quick Start

### 1. Prerequisites

```bash
# Install Terraform
brew install terraform        # macOS
# or download from https://developer.hashicorp.com/terraform/install

# Install AWS CLI
brew install awscli

# Configure AWS credentials
aws configure
# AWS Access Key ID:     <your key>
# AWS Secret Access Key: <your secret>
# Default region:        eu-central-1
```

### 2. Create an SSH Key Pair

```bash
aws ec2 create-key-pair \
  --key-name devsecops-demo-key \
  --region eu-central-1 \
  --query 'KeyMaterial' \
  --output text > ~/.ssh/devsecops-demo-key.pem

chmod 400 ~/.ssh/devsecops-demo-key.pem
```

### 3. Bootstrap S3 + DynamoDB (run once)

> These resources must exist **before** running `terraform init`
> because Terraform uses them to store its own state.

```bash
# Create S3 bucket for Terraform state
aws s3api create-bucket \
  --bucket devsecops-demo-terraform-state \
  --region eu-central-1 \
  --create-bucket-configuration LocationConstraint=eu-central-1

# Enable versioning (allows rollback to previous state)
aws s3api put-bucket-versioning \
  --bucket devsecops-demo-terraform-state \
  --versioning-configuration Status=Enabled

# Create DynamoDB table for state locking
aws dynamodb create-table \
  --table-name terraform-state-lock \
  --attribute-definitions AttributeName=LockID,AttributeType=S \
  --key-schema AttributeName=LockID,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST \
  --region eu-central-1
```

### 4. Configure Variables

```bash
cp terraform.tfvars.example terraform.tfvars
# Edit terraform.tfvars with your values
```

### 5. Deploy

```bash
cd terraform/

# Download providers and connect to S3 backend
terraform init

# Preview what will be created (no changes applied)
terraform plan

# Apply — create the infrastructure
terraform apply
```

After a successful apply, Terraform will print:

```
app_url     = "http://x.x.x.x:8000"
app_docs_url = "http://x.x.x.x:8000/docs"
ssh_command = "ssh -i ~/.ssh/devsecops-demo-key.pem ec2-user@x.x.x.x"
```

### 6. Destroy Infrastructure (to avoid charges)

```bash
terraform destroy
```

---

## 🔄 CI/CD Integration

The `.github/workflows/terraform.yml` pipeline runs automatically:

| Event | Action |
|-------|--------|
| Pull Request to `main` | `terraform plan` — posts result as a PR comment |
| Push to `main` | `terraform apply` — deploys infrastructure |

### Required GitHub Secrets

Add these in `Settings → Secrets → Actions`:

| Secret | Value |
|--------|-------|
| `AWS_ACCESS_KEY_ID` | IAM user access key |
| `AWS_SECRET_ACCESS_KEY` | IAM user secret key |
| `AWS_REGION` | `eu-central-1` |

---

## 💰 AWS Free Tier Cost Estimate

| Resource | Free Tier | After Free Tier |
|----------|-----------|-----------------|
| EC2 t2.micro | 750 hours/month free | ~$8.5/month |
| S3 (state storage) | 5 GB free | < $0.01/month |
| DynamoDB (locking) | 25 GB free | < $0.01/month |
| Elastic IP | Free when attached to EC2 | $3.6/month |

> ⚠️ Always run `terraform destroy` after testing to stay within Free Tier limits.

---

## 🔐 Security Notes

- `terraform.tfvars` is listed in `.gitignore` — never commit it to Git
- Terraform state in S3 is encrypted at rest (`encrypt = true` in `backend.tf`)
- EC2 runs as a non-root user inside Docker (see `Dockerfile`)
- SSH access should be restricted to your IP in production:
  change `cidr_blocks = ["0.0.0.0/0"]` to `["your.ip.address/32"]` in `vpc.tf`