# -*- coding: utf-8 -*-

# Mincar
# update_util.py
# (C) 2022 Cube
# cubezeero@gmail.com

import PySimpleGUI as psg
import json
import webbrowser
from packaging.version import parse

import sys
sys.path.append('../')
import aws_info
import software_info

def update_msg(update_info_all):

    update_msg = 'Mincarの新しいバージョンが利用可能です\n\n現在のバージョン: v' + software_info.Version_Name() + '\n最新バージョン: v' + update_info_all + '\n\n最新バージョンをダウンロードしますか？'
    return update_msg

def update_check_start(aws_s3_client):

    aws_s3_response = aws_s3_client.get_object(Bucket = aws_info.BUCKET_NAME(), Key = '00_latest_software_vesion/latest_version.db')
    update_info = json.loads(aws_s3_response["Body"].read())

    if parse(update_info['version']) > parse(software_info.Version_Name_List()[0]):
        update_info_all = update_info['version'] + update_info['version_space'] + update_info['version_prerelease']
        if psg.popup_yes_no(update_msg(update_info_all), title = software_info.Software_Name_All(), icon = software_info.Icon_Path(), modal = True, keep_on_top = True) == 'Yes':
            webbrowser.open(update_info['url'])
    
    return

def update_check_setting(aws_s3_client):

    aws_s3_response = aws_s3_client.get_object(Bucket = aws_info.BUCKET_NAME(), Key = '00_latest_software_vesion/latest_version.db')
    update_info = json.loads(aws_s3_response["Body"].read())

    if parse(update_info['version']) > parse(software_info.Version_Name_List()[0]):
        update_info_all = update_info['version'] + update_info['version_space'] + update_info['version_prerelease']
        if psg.popup_yes_no(update_msg(update_info_all), title = software_info.Software_Name_All(), icon = software_info.Icon_Path(), modal = True, keep_on_top = True) == 'Yes':
            webbrowser.open(update_info['url'])
    
    else:
        psg.popup_ok('お使いのMincarは最新バージョンです', title = software_info.Software_Name_All(), icon = software_info.Icon_Path(), modal = True, keep_on_top = True)
    
    return

