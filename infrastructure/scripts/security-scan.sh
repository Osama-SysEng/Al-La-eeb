#!/bin/bash
# Al-La'eeb Security Scan Script
# Run before deployment

echo "🔒 Al-La'eeb Security Scan"
echo "=============================="

# Check for secrets in code
echo "🔍 Scanning for secrets..."
if command -v git &> /dev/null; then
    git log --all --full-history --source -- .env* 2>/dev/null | head -5
fi

# Check for hardcoded passwords
echo "🔍 Checking for hardcoded credentials..."
grep -r "password.*=" backend/ --include="*.py" | grep -v "PASSWORD.*\${" | grep -v "example" | head -5

# Check file permissions
echo "🔍 Checking file permissions..."
find backend/ -type f -perm /o+w 2>/dev/null

# Check Docker security
echo "🔍 Checking Docker security..."
if command -v docker &> /dev/null; then
    docker-compose config --quiet 2>/dev/null && echo "✅ Docker Compose valid" || echo "❌ Docker Compose invalid"
fi

# Check for dependency vulnerabilities
echo "🔍 Checking Python dependencies..."
if command -v safety &> /dev/null; then
    safety check -r backend/services/auth-service/requirements.txt
else
    echo "⚠️  Install 'safety' for dependency scanning: pip install safety"
fi

echo ""
echo "✅ Security scan complete"
echo "📋 Review any findings above before deployment"
