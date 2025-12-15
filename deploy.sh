#!/bin/bash
# Cloud deployment helper script for 500MB memory

echo "🚀 PDF QA Chatbot - Cloud Deployment Setup"
echo "==========================================="
echo ""

# Check if Python 3.11 is available
if ! command -v python3.11 &> /dev/null; then
    echo "⚠️  Python 3.11 not found. Cloud providers need Python 3.11+"
    echo "   Available: $(python3 --version 2>&1)"
fi

# Check requirements
echo "📋 Checking dependencies..."
if [ -f "requirements.txt" ]; then
    echo "✓ requirements.txt found"
else
    echo "✗ requirements.txt not found"
    exit 1
fi

# Check environment variables
echo ""
echo "🔐 Environment Variables Check:"
echo ""

required_vars=("GROQ_API_KEY" "HUGGINGFACE_API_KEY" "SUPABASE_URL" "SUPABASE_ANON_KEY")
missing_vars=()

for var in "${required_vars[@]}"; do
    if [ -z "${!var}" ]; then
        echo "⚠️  $var not set"
        missing_vars+=("$var")
    else
        # Show first/last chars to verify it's set
        value="${!var}"
        echo "✓ $var is set (${#value} chars)"
    fi
done

echo ""

if [ ${#missing_vars[@]} -gt 0 ]; then
    echo "❌ Missing environment variables:"
    printf '   %s\n' "${missing_vars[@]}"
    echo ""
    echo "Set them in your cloud provider dashboard:"
    echo "  - Render: Settings → Environment"
    echo "  - Railway: Variables → Add"
    echo "  - Fly: flyctl secrets set KEY=value"
    exit 1
fi

echo "✓ All environment variables set!"
echo ""

# Check .env file for local testing
if [ -f ".env" ]; then
    echo "✓ .env file found (for local testing)"
else
    echo "⚠️  .env file not found (needed for local testing)"
    echo "   Create .env with your environment variables for local testing"
fi

echo ""
echo "📊 Memory Configuration:"
echo "   Chunk size: 300 (optimized for 500MB)"
echo "   Batch size: 2 (minimal memory)"
echo "   Max PDF size: ~40MB recommended"
echo ""

echo "🌐 Cloud Provider Options:"
echo ""
echo "1. Render.com (FREE - Easiest)"
echo "   - Free tier: 512MB memory"
echo "   - Deploy: Push to GitHub → Connect to Render"
echo "   - URL: https://render.com"
echo ""

echo "2. Railway.app ($5/month)"
echo "   - 512MB guaranteed memory"
echo "   - Better reliability than free tier"
echo "   - URL: https://railway.app"
echo ""

echo "3. Fly.io ($2.50/month)"
echo "   - Scalable pricing"
echo "   - Auto-scaling available"
echo "   - URL: https://fly.io"
echo ""

echo "✅ Setup Complete!"
echo ""
echo "Next steps:"
echo "1. Test locally: python main.py"
echo "2. Push to GitHub"
echo "3. Connect to your cloud provider"
echo "4. Set environment variables"
echo "5. Deploy!"
echo ""
echo "For detailed guide, see: CLOUD_DEPLOYMENT_500MB.md"
