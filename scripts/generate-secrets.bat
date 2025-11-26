@echo off
REM ============================================================================
REM GreenStack Production Secrets Generator (Windows)
REM ============================================================================
REM Purpose: Generate strong, cryptographically secure secrets for production
REM Created: 2025-11-25
REM Usage: scripts\generate-secrets.bat > .env.production
REM ============================================================================

setlocal enabledelayedexpansion

echo # =============================================================================
echo # GreenStack Production Secrets
echo # Generated: %date% %time%
echo # =============================================================================
echo # SECURITY WARNING: Keep this file secure! Never commit to version control!
echo # =============================================================================
echo.

REM Check if OpenSSL is available
where openssl >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: OpenSSL not found! Install OpenSSL for Windows: >&2
    echo https://slproweb.com/products/Win32OpenSSL.html >&2
    exit /b 1
)

echo # =============================================================================
echo # CORE SECURITY
echo # =============================================================================
echo.

echo # Secret key for JWT tokens and session encryption
for /f %%i in ('openssl rand -hex 32') do echo SECRET_KEY=%%i
echo.

echo # JWT secret key (should be different from SECRET_KEY)
for /f %%i in ('openssl rand -hex 32') do echo JWT_SECRET_KEY=%%i
echo.

echo # =============================================================================
echo # DATABASE CREDENTIALS
echo # =============================================================================
echo.

echo # PostgreSQL database password
echo # Username: iodd_user ^| Database: iodd_manager
for /f %%i in ('openssl rand -base64 32') do echo POSTGRES_PASSWORD=%%i
echo.

echo # =============================================================================
echo # CACHE ^& MESSAGE QUEUE
echo # =============================================================================
echo.

echo # Redis password for cache and message queue
for /f %%i in ('openssl rand -base64 32') do echo REDIS_PASSWORD=%%i
echo.

echo # =============================================================================
echo # IOT PLATFORM SERVICES
echo # =============================================================================
echo.

echo # MQTT broker authentication password
echo # Username: iodd
for /f %%i in ('openssl rand -base64 32') do echo MQTT_PASSWORD=%%i
echo.

echo # InfluxDB authentication token
echo # Organization: iodd-manager ^| Bucket: device-telemetry
for /f %%i in ('openssl rand -base64 32') do echo INFLUXDB_TOKEN=%%i
echo.

echo # InfluxDB admin password
echo # Username: admin
for /f %%i in ('openssl rand -base64 32') do echo INFLUXDB_ADMIN_PASSWORD=%%i
echo.

echo # Grafana admin password
echo # Username: admin ^| Access: http://localhost:3000
for /f %%i in ('openssl rand -base64 32') do echo GRAFANA_ADMIN_PASSWORD=%%i
echo.

echo # Node-RED credential encryption secret
echo # Access: http://localhost:1880
for /f %%i in ('openssl rand -hex 32') do echo NODERED_CREDENTIAL_SECRET=%%i
echo.

echo # =============================================================================
echo # PRODUCTION CHECKLIST
echo # =============================================================================
echo #
echo # Before deploying to production, ensure you also:
echo # 1. Set ENVIRONMENT=production
echo # 2. Set DEBUG=false
echo # 3. Update CORS_ORIGINS to your domain (no wildcards!)
echo # 4. Set SHOW_ERROR_DETAILS=false
echo # 5. Enable TLS/SSL for all services
echo # 6. Configure backups (see scripts\backup.bat)
echo # 7. Set up monitoring alerts
echo # 8. Review all alert email addresses
echo # 9. Test disaster recovery procedures
echo # 10. Enable authentication (ENABLE_AUTH=true)
echo #
echo # Store this file securely:
echo # - Use secrets manager (AWS Secrets Manager, HashiCorp Vault, etc.)
echo # - Or encrypted storage with limited access
echo # - Never commit to version control
echo # - Rotate secrets every 90 days
echo #
echo # =============================================================================
echo.

echo SUCCESS: Secrets generated! Save to .env.production and keep secure! >&2
echo USAGE: scripts\generate-secrets.bat ^> .env.production >&2
