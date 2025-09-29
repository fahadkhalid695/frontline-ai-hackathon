#!/bin/bash

echo "🐳 Starting Frontline Worker AI System with Docker"
echo "=================================================="

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Create data directory if it doesn't exist
mkdir -p data

# Build and start services
echo "🔨 Building and starting services..."
docker-compose up --build

echo "✅ System started with Docker!"
echo "📍 Backend:  http://localhost:5000"
echo "📍 Frontend: http://localhost:3000"
echo "🔗 Health:   http://localhost:5000/health"