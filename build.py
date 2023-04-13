# -*- coding: utf-8 -*-

import os
import shutil
import subprocess
import json

from src import software_info 

version = software_info.Version_Name()

print('Pack for distribution? [y/n]')
while True:
    pack_yn = input('Enter: ')
    if pack_yn == 'y' or  pack_yn == 'n' : break

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
shutil.rmtree('build/function')
shutil.rmtree('build/util')
os.remove('build/mincar_gui.py')
os.remove('build/aws_info.py')
os.remove('build/aws_info_sample.py')
os.remove('build/software_info.py')
os.remove('build/software_info_sample.py')
os.remove('build/muuid.py')
os.remove('build/menu_icon_list.py')
os.remove('build/global_values.py')

shutil.rmtree('build/__pycache__')

general_setting_dict = {
    'themename': 'Light',
    'editkey': '',
    'savefolder': '',
    'start_update_check': 1
}

with open('build/mincar_data/setting.json', 'w', encoding = 'UTF-8') as file : json.dump(general_setting_dict, file, ensure_ascii = False, indent = 4)

with open('build/Readme.txt', encoding = 'UTF-8') as rm_reader : rm_text = rm_reader.read().replace(r'{version}', version)
with open('build/Readme.txt', 'w', encoding = 'UTF-8') as rm_writer : rm_writer.write(rm_text)

if pack_yn == 'y':
    if os.path.isdir('dist/Mincar_' + version) : shutil.rmtree('dist/Mincar_' + version)
    if os.path.isfile('dist/Mincar_' + version + '.zip') : os.remove('dist/Mincar_' + version + '.zip')
    shutil.copytree('build', 'dist/Mincar_' + version)
    shutil.make_archive('dist/Mincar_' + version, 'zip', root_dir = 'dist/Mincar_' + version)

print('\nComplete!')