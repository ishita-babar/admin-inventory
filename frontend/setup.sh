#!/bin/bash

echo "🚀 Setting up Inventory Dashboard Frontend..."

# Install dependencies
echo "📦 Installing dependencies..."
npm install

# Check if installation was successful
if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully!"
    echo ""
    echo "🎯 Next steps:"
    echo "1. Make sure your backend is running on http://localhost:8080"
    echo "2. Start the development server: npm run dev"
    echo "3. Open http://localhost:3000 in your browser"
    echo ""
    echo "📋 Available commands:"
    echo "  npm run dev    - Start development server"
    echo "  npm run build  - Build for production"
    echo "  npm run start  - Start production server"
    echo "  npm run lint   - Run ESLint"
else
    echo "❌ Failed to install dependencies. Please check your Node.js installation."
    exit 1
fi 