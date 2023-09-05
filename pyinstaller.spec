# -*- mode: python ; coding: utf-8 -*-


from kivy_deps import sdl2, glew


block_cipher = None


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('kvgui/kv', 'kvgui/kv'),
        ('resources', 'resources')
    ],
    hiddenimports=[
        'py_ballisticcalc.profile',
        'py_ballisticcalc.drag_tables',
        'kivymd.uix.widget',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    #excludes=[
    #    'wheel', 'jnius', 'kivy_install', 'setuptools', 'docutils',
    #    'numpy', 'pywin32', 'win32', 'win32com' 'pythonwin', 'PIL'
    #],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)


exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='eBallistica',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['resources/icons/icon.png'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)],
    strip=False,
    upx=True,
    upx_exclude=[],
    name='eBallistica',
)
