#!/bin/bash
set -euo pipefail

exec > >(tee /var/log/user-data.log | logger -t user-data -s 2>/dev/console) 2>&1
echo "=== Bootstrap started at $(date) ==="


apt-get update -y
apt-get install -y docker.io git curl


curl -SL https://github.com/docker/compose/releases/download/v2.24.0/docker-compose-linux-x86_64 \
  -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose


systemctl start docker
systemctl enable docker
usermod -aG docker ubuntu


cd /home/ubuntu
git clone https://github.com/Roma-rgb-tech/devsecops-pipeline-demo.git app
cd app

sudo -u ubuntu docker-compose up -d --build

echo "=== Bootstrap completed at $(date) ==="


GRAFANA_ENDPOINT=$(aws ssm get-parameter \
  --name "/devsecops/grafana/endpoint" \
  --query "Parameter.Value" --output text --region eu-central-1)

GRAFANA_INSTANCE_ID=$(aws ssm get-parameter \
  --name "/devsecops/grafana/instance_id" \
  --query "Parameter.Value" --output text --region eu-central-1)

GRAFANA_API_KEY=$(aws ssm get-parameter \
  --name "/devsecops/grafana/api_key" \
  --with-decryption \
  --query "Parameter.Value" --output text --region eu-central-1)


cat > /home/ubuntu/app/.env << EOF
GRAFANA_ENDPOINT=${GRAFANA_ENDPOINT}
GRAFANA_INSTANCE_ID=${GRAFANA_INSTANCE_ID}
GRAFANA_API_KEY=${GRAFANA_API_KEY}
EOF

chown ubuntu:ubuntu /home/ubuntu/app/.env