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
import aws_info
import global_values as gv
import util

def function_setting(aws_s3_client, gui_layout):

    setting_menu_list = ['一般', '情報']
    setting_theme_list = ['Light', 'Dark']
    library_list = 'boto3,pysimplegui,libdiscid,python-discid,pyperclip,pillow'

    setting_window = gui_layout.lo_setting_window(software_info.Software_Name(), software_info.Version_Name(), setting_menu_list, library_list, setting_theme_list, gv.general_setting_dict)

    while True:
        setting_event, setting_values = setting_window.read()

        if setting_event == psg.WIN_CLOSED or setting_event == '-cancel_btn-' : break
            
        if setting_event == '-listbox_menu-':
            for menuname in setting_menu_list:
                if setting_values['-listbox_menu-'][0] == menuname : setting_window[menuname].update(visible = True)
                else : setting_window[menuname].update(visible = False)

        if setting_event == '-get_folder_btn-':
            coverart_path = psg.popup_get_folder(message = 'none', title = 'none', no_window = True, modal = True)
            if coverart_path != '' : setting_window['-get_folder_input-'].update(value = coverart_path)
            
        if setting_event == '-homepage-' : webbrowser.open('https://github.com/CubeZeero/Mincar')
        
        if setting_event == '-update_check_btn-':
            aws_s3_response = aws_s3_client.get_object(Bucket = aws_info.BUCKET_NAME(), Key = '00_latest_software_vesion/latest_version.db')
            update_info = json.loads(aws_s3_response["Body"].read())

            if parse(update_info['version']) > parse(software_info.Version_Name_List()[0]):
                update_info_all = update_info['version'] + update_info['version_space'] + update_info['version_prerelease']
                if psg.popup_yes_no(util.update_msg(update_info_all), title = software_info.Software_Name_All(), icon = software_info.Icon_Path(), modal = True, keep_on_top = True) == 'Yes' : webbrowser.open(update_info['url'])
            
            else:
                psg.popup_ok('お使いのMincarは最新バージョンです', title = software_info.Software_Name_All(), icon = software_info.Icon_Path(), modal = True, keep_on_top = True)
        
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
    return