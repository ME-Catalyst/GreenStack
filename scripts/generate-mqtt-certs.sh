#!/bin/bash
###########################################
# MQTT TLS Certificate Generation Script
# Version: 1.0
# Purpose: Generate self-signed certificates for Mosquitto MQTT broker
###########################################

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Certificate directory
CERT_DIR="./config/mosquitto/certs"

echo -e "${GREEN}╔════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║  MQTT TLS Certificate Generator        ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════╝${NC}"
echo ""

# Check if openssl is available
if ! command -v openssl &> /dev/null; then
    echo -e "${RED}ERROR: openssl is required but not installed${NC}"
    exit 1
fi

# Create certificate directory
mkdir -p "$CERT_DIR"

echo -e "${YELLOW}Generating certificates in $CERT_DIR...${NC}"
echo ""

# Certificate configuration
DAYS=3650  # 10 years
COUNTRY="US"
STATE="State"
CITY="City"
ORG="GreenStack"
ORG_UNIT="IoT Platform"
COMMON_NAME="mqtt.greenstack.local"

# Generate CA (Certificate Authority)
echo -e "${GREEN}[1/3] Generating Certificate Authority (CA)...${NC}"
openssl req -new -x509 -days $DAYS -extensions v3_ca \
    -keyout "$CERT_DIR/ca.key" \
    -out "$CERT_DIR/ca.crt" \
    -subj "/C=$COUNTRY/ST=$STATE/L=$CITY/O=$ORG/OU=$ORG_UNIT/CN=CA" \
    -passout pass:

# Generate server key
echo -e "${GREEN}[2/3] Generating server private key...${NC}"
openssl genrsa -out "$CERT_DIR/server.key" 2048

# Generate server certificate signing request (CSR)
echo -e "${GREEN}[3/3] Generating and signing server certificate...${NC}"
openssl req -new -key "$CERT_DIR/server.key" \
    -out "$CERT_DIR/server.csr" \
    -subj "/C=$COUNTRY/ST=$STATE/L=$CITY/O=$ORG/OU=$ORG_UNIT/CN=$COMMON_NAME"

# Sign server certificate with CA
openssl x509 -req -in "$CERT_DIR/server.csr" \
    -CA "$CERT_DIR/ca.crt" \
    -CAkey "$CERT_DIR/ca.key" \
    -CAcreateserial \
    -out "$CERT_DIR/server.crt" \
    -days $DAYS

# Remove CSR (no longer needed)
rm "$CERT_DIR/server.csr"

# Set proper permissions
chmod 644 "$CERT_DIR/ca.crt"
chmod 644 "$CERT_DIR/server.crt"
chmod 600 "$CERT_DIR/server.key"
chmod 600 "$CERT_DIR/ca.key"

echo ""
echo -e "${GREEN}✓ Certificates generated successfully!${NC}"
echo ""
echo -e "${YELLOW}Generated files:${NC}"
echo "  - $CERT_DIR/ca.crt          (CA certificate - distribute to clients)"
echo "  - $CERT_DIR/ca.key          (CA private key - KEEP SECURE)"
echo "  - $CERT_DIR/server.crt      (Server certificate)"
echo "  - $CERT_DIR/server.key      (Server private key - KEEP SECURE)"
echo ""
echo -e "${YELLOW}NEXT STEPS:${NC}"
echo "  1. Update mosquitto.conf to enable TLS listener"
echo "  2. Restart Mosquitto broker: docker-compose restart mosquitto"
echo "  3. Distribute ca.crt to MQTT clients for verification"
echo "  4. Update client connections to use port 8883 with TLS"
echo ""
echo -e "${YELLOW}SECURITY NOTES:${NC}"
echo "  - These are self-signed certificates for development/testing"
echo "  - For production, use certificates from a trusted CA (Let's Encrypt, etc.)"
echo "  - Keep .key files secure and never commit to version control"
echo "  - Add $CERT_DIR/*.key to .gitignore"
echo ""
echo -e "${YELLOW}Testing TLS connection:${NC}"
echo "  mosquitto_sub -h localhost -p 8883 -t test/topic \\"
echo "    --cafile $CERT_DIR/ca.crt \\"
echo "    -u <username> -P <password>"
echo ""
