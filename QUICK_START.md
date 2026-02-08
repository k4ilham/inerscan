# 🚀 Quick Start - InerScan Pro Installer

## Untuk Developer

### Build Complete Package

```bash
# 1. Navigate ke scripts folder
cd "C:\inercorp\aplikasi scanner\scripts"

# 2. Run complete build (Executable + Installer)
.\build_all.bat
```

**Output:**
- `dist\InerScanPro.exe` - Standalone executable
- `installer_output\InerScanPro_Setup_v3.1.exe` - Installer

---

## Untuk End User

### Install InerScan Pro

1. **Download** installer: `InerScanPro_Setup_v3.1.exe`
2. **Double-click** installer
3. **Follow** installation wizard
4. **Launch** from Start Menu or Desktop

### System Requirements

- Windows 10/11 (64-bit)
- 4GB RAM minimum
- 500MB disk space
- Scanner (optional)

---

## File Structure

```
InerScan Pro/
├── scripts/
│   ├── build_exe.bat          # Build executable only
│   ├── build_installer.bat    # Build installer only
│   └── build_all.bat          # Build both (recommended)
├── installer/
│   └── InerScanPro.iss        # Inno Setup script
├── dist/
│   └── InerScanPro.exe        # Built executable
└── installer_output/
    └── InerScanPro_Setup_v3.1.exe  # Built installer
```

---

## Build Commands

| Command | Description |
|---------|-------------|
| `build_exe.bat` | Build executable only |
| `build_installer.bat` | Build installer (requires exe) |
| `build_all.bat` | Build everything |

---

## Prerequisites

### For Building Executable
- ✅ Python 3.8+
- ✅ pip
- ✅ Virtual environment (auto-created)

### For Building Installer
- ✅ Inno Setup 6
- ✅ Built executable (`dist\InerScanPro.exe`)

**Download Inno Setup:** https://jrsoftware.org/isdl.php

---

## Troubleshooting

### "Inno Setup not found"
→ Install from https://jrsoftware.org/isdl.php

### "InerScanPro.exe not found"
→ Run `build_exe.bat` first

### "Python not found"
→ Install Python from python.org

---

## Distribution

### What to Share

**Option 1: Installer (Recommended)**
- File: `InerScanPro_Setup_v3.1.exe`
- Size: ~20 MB
- User-friendly installation

**Option 2: Standalone Executable**
- File: `InerScanPro.exe`
- Size: ~100 MB
- No installation needed

---

## Documentation

- `README.md` - Main documentation
- `BUILD_GUIDE.md` - Build instructions
- `INSTALLER_GUIDE.md` - Installer details
- `ANIMASI_README.md` - Animation features

---

<div align="center">

**Made with ❤️ by InerCorp**

</div>
