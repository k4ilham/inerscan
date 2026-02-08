# 📄 InerScan Pro

[![Build and Release](https://github.com/k4ilham/inerscan/workflows/Build%20and%20Release/badge.svg)](https://github.com/k4ilham/inerscan/actions)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-2.0-brightgreen.svg)](https://github.com/k4ilham/inerscan/releases)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-blue.svg)](https://github.com/k4ilham/inerscan/releases)

> **Professional Document Scanner & Editor** - Transform your scanner into a powerful document digitization tool with advanced editing, photo grid creation, and multi-format export.

![InerScan Pro](https://via.placeholder.com/800x450/EEF2FF/3B82F6?text=InerScan+Pro+-+Modern+Document+Scanner)

---

## ✨ Features Overview

### 🖨️ **Scanner Integration**
- **WIA Scanner Support** - Native Windows Image Acquisition integration
- **Multi-Page Batch Scanning** - Scan entire documents in one session
- **Live Preview** - See your scanned pages instantly
- **Auto-Detection** - Automatically detects connected scanners

### 🎨 **Advanced Image Editing**

#### Basic Transformations
- **Rotate** - 90° left/right rotation with visual preview
- **Flip** - Horizontal and vertical flipping
- **Crop Tool** - Interactive crop with drag-to-select interface
- **Auto Crop** - Intelligent content boundary detection

#### Image Adjustments
- **Brightness Control** - Fine-tune image brightness (0.5x - 2.0x)
- **Contrast Control** - Adjust contrast levels (0.5x - 2.0x)
- **Black & White Mode** - Convert to grayscale for documents
- **Background Removal** - Transparent background for presentations
- **Background Color** - Apply custom background colors

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
- 3×5 inches
- 4×6 inches
- 5×7 inches
- 8×10 inches

#### Card Sizes
- **Business Card** (3.5×2")
- **ATM/Credit Card**
- **ID Card**
- **Passport Photo** (35×45mm)

#### Custom
- **Define Your Own** - Enter custom dimensions in pixels

### 📚 **Book & Duplex Scanning**
- **Split Page** - Divide scanned book pages into left/right
- **Reverse Order** - Flip page sequence for back-to-front scans
- **Interleave Stacks** - Merge front and back page stacks

### 🖼️ **Photo Grid & Collage Creator**
Create stunning photo grids with multiple layouts:
- **1×2** or **2×1** - Side-by-side or stacked
- **2×2** - Perfect square grid
- **3×2** or **2×3** - Portrait/landscape grids
- **3×3** - Classic photo wall
- **4×4** - Large collages (16 images)

**Features:**
- Automatic image resizing
- Configurable spacing (default: 20px)
- Maintains aspect ratios
- White background fill

### 💾 **Export Options**
- **Single Image Export** - Save current page as JPG
- **Multi-Page PDF** - Combine all pages into one PDF
- **Batch Processing** - Export all edited pages at once
- **Custom Naming** - Set filename prefix and output directory
- **Settings Persistence** - Remembers your last used settings

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

---

## 📥 Download & Installation

### 📦 **Download Pre-Built Releases**

Get the latest version for your platform:

**[⬇️ Download Latest Release](https://github.com/k4ilham/inerscan/releases/latest)**

| Platform | File | Size | Compatibility |
|----------|------|------|--------------|
| 🪟 **Windows** | `InerScanPro.exe` | ~60 MB | Windows 7+ (64-bit) |
| 🐧 **Linux** | `InerScanPro` | ~50 MB | Ubuntu 20.04+ |
| 🍎 **macOS** | `InerScanPro.dmg` | ~70 MB | macOS 10.13+ |

### 🚀 **Quick Start (End Users)**

1. **Download** the file for your operating system
2. **Run** the executable (no installation required!)
3. **Connect** your scanner via USB
4. **Click** "🚀 Start Scan" and begin digitizing!

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
numpy>=1.24.0
pywin32>=305  # Windows only
comtypes>=1.4.0  # Windows only
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
| **Storage** | 100 MB free space |
| **Display** | 1024×768 |
| **Scanner** | WIA-compatible (Windows) |

### **Recommended**
| Component | Recommendation |
|-----------|---------------|
| **Operating System** | Windows 10/11 / Ubuntu 22.04 / macOS 12+ |
| **RAM** | 4 GB or more |
| **Storage** | 500 MB free space |
| **Display** | 1280×800 or higher |
| **Scanner** | High-resolution flatbed or ADF scanner |

---

## 📖 Documentation

| Document | Description |
|----------|-------------|
| [**User Manual**](MANUAL_BOOK.md) | Complete feature guide and tutorials |
| [**Release Guide**](RELEASE.md) | Building and releasing instructions |
| [**Changelog**](#) | Version history and updates _(coming soon)_ |

---

## 🎯 Usage Examples

### **Basic Workflow**

```python
1. Launch InerScan Pro
2. Click "🚀 Start Scan"
3. Place document on scanner
4. Scan appears in preview area
5. Edit using tools on the left sidebar
6. Click "💾 Save as PDF" to export
```

### **Creating a Photo Grid**

```python
1. Scan multiple pages (e.g., 4 photos)
2. Go to "🎨 Collage & Photo Grid" section
3. Select layout (e.g., "2x2")
4. Click "🖼️ Create Grid from All Pages"
5. New collage page is added
6. Export as image or PDF
```

### **Book Scanning Workflow**

```python
1. Scan all odd pages (1, 3, 5...)
2. Flip document and scan even pages
3. Use "Interleave Stacks" to merge
4. Use "Split Page" for book spreads
5. Export as multi-page PDF
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

---

## 📊 Project Stats

![GitHub stars](https://img.shields.io/github/stars/k4ilham/inerscan?style=social)
![GitHub forks](https://img.shields.io/github/forks/k4ilham/inerscan?style=social)
![GitHub issues](https://img.shields.io/github/issues/k4ilham/inerscan)
![GitHub pull requests](https://img.shields.io/github/issues-pr/k4ilham/inerscan)

---

## 🗺️ Roadmap

### Version 2.1 (Planned)
- [ ] OCR text recognition
- [ ] Cloud storage integration
- [ ] Mobile companion app
- [ ] Template library

### Version 2.2 (Future)
- [ ] Batch file processing
- [ ] Email integration
- [ ] QR code generation
- [ ] Multi-language support

---

<div align="center">

**Made with ❤️ by [InerCorp](https://inercorp.com)**

[Report Bug](https://github.com/k4ilham/inerscan/issues) · [Request Feature](https://github.com/k4ilham/inerscan/issues) · [Documentation](MANUAL_BOOK.md)

</div>
