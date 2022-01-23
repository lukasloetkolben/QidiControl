# -*- mode: python -*-

import os
from os.path import join


from PyInstaller.utils.hooks import (
    collect_data_files,
    copy_metadata,
    collect_submodules
)
from kivy import kivy_data_dir
from kivy_deps import sdl2, glew
from kivy.tools.packaging import pyinstaller_hooks as hooks
from kivymd import hooks_path as kivymd_hooks_path
import pkgutil

path = os.path.abspath(".")

block_cipher = None
kivy_deps_all = hooks.get_deps_all()
kivy_factory_modules = hooks.get_factory_modules()

datas = [    (join('./', '*.json'), './')]
# list of modules to exclude from analysis
excludes_a = ['Tkinter', '_tkinter', 'twisted', 'docutils', 'pygments', '.git', '.idea']

# list of hiddenimports
hiddenimports = kivy_deps_all['hiddenimports'] + kivy_factory_modules + collect_submodules('kivymd') + collect_submodules('plyer')

# binary data
sdl2_bin_tocs = [Tree(p) for p in sdl2.dep_bins]
glew_bin_tocs = [Tree(p) for p in glew.dep_bins]
bin_tocs = sdl2_bin_tocs + glew_bin_tocs

# assets
kivy_assets_toc = Tree(kivy_data_dir, prefix=join('kivy_install', 'data'))
source_assets_toc = Tree('resources')
assets_toc = [kivy_assets_toc, source_assets_toc]

tocs = bin_tocs + assets_toc

a = Analysis(['qidi_control_application.py'],
             pathex=[path],
             binaries=None,
             datas=datas,
             hiddenimports=hiddenimports,
             hookspath=[kivymd_hooks_path],
             runtime_hooks=[],
             excludes=excludes_a,
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)


pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)


exe1 = EXE(pyz,
          a.scripts,
          name='QidiControl',
          exclude_binaries=True,
          debug=False,
          strip=False,
          upx=True,
          console=False)


coll = COLLECT(exe1,
              Tree(path),
               a.binaries,
               a.zipfiles,
               a.datas,
               *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)],
               *tocs,
               strip=False,
               upx=True,
               name='QidiControl')