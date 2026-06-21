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


curl -L https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb \
  -o /tmp/cloudflared.deb
dpkg -i /tmp/cloudflared.deb


cloudflared tunnel --url http://localhost:8000 \
  --no-autoupdate \
  --logfile /var/log/cloudflared.log \
  --pidfile /var/run/cloudflared.pid \
  --log-level info &


sleep 5
grep -o 'https://.*\.trycloudflare\.com' /var/log/cloudflared.log | head -1 | \
  xargs -I{} echo "=== Tunnel URL: {} ===" | tee -a /var/log/user-data.log