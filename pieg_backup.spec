# -*- mode: python -*-
from kivy.deps import sdl2, glew

block_cipher = None


a = Analysis(['main.py'],
             pathex=['C:\\Users\\tokariew\\Desktop\\PIEG'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=['PySide', 'PyQt4', 'PyQt5'],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
			 
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='PIEG',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
			   *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)],
               strip=False,
               upx=True,
               name='PIEG')
