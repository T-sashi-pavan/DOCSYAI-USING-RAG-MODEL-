#!/bin/bash

# Frontend Production Build Script for Cloudflare Pages
# This script prepares the frontend for deployment to Cloudflare Pages

echo "🚀 Preparing frontend for Cloudflare Pages deployment..."

# Create frontend-dist directory
FRONTEND_DIR="frontend-dist"
rm -rf $FRONTEND_DIR
mkdir -p $FRONTEND_DIR

# Copy static files
echo "📦 Copying static files..."
cp -r static/* $FRONTEND_DIR/

# Prompt for backend URL
read -p "Enter your production backend URL (e.g., https://your-backend.com or http://YOUR_VM_IP): " BACKEND_URL

# Update API_BASE in index.html
echo "🔧 Updating API_BASE to: $BACKEND_URL"
sed -i "s|const API_BASE = 'http://localhost:10000';|const API_BASE = '$BACKEND_URL';|g" $FRONTEND_DIR/index.html

# For Windows/Mac compatibility, also try with backup flag
if [[ "$OSTYPE" == "darwin"* ]]; then
    sed -i '' "s|const API_BASE = 'http://localhost:10000';|const API_BASE = '$BACKEND_URL';|g" $FRONTEND_DIR/index.html
fi

echo "✅ Frontend build complete!"
echo ""
echo "📁 Files ready in: $FRONTEND_DIR/"
echo ""
echo "Next steps:"
echo "1. Push the $FRONTEND_DIR directory to a GitHub repository"
echo "2. Connect the repository to Cloudflare Pages"
echo "3. Set build output directory to '/' (root)"
echo "4. Deploy!"
echo ""
echo "Or manually upload the contents of $FRONTEND_DIR/ to Cloudflare Pages"
