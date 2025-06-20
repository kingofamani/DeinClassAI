#!/bin/bash

# DeinClassAI System Startup Script (Linux/macOS)
# This script will start all necessary services

echo "🚀 Starting DeinClassAI System..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Error: Docker is not running, please start Docker first"
    exit 1
fi
echo "✅ Docker is running normally"

# Check if docker-compose is available
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Error: docker-compose is not installed or unavailable"
    exit 1
fi
echo "✅ docker-compose is available"

# Check for required environment variable files
if [ ! -f ".env.litellm" ]; then
    echo "⚠️  Warning: .env.litellm file does not exist"
    echo "📋 Please create .env.litellm file based on .env.litellm.example"
    echo ""
    echo "Quick create command:"
    echo "cp .env.litellm.example .env.litellm"
    echo ""
    
    read -p "Do you want to automatically create .env.litellm file? (y/N): " response
    if [[ "$response" =~ ^[Yy]$ ]]; then
        cp .env.litellm.example .env.litellm
        echo "✅ Created .env.litellm file, please edit the configuration values"
    else
        echo "❌ Please manually create .env.litellm file and run again"
        exit 1
    fi
fi

echo ""
echo "🔧 Starting services..."

# Build and start all services (including teacher panel)
docker-compose --profile full up -d

# Wait for services to start
echo "⏳ Waiting for services to start..."
sleep 10

# Check service status
echo ""
echo "📊 Service Status Check:"

# Check PostgreSQL
if docker-compose ps postgres | grep -q "Up"; then
    echo "✅ PostgreSQL Database: Running"
else
    echo "❌ PostgreSQL Database: Failed to start"
fi

# Check LiteLLM
if docker-compose ps litellm | grep -q "Up"; then
    echo "✅ LiteLLM Service: Running"
    echo "   📍 Management Interface: http://localhost:4000"
else
    echo "❌ LiteLLM Service: Failed to start"
fi

# Check Open WebUI
if docker-compose ps open_webui | grep -q "Up"; then
    echo "✅ Open WebUI: Running"
    echo "   📍 Student Interface: http://localhost:8080"
else
    echo "❌ Open WebUI: Failed to start"
fi

# Check Teacher Panel
if docker-compose ps teacher_panel | grep -q "Up"; then
    echo "✅ Teacher Management Panel: Running"
    echo "   📍 Management Interface: http://localhost:5000"
else
    echo "⚠️  Teacher Management Panel: Not started (use --profile full to start)"
fi

echo ""
echo "🎉 DeinClassAI System startup completed!"
echo ""
echo "📌 Service URLs:"
echo "   🧑‍🏫 Teacher Management Panel: http://localhost:5000"
echo "   🎓 Student AI Classroom: http://localhost:8080"
echo "   ⚙️  LiteLLM Management: http://localhost:4000"
echo ""
echo "📖 Usage Instructions:"
echo "   1. Open Teacher Management Panel to create student passes"
echo "   2. Let students scan QR Code or use the link to setup"
echo "   3. Students can start learning in the AI classroom"
echo ""
echo "🛑 Stop system: docker-compose down"
echo "📋 View logs: docker-compose logs -f [service-name]"

# Ask if user wants to open browser
echo ""
read -p "Do you want to open the Teacher Management Panel in browser? (y/N): " openBrowser
if [[ "$openBrowser" =~ ^[Yy]$ ]]; then
    # Try different browsers based on the system
    if command -v xdg-open > /dev/null; then
        xdg-open "http://localhost:5000"
    elif command -v open > /dev/null; then
        open "http://localhost:5000"
    else
        echo "Please manually open http://localhost:5000 in your browser"
    fi
fi 