# -*- coding: utf-8 -*-

# Mincar
# mincar_gui.py
# (C) 2022 Cube
# cubezeero@gmail.com

import global_values as gv

import PySimpleGUI as psg
import boto3
import webbrowser
import json
import sys

import aws_info
import software_info
from layout import gui_layout, gui_theme
import menu_icon_list
import util

import function

#---------------------------------------------------------------------------------
# System init
#---------------------------------------------------------------------------------

gv.icon_path_list = menu_icon_list.list()
gv.icon_io_list = []

with open('mincar_data/setting.json', encoding = 'UTF-8') as file : gv.general_setting_dict = json.load(file)

psg.LOOK_AND_FEEL_TABLE['theme'] = gui_theme.white(psg) if gv.general_setting_dict['themename'] == 'Light' else gui_theme.dark(psg)
gui_theme.theme_changer(psg.LOOK_AND_FEEL_TABLE['theme']['colorname'])
psg.theme('theme')

aws_s3_client = boto3.client('s3', aws_access_key_id = aws_info.ACCESS_KEY(), aws_secret_access_key = aws_info.SECRET_ACCESS_KEY(), region_name = aws_info.REGION_NAME())

if bool(gv.general_setting_dict['start_update_check']):
    update_check_res = util.update_check_start(aws_s3_client)
    if 0 != update_check_res[0]:
        psg.popup_ok('現在のMincarのバージョンはデータベースの仕様変更により利用できません。\nお手数ですが最新バージョンへの更新をお願い致します。', title = software_info.Software_Name_All(), icon = software_info.Icon_Path(), modal = True, keep_on_top = True)
        webbrowser.open(update_check_res[1])
        sys.exit()

#---------------------------------------------------------------------------------
# GUI Window
#---------------------------------------------------------------------------------

home_window = gui_layout.lo_home_window(gv.icon_io_list, gv.menu_button_bgcolor)

while True:
    home_event, home_values = home_window.read()

    if home_event == psg.WIN_CLOSED : break

    if home_event == '-htu_btn-' : webbrowser.open('https://cubezeero.notion.site/cubezeero/Mincar-fa40bb8295074f67b9b6f8ffde1313e7')

    if home_event == '-menu_upload_btn-'      : function.function_upload(aws_s3_client, gui_layout)
    if home_event == '-menu_download_btn-'    : function.function_download(aws_s3_client, gui_layout)
    if home_event == '-menu_edit_btn-'        : function.function_edit(aws_s3_client, gui_layout)
    if home_event == '-menu_detail_btn-'      : function.function_discdetail(gui_layout)
    if home_event == '-menu_editkeyloss_btn-' : function.function_editkeylost(aws_s3_client, gui_layout)
    if home_event == '-menu_setting_btn-'     : function.function_setting(aws_s3_client, gui_layout)

home_window.close()