#!/bin/bash
# Sales Data Processing Script - Quick Installation Script
# This script provides a quick way to install dependencies on Unix-like systems

set -e  # Exit on any error

echo "🚀 Sales Data Processing Script - Quick Install"
echo "=============================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.7 or higher."
    exit 1
fi

echo "✓ Python 3 is available: $(python3 --version)"

# Check if pip is installed
if ! command -v pip3 &> /dev/null && ! python3 -m pip --version &> /dev/null; then
    echo "❌ pip is not available. Please install pip."
    exit 1
fi

echo "✓ pip is available"

# Upgrade pip
echo "📦 Upgrading pip..."
python3 -m pip install --upgrade pip

# Install dependencies
echo "📦 Installing dependencies from requirements.txt..."
python3 -m pip install -r requirements.txt

echo ""
echo "✅ Installation completed successfully!"
echo ""
echo "📋 Next steps:"
echo "   1. Make sure you have 'sales_data.csv' in the current directory"
echo "   2. Run: python3 process_sales_data.py"
echo ""
echo "💡 For more options, run: python3 setup.py --help"