# GreenStack SSL/TLS Production Deployment

This directory contains Nginx configuration and setup scripts for deploying GreenStack with HTTPS in production.

## Quick Start

### Prerequisites

- Ubuntu/Debian Linux server with root access
- Domain name pointing to your server's IP address
- Ports 80 and 443 open in firewall

### Automated Setup

Run the automated setup script:

```bash
cd deployment/nginx
sudo chmod +x setup-ssl.sh
sudo ./setup-ssl.sh
```

The script will:
1. Install Nginx and Certbot
2. Configure Nginx with security best practices
3. Obtain Let's Encrypt SSL certificate
4. Set up automatic certificate renewal
5. Enable HTTPS with HTTP redirect

### Manual Setup

If you prefer manual configuration:

#### 1. Install Dependencies

```bash
sudo apt-get update
sudo apt-get install -y nginx certbot python3-certbot-nginx
```

#### 2. Copy Configuration

```bash
sudo cp greenstack.conf /etc/nginx/sites-available/greenstack.conf
```

Edit the configuration file and replace `greenstack.example.com` with your domain:

```bash
sudo nano /etc/nginx/sites-available/greenstack.conf
```

#### 3. Enable Site

```bash
sudo ln -s /etc/nginx/sites-available/greenstack.conf /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default  # Remove default site
sudo nginx -t  # Test configuration
sudo systemctl restart nginx
```

#### 4. Obtain SSL Certificate

```bash
sudo certbot --nginx -d your-domain.com
```

Follow the prompts to complete setup.

#### 5. Setup Auto-Renewal

```bash
sudo crontab -e
```

Add this line:

```
0 */12 * * * certbot renew --quiet --post-hook "systemctl reload nginx"
```

## Configuration Details

### Security Features

The Nginx configuration includes:

- **TLS 1.2 and 1.3 only** - Older protocols disabled
- **Strong cipher suites** - Mozilla Intermediate configuration
- **HSTS** - HTTP Strict Transport Security (1 year)
- **OCSP Stapling** - Improved SSL handshake performance
- **Security headers** - X-Frame-Options, X-Content-Type-Options, CSP, etc.
- **Rate limiting** - Protection against DoS attacks (configurable)

### File Upload Settings

- **Max upload size**: 100 MB (for IODD/EDS files)
- **Upload timeout**: 300 seconds
- Configurable in `client_max_body_size` directive

### Proxy Configuration

- Backend API on port 8000
- WebSocket support enabled
- Proper forwarding headers (X-Real-IP, X-Forwarded-For, etc.)
- Streaming response support (no buffering)

## Directory Structure

```
/var/www/greenstack/
├── frontend/
│   └── dist/          # React build output
└── backend/
    └── greenstack.db  # SQLite database

/etc/nginx/
├── sites-available/
│   └── greenstack.conf
└── sites-enabled/
    └── greenstack.conf -> ../sites-available/greenstack.conf

/etc/letsencrypt/live/your-domain/
├── fullchain.pem      # SSL certificate
├── privkey.pem        # Private key
└── chain.pem          # Certificate chain
```

## Deployment Steps

### 1. Build Frontend

```bash
cd frontend
npm install
npm run build
```

### 2. Deploy Frontend

```bash
sudo mkdir -p /var/www/greenstack/frontend
sudo cp -r dist /var/www/greenstack/frontend/
sudo chown -R www-data:www-data /var/www/greenstack
```

### 3. Start Backend

```bash
cd backend
python3 -m uvicorn src.api:app --host 127.0.0.1 --port 8000
```

For production, use a process manager like systemd or supervisor.

### 4. Verify

Visit `https://your-domain.com` and confirm:
- HTTPS is working
- No certificate warnings
- API endpoints respond correctly
- Static assets load properly

## Troubleshooting

### Check Nginx Status

```bash
sudo systemctl status nginx
```

### View Error Logs

```bash
sudo tail -f /var/log/nginx/greenstack-error.log
```

### Test Configuration

```bash
sudo nginx -t
```

### Check SSL Certificate

```bash
sudo certbot certificates
```

### Force Certificate Renewal

```bash
sudo certbot renew --force-renewal
```

### Common Issues

#### 1. Port 80/443 Already in Use

```bash
sudo netstat -tulpn | grep :80
sudo netstat -tulpn | grep :443
```

Stop conflicting services or change ports.

#### 2. Certificate Validation Failed

Ensure:
- Domain DNS points to your server
- Port 80 is accessible from internet
- No firewall blocking Let's Encrypt validation

#### 3. 502 Bad Gateway

Backend not running or wrong port:

```bash
curl http://127.0.0.1:8000/health
```

Should return backend health check response.

#### 4. Upload Size Limit

If uploads fail, check:
- `client_max_body_size` in Nginx config
- Backend file size limits
- Available disk space

## SSL Certificate Renewal

Certificates auto-renew via cron job. Manual renewal:

```bash
sudo certbot renew
sudo systemctl reload nginx
```

Test renewal without actually renewing:

```bash
sudo certbot renew --dry-run
```

## Security Recommendations

1. **Firewall**: Only open ports 22 (SSH), 80 (HTTP), 443 (HTTPS)
2. **SSH**: Use key-based authentication, disable root login
3. **Updates**: Keep system and packages updated
4. **Monitoring**: Set up log monitoring and alerting
5. **Backups**: Regular database and configuration backups
6. **Rate Limiting**: Configure based on your traffic patterns

## Performance Optimization

### Enable Gzip Compression

Already configured in main nginx.conf. If needed:

```nginx
gzip on;
gzip_types text/plain text/css application/json application/javascript;
gzip_min_length 1000;
```

### Enable HTTP/2

Already enabled with `http2` flag in `listen` directive.

### Cache Static Assets

Already configured with 1-year expiration for static files.

## Monitoring

### SSL Certificate Expiry

Set up monitoring to alert 30 days before expiry:

```bash
# Check expiry date
openssl x509 -enddate -noout -in /etc/letsencrypt/live/your-domain/cert.pem
```

### Uptime Monitoring

Use external services like:
- UptimeRobot
- Pingdom
- StatusCake

### Log Analysis

Install and configure log analysis tools:

```bash
sudo apt-get install goaccess
sudo goaccess /var/log/nginx/greenstack-access.log --log-format=COMBINED
```

## Support

For issues or questions:
- GitHub Issues: https://github.com/anthropics/greenstack/issues
- Documentation: https://docs.greenstack.io

## License

Same as GreenStack project license.
