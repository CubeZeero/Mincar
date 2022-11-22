# -*- coding: utf-8 -*-

import os
import shutil
import subprocess
import json

if os.path.isdir('build') : shutil.rmtree('build')

shutil.copytree('src', 'build')
shutil.rmtree('build/__pycache__')

#pyarmor == 7.6.0 pyinstaller == 5.6.2
subprocess.run('pyarmor pack -e "--noconsole --onefile --exclude numpy --exclude pandas --icon=build/mincar_data/img/mincar_logo.ico" --clean --name Mincar build/mincar_gui.py')

if os.path.isfile('build/Mincar.exe') : os.remove('build/Mincar.exe')
shutil.copy('build/dist/Mincar.exe', 'build/Mincar.exe')

shutil.rmtree('build/discid')
shutil.rmtree('build/dist')
shutil.rmtree('build/layout')
shutil.rmtree('build/Mincar-patched')
os.remove('build/util.py')
os.remove('build/mincar_gui.py')
os.remove('build/aws_info.py')
os.remove('build/version.py')

general_setting_dict = {
    'themename': 'Light',
    'editkey': '',
    'savefolder': ''
}

with open('build/mincar_data/setting.json', 'w', encoding = 'UTF-8') as file:
    json.dump(general_setting_dict, file, ensure_ascii = False, indent = 4)

print('\nComplete!')