#!/bin/bash
# Build script for Linux

echo "========================================"
echo "InerScan Pro - Linux Build Script"
echo "========================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install/upgrade dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
pip install pyinstaller

# Clean previous builds
echo "Cleaning previous builds..."
rm -rf build dist

# Build executable
echo ""
echo "Building executable..."
pyinstaller --clean InerScanPro.spec

# Check if build succeeded
if [ -f "dist/InerScanPro" ]; then
    echo ""
    echo "========================================"
    echo "✅ Build succeeded!"
    echo "========================================"
    echo ""
    echo "Executable location: dist/InerScanPro"
    ls -lh dist/InerScanPro
    echo ""
    echo "Making executable..."
    chmod +x dist/InerScanPro
    echo ""
    echo "You can now distribute dist/InerScanPro"
    echo ""
else
    echo ""
    echo "========================================"
    echo "❌ Build failed!"
    echo "========================================"
    echo "Check the output above for errors."
    echo ""
    exit 1
fi
