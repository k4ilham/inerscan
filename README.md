# 📄 InerScan Pro

[![Build and Release](https://github.com/k4ilham/inerscan/workflows/Build%20and%20Release/badge.svg)](https://github.com/k4ilham/inerscan/actions)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-3.1-brightgreen.svg)](https://github.com/k4ilham/inerscan/releases)
[![Platform](https://img.shields.io/badge/platform-Windows-blue.svg)](https://github.com/k4ilham/inerscan/releases)

> **Professional Document Scanner & Editor** - Transform your scanner into a powerful document digitization tool with a modern clean blue & white interface, AI-powered features, smooth animations, and comprehensive file management.

---

## 🎯 What's New in v3.1

✨ **Clean Blue & White Theme** - Professional color scheme  
🎬 **Loading & Animations** - Smooth spinners, progress bars, and toast notifications  
📦 **Windows Installer** - Professional Inno Setup installer  
🚀 **Improved Build System** - Automated build pipeline  
📚 **Complete Documentation** - Comprehensive guides for users and developers  
🔧 **Bug Fixes** - Fixed database and scanner permission issues for installed apps  
💾 **Smart Data Storage** - Database and temp files now stored in user AppData folder  

---

## ✨ Features Overview

### 🎨 **Modern Clean Blue & White UI**
- **Professional Theme** - Clean blue and white color scheme for a professional look
- **Smooth Animations** - Loading spinners, progress bars, and toast notifications
- **Ribbon Interface** - Organized features into logical tabs: Home, Edit, AI Tools, Annotate, Layout, and Library
- **Responsive Design** - Intuitive layout with clear visual hierarchy
- **Large Action Icons** - High-visibility buttons for the most common tasks

### 🎬 **Loading & Animations**
- **🔄 Loading Spinner** - Animated spinner for ongoing operations
- **📊 Animated Progress Bar** - Smooth progress transitions with ease-out animation
- **🔔 Toast Notifications** - Slide-in notifications for all operations:
  - Info (blue) - General information
  - Success (green) - Successful operations
  - Warning (yellow) - Warnings and alerts
  - Error (red) - Error messages
- **⏳ Progress Overlay** - Full-screen loading for long operations
- **✨ Smooth Transitions** - Enhanced user experience with visual feedback

### 🧠 **OpenAI Integration & AI Features**
- **💬 AI Chat Assistant** - Chat with your documents directly in the sidebar
- **📝 OCR Text Extraction** - Convert scanned images to editable text
- **🤖 Smart Rename** - AI automatically suggests filenames based on content
- **📊 Document Analysis** - Summarize and extract key data instantly
- **🎯 AI Enhancement** - Perspective correction, document cleaning, and more

### 📝 **Annotation & Watermark**
- **✍️ Add Text** - Overlay custom text onto your scans
- **🏷️ Watermarks** - Apply stamps like COPY, DRAFT, CONFIDENTIAL, etc.
- **📍 Position Control** - Place watermarks at various positions
- **🎨 Interactive Help** - Step-by-step voice-guided tour of features

### 🖼️ **Advanced Scanning & Editing**
- **📷 WIA Scanner Support** - Native Windows Image Acquisition integration
- **🚀 Batch Mode** - Automatic multi-page batch processing
- **🔄 Undo & Redo** - Full state management for every page
- **🔍 Zoom & Pan** - Inspect fine details with the zoom slider
- **✂️ Interactive Crop** - Precision cropping tool
- **🎨 Image Adjustments** - Brightness, contrast, grayscale, rotation, flip
- **📐 Resize Tool** - Resize images with custom dimensions

### 📚 **Layout & Organization**
- **📖 Book Tools** - Split pages, reverse order for book scanning
- **🎯 Grid Creation** - Create photo grids and collages
- **🔢 Multi-page Management** - Organize and reorder pages easily
- **👁️ Thumbnail View** - Quick navigation through scanned pages

### 💾 **File Management**
- **📄 Multi-Format Export** - Save as high-quality JPEG or multi-page PDF
- **📜 Scan History** - Persistent track record of all your files
- **📁 Folder Browser** - Quick access to saved documents
- **🗑️ Clear Logs** - Maintain system cleanliness

---

## 📥 Installation

### For End Users (Recommended)

#### Option 1: Windows Installer (Easiest)

1. **Download** the installer: `InerScanPro_Setup_v3.1.exe`
2. **Run** the installer
3. **Follow** the installation wizard
4. **Launch** from Start Menu or Desktop icon

**Features:**
- ✅ Automatic installation to Program Files
- ✅ Desktop shortcut (optional)
- ✅ Start Menu integration
- ✅ File associations (.pdf, .jpg, .png)
- ✅ Clean uninstaller

#### Option 2: Standalone Executable

1. **Download** `InerScanPro.exe`
2. **Run** directly - no installation needed
3. **Portable** - can run from USB drive

### For Developers

```bash
# 1. Clone the repository
git clone https://github.com/k4ilham/inerscan.git
cd inerscan

# 2. Run from scripts folder
cd scripts
run_with_venv.bat
```

---

## 🔨 Building from Source

### Build Executable

```bash
cd scripts
.\build_exe.bat
```

Output: `dist\InerScanPro.exe`

### Build Installer

**Prerequisites:** Install [Inno Setup 6](https://jrsoftware.org/isdl.php)

```bash
cd scripts
.\build_installer.bat
```

Output: `installer_output\InerScanPro_Setup_v3.1.exe`

### Build Everything (Recommended)

```bash
cd scripts
.\build_all.bat
```

Builds both executable and installer in one go!

**See:** [BUILD_GUIDE.md](BUILD_GUIDE.md) and [INSTALLER_GUIDE.md](INSTALLER_GUIDE.md) for detailed instructions.

---

## 📋 System Requirements

### Minimum Requirements
- **OS**: Windows 10 (64-bit)
- **RAM**: 4GB
- **Storage**: 500MB free space
- **Scanner**: WIA-compatible (optional)

### Recommended
- **OS**: Windows 11 (64-bit)
- **RAM**: 8GB or more
- **Storage**: 2GB free space
- **Scanner**: Any modern USB scanner

---

## 🗺️ Project Structure

```
inerscan/
├── main.py                      # Application entry point
├── requirements.txt             # Python dependencies
├── InerScanPro.spec            # PyInstaller configuration
├── LICENSE                      # MIT License
├── README.md                    # This file
├── QUICK_START.md              # Quick reference guide
├── BUILD_GUIDE.md              # Build documentation
├── INSTALLER_GUIDE.md          # Installer documentation
├── ANIMASI_README.md           # Animation features guide
│
├── app/
│   ├── core/
│   │   └── constants.py        # Color themes and fonts
│   ├── services/
│   │   ├── scanner_service.py  # Scanner integration
│   │   ├── image_service.py    # Image processing
│   │   ├── db_service.py       # Database operations
│   │   ├── guide_service.py    # Help system
│   │   └── ai_openai_service.py # OpenAI integration
│   └── ui/
│       ├── main_window.py      # Main application window
│       ├── widgets/
│       │   ├── animations.py   # Loading & animations
│       │   ├── ai_chat_window.py
│       │   └── ...
│       └── ribbons/
│           ├── scanner_tab.py  # Home tab
│           ├── editor_tab.py   # Edit tab
│           ├── ai_tab.py       # AI Tools tab
│           ├── annotate_tab.py # Annotate tab
│           ├── layout_tab.py   # Layout tab
│           └── library_tab.py  # Library tab
│
├── scripts/
│   ├── run_with_venv.bat       # Run with virtual environment
│   ├── build_exe.bat           # Build executable
│   ├── build_installer.bat     # Build installer
│   └── build_all.bat           # Build everything
│
├── installer/
│   └── InerScanPro.iss         # Inno Setup script
│
├── dist/                        # Built executable
│   └── InerScanPro.exe
│
└── installer_output/            # Built installer
    └── InerScanPro_Setup_v3.1.exe
```

---

## 🎯 Feature Guide by Tab

### 🏠 Home (Scanner Tab)
- **Start Scan** - Single page scanning
- **Batch Scan** - Continuous multi-page scanning
- **Paper Size** - A4, Letter, A3, Legal, A5, Custom
- **Save Image** - Export as JPEG
- **Save PDF** - Export as multi-page PDF
- **Preview & Print** - Quick preview and print

### ✏️ Edit (Editor Tab)
- **Undo/Redo** - Full edit history
- **Rotate & Flip** - Transform images (90°, 180°, 270°)
- **Brightness & Contrast** - Adjust image quality
- **Grayscale** - Convert to black & white
- **Crop Tool** - Precision cropping
- **Resize** - Custom dimensions

### 🤖 AI Tools
- **Perspective Correction** - Auto-straighten documents
- **Clean Document** - Remove noise and artifacts
- **Privacy Mode** - Redact sensitive information
- **Straighten** - Auto-align skewed scans
- **OCR Text** - Extract text from images
- **Smart Rename** - AI-powered file naming
- **Analyze** - Document analysis
- **Chat AI** - Interactive AI assistant

### 📝 Annotate
- **Add Text** - Custom text overlay
- **Watermarks** - COPY, DRAFT, CONFIDENTIAL, APPROVED, SAMPLE, VOID, ORIGINAL
- **Position Control** - Center, top-right, bottom-right, top-left, bottom-left

### 📐 Layout
- **Split Page** - Divide pages for book scanning
- **Reverse Pages** - Reorder for proper sequence
- **Create Grid** - Photo collages (1x2, 2x1, 2x2, 3x2, 2x3, 3x3, 4x4)

### 📚 Library
- **History** - View scan history
- **Open Folder** - Quick access to saved files
- **Clear Logs** - System maintenance

---

## 🎨 Animation Features

### Toast Notifications
```python
# Automatically shown for all operations:
✅ "Page added successfully!" (Success)
⚠️ "Blank page skipped" (Warning)
ℹ️ "Scan cancelled" (Info)
❌ "Scan failed" (Error)
```

### Loading Indicators
- **Spinner** - Shown during scanning
- **Progress Bar** - Smooth animated progress (0% → 30% → 70% → 100%)
- **Overlay** - For long operations (AI processing, batch operations)

**See:** [ANIMASI_README.md](ANIMASI_README.md) for detailed animation documentation.

---

## 🔧 Configuration

### OpenAI API Setup

1. Click **Settings** in the AI Tools tab
2. Enter your OpenAI API Key
3. Select your preferred model:
   - GPT-4 (Recommended)
   - GPT-4 Turbo
   - GPT-3.5 Turbo
4. Save settings

### Scanner Configuration

The application automatically detects WIA-compatible scanners.

**Troubleshooting:**
- Ensure scanner drivers are installed
- Check USB connection
- Restart the application
- Run as administrator if needed

---

## 📝 Dependencies

### Core Dependencies
- **customtkinter** 5.2.2 - Modern UI framework
- **Pillow** 12.1.0 - Image processing
- **pywin32** 311 - Windows integration
- **numpy** 2.4.2 - Numerical operations
- **opencv-python-headless** 4.13.0 - Computer vision
- **openai** 2.17.0 - AI integration
- **pyttsx3** 2.99 - Text-to-speech

### Build Dependencies
- **pyinstaller** 6.18.0 - Executable building
- **Inno Setup 6** - Installer creation (external)

---

## 🐛 Troubleshooting

### Scanner Not Detected
- ✅ Install latest scanner drivers
- ✅ Check USB connection
- ✅ Run application as administrator
- ✅ Restart computer

### Scanner "Access Denied" Error
**Error:** `WIA.ImageFile: Access is denied`

**Solutions:**
- ✅ **Run as Administrator** - Right-click InerScanPro.exe → Run as administrator
- ✅ **Check Scanner Status** - Ensure scanner is powered on and connected
- ✅ **Close Other Apps** - Close any other scanning software
- ✅ **Restart WIA Service**:
  1. Press `Win + R`
  2. Type `services.msc`
  3. Find "Windows Image Acquisition (WIA)"
  4. Right-click → Restart
- ✅ **Reinstall Scanner Drivers** - Download latest drivers from manufacturer
- ✅ **Check Permissions** - Ensure your user account has scanner access

### Database Errors
**Error:** `unable to open database file`

**Solutions:**
- ✅ Database is now stored in `%APPDATA%\InerScanPro\`
- ✅ Ensure you have write permissions to AppData folder
- ✅ Check disk space availability
- ✅ Run application as administrator if needed
- ✅ Application will use in-memory database as fallback

### OpenAI Features Not Working
- ✅ Verify API key in settings
- ✅ Check internet connection
- ✅ Ensure sufficient API credits
- ✅ Try different model

### Application Won't Start
- ✅ Install Python 3.8+ (for source)
- ✅ Run `pip install -r requirements.txt`
- ✅ Check antivirus settings
- ✅ Reinstall application

### Build Errors
- ✅ See [BUILD_GUIDE.md](BUILD_GUIDE.md)
- ✅ Ensure all prerequisites installed
- ✅ Check Python version compatibility

---

## 📚 Documentation

- **[README.md](README.md)** - Main documentation (this file)
- **[QUICK_START.md](QUICK_START.md)** - Quick reference guide
- **[BUILD_GUIDE.md](BUILD_GUIDE.md)** - Building from source
- **[INSTALLER_GUIDE.md](INSTALLER_GUIDE.md)** - Creating installer
- **[ANIMASI_README.md](ANIMASI_README.md)** - Animation features
- **[LICENSE](LICENSE)** - MIT License

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### How to Contribute

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guide
- Add comments for complex logic
- Update documentation
- Test thoroughly before submitting

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Ilham Maulana** - [InerCorp](https://inercorp.com)

---

## 🙏 Acknowledgments

- **CustomTkinter** - Modern UI framework
- **OpenAI** - AI capabilities
- **Inno Setup** - Professional installer
- **Python Community** - Excellent libraries

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/k4ilham/inerscan/issues)
- **Email**: support@inercorp.com
- **Website**: [inercorp.com](https://inercorp.com)

---

## 🔄 Changelog

### v3.1 (2026-02-08)
- ✨ New clean blue & white theme
- 🎬 Added loading animations and toast notifications
- 📦 Professional Windows installer
- 🚀 Improved build system
- 📚 Complete documentation
- 🐛 Bug fixes:
  - Fixed database permission issues (now stored in AppData)
  - Fixed scanner temp file access errors
  - Improved error messages for scanner issues
  - Better error handling throughout the application
- 💾 Smart data storage in user AppData folder
- 🔧 Enhanced WIA scanner error handling

### v3.0 (Previous)
- 🎨 Modern Shadcn-style UI
- 🧠 OpenAI integration
- 💬 AI Chat Assistant
- 📝 OCR and document analysis
- 🔄 Undo/Redo system

---

<div align="center">

**Made with ❤️ for Professional Document Digitization**

[⬇️ Download](https://github.com/k4ilham/inerscan/releases) · [📖 Documentation](BUILD_GUIDE.md) · [🐛 Report Bug](https://github.com/k4ilham/inerscan/issues) · [✨ Request Feature](https://github.com/k4ilham/inerscan/issues)

</div>
