import sys
import os

# Add project root to path
sys.path.append(os.getcwd())

try:
    from app.services.db_service import DatabaseService
    from app.services.ai_openai_service import OpenAIService
    from app.ui.widgets.openai_settings_dialog import OpenAISettingsDialog
    import customtkinter as ctk

    print("Imports successful.")

    # Mock DB
    class MockDB:
        def get_setting(self, key, default): return default
        def save_setting(self, key, value): pass

    db = MockDB()
    service = OpenAIService(db)
    print("OpenAIService initialized.")

    # Check methods exist
    assert hasattr(service, 'extract_text_ocr')
    assert hasattr(service, 'smart_rename')
    assert hasattr(service, 'analyze_document')
    print("OpenAIService methods verified.")

    print("Verification script completed successfully.")

except Exception as e:
    print(f"Verification failed: {e}")
    import traceback
    traceback.print_exc()
