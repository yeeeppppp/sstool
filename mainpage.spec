# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['mainpage.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        'rich',
        'rich.console',
        'rich.panel',
        'rich.text',
        'rich.prompt',
        'rich.table',
        'src',
        'src.file_searcher',
        'src.recycle_bin_analyzer',
        'src.registry_parser',
        'src.LastExt',
        'src.signature_checker_dll',
        'src.firewall_parser',
        'src.service_checker',
        'src.evtx_check',
        'src.usb',
        'src.ddfo_detect',
        'src.modanalyzer'
    ],
    hookspath=[],
    hooksconfig={},
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
    name='sstool',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
    onefile=True  # This creates a single executable file
)
