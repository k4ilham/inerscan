# 📦 Installer Guide - InerScan Pro

Panduan lengkap untuk membuat dan mendistribusikan installer Windows untuk InerScan Pro.

---

## 🎯 Overview

Installer ini dibuat menggunakan **Inno Setup**, tool gratis dan powerful untuk membuat installer Windows profesional.

### Fitur Installer:

✅ **Professional UI** - Modern wizard-style installer  
✅ **Multi-language** - English & Indonesian  
✅ **Desktop Icon** - Optional desktop shortcut  
✅ **Start Menu** - Program group dengan shortcuts  
✅ **File Association** - Associate dengan file types (.pdf, .jpg, .png)  
✅ **Registry Entries** - Proper Windows integration  
✅ **Uninstaller** - Clean uninstall capability  
✅ **Admin Rights** - Proper installation di Program Files  
✅ **64-bit Support** - Optimized untuk Windows 64-bit  

---

## 📋 Prerequisites

### 1. Install Inno Setup

Download dan install Inno Setup 6:
- **Website**: https://jrsoftware.org/isdl.php
- **Download**: Inno Setup 6.x (Latest version)
- **Install ke**: `C:\Program Files (x86)\Inno Setup 6\`

### 2. Build Executable Terlebih Dahulu

Sebelum membuat installer, executable harus sudah di-build:

```bash
cd scripts
.\build_exe.bat
```

Pastikan file `dist\InerScanPro.exe` sudah ada.

---

## 🚀 Quick Start

### Metode 1: Build Installer Saja

Jika executable sudah ada:

```bash
cd scripts
.\build_installer.bat
```

### Metode 2: Build Semua (Recommended)

Build executable dan installer sekaligus:

```bash
cd scripts
.\build_all.bat
```

Script akan:
1. ✅ Build executable dari source code
2. ✅ Verify build berhasil
3. ✅ Build installer dari executable
4. ✅ Verify installer berhasil

### Metode 3: Manual dengan Inno Setup GUI

1. Buka Inno Setup Compiler
2. File → Open → Pilih `installer\InerScanPro.iss`
3. Build → Compile
4. Installer akan dibuat di `installer_output\`

---

## 📁 Output Files

Setelah build berhasil:

```
installer_output/
└── InerScanPro_Setup_v3.1.exe    # Installer (15-25 MB)
```

**File ini siap didistribusikan!**

---

## 🔧 Installer Configuration

### File: `installer\InerScanPro.iss`

#### Basic Settings

```ini
AppName=InerScan Pro
AppVersion=3.1
AppPublisher=InerCorp
DefaultDirName={autopf}\InerScan Pro
```

#### Compression

```ini
Compression=lzma2/max        # Maximum compression
SolidCompression=yes         # Better compression ratio
```

#### Files Included

- `InerScanPro.exe` - Main executable
- `README.md` - User documentation
- `ANIMASI_README.md` - Animation features doc
- `BUILD_GUIDE.md` - Build documentation

#### Registry Entries

Installer akan membuat registry entries untuk:
- File associations (.pdf, .jpg, .jpeg, .png)
- Default icon
- Open with menu integration

---

## 🎨 Customization

### Mengubah Icon

1. Buat atau dapatkan file `.ico` (256x256 recommended)
2. Simpan sebagai `app_icon.ico` di root folder
3. Update di `InerScanPro.iss`:
   ```ini
   SetupIconFile=..\app_icon.ico
   ```

### Mengubah Version

Update di `InerScanPro.iss`:
```ini
#define MyAppVersion "3.2"
```

### Menambahkan Files

Tambahkan di section `[Files]`:
```ini
Source: "..\docs\manual.pdf"; DestDir: "{app}\docs"; Flags: ignoreversion
```

### Menambahkan Shortcuts

Tambahkan di section `[Icons]`:
```ini
Name: "{group}\User Manual"; Filename: "{app}\docs\manual.pdf"
```

---

## 📊 Installer Behavior

### Installation Process

1. **Welcome Screen** - Greet user
2. **License Agreement** - Show LICENSE file
3. **Information** - Display README.md
4. **Select Destination** - Choose install location
5. **Select Components** - Optional components
6. **Select Tasks** - Desktop icon, etc.
7. **Ready to Install** - Confirmation
8. **Installing** - Copy files, create shortcuts
9. **Finish** - Option to launch app

### Default Installation Path

```
C:\Program Files\InerScan Pro\
```

### Created Shortcuts

- Start Menu → InerScan Pro
- Desktop (optional)
- Quick Launch (optional, Windows 7)

### Registry Changes

```
HKEY_CLASSES_ROOT\
  .iscan\
  InerScanDocument\
  Applications\InerScanPro.exe\
