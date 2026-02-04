#!/bin/bash

# SSL Certificate Troubleshooting Script
# Run this on the server to diagnose SSL certificate issues

DOMAIN="smartleaves.dclouds.ru"
SERVER_IP="37.9.5.160"

echo "🔍 SSL Certificate Troubleshooting for $DOMAIN"
echo "================================================"
echo ""

# 1. Check DNS configuration
echo "1️⃣ Checking DNS configuration..."
if command -v dig &> /dev/null; then
    dig +short $DOMAIN A
else
    nslookup $DOMAIN | grep Address | tail -n1
fi
echo ""

# 2. Check if domain resolves to correct IP
echo "2️⃣ Checking if domain resolves to $SERVER_IP..."
RESOLVED_IP=$(dig +short $DOMAIN A 2>/dev/null || nslookup $DOMAIN | grep Address | tail -n1 | awk '{print $2}')
if [ "$RESOLVED_IP" == "$SERVER_IP" ]; then
    echo "✅ DNS correctly points to $SERVER_IP"
else
    echo "❌ DNS issue: Domain resolves to $RESOLVED_IP instead of $SERVER_IP"
    echo "   Please update your DNS A record to point to $SERVER_IP"
fi
echo ""

# 3. Check if port 80 is accessible
echo "3️⃣ Checking if port 80 is accessible..."
if curl -s -o /dev/null -w "%{http_code}" http://$DOMAIN --connect-timeout 5 > /dev/null 2>&1; then
    HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://$DOMAIN --connect-timeout 5)
    echo "✅ Port 80 is accessible (HTTP $HTTP_CODE)"
else
    echo "❌ Cannot connect to port 80"
    echo "   Check firewall: sudo ufw status"
fi
echo ""

# 4. Check if nginx is serving certbot webroot
echo "4️⃣ Testing certbot webroot path..."
if docker compose -f docker-compose.prod.yml &> /dev/null; then
    DOCKER_COMPOSE="docker compose"
else
    DOCKER_COMPOSE="docker-compose"
fi

# Create test file
$DOCKER_COMPOSE -f docker-compose.prod.yml exec -T nginx sh -c "mkdir -p /var/www/certbot/.well-known/acme-challenge && echo 'test' > /var/www/certbot/.well-known/acme-challenge/test.txt" 2>/dev/null

if curl -s http://$DOMAIN/.well-known/acme-challenge/test.txt | grep -q "test"; then
    echo "✅ Webroot is correctly configured and accessible"
else
    echo "❌ Webroot test failed - nginx cannot serve challenge files"
fi

# Cleanup
$DOCKER_COMPOSE -f docker-compose.prod.yml exec -T nginx rm -f /var/www/certbot/.well-known/acme-challenge/test.txt 2>/dev/null
echo ""

# 5. Check existing certificates
echo "5️⃣ Checking for existing certificates..."
CERTS=$($DOCKER_COMPOSE -f docker-compose.prod.yml run --rm certbot certificates 2>&1)
if echo "$CERTS" | grep -q "No certificates found"; then
    echo "✅ No existing certificates found - ready to obtain new certificate"
else
    echo "📋 Existing certificates:"
    echo "$CERTS"
fi
echo ""

# 6. Check certbot logs
echo "6️⃣ Checking recent certbot logs..."
if [ -f /var/log/letsencrypt/letsencrypt.log ]; then
    echo "Last 20 lines of certbot log:"
    tail -n 20 /var/log/letsencrypt/letsencrypt.log
else
    echo "⚠️  No certbot log file found at /var/log/letsencrypt/letsencrypt.log"
fi
echo ""

# 7. Recommendations
echo "📝 Recommendations:"
echo "================================================"
echo ""

if [ "$RESOLVED_IP" != "$SERVER_IP" ]; then
    echo "❌ CRITICAL: Fix DNS first!"
    echo "   - Log into your DNS provider (dclouds.ru)"
    echo "   - Create/update A record: $DOMAIN → $SERVER_IP"
    echo "   - Wait 5-15 minutes for DNS propagation"
    echo "   - Run this script again to verify"
    echo ""
fi

echo "To obtain SSL certificate after DNS is configured:"
echo ""
echo "   ./deploy.sh ssl your_email@example.com $DOMAIN"
echo ""
echo "Or manually with verbose output:"
echo ""
echo "   $DOCKER_COMPOSE -f docker-compose.prod.yml run --rm certbot certonly \\"
echo "     --webroot \\"
echo "     --webroot-path=/var/www/certbot \\"
echo "     --email your_email@example.com \\"
echo "     --agree-tos \\"
echo "     --no-eff-email \\"
echo "     --verbose \\"
echo "     -d $DOMAIN"
echo ""
