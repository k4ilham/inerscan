# 🚀 InerScan Pro - Release Notes (v3.0)

We are proud to announce the release of **InerScan Pro v3.0**, a massive update that transforms the application into a professional document scanning and editing suite.

---

## 🎨 New Features & Enhancements

### 1. Nitro-Style Ribbon UI
- Completely redesigned interface with logical tabs: **Home, Edit, AI Tools, Annotate, Layout, and Library**.
- High-visibility action icons for a premium look and feel.
- Organized modular architecture for better performance.

### 2. 🔄 Full Undo & Redo System
- Every editing action is now undoable and redoable per page.
- History stack allows you to experiment with AI tools and edits without losing original quality.

### 3. 🔍 Zoom & Interactive Pan
- New **Zoom Slider** in the status bar (20% to 300%).
- Integrated **Panning & Scrollbars** to navigate large documents or fine-tune crops.

### 4. 🪄 AI Computer Vision Tools
- **Perspective Fix**: Auto-detect document corners and flatten images.
- **Clean Document**: Enhance text and remove background noise.
- **Privacy Blur**: Automatic face detection and redaction for sensitive IDs.
- **Auto-Straighten**: Fix tilted or skewed scans with one click.

### 5. 🧠 OpenAI Integration (New!)
- **OCR Text Extraction**: Extract editable text from any scanned document using GPT-4o.
- **Smart Rename**: Automatically generate descriptive filenames based on document content.
- **Document Analysis**: Get instant summaries and key data extraction (dates, amounts, names).
- **Customizable**: Bring your own API Key and support for custom Base URLs (e.g., SumoPod).

### 5. 📑 Modular Project Structure
- Separated business logic into **Services** and **UI Components**.
- New **`scripts/`** folder for easy execution and building.
- New **`docs/`** folder for comprehensive user manuals.

### 6. 🎙️ Interactive Help Guide
- New **HELP** button in the menu bar.
- Step-by-step interactive tour with **Text-to-Speech** assistance to guide new users.

---

## 🏗️ Technical Changes
- Switched entry point from `scanner_app.py` to `main.py`.
- Integrated **SQLite** for persistent scan history and settings.
- Improved **WIA Scanner** integration stability.
- Optimized image processing pipeline using **OpenCV** and **PIL**.

---

## 🛠️ How to Upgrade
1. Pull the latest code from the repository.
2. Run `pip install -r requirements.txt` to get new AI and UI dependencies.
3. Start the app using `scripts/run_with_venv.bat`.

---
<div align="center">
**© 2026 InerCorp - Professional Document Digitization**
</div>
