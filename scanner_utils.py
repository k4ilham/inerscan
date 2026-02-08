import os
import win32com.client
from PIL import Image

class ScannerService:
    def __init__(self):
        pass

    def scan_document(self, temp_path="temp_scan.png"):
        """
        Connects to the scanner using WIA and returns a PIL Image.
        Raises Exception if scanning fails.
        """
        try:
            # WIA Common Dialog
            wia_dialog = win32com.client.Dispatch("WIA.CommonDialog")
            image_file = wia_dialog.ShowAcquireImage()

            if image_file:
                # Remove existing temp file
                if os.path.exists(temp_path):
                    os.remove(temp_path)
                    
                # Save to temp path
                image_file.SaveFile(os.path.abspath(temp_path))
                
                # Load with PIL
                img = Image.open(temp_path)
                return img
            return None
        except Exception as e:
            raise e
