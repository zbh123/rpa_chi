# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['write_url.py'],
             pathex=['D:\\pyfile\\github_files\\hobby\\数据处理\\hegui'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries+[('oci.dll','D:\\pyfile\\Oracle_connect\\instantclient_12_2\\oci.dll','BINARY'),('oraociei12.dll','D:\\pyfile\\Oracle_connect\\instantclient_12_2\\oraociei12.dll','BINARY')],
          a.zipfiles,
          a.datas,
          [],
          name='write_url',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False )
