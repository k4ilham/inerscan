# Release Instructions

## Building Locally

### Windows
1. Run `build_windows.bat`
2. Executable will be in `dist/InerScanPro.exe`

### Linux
1. Make script executable: `chmod +x build_linux.sh`
2. Run `./build_linux.sh`
3. Executable will be in `dist/InerScanPro`

### macOS
1. Make script executable: `chmod +x build_macos.sh`
2. Run `./build_macos.sh`
3. App bundle will be in `dist/InerScan Pro.app`
4. DMG installer will be in `dist/InerScanPro.dmg`

## GitHub Releases (Automated)

### Creating a Release

1. **Commit and push your changes:**
   ```bash
   git add .
   git commit -m "Release v1.0.0"
   git push
   ```

2. **Create and push a tag:**
   ```bash
   git tag v1.0.0
   git push origin v1.0.0
   ```

3. **GitHub Actions will automatically:**
   - Build for Windows, Linux, and macOS
   - Create a GitHub Release
   - Upload all executables

### Manual Release

If you prefer to build manually and upload:

1. Build on each platform using the scripts above
2. Go to GitHub → Releases → "Draft a new release"
3. Create a new tag (e.g., `v1.0.0`)
4. Upload the built files:
   - `InerScanPro.exe` (Windows)
   - `InerScanPro` (Linux)
   - `InerScanPro.dmg` (macOS)
5. Write release notes
6. Click "Publish release"

## Version Numbering

Use semantic versioning: `vMAJOR.MINOR.PATCH`

- **MAJOR**: Breaking changes
- **MINOR**: New features (backwards compatible)
- **PATCH**: Bug fixes

Examples:
- `v1.0.0` - Initial release
- `v1.1.0` - Added photo grid feature
- `v1.1.1` - Fixed bug in paper size selector

## Release Checklist

Before creating a release:

- [ ] Update version in `scanner_app.py` (window title or about section)
- [ ] Update `MANUAL_BOOK.md` with new features
- [ ] Test on target platform
- [ ] Update `requirements.txt` if dependencies changed
- [ ] Write clear release notes
- [ ] Tag with semantic version

## Platform-Specific Notes

### Windows
- Requires Windows 7 or later
- 64-bit only
- Includes all Python dependencies
- Size: ~50-70 MB

### Linux
- Requires GTK3 libraries
- Tested on Ubuntu 20.04+
- May need: `sudo apt install python3-tk`
- Size: ~40-60 MB

### macOS
- Requires macOS 10.13 or later
- Universal binary (Intel + Apple Silicon)
- May need to allow in System Preferences → Security
- Size: ~60-80 MB

## Troubleshooting Build Issues

### "Module not found" errors
- Add missing module to `hiddenimports` in `InerScanPro.spec`

### Large file size
- Remove unnecessary dependencies
- Use UPX compression (enabled by default)

### Icon not showing (Windows)
- Ensure `app_icon.ico` exists
- Rebuild with `pyinstaller --clean`

## Distribution

After building, you can distribute:
1. As standalone files (from `dist/` folder)
2. Via GitHub Releases (automated)
3. Via your website
4. Via package managers (future work)
