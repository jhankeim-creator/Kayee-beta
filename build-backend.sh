#!/bin/bash
# Render.com deployment script for Kayee01 Backend

echo "🚀 Starting Kayee01 backend deployment..."

# Install dependencies
echo "📦 Installing Python dependencies..."
pip install -r backend/requirements.txt

# Create uploads directory if it doesn't exist
echo "📁 Creating uploads directory..."
mkdir -p backend/uploads

echo "✅ Backend deployment preparation complete!"
echo "🎯 Backend will start with: uvicorn server:app --host 0.0.0.0 --port \$PORT"
