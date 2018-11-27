# -*- mode: python -*-

block_cipher = None


a = Analysis(['main.py'],
             pathex=['/Users/huangyuemei/PycharmProjects/ReadlingList'],
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
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='main',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=False , icon='icon.icns')
app = BUNDLE(exe,
         name='AcademicReadingList.app',
         icon='icon.icns',
         bundle_identifier='com.metahlm.app.acrl',
         info_plist={
            'NSHighResolutionCapable': True,
            'CFBundleVersion': '0.1.0',
            'CFBundleShortVersionString': '0.1.0',
            'CFBundleDocumentTypes': [
                {
                    'CFBundleTypeName': 'Reading List',
                    'CFBundleTypeExtensions': 'rl',
                    'CFBundleTypeIconFile': 'icon.icns'
                    }
                ]
            },
         )
