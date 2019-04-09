# -*- mode: python -*-

block_cipher = None


a = Analysis(['main.py'],
             pathex=['C:\\Users\\tokariew\\Desktop\\PIEG'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=['PySide', 'PyQt4'],
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
          name='PIEG',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=False,
          console=False, icon='data\\pieg.ico' )

