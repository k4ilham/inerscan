# 🔨 Build Guide - InerScan Pro

Panduan lengkap untuk membuild aplikasi InerScan Pro menjadi executable Windows.

---

## 📋 Prerequisites

Sebelum build, pastikan Anda memiliki:

- ✅ Python 3.8 atau lebih tinggi
- ✅ Git (untuk clone repository)
- ✅ Windows 10/11
- ✅ Koneksi internet (untuk download dependencies)

---

## 🚀 Quick Build

### Metode 1: Menggunakan Build Script (Recommended)

1. **Buka Command Prompt atau PowerShell**

2. **Navigate ke folder scripts**
   ```bash
   cd "C:\inercorp\aplikasi scanner\scripts"
   ```

3. **Jalankan build script**
   ```bash
   .\build_exe.bat
   ```

4. **Tunggu proses selesai**
   - Script akan otomatis:
     - Membuat virtual environment (jika belum ada)
     - Install semua dependencies
     - Clean build sebelumnya
     - Build executable baru

5. **Executable akan tersedia di:**
   ```
   C:\inercorp\aplikasi scanner\dist\InerScanPro.exe
   ```

### Metode 2: Manual Build

```bash
# 1. Navigate ke root folder
cd "C:\inercorp\aplikasi scanner"

# 2. Buat virtual environment (jika belum ada)
python -m venv venv

# 3. Aktivasi virtual environment
venv\Scripts\activate

# 4. Install dependencies
pip install -r requirements.txt
pip install pyinstaller

# 5. Clean previous builds
rmdir /s /q build
rmdir /s /q dist

# 6. Build dengan spec file
pyinstaller --clean InerScanPro.spec
```

---

## 📦 Build Output

Setelah build berhasil, Anda akan mendapatkan:

```
dist/
└── InerScanPro.exe    # Executable utama (single file)
```

**File Size:** Sekitar 80-120 MB (termasuk semua dependencies)

---

## 🔧 Build Configuration

### File Spec (`InerScanPro.spec`)

File spec mengatur konfigurasi build:

- **Entry Point:** `main.py`
- **Mode:** `--noconsole` (GUI mode, no command prompt)
- **Type:** `--onefile` (single executable)
- **Hidden Imports:** Semua modul yang diperlukan
- **Data Files:** Folder `app` dengan semua UI dan services

### Hidden Imports yang Disertakan:

```python
'PIL._tkinter_finder'
'tkinter'
'customtkinter'
'pyttsx3'
'win32com.client'
'comtypes'
'openai'
'cv2'
'numpy'
'app.ui.widgets.animations'
# ... dan modul lainnya
```

---

## 🐛 Troubleshooting

### Error: "Python not found"

**Solusi:**
```bash
# Install Python dari python.org
# Atau gunakan winget:
winget install Python.Python.3.12
```

### Error: "pip not found"

**Solusi:**
```bash
python -m ensurepip --upgrade
```

### Error: "Module not found" saat menjalankan exe

**Solusi:**
- Tambahkan module ke `hiddenimports` di `InerScanPro.spec`
- Rebuild aplikasi

### Build Berhasil tapi Exe Tidak Jalan

**Solusi:**
1. Cek antivirus (mungkin memblokir)
2. Jalankan dari Command Prompt untuk lihat error:
   ```bash
   cd dist
   InerScanPro.exe
   ```
3. Pastikan semua dependencies ter-install dengan benar

### Exe Terlalu Besar

**Solusi:**
- Gunakan UPX compression (sudah enabled di spec)
- Exclude modul yang tidak diperlukan
- Pertimbangkan build dengan `--onedir` untuk size lebih kecil

---

## 📊 Build Optimization

### Mengurangi Ukuran File

1. **Exclude modul yang tidak perlu:**
   ```python
   # Di InerScanPro.spec
   excludes=['matplotlib', 'scipy', 'pandas']
   ```

2. **Enable UPX compression:**
   ```python
   upx=True,
   upx_exclude=[],
   ```

3. **Strip debug symbols:**
   ```python
   strip=True,
   ```

### Meningkatkan Startup Speed

1. **Gunakan `--onedir` mode:**
   ```bash
   # Lebih cepat startup, tapi banyak file
   pyinstaller --onedir InerScanPro.spec
   ```

2. **Disable UPX untuk startup lebih cepat:**
   ```python
   upx=False,
   ```

---

## 🚢 Distribution

### Membuat Installer (Optional)

Gunakan tools seperti:
- **Inno Setup** - Free, powerful
- **NSIS** - Scriptable
- **WiX Toolset** - MSI installer

### Contoh dengan Inno Setup:

```iss
[Setup]
AppName=InerScan Pro
AppVersion=3.1
DefaultDirName={pf}\InerScanPro
DefaultGroupName=InerScan Pro
OutputDir=output
OutputBaseFilename=InerScanPro_Setup

[Files]
Source: "dist\InerScanPro.exe"; DestDir: "{app}"

[Icons]
Name: "{group}\InerScan Pro"; Filename: "{app}\InerScanPro.exe"
Name: "{commondesktop}\InerScan Pro"; Filename: "{app}\InerScanPro.exe"
```

---

## 📝 Build Checklist

Sebelum distribusi, pastikan:

- [ ] Aplikasi berjalan tanpa error
- [ ] Semua fitur berfungsi (scan, edit, AI, dll)
- [ ] Icon aplikasi muncul dengan benar
- [ ] File size reasonable (<150 MB)
- [ ] Tested di Windows 10 dan 11
- [ ] Antivirus tidak mendeteksi sebagai malware
- [ ] README.md up-to-date
- [ ] Version number di-update

---

## 🔄 Continuous Integration (Optional)

Untuk automated builds, gunakan GitHub Actions:

```yaml
name: Build and Release

on:
  push:
    tags:
      - 'v*'

jobs:
  build:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pyinstaller
      - name: Build
        run: pyinstaller --clean InerScanPro.spec
      - name: Upload artifact
        uses: actions/upload-artifact@v2
        with:
          name: InerScanPro
          path: dist/InerScanPro.exe
```

---

## 📞 Support

Jika mengalami masalah saat build:

1. Cek [Issues](https://github.com/k4ilham/inerscan/issues)
2. Buat issue baru dengan detail error
3. Sertakan:
   - Python version
   - OS version
   - Error message lengkap
   - Build command yang digunakan

---

## 📚 Resources

- [PyInstaller Documentation](https://pyinstaller.org/)
- [CustomTkinter Packaging](https://customtkinter.tomschimansky.com/documentation/packaging)
- [Python Packaging Guide](https://packaging.python.org/)

---

<div align="center">

**Happy Building! 🚀**

</div>
