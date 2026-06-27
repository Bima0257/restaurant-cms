#!/usr/bin/env bash
# ============================================
# Restaurant CMS - VPS Initial Setup Script
# ============================================
# Run this ONCE on a fresh Ubuntu 22.04/24.04 VPS.
#   chmod +x setup-vps.sh
#   sudo ./setup-vps.sh
# ============================================
set -euo pipefail

DOMAIN="${1:-}"  # pass domain as first arg, or edit below
if [ -z "$DOMAIN" ]; then
    echo "Usage: $0 your-domain.com"
    exit 1
fi

echo "=== Updating system packages ==="
apt update && apt upgrade -y

echo "=== Installing dependencies ==="
apt install -y \
    nginx \
    certbot \
    python3-certbot-nginx \
    python3.11 \
    python3.11-venv \
    python3-pip \
    mysql-server \
    git \
    rsync

echo "=== Creating restaurant-app user ==="
id -u restaurant-app &>/dev/null || useradd -m -s /bin/bash restaurant-app

echo "=== Setting up directory structure ==="
mkdir -p /var/www/restaurant-cms/frontend
mkdir -p /opt/restaurant-cms/backend
mkdir -p /opt/restaurant-cms/backend/storage/uploads
mkdir -p /opt/restaurant-cms/backend/storage/backups

echo "=== Setting up MySQL ==="
systemctl enable mysql --now
mysql_secure_installation

echo "=== Please create the database manually ==="
echo "Run:"
echo "  mysql -u root -p"
echo "  CREATE DATABASE restaurant_cms;"
echo "  CREATE USER 'restaurant_user'@'localhost' IDENTIFIED BY 'your-strong-password';"
echo "  GRANT ALL ON restaurant_cms.* TO 'restaurant_user'@'localhost';"
echo "  FLUSH PRIVILEGES;"
echo "  EXIT;"

echo "=== Setting up Python virtual environment ==="
python3.11 -m venv /opt/restaurant-cms/venv

echo "=== Setting up Nginx ==="
cp deploy/nginx.conf /etc/nginx/sites-available/restaurant-cms
sed -i "s/your-domain.com/$DOMAIN/g" /etc/nginx/sites-available/restaurant-cms
ln -sf /etc/nginx/sites-available/restaurant-cms /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default
nginx -t && systemctl reload nginx

echo "=== Setting up SSL with Let's Encrypt ==="
certbot --nginx -d "$DOMAIN" --non-interactive --agree-tos -m admin@"$DOMAIN" || echo "Run certbot manually: certbot --nginx -d $DOMAIN"

echo "=== Setting up systemd service ==="
cp deploy/restaurant-backend.service /etc/systemd/system/restaurant-backend.service
systemctl daemon-reload
systemctl enable restaurant-backend.service

echo "=== Setting ownership ==="
chown -R restaurant-app:restaurant-app /opt/restaurant-cms
chown -R www-data:www-data /var/www/restaurant-cms

echo ""
echo "============================================"
echo "  Setup complete!"
echo ""
echo "  Next steps:"
echo "  1. Copy your .env file to /opt/restaurant-cms/.env"
echo "  2. Install Python deps:"
echo "     sudo -u restaurant-app /opt/restaurant-cms/venv/bin/pip install -r /opt/restaurant-cms/backend/requirements.txt"
echo "  3. Start backend: systemctl start restaurant-backend"
echo "  4. Push frontend build from CI/CD"
echo "============================================"
