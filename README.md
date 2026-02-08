# 📄 InerScan Pro

[![Build and Release](https://github.com/k4ilham/inerscan/workflows/Build%20and%20Release/badge.svg)](https://github.com/k4ilham/inerscan/actions)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-3.0-brightgreen.svg)](https://github.com/k4ilham/inerscan/releases)
[![Platform](https://img.shields.io/badge/platform-Windows-blue.svg)](https://github.com/k4ilham/inerscan/releases)

> **Professional Document Scanner & Editor** - Transform your scanner into a powerful document digitization tool with a modern Nitro-style Ribbon interface, AI-powered computer vision, batch processing, and comprehensive file management.

---

## ✨ Features Overview

### 🎨 **Modern Shadcn-Style UI (NEW!)**
- **Sleek & Clean** - A professional "Zinc" theme inspired by modern web interfaces.
- **Unified Sidebar** - All tools (Chat, OCR, Edit, History) open in a persistent sidebar panel—no more popup windows.
- **Ribbon Interface** - Organized features into logical tabs: Home, Edit, AI Tools, Annotate, Layout, and Library.
- **Large Action Icons** - High-visibility buttons for the most common tasks.

### 🧠 **OpenAI Integration & Chat**
- **💬 AI Chat Assistant** - Chat with your documents directly in the sidebar!
- **OCR Text Extraction** - Convert scanned images to editable text.
- **Smart Rename** - AI automatically suggests filenames based on content.
- **Document Analysis** - Summarize and extract key data instantly.

### 📝 **Annotate & Help**
- **Add Text** - Overlay custom text onto your scans.
- **Interactive Help** - Step-by-step voice-guided tour of features.

### 🖼️ **Advanced Scanning & Editing**
- **WIA Scanner Support** - Native Windows Image Acquisition integration.
- **🚀 Batch Mode** - Automatic multi-page batch processing.
- **🔄 Undo & Redo** - Full state management for every page.
- **🔍 Zoom & Pan** - Inspect fine details with the zoom slider.
- **✂️ Interactive Crop** - Precision cropping tool.

### 💾 **File Management**
- **Multi-Format Export** - Save as high-quality JPEG or multi-page PDF.
- **📜 Scan History** - Persistent track record of all your files.

---

## 📥 Quick Start

1. **Download** the latest release.
2. **Run** the application:
   - Navigate to the `scripts/` folder.
   - Double-click `run_with_venv.bat` (automatically sets up dependencies).
3. **Connect** your scanner via USB and start scanning from the **HOME** tab!

---

## 🛠️ Development Setup

```bash
# 1. Clone & Navigate
git clone https://github.com/k4ilham/inerscan.git
cd inerscan

# 2. Run from Scripts Folder
cd scripts
run_with_venv.bat
```

---

## 🗺️ Project Structure

- `main.py`: Application entry point.
- `app/`: Core logic (UI, Services, Core constants).
- `scripts/`: Implementation scripts for running and building the app.
- `docs/`: Extended documentation (User Manual, Release notes).
- `requirements.txt`: Python dependency list.

---

## 👨‍💻 Author
**Ilham Maulana** - [InerCorp](https://inercorp.com)

---
<div align="center">
**Made with ❤️ for Professional Document Digitization**
</div>
