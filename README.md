# InerScan - Advanced Document Scanner

InerScan is a modern, Python-based document scanning application designed for Windows. It provides a sleek user interface for scanning documents, performing advanced image edits, and exporting them as Images or PDFs.

## Features

*   **Multi-Page Scanning**: Scan multiple pages into a single session and export them as a multi-page PDF.
*   **Modern UI**: Built with `customtkinter` for a professional Dark/Light mode interface.
*   **Image Editing**:
    *   **Rotation & Flipping**: Rotate 90° or flip images horizontally/vertically.
    *   **Adjustments**: Real-time Brightness and Contrast sliders.
    *   **Grayscale/B&W**: Convert scans to black and white for clearer text.
    *   **Crop Tool**: Manual cropping to select specific areas of the document.
    *   **Background Removal**: Automatically remove white backgrounds or replace them with a custom color.
*   **Export Options**:
    *   Save individual pages as JPG/PNG.
    *   Save all scanned pages as a single PDF.
    *   Customizable output folder and filename prefixes.

## Prerequisites

*   **Windows OS**: Required for WIA (Windows Image Acquisition) support.
*   **Scanner Driver**: Ensure your scanner (e.g., Epson L3110) drivers are installed and the device is connected.
*   **Python 3.x**: Installed on your system.

## Installation

1.  Clone or download this repository.
2.  Run the setup script to create a virtual environment and install dependencies:
    ```bat
    run_with_venv.bat
    ```
    Alternatively, install manually:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1.  Connect your scanner to the PC.
2.  Double-click `run_with_venv.bat` to launch the application.
3.  Click **START SCAN** to scan a document.
4.  Use the **Edit Controls** in the left sidebar to adjust the image.
5.  Use the **Crop Tool** to refine the image area.
6.  Click **Save All to PDF** to finish your session.

## Dependencies

*   `customtkinter`
*   `Pillow`
*   `pywin32`
*   `numpy`

## Troubleshooting

*   **Scanner not found**: Ensure the scanner is on and connected via USB. Try restarting the application.
*   **WIA Error**: If you see a WIA 0x80210015 error, the scanner might be busy or disconnected.
