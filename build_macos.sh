#!/bin/bash
# Build script for macOS

echo "========================================"
echo "InerScan Pro - macOS Build Script"
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
echo "Building macOS app bundle..."
pyinstaller --clean --windowed --name "InerScan Pro" scanner_app.py

# Check if build succeeded
if [ -d "dist/InerScan Pro.app" ]; then
    echo ""
    echo "========================================"
    echo "✅ Build succeeded!"
    echo "========================================"
    echo ""
    echo "App bundle location: dist/InerScan Pro.app"
    du -sh "dist/InerScan Pro.app"
    echo ""
    echo "Creating DMG installer..."
    
    # Create DMG (optional, requires hdiutil)
    if command -v hdiutil &> /dev/null; then
        hdiutil create -volname "InerScan Pro" -srcfolder "dist/InerScan Pro.app" -ov -format UDZO "dist/InerScanPro.dmg"
        echo "DMG created: dist/InerScanPro.dmg"
    else
        echo "hdiutil not found. Skipping DMG creation."
    fi
    
    echo ""
    echo "You can now distribute the .app bundle or .dmg file"
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
