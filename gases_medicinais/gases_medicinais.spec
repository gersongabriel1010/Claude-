# -*- mode: python ; coding: utf-8 -*-
# Arquivo de build do PyInstaller. Funciona tanto no Windows quanto no
# Linux/Mac: o executável gerado sempre corresponde ao sistema operacional
# onde o comando "pyinstaller gases_medicinais.spec" for executado
# (o PyInstaller não faz compilação cruzada entre sistemas operacionais).

block_cipher = None

a = Analysis(
    ['run_app.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['openpyxl'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='ControleGasesMedicinais',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
