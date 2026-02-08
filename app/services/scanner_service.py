import os
import win32com.client
from PIL import Image
import tempfile

class ScannerService:
    def __init__(self):
        # Create temp directory in user's temp folder
        self.temp_dir = os.path.join(tempfile.gettempdir(), 'InerScanPro')
        if not os.path.exists(self.temp_dir):
            os.makedirs(self.temp_dir)

    def scan_document(self, temp_filename="temp_scan.png"):
        """
        Connects to the scanner using WIA and returns a PIL Image.
        Raises Exception if scanning fails.
        """
        try:
            # Full path to temp file in user's temp directory
            temp_path = os.path.join(self.temp_dir, temp_filename)
            
            # WIA Common Dialog
            wia_dialog = win32com.client.Dispatch("WIA.CommonDialog")
            image_file = wia_dialog.ShowAcquireImage()

            if image_file:
                # Remove existing temp file
                if os.path.exists(temp_path):
                    try:
                        os.remove(temp_path)
                    except:
                        pass  # Ignore if can't remove
                    
                # Save to temp path
                image_file.SaveFile(temp_path)
                
                # Load with PIL
                img = Image.open(temp_path)
                
                # Clean up temp file after loading
                try:
                    os.remove(temp_path)
                except:
                    pass  # Ignore cleanup errors
                
                return img
            return None
        except Exception as e:
            # Provide more helpful error message
            error_msg = str(e)
            if "Access is denied" in error_msg:
                raise Exception("Scanner access denied. Please check:\n1. Scanner is connected and powered on\n2. Scanner drivers are installed\n3. No other application is using the scanner\n4. Try running as Administrator")
            elif "2147352567" in error_msg or "WIA" in error_msg:
                raise Exception(f"Scanner error: {error_msg}\n\nTry:\n1. Reconnect scanner\n2. Restart application\n3. Check Windows Image Acquisition service")
            else:
                raise Exception(f"Scan failed: {error_msg}")
