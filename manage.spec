# -*- mode: python ; coding: utf-8 -*-

import os
from pathlib import Path

venv_path = Path(os.getenv("VIRTUAL_ENV", ".venv"))
site_packages = venv_path / "lib" / "python3.8" / "site-packages"

a = Analysis(
    ['manage.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('app/templates', 'templates'),
        (str(site_packages / 'mne/utils/__init__.pyi'), 'mne/utils'),
        (str(site_packages / 'mne/__init__.pyi'), 'mne'),
    ],
     hiddenimports=[
        'mne.utils._logging',
        'mne.utils._bunch',
        'mne.utils._check_version',
    ],
    hookspath=['app/dataProcess/utils/hook_mne.py'],  # 指定钩子文件所在目录
    hooksconfig={},
    runtime_hooks=[],

    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='manage',
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
)
