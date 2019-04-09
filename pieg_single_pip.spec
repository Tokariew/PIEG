# -*- mode: python -*-
from kivy.deps import sdl2, glew

block_cipher = None


a = Analysis(['main.py'],
             pathex=['C:\\Users\\tokariew\\Desktop\\PIEG'],
             binaries=[],
             datas=None,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=['PySide', 'PyQt4'],#['PySide', 'PyQt4', 'PyQt5'],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

a.datas += [('gab.kv', 'gab.kv', 'DATA')]
a.datas += [('data/pieg.png', 'data/pieg.png', 'DATA')]

exe = EXE(pyz,
          a.scripts,
          a.binaries,
		  a.zipfiles,
		  a.datas,
		  *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)],
          name='PIEG',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=False,
          console=True, icon='data\\pieg.ico')