#!/bin/bash
# GreenStack SSL/TLS Setup Script
# Automates Let's Encrypt certificate installation and Nginx configuration

set -e  # Exit on any error

# Color output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}======================================${NC}"
echo -e "${GREEN}GreenStack SSL/TLS Setup${NC}"
echo -e "${GREEN}======================================${NC}"
echo ""

# Check if running as root
if [[ $EUID -ne 0 ]]; then
   echo -e "${RED}Error: This script must be run as root${NC}"
   exit 1
fi

# Prompt for domain name
read -p "Enter your domain name (e.g., greenstack.example.com): " DOMAIN
read -p "Enter your email address for Let's Encrypt notifications: " EMAIL

if [[ -z "$DOMAIN" || -z "$EMAIL" ]]; then
    echo -e "${RED}Error: Domain and email are required${NC}"
    exit 1
fi

echo -e "${YELLOW}Configuration:${NC}"
echo "  Domain: $DOMAIN"
echo "  Email: $EMAIL"
echo ""
read -p "Continue? (y/n): " CONFIRM
if [[ "$CONFIRM" != "y" ]]; then
    echo "Setup cancelled."
    exit 0
fi

# Install dependencies
echo -e "${GREEN}[1/7] Installing dependencies...${NC}"
apt-get update
apt-get install -y nginx certbot python3-certbot-nginx

# Stop Nginx if running
echo -e "${GREEN}[2/7] Stopping Nginx...${NC}"
systemctl stop nginx || true

# Create directories
echo -e "${GREEN}[3/7] Creating directories...${NC}"
mkdir -p /var/www/certbot
mkdir -p /var/www/greenstack/frontend/dist
mkdir -p /var/log/nginx

# Copy Nginx configuration
echo -e "${GREEN}[4/7] Configuring Nginx...${NC}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cp "$SCRIPT_DIR/greenstack.conf" /etc/nginx/sites-available/greenstack.conf

# Replace domain placeholder
sed -i "s/greenstack.example.com/$DOMAIN/g" /etc/nginx/sites-available/greenstack.conf

# Enable site
ln -sf /etc/nginx/sites-available/greenstack.conf /etc/nginx/sites-enabled/greenstack.conf

# Remove default site if exists
rm -f /etc/nginx/sites-enabled/default

# Test Nginx configuration
echo -e "${GREEN}[5/7] Testing Nginx configuration...${NC}"
nginx -t

# Start Nginx
echo -e "${GREEN}[6/7] Starting Nginx...${NC}"
systemctl start nginx
systemctl enable nginx

# Obtain Let's Encrypt certificate
echo -e "${GREEN}[7/7] Obtaining SSL certificate from Let's Encrypt...${NC}"
certbot certonly \
    --nginx \
    --non-interactive \
    --agree-tos \
    --email "$EMAIL" \
    -d "$DOMAIN" \
    --rsa-key-size 4096

# Reload Nginx with SSL configuration
echo -e "${GREEN}Reloading Nginx with SSL configuration...${NC}"
systemctl reload nginx

# Setup auto-renewal
echo -e "${GREEN}Setting up automatic certificate renewal...${NC}"
cat > /etc/cron.d/certbot-renew << EOF
# Renew Let's Encrypt certificates twice daily
0 */12 * * * root certbot renew --quiet --post-hook "systemctl reload nginx"
EOF

# Test auto-renewal
echo -e "${GREEN}Testing certificate renewal...${NC}"
certbot renew --dry-run

echo ""
echo -e "${GREEN}======================================${NC}"
echo -e "${GREEN}SSL/TLS Setup Complete!${NC}"
echo -e "${GREEN}======================================${NC}"
echo ""
echo -e "${GREEN}✓${NC} Nginx configured and running"
echo -e "${GREEN}✓${NC} SSL certificate obtained from Let's Encrypt"
echo -e "${GREEN}✓${NC} Automatic renewal configured"
echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo "1. Deploy your frontend build to: /var/www/greenstack/frontend/dist"
echo "2. Ensure backend is running on port 8000"
echo "3. Visit: https://$DOMAIN"
echo ""
echo -e "${YELLOW}Certificate locations:${NC}"
echo "  Certificate: /etc/letsencrypt/live/$DOMAIN/fullchain.pem"
echo "  Private Key: /etc/letsencrypt/live/$DOMAIN/privkey.pem"
echo ""
echo -e "${YELLOW}Useful commands:${NC}"
echo "  Check certificate status: certbot certificates"
echo "  Renew certificates: certbot renew"
echo "  Nginx status: systemctl status nginx"
echo "  View logs: tail -f /var/log/nginx/greenstack-error.log"
echo ""
