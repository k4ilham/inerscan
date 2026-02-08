# 📄 InerScan Pro

[![Build and Release](https://github.com/k4ilham/inerscan/workflows/Build%20and%20Release/badge.svg)](https://github.com/k4ilham/inerscan/actions)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-2.5-brightgreen.svg)](https://github.com/k4ilham/inerscan/releases)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-blue.svg)](https://github.com/k4ilham/inerscan/releases)

> **Professional Document Scanner & Editor** - Transform your scanner into a powerful document digitization tool with AI-powered features, batch processing, watermarking, and comprehensive file management.

---

## ✨ Features Overview

### 🖨️ **Advanced Scanning**
- **WIA Scanner Support** - Native Windows Image Acquisition integration
- **Single Scan Mode** - Scan one page at a time
- **📚 Batch Scanning (NEW!)** - Automatic multi-page scanning
  - Set target number of pages or continuous mode
  - 2-second delay between scans
  - Real-time progress tracking
  - Stop anytime with one click
- **Live Preview** - See your scanned pages instantly
- **Auto-Detection** - Automatically detects connected scanners

### 🎨 **Professional Image Editing**

#### Basic Transformations
- **Rotate** - 90° left/right rotation with visual preview
- **Flip** - Horizontal and vertical flipping
- **Crop Tool** - Interactive crop with drag-to-select interface
- **📐 Auto-Straighten (NEW!)** - AI-powered skew correction
  - Detects and fixes tilted documents automatically
  - Option 1: Straighten only
  - Option 2: Straighten + Remove background + Auto crop
  - Edge detection + Contour analysis

#### Image Adjustments
- **Brightness Control** - Fine-tune image brightness (0.5x - 2.0x)
- **Contrast Control** - Adjust contrast levels (0.5x - 2.0x)
- **Black & White Mode** - Convert to grayscale for documents
- **Background Removal** - Transparent background for presentations
- **Background Color** - Apply custom background colors
- **Auto Crop** - Intelligent content boundary detection

#### 🏷️ **Watermark / Stamp (NEW!)**
- **Built-in Templates**:
  - COPY
  - DRAFT
  - CONFIDENTIAL
  - APPROVED
  - SAMPLE
  - VOID
  - ORIGINAL
  - Custom text option
- **Position Control**: center, corners, custom placement
- **Opacity Slider**: 0-100% transparency
- **Automatic Diagonal Rotation**: -45° for professional look
- **Color**: Red stamp for visibility

### 📏 **Paper Size Presets** (23+ Formats)

#### ISO Standards
- **A-Series**: A0, A1, A2, A3, **A4**, A5, A6
- **B-Series**: B4, B5

#### North American
- **Letter** (8.5×11")
- **Legal** (8.5×14")
- **Executive** (7.25×10.5")
- **Ledger/Tabloid** (11×17")
- **Folio** (8.5×13")

#### Photo Formats
- 3×5, 4×6, 5×7, 8×10 inches

#### Card Sizes
- Business Card, ATM/Credit Card, ID Card, Passport Photo

#### Custom
- **Define Your Own** - Enter custom dimensions

### 📚 **Book & Duplex Scanning**
- **Split Page** - Divide scanned book pages into left/right
- **Reverse Order** - Flip page sequence for back-to-front scans
- **Interleave Stacks** - Merge front and back page stacks

### 🖼️ **Photo Grid & Collage Creator**
Create stunning photo grids with multiple layouts:
- 1×2, 2×1 - Side-by-side or stacked
- 2×2 - Perfect square grid
- 3×2, 2×3 - Portrait/landscape grids
- 3×3 - Classic photo wall
- 4×4 - Large collages (16 images)

**Features:**
- Automatic image resizing
- Configurable spacing
- Maintains aspect ratios
- White background fill

### 💾 **Export & File Management**

#### Export Options
- **Single Image Export** - Save current page as JPG
- **Multi-Page PDF** - Combine all pages into one PDF
- **Batch Processing** - Export all edited pages at once
- **Custom Naming** - Set filename prefix and output directory

#### 📂 **History & File Manager (NEW!)**
- **Scan History Database** - SQLite-based history tracking
- **Metadata Tracking**:
  - Filename & filepath
  - File type (PDF/JPEG)
  - Page count
  - File size
  - Scan date & time
  - Custom notes
- **History Viewer Window**:
  - Beautiful card-based layout
  - Quick file preview info
  - One-click file opening
  - One-click folder navigation
- **File Operations**:
  - Open files directly from history
  - Navigate to file location
  - Clear history (files remain safe)
- **Settings Persistence** - Remembers your preferences

### 🎧 **Interactive User Guide**
- **Voice Assistant** - Step-by-step audio guidance using TTS
- **Visual Tutorial** - On-screen instructions with examples
- **Context-Sensitive Help** - Learn features as you use them

### 🎯 **Modern UI Design**
- **Cockpit-Style Interface** - Inspired by modern dashboard UIs
- **Card-Based Layout** - Clean, organized controls
- **Tab Navigation** - Scanner / Editor / Library modes
- **Live Thumbnails** - See all pages at a glance
- **Page Badge Counter** - Track your document count
- **Real-time Status** - Live progress and status updates

---

## 📥 Download & Installation

### 📦 **Download Pre-Built Releases**

Get the latest version for your platform:

**[⬇️ Download Latest Release](https://github.com/k4ilham/inerscan/releases/latest)**

| Platform | File | Size | Compatibility |
|----------|------|------|--------------|
| 🪟 **Windows** | `InerScanPro.exe` | ~70 MB | Windows 7+ (64-bit) |
| 🐧 **Linux** | `InerScanPro` | ~60 MB | Ubuntu 20.04+ |
| 🍎 **macOS** | `InerScanPro.dmg` | ~80 MB | macOS 10.13+ |

### 🚀 **Quick Start (End Users)**

1. **Download** the file for your operating system
2. **Run** the executable (no installation required!)
3. **Connect** your scanner via USB
4. **Click** "🚀 Start Scan" or "📚 Batch Scan" and begin digitizing!

---

## 🛠️ Development Setup

### **Prerequisites**
- Python 3.9 or higher
- Scanner with WIA support (Windows only)
- Git

### **Installation Steps**

```bash
# 1. Clone the repository
git clone https://github.com/k4ilham/inerscan.git
cd inerscan

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run the application
python scanner_app.py
```

### **Dependencies**
```
customtkinter>=5.0.0
Pillow>=10.0.0
pywin32>=305  # Windows only
comtypes>=1.4.0  # Windows only
numpy>=1.24.0
opencv-python-headless>=4.8.0  # For auto-straighten
pyttsx3>=2.90  # Text-to-speech
```

---

## 🏗️ Building from Source

### **Windows Build**
```bash
# Install PyInstaller
pip install pyinstaller

# Build executable
build_windows.bat

# Output: dist/InerScanPro.exe
```

### **Linux Build**
```bash
# Make script executable
chmod +x build_linux.sh

# Build
./build_linux.sh

# Output: dist/InerScanPro
```

### **macOS Build**
```bash
# Make script executable
chmod +x build_macos.sh

# Build
./build_macos.sh

# Output: dist/InerScan Pro.app
#         dist/InerScanPro.dmg (optional)
```

📖 **Detailed build instructions:** See [RELEASE.md](RELEASE.md)

---

## 📋 System Requirements

### **Minimum Requirements**
| Component | Requirement |
|-----------|------------|
| **Operating System** | Windows 7 / Ubuntu 20.04 / macOS 10.13 |
| **RAM** | 2 GB |
| **Storage** | 200 MB free space |
| **Display** | 1024×768 |
| **Scanner** | WIA-compatible (Windows) |

### **Recommended**
| Component | Recommendation |
|-----------|---------------|
| **Operating System** | Windows 10/11 / Ubuntu 22.04 / macOS 12+ |
| **RAM** | 4 GB or more |
| **Storage** | 1 GB free space |
| **Display** | 1280×800 or higher |
| **Scanner** | High-resolution flatbed or ADF scanner |

---

## 📖 Documentation

| Document | Description |
|----------|-------------|
| [**User Manual**](MANUAL_BOOK.md) | Complete feature guide and tutorials |
| [**Release Guide**](RELEASE.md) | Building and releasing instructions |
| [**Changelog**](#) | Version history _(coming soon)_ |

---

## 🎯 Usage Examples

### **Basic Workflow**

```python
1. Launch InerScan Pro
2. Click "🚀 Start Scan" or "📚 Batch Scan"
3. Place document(s) on scanner
4. Pages appear in preview area
5. Edit using tools on the left sidebar
6. Click "💾 Save as PDF" to export
```

### **Batch Scanning Workflow**

```python
1. Click "📚 Batch Scan"
2. Enter number of pages (e.g., 10) or 0 for continuous
3. Prepare your document stack
4. App scans automatically every 2 seconds
5. Click "⏹️ Stop Batch" when done
6. All pages ready for editing!
```

### **Auto-Straighten + Clean Workflow**

```python
1. Scan a tilted ID card or document
2. Click "📐 Auto-Straighten"
3. Choose "Yes" for full cleaning
   - Auto-detects angle
   - Straightens image
   - Removes background
   - Crops to content
4. Perfect result in seconds!
```

### **Watermark Workflow**

```python
1. Select or scan a page
2. Go to "🏷️ Watermark / Stamp" section
3. Choose template (e.g., "COPY")
4. Select position (e.g., "center")
5. Adjust opacity (50% recommended)
6. Click "🏷️ Add Watermark"
7. Professional stamp applied!
```

### **History Management**

```python
1. Save documents as PDF or images
2. Click "📜 View Scan History"
3. See all saved files with metadata
4. Click "📂 Open" to view file
5. Click "📁 Folder" to navigate to location
6. Manage files efficiently!
```

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### **Areas for Contribution**
- 🌍 Translations (internationalization)
- 🐛 Bug fixes and testing
- ✨ New features and improvements
- 📝 Documentation enhancements
- 🎨 UI/UX improvements
- 🧪 Unit tests

---

## 📝 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Ilham Maulana**

- 📧 Email: [k4ilham@gmail.com](mailto:k4ilham@gmail.com)
- 🌐 Website: [inercorp.com](https://inercorp.com)
- 💼 GitHub: [@k4ilham](https://github.com/k4ilham)

---

## 🙏 Acknowledgments

- **UI Framework**: [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) by Tom Schimansky
- **Image Processing**: [Pillow (PIL Fork)](https://python-pillow.org/)
- **Computer Vision**: [OpenCV](https://opencv.org/)
- **Scanner Integration**: Windows Image Acquisition (WIA)
- **Text-to-Speech**: [pyttsx3](https://github.com/nateshmbhat/pyttsx3)
- **Build Tool**: [PyInstaller](https://pyinstaller.org/)

---

## ⭐ Show Your Support

If you find InerScan Pro useful, please consider:

- ⭐ **Starring** this repository
- 🐛 **Reporting** bugs and issues
- 💡 **Suggesting** new features
- 📢 **Sharing** with others
- 🤝 **Contributing** code or documentation

---

## 📊 Project Stats

![GitHub stars](https://img.shields.io/github/stars/k4ilham/inerscan?style=social)
![GitHub forks](https://img.shields.io/github/forks/k4ilham/inerscan?style=social)
![GitHub issues](https://img.shields.io/github/issues/k4ilham/inerscan)
![GitHub pull requests](https://img.shields.io/github/issues-pr/k4ilham/inerscan)

---

## 🗺️ Roadmap

### Version 2.6 (Planned)
- [ ] OCR text recognition
- [ ] Cloud storage integration (Google Drive, Dropbox)
- [ ] Email integration (send scans directly)
- [ ] Template library for watermarks

### Version 3.0 (Future)
- [ ] Mobile companion app
- [ ] Batch file processing
- [ ] QR code generation and scanning
- [ ] Multi-language support
- [ ] Plugin system for extensions

---

## 📸 Screenshots

### Main Interface
![Scanner Interface](https://via.placeholder.com/800x500/EEF2FF/3B82F6?text=InerScan+Pro+-+Main+Interface)

### Batch Scanning
![Batch Scan](https://via.placeholder.com/800x500/10B981/FFFFFF?text=Batch+Scanning+Mode)

### Watermark Feature
![Watermark](https://via.placeholder.com/800x500/DC2626/FFFFFF?text=Watermark+%2F+Stamp)

### Scan History
![History](https://via.placeholder.com/800x500/8B5CF6/FFFFFF?text=Scan+History+Manager)

---

<div align="center">

**Made with ❤️ by [InerCorp](https://inercorp.com)**

[Report Bug](https://github.com/k4ilham/inerscan/issues) · [Request Feature](https://github.com/k4ilham/inerscan/issues) · [Documentation](MANUAL_BOOK.md)

</div>