```

---

## 🧪 Testing Installer

### Before Distribution

Test installer di clean environment:

1. **Fresh Windows VM** - Test di Windows 10/11 VM
2. **Different User Accounts** - Admin & Standard user
3. **Installation Paths** - Default & custom paths
4. **Upgrade Scenario** - Install over previous version
5. **Uninstall** - Verify clean removal

### Test Checklist

- [ ] Installer runs without errors
- [ ] Application launches after install
- [ ] Desktop icon works (if selected)
- [ ] Start menu shortcuts work
- [ ] File associations work
- [ ] All features functional
- [ ] Uninstaller removes everything
- [ ] No registry leftovers after uninstall

---

## 🐛 Troubleshooting

### "Inno Setup not found"

**Solusi:**
1. Install Inno Setup dari https://jrsoftware.org/isdl.php
2. Install ke default path: `C:\Program Files (x86)\Inno Setup 6\`
3. Atau update path di `build_installer.bat`

### "InerScanPro.exe not found"

**Solusi:**
```bash
# Build executable terlebih dahulu
cd scripts
.\build_exe.bat
```

### Installer Build Failed

**Solusi:**
1. Buka `installer\InerScanPro.iss` di Inno Setup GUI
2. Compile dari GUI untuk melihat error detail
3. Fix error yang muncul
4. Coba build lagi

### Antivirus Blocking Installer

**Solusi:**
1. Add exception untuk installer_output folder
2. Sign installer dengan code signing certificate
3. Submit ke antivirus vendors untuk whitelisting

---

## 🔐 Code Signing (Optional)

Untuk installer yang lebih terpercaya:

### 1. Dapatkan Code Signing Certificate

- Dari CA seperti DigiCert, Sectigo, dll
- Harga: ~$100-300/tahun

### 2. Sign Installer

```bash
signtool sign /f "certificate.pfx" /p "password" /t "http://timestamp.digicert.com" "InerScanPro_Setup_v3.1.exe"
```

### 3. Update Inno Setup Script

```ini
[Setup]
SignTool=signtool
SignedUninstaller=yes
```

---

## 📦 Distribution

### Upload Options

1. **GitHub Releases**
   - Tag version: `v3.1`
   - Upload installer sebagai release asset
   - Write release notes

2. **Website**
   - Host di website sendiri
   - Provide download link
   - Include SHA256 checksum

3. **Cloud Storage**
   - Google Drive
   - Dropbox
   - OneDrive

### Download Page Template

```markdown
# Download InerScan Pro

**Latest Version:** 3.1  
**Release Date:** February 8, 2026  
**File Size:** ~20 MB  
**Platform:** Windows 10/11 (64-bit)

[Download Installer](link-to-installer)

**SHA256:** [checksum-here]

## System Requirements
- Windows 10/11 (64-bit)
- 4GB RAM minimum
- 500MB disk space
- WIA-compatible scanner (optional)
```

---

## 🔄 Update Strategy

### Versioning

Follow Semantic Versioning:
- **Major.Minor.Patch** (e.g., 3.1.0)
- Major: Breaking changes
- Minor: New features
- Patch: Bug fixes

### Auto-Update (Future Enhancement)

Consider implementing:
- Check for updates on startup
- Download and install updates
- Notify users of new versions

---

## 📊 Installer Analytics (Optional)

Track installer downloads:

```javascript
// Google Analytics example
gtag('event', 'download', {
  'event_category': 'installer',
  'event_label': 'v3.1',
  'value': 1
});
```

---

## 📝 Checklist Before Release

- [ ] Version number updated
- [ ] README.md updated
- [ ] CHANGELOG.md created/updated
- [ ] All features tested
- [ ] Installer tested on clean Windows
- [ ] Uninstaller tested
- [ ] Screenshots updated
- [ ] Documentation complete
- [ ] License file included
- [ ] Code signed (optional)
- [ ] SHA256 checksum generated
- [ ] Release notes written

---

## 🎯 Best Practices

1. **Version Control** - Tag releases in git
2. **Changelog** - Document all changes
3. **Testing** - Test on multiple Windows versions
4. **Backup** - Keep old versions available
5. **Support** - Provide clear installation instructions
6. **Feedback** - Collect user feedback
7. **Updates** - Regular updates and bug fixes

---

## 📞 Support

Jika user mengalami masalah instalasi:

### Common Issues

**"Windows protected your PC"**
- Click "More info" → "Run anyway"
- Or get code signing certificate

**"Installation failed"**
- Run as administrator
- Disable antivirus temporarily
- Check disk space

**"Application won't start"**
- Install Visual C++ Redistributable
- Check Windows version compatibility

---

## 📚 Resources

- [Inno Setup Documentation](https://jrsoftware.org/ishelp/)
- [Inno Setup Examples](https://jrsoftware.org/isinfo.php)
- [Code Signing Guide](https://docs.microsoft.com/en-us/windows/win32/seccrypto/cryptography-tools)

---

<div align="center">

**Happy Distributing! 📦**

</div>
