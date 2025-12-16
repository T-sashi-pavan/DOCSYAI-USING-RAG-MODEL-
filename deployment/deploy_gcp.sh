#!/bin/bash

# Backend Deployment Script for Google Cloud Compute Engine e2-micro
# This script automates the deployment of the RAG backend

set -e  # Exit on error

echo "🚀 Starting RAG Backend Deployment on Google Cloud..."

# Update system
echo "📦 Updating system packages..."
sudo apt-get update
sudo apt-get upgrade -y

# Install Python 3.11 and dependencies
echo "🐍 Installing Python 3.11..."
sudo apt-get install -y python3.11 python3.11-venv python3.11-dev python3-pip
sudo apt-get install -y git nginx

# Create user for running the service
echo "👤 Creating service user..."
sudo useradd -m -s /bin/bash raguser || echo "User raguser already exists"

# Create directories
echo "📁 Creating application directories..."
sudo -u raguser mkdir -p /home/raguser/ragbackend
sudo -u raguser mkdir -p /home/raguser/ragbackend/logs

# Clone repository (replace with your GitHub repo URL)
echo "📥 Cloning repository..."
read -p "Enter your GitHub repository URL: " REPO_URL
cd /home/raguser/ragbackend
sudo -u raguser git clone "$REPO_URL" . || echo "Repository already cloned"

# Create Python virtual environment
echo "🔧 Setting up Python virtual environment..."
sudo -u raguser python3.11 -m venv venv
sudo -u raguser /home/raguser/ragbackend/venv/bin/pip install --upgrade pip

# Install Python dependencies
echo "📚 Installing Python packages..."
sudo -u raguser /home/raguser/ragbackend/venv/bin/pip install -r requirements.txt

# Create .env file
echo "🔐 Setting up environment variables..."
if [ ! -f .env ]; then
    echo "Creating .env file. Please enter your API credentials:"
    read -p "Supabase URL: " SUPABASE_URL
    read -p "Supabase Key: " SUPABASE_KEY
    read -p "Groq API Key: " GROQ_API_KEY
    read -p "HuggingFace Token: " HUGGINGFACE_TOKEN
    
    sudo -u raguser tee .env > /dev/null <<EOF
SUPABASE_URL=$SUPABASE_URL
SUPABASE_KEY=$SUPABASE_KEY
GROQ_API_KEY=$GROQ_API_KEY
HUGGINGFACE_TOKEN=$HUGGINGFACE_TOKEN
EOF
    echo "✅ .env file created"
else
    echo "⚠️  .env file already exists. Skipping..."
fi

# Install systemd service
echo "🔧 Installing systemd service..."
sudo cp deployment/ragbackend.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable ragbackend
sudo systemctl start ragbackend

# Configure Nginx
echo "🌐 Configuring Nginx..."
sudo cp deployment/nginx.conf /etc/nginx/sites-available/ragbackend
sudo ln -sf /etc/nginx/sites-available/ragbackend /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# Get external IP
EXTERNAL_IP=$(curl -s ifconfig.me)
echo "🔧 Updating nginx config with IP: $EXTERNAL_IP"
sudo sed -i "s/your-backend-domain.com/$EXTERNAL_IP/g" /etc/nginx/sites-available/ragbackend

# Test and reload Nginx
sudo nginx -t
sudo systemctl restart nginx

# Open firewall ports
echo "🔥 Configuring firewall..."
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
echo "y" | sudo ufw enable || echo "Firewall already enabled"

# Check service status
echo ""
echo "✅ Deployment complete!"
echo ""
echo "📊 Service Status:"
sudo systemctl status ragbackend --no-pager -l
echo ""
echo "🌐 Your backend is accessible at:"
echo "   http://$EXTERNAL_IP"
echo ""
echo "📝 Useful commands:"
echo "   - Check logs: sudo journalctl -u ragbackend -f"
echo "   - Restart service: sudo systemctl restart ragbackend"
echo "   - Check Nginx: sudo nginx -t && sudo systemctl status nginx"
echo ""
echo "🔗 Update your Cloudflare Pages frontend to use:"
echo "   API_BASE = 'http://$EXTERNAL_IP'"
echo ""
