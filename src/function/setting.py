# -*- coding: utf-8 -*-

# Mincar
# setting.py
# (C) 2022 Cube
# cubezeero@gmail.com

import PySimpleGUI as psg
import json
import webbrowser
from packaging.version import Version, parse

import sys
sys.path.append('../')
import software_info
import util
import global_values as gv

def function_setting(aws_s3_client, gui_layout, general_setting_dict):

    setting_menu_list = ['一般', '情報']
    setting_theme_list = ['Light', 'Dark']
    library_list = 'boto3,pysimplegui,libdiscid,python-discid,pyperclip,pillow'

    setting_window = gui_layout.lo_setting_window(software_info.Software_Name(), software_info.Version_Name(), setting_menu_list, library_list, setting_theme_list, general_setting_dict)

    while True:
        setting_event, setting_values = setting_window.read()

        if setting_event == psg.WIN_CLOSED or setting_event == '-cancel_btn-' : break
            
        if setting_event == '-listbox_menu-':
            for menuname in setting_menu_list:
                if setting_values['-listbox_menu-'][0] == menuname:
                    setting_window[menuname].update(visible = True)
                else:
                    setting_window[menuname].update(visible = False)

        if setting_event == '-get_folder_btn-':
            coverart_path = psg.popup_get_folder(message = 'none', title = 'none', no_window = True, modal = True)

            if coverart_path != '' : setting_window['-get_folder_input-'].update(value = coverart_path)
            
        if setting_event == '-homepage-':
            webbrowser.open('https://github.com/CubeZeero/Mincar')
        
        if setting_event == '-update_check_btn-':
            util.update_check_setting(aws_s3_client)
        
        if setting_event == '-ok_btn-':
            gs_theme_name = setting_values['-theme_combo-']
            gs_default_editkey = setting_values['-default_editkey_input-']
            gs_default_savefolder = setting_values['-get_folder_input-']
            gs_startupdate_check = int(setting_values['-start_update_check-'])

            general_setting_dict = {
                'themename': gs_theme_name,
                'editkey': gs_default_editkey,
                'savefolder': gs_default_savefolder,
                'start_update_check': gs_startupdate_check
            }

            gv.general_setting_dict = general_setting_dict

            with open('mincar_data/setting.json', 'w', encoding = 'UTF-8') as file:
                json.dump(general_setting_dict, file, ensure_ascii = False, indent = 4)

            break

    setting_window.close()