import sys
import os

sys.path.append(os.getcwd())

try:
    from app.ui.main_window import ScannerApp
    print("ScannerApp imported successfully.")
except Exception as e:
    print(f"Import failed: {e}")
    import traceback
    traceback.print_exc()
