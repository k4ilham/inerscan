# 📚 InerScan Pro - User Manual

**Version 2.5** | Complete Guide to Professional Document Scanning

---

## Table of Contents

1. [Getting Started](#getting-started)
2. [Basic Scanning](#basic-scanning)
3. [Batch Scanning](#batch-scanning)
4. [Image Editing Tools](#image-editing-tools)
5. [Auto-Straighten Feature](#auto-straighten-feature)
6. [Watermark & Stamp](#watermark--stamp)
7. [Paper Size Management](#paper-size-management)
8. [Photo Grids & Collages](#photo-grids--collages)
9. [Book & Duplex Scanning](#book--duplex-scanning)
10. [Export Options](#export-options)
11. [Scan History & File Manager](#scan-history--file-manager)
12. [Settings & Preferences](#settings--preferences)
13. [Troubleshooting](#troubleshooting)

---

## Getting Started

### System Requirements

**Minimum:**
- Windows 7 / Ubuntu 20.04 / macOS 10.13
- 2 GB RAM
- 200 MB free disk space
- WIA-compatible scanner (Windows)

**Recommended:**
- Windows 10/11 / Ubuntu 22.04 / macOS 12+
- 4 GB RAM or more
- 1 GB free disk space
- High-resolution flatbed or ADF scanner

### First Launch

1. **Connect Your Scanner**
   - Connect scanner via USB
   - Ensure drivers are installed
   - Power on the scanner

2. **Launch InerScan Pro**
   - Double-click `InerScanPro.exe` (Windows)
   - Scanner will be auto-detected

3. **Configure Output Folder**
   - Default: `Documents/Scans`
   - Click "📁 Browse..." to change
   - Set filename prefix (default: "scan")

---

## Basic Scanning

### Single Page Scan

1. **Prepare Document**
   - Place document face-down on scanner
   - Align with guides

2. **Start Scan**
   - Click "🚀 Start Scan" button
   - Scanner dialog will appear
   - Click "Scan" in the scanner dialog
   - Wait for scan to complete

3. **View Result**
   - Scanned page appears in preview area
   - Thumbnail added to right sidebar
   - Page counter updated

### Multi-Page Scan (Manual)

1. Scan first page using "🚀 Start Scan"
2. Replace document
3. Click "🚀 Start Scan" again
4. Repeat for all pages
5. All pages stored in sequence

---

## Batch Scanning

**NEW FEATURE!** Automatically scan multiple pages with minimal interaction.

### Starting Batch Scan

1. **Click "📚 Batch Scan" Button**
   - Green button below Start Scan

2. **Configure Batch Settings**
   - **Target Mode**: Enter number of pages (e.g., 10)
   - **Continuous Mode**: Enter 0 to scan until stopped
   - Click OK

3. **Batch Scan Process**
   - Status shows: "Scanning 1/10 pages..."
   - Place first document
   - Scanner automatically triggers every 2 seconds
   - Replace document when prompted
   - Progress updates in real-time

4. **Stop Batch Scan**
   - Click "⏹️ Stop Batch" to end early
   - Or wait for target to complete
   - All pages saved automatically

### Batch Scan Tips

✅ **Best Practices:**
- Prepare all documents before starting
- Use consistent document orientation
- Keep documents organized by order
- Use ADF scanner for fastest results

⚠️ **Important:**
- 2-second delay between scans
- Single scan button disabled during batch
- Can't edit pages while batch scanning
- Stop batch before making changes

---

## Image Editing Tools

### Basic Transformations

#### Rotate
- **Rotate Left (↺)**: Rotate 90° counter-clockwise
- **Rotate Right (↻)**: Rotate 90° clockwise
- **Usage**: Click button repeatedly for 180°/270° rotation

#### Flip
- **Flip Horizontal (↔)**: Mirror left-to-right
- **Flip Vertical (↕)**: Mirror top-to-bottom
- **Useful for**: Correcting mirrored scans

### Brightness & Contrast

#### Brightness Slider (💡)
- **Range**: 0.5x (dark) to 2.0x (bright)
- **Default**: 1.0x (no change)
- **Usage**: Drag slider left/right
- **Live Preview**: Changes appear instantly

#### Contrast Slider (🎭)
- **Range**: 0.5x (low) to 2.0x (high)
- **Default**: 1.0x (no change)
- **Usage**: Increase for sharper text
- **Live Preview**: Real-time updates

### Black & White Mode

- **Toggle**: Click "⚫ Black & White" switch
- **Effect**: Converts to grayscale
- **Best For**: Text documents, contracts
- **File Size**: Reduces final file size

### Advanced Tools

#### Crop Tool (✂️)
1. Click "✂️ Crop Tool"
2. Click and drag on image to select area
3. Confirm or cancel crop
4. Cropped area becomes new image

#### Auto Crop (📐)
- **One-click**: Automatically detect content
- **Removes**: White/empty borders
- **Algorithm**: Edge detection
- **Result**: Perfectly cropped document

#### Remove Background (🧹)
- **Function**: Makes white areas transparent
- **Threshold**: Adjustable (default 240/255)
- **Use Cases**: Logos, signatures, stamps
- **Output**: RGBA image with transparency

---

## Auto-Straighten Feature

**AI-Powered skew correction** for tilted documents and cards.

### How It Works

**Technology:**
- **Edge Detection**: Finds document borders
- **Contour Analysis**: Detects main object
- **Angle Calculation**: Computes tilt angle
- **Rotation**: Applies correction

### Using Auto-Straighten

1. **Scan a Tilted Document**
   - ID card, receipt, or any document
   - Can be rotated up to ±45°

2. **Click "📐 Auto-Straighten"**
   - Dialog appears with 3 options:
     - **Yes**: Straighten + Clean + Crop
     - **No**: Straighten only
     - **Cancel**: Abort

3. **Choose Option**
   
   **Option 1 - Full Clean (Recommended)**
   - ✅ Detects and fixes angle
   - ✅ Removes white background
   - ✅ Auto-crops to content
   - ✅ Perfect for ID cards!

   **Option 2 - Basic Straighten**
   - ✅ Fixes angle only
   - ❌ Keeps background
   - ❌ No auto-crop

4. **Result**
   - Success message shows method used
   - Image updated instantly
   - Ready to save!

### Best Results

✅ **Works Best With:**
- ID cards, passports
- Business cards
- Receipts
- Certificates
- Photos with clear edges

⚠️ **May Not Work Well:**
- Very low contrast images
- Heavily decorated backgrounds
- Circular/irregular shapes

---

## Watermark & Stamp

**Professional document stamping** with customizable watermarks.

### Built-in Templates

1. **COPY** - For photocopies
2. **DRAFT** - For draft versions
3. **CONFIDENTIAL** - For sensitive docs
4. **APPROVED** - For approved documents
5. **SAMPLE** - For samples
6. **VOID** - For voided documents
7. **ORIGINAL** - To mark originals
8. **Custom...** - Your own text

### Adding a Watermark

1. **Select Template**
   - Choose from dropdown
   - Or select "Custom..." to enter text

2. **Choose Position**
   - `center` - Middle of document (recommended)
   - `top-right` - Upper right corner
   - `bottom-right` - Lower right corner
   - `top-left` - Upper left corner
   - `bottom-left` - Lower left corner

3. **Adjust Opacity**
   - Use "💧 Opacity" slider
   - 0% = Invisible
   - 50% = Semi-transparent (recommended)
   - 100% = Fully opaque

4. **Apply Watermark**
   - Click "🏷️ Add Watermark"
   - Watermark appears diagonally (-45°)
   - Red color for visibility
   - Font size auto-calculated

### Watermark Tips

✅ **Best Practices:**
- Use 50% opacity for readability
- Center position for maximum impact
- Red color makes it official-looking
- Apply before saving final document

⚠️ **Note:**
- Watermark is permanent after saving
- Can't be removed easily
- Make a backup before watermarking

---

## Paper Size Management

**23+ preset paper sizes** plus custom dimensions.

### Standard Sizes

**ISO A-Series:**
- A0 (841×1189mm) - Architectural drawings
- A1-A3 - Posters, technical drawings
- **A4 (210×297mm)** - Standard documents
- A5-A6 - Pocket-sized

**ISO B-Series:**
- B4, B5 - Between A-sizes

**North American:**
- Letter (8.5×11") - US standard
- Legal (8.5×14") - Legal documents
- Executive (7.25×10.5") - Corporate
- Ledger/Tabloid (11×17") - Spreadsheets
- Folio (8.5×13") - Manuscripts

**Photo Sizes:**
- 3×5, 4×6, 5×7, 8×10 inches

**Card Sizes:**
- Business Card (3.5×2")
- ATM/Credit Card (85.6×53.98mm)
- ID Card
- Passport Photo (35×45mm)

### Resizing to Paper Size

1. **Select Paper Size**
   - Choose from dropdown
   - Or click "Custom..." for manual entry

2. **Click "✂️ Resize to Selected"**
   - Dialog appears with 2 options:

3. **Choose Resize Method**
   
   **Option 1 - Fit (Maintain Aspect)**
   - ✅ No distortion
   - ✅ Entire image visible
   - ❌ May have white borders
   
   **Option 2 - Crop to Center**
   - ✅ Fills entire area
   - ❌ May crop edges
   - ✅ No white space

4. **Result**
   - Image resized to exact dimensions
   - Ready for printing!

---

## Photo Grids & Collages

**Create beautiful photo collages** from multiple scanned pages.

### Available Layouts

- **1×2** or **2×1** - 2 photos side-by-side or stacked
- **2×2** - 4 photos in square grid
- **3×2** or **2×3** - 6 photos
- **3×3** - 9 photos in grid
- **4×4** - 16 photos in large grid

### Creating a Photo Grid

1. **Scan Multiple Pages**
   - Scan all photos/pages you want in grid
   - At least 2 pages required
   - No maximum limit

2. **Select Grid Layout**
   - Go to "🎨 Collage & Photo Grid" section
   - Choose layout from dropdown (e.g., "2x2")

3. **Create Grid**
   - Click "🖼️ Create Grid from All Pages"
   - Grid is generated automatically
   - New page added to your library

4. **Result**
   - All pages arranged in grid
   - Equal spacing (20px default)
   - Images auto-resized to fit
   - White background

### Grid Tips

✅ **Best Practices:**
- Use similar-sized images
- Scan all photos first
- Choose layout based on count
  - 4 photos = 2×2
  - 9 photos = 3×3
- Save grid as separate file

---

## Book & Duplex Scanning

**Advanced features** for scanning books and double-sided documents.

### Split Page (Book Scanning)

**For scans of open books** (2 pages in one scan):

1. Scan an open book spread
2. Click "Split Page (L/R)"
3. Image split into left and right halves
4. Two separate pages created

### Reverse Order

**For stacks scanned backwards**:

1. Scan pages (e.g., page 10, 9, 8...)
2. Click "Reverse Order"
3. Pages reordered (8, 9, 10...)
4. Correct sequence restored

### Interleave Stacks

**For duplex (front/back) scanning**:

#### Workflow:
1. **Scan all FRONT pages** (1, 3, 5, 7...)
2. Note page count (e.g., 4 pages)
3. **Flip stack and scan all BACK pages** (8, 6, 4, 2...)
4. Now you have 8 pages total
5. **Click "Interleave Stacks"**
6. Enter split point (e.g., 4)
7. Pages interleaved: 1, 2, 3, 4, 5, 6, 7, 8

#### Result:
- Front and back pages merged
- Correct reading order
- Perfect for duplex documents

---

## Export Options

### Save as Image (🖼️)

**Saves current page as JPEG**:

1. Select page to save
2. Click "🖼️ Save as Image"
3. File saved to output folder
4. Filename: `{prefix}_{number}.jpg`
5. Quality: 95% (high quality)
6. **Recorded in history automatically**

### Save as PDF (📄)

**Combines all pages into one PDF**:

1. Scan/edit all pages
2. Click "📄 Save as PDF"
3. All pages combined
4. Filename: `{prefix}.pdf`
5. Multi-page PDF created
6. **Recorded in history automatically**

### File Naming

- **Prefix**: Set in "Filename" field (default: "scan")
- **Location**: Set in "Location" field
- **Browse**: Click "📁 Browse..." to change folder
- **Auto-increment**: Images numbered automatically

---

## Scan History & File Manager

**NEW FEATURE!** Complete file management system.

### Viewing Scan History

1. **Click "📜 View Scan History"**
   - New window opens
   - Shows all saved scans
   - Up to 100 recent scans

2. **History Information**
   Each entry shows:
   - 📄 **Filename**
   - 📄 **File type** (PDF/JPEG)
   - 📑 **Page count**
   - 💾 **File size** (MB)
   - 🕒 **Scan date & time**

3. **File Actions**
   - **📂 Open**: Opens file directly
   - **📁 Folder**: Opens containing folder
   - **Status**: Shows if file still exists

### Opening File Location

- **Click "📁 Open File Location"**
- Opens output folder in Explorer
- Quick access to all scans
- Manage files manually

### Clear History

- **Click "🗑️ Clear History"**
- Confirmation dialog appears
- **Only deletes history records**
- **Files remain safe!**
- Use to clean up database

### History Database

**Technical Details:**
- **Storage**: SQLite database
- **File**: `settings.db`
- **Location**: App directory
- **Tracking**: Automatic
- **Privacy**: Local only

---

## Settings & Preferences

### Persistent Settings

**Auto-saved settings:**
- Output directory
- Filename prefix
- Last used paper size
- Window position
- UI preferences

### Changing Settings

#### Output Directory
1. Click "📁 Browse..."
2. Select folder
3. Click "Select Folder"
4. Saved automatically

#### Filename Prefix
1. Click in "Filename" field
2. Type new prefix
3. Press Enter or click away
4. Saved automatically

### Resetting Settings

**To reset to defaults:**
1. Close application
2. Delete `settings.db`
3. Restart application
4. Default settings restored

---

## Troubleshooting

### Scanner Not Detected

**Problem**: Scanner button disabled

**Solutions:**
1. Check USB connection
2. Ensure scanner powered on
3. Reinstall scanner drivers
4. Restart computer
5. Try different USB port

### Batch Scan Issues

**Problem**: Batch scan not triggering

**Solutions:**
1. Check scanner supports auto-scan
2. Increase delay in code (default 2s)
3. Use manual mode instead
4. Ensure scanner dialog doesn't require clicks

### Auto-Straighten Not Working

**Problem**: Image still tilted

**Solutions:**
1. Ensure clear document edges
2. Try "No" option (straighten only)
3. Use manual rotation
4. Check image has good contrast
5. Ensure OpenCV installed

### Watermark Too Faint

**Problem**: Can't see watermark

**Solutions:**
1. Increase opacity to 70-100%
2. Use darker background image
3. Try different position
4. Increase font size in code

### Export Fails

**Problem**: Can't save files

**Solutions:**
1. Check folder permissions
2. Ensure enough disk space
3. Close other programs using files
4. Try different output folder
5. Check filename for special characters

### History Window Empty

**Problem**: No history showing

**Solutions:**
1. Save at least one file first
2. Check database file exists
3. Restart application
4. Clear and rebuild history

---

## Keyboard Shortcuts

_(Coming in future version)_

- `Ctrl+S` - Save as Image
- `Ctrl+P` - Save as PDF
- `Ctrl+R` - Rotate Right
- `Ctrl+Shift+R` - Rotate Left
- `Ctrl+Delete` - Delete Current Page

---

## Tips & Best Practices

### For Best Scan Quality

✅ **Do:**
- Clean scanner glass regularly
- Align documents properly
- Use highest DPI scanner setting
- Scan in good lighting
- Remove staples and clips

❌ **Don't:**
- Scan wrinkled documents
- Scan very small text at low DPI
- Stack multiple pages
- Scan folded documents
- Use dirty scanner glass

### For Efficient Workflow

✅ **Recommended:**
- Use batch scanning for multi-page docs
- Edit after all pages scanned
- Save periodically
- Use meaningful filenames
- Organize by date/topic folders

### For Professional Results

✅ **Best:**
- Use auto-straighten for alignment
- Apply watermarks to drafts
- Use black & white for text documents
- Create PDFs for multi-page docs
- Keep originals until verified

---

## Support & Contact

### Getting Help

- 📧 **Email**: k4ilham@gmail.com
- 🌐 **Website**: [inercorp.com](https://inercorp.com)
- 💬 **Issues**: [GitHub Issues](https://github.com/k4ilham/inerscan/issues)

### Reporting Bugs

**Include:**
1. Operating system & version
2. InerScan Pro version
3. Scanner model
4. Steps to reproduce
5. Error messages
6. Screenshots if possible

### Feature Requests

**Submit via GitHub Issues:**
1. Describe the feature
2. Explain use case
3. Provide examples
4. Tag as "enhancement"

---

## Appendix

### Supported File Formats

**Input:**
- Any format scanner produces
- WIA standard formats

**Output:**
- JPEG (.jpg) - High quality (95%)
- PDF (.pdf) - Multi-page support
- PNG (via code modification)

### Version History

**v2.5** (Current)
- ✨ Batch scanning
- ✨ Watermark/stamp
- ✨ Scan history & file manager
- ✨ Auto-straighten improvements

**v2.0**
- Photo grid/collage
- Paper size presets
- Book scanning tools
- Interactive user guide

**v1.0**
- Initial release
- Basic scanning
- Image editing
- PDF export

---

<div align="center">

**© 2026 InerCorp - All Rights Reserved**

Made with ❤️ for Document Digitization

</div>
