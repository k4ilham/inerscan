# -*- mode: python ; coding: utf-8 -*-
import os

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('app', 'app'),
    ],
    hiddenimports=[
        'PIL._tkinter_finder',
        'tkinter',
        'customtkinter',
        'pyttsx3',
        'win32com.client',
        'comtypes',
        'openai',
        'cv2',
        'numpy',
        'app.ui.widgets.animations',
        'app.ui.widgets.openai_settings_dialog',
        'app.ui.widgets.ai_chat_window',
        'app.ui.widgets.text_result_panel',
        'app.ui.widgets.sidebar_panels',
        'app.ui.ribbons.scanner_tab',
        'app.ui.ribbons.editor_tab',
        'app.ui.ribbons.ai_tab',
        'app.ui.ribbons.annotate_tab',
        'app.ui.ribbons.layout_tab',
        'app.ui.ribbons.library_tab',
        'app.services.scanner_service',
        'app.services.image_service',
        'app.services.db_service',
        'app.services.guide_service',
        'app.services.ai_openai_service',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='InerScanPro',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='app_icon.ico' if os.path.exists('app_icon.ico') else None,
)
