# -*- coding: utf-8 -*-

# Mincar
# upload.py
# (C) 2022 Cube
# cubezeero@gmail.com

import PySimpleGUI as psg
import pyperclip
from PIL import Image
import os
import json

import sys
sys.path.append('../')
import muuid
import aws_info
import software_info
import discid
import global_values as gv
import util

def function_upload(aws_s3_client, gui_layout):

    coverart_path = ''
    title_list = []
    coverart_type_list = []
    title_name = ''

    prefix_discid_dir = "discid_dir"

    if muuid.check_mbl(muuid.get_muuid(), aws_s3_client, aws_info.BUCKET_NAME()):
        psg.popup_ok('サーバ側からブロックされました', title = software_info.Software_Name_All(), icon = software_info.Icon_Path(), modal = True, keep_on_top = True)
        return
    
    aws_s3_response = aws_s3_client.get_object(Bucket = aws_info.BUCKET_NAME(), Key = '03_maintenance/maintenance_info.db')
    maintenance_info = json.loads(aws_s3_response["Body"].read())

    if maintenance_info['maintenance'] == 1:
        psg.popup_ok(maintenance_info['info_massage'], title = software_info.Software_Name_All(), icon = software_info.Icon_Path(), modal = True, keep_on_top = True)
        return

    psg.popup_ok('カバーアートの登録は著作権者(作曲者)本人による登録を推奨します\n\nまた本データベースは「同人音楽作品」専用です\nメジャー作品などの一般流通作品の登録はお控えください', title = software_info.Software_Name_All(), icon = software_info.Icon_Path(), modal = True, keep_on_top = True)

    try:
        current_disc_info = discid.read()
    
    except discid.DiscError:
        psg.popup_ok('ディスクの読み込み時にエラーが発生しました\nディスク本体が挿入されているか確認してください', title = software_info.Software_Name_All(), icon = software_info.Icon_Path(), modal = True, keep_on_top = True)
        return
    
    aws_s3_response = aws_s3_client.list_objects_v2(Bucket = aws_info.BUCKET_NAME(), Prefix = prefix_discid_dir + "/" + current_disc_info.id + '/')
    
    # DiscIDと一致したタイトルの取得
    if "Contents" in aws_s3_response:
        for aws_s3_obj in aws_s3_response['Contents']:
            if aws_s3_obj['Key'].split('/')[2] not in title_list:
                title_list.append(aws_s3_obj['Key'].split('/')[2])
        

        #---------------------------------------------------------------------------------
        # Upload TitleList Window
        #---------------------------------------------------------------------------------


        upload_dl_window = gui_layout.lo_upload_disclist_window(title_list)

        while True:
            upload_dl_event, upload_dl_values = upload_dl_window.read()
            
            if upload_dl_event == psg.WIN_CLOSED or upload_dl_event == '-cancel_btn-':
                upload_dl_window.close()
                return

            if upload_dl_event == '-identical_btn-':
                title_name = upload_dl_values['-listbox_titlename-'][0]
                break
            
            if upload_dl_event == '-other_btn-' : break
        
        upload_dl_window.close()

    # カバーアートタイプの取得
    if "Contents" in aws_s3_response:
        for aws_s3_obj in aws_s3_response['Contents']:
            if aws_s3_obj['Key'].split('/')[2] == title_name : coverart_type_list.append(aws_s3_obj['Key'].split('/')[3].split('.')[0])


    #---------------------------------------------------------------------------------
    # Upload Main Window
    #---------------------------------------------------------------------------------


    upload_window = gui_layout.lo_upload_window(current_disc_info.id, current_disc_info.last_track_num, title_name, gv.input_disabled_color, gv.default_ca, gv.general_setting_dict['editkey'])

    while True:
        upload_event, upload_values = upload_window.read()
                
        if upload_event == psg.WIN_CLOSED or upload_event == '-cancel_btn-' : break

        if upload_event == '-copy_discid-' : pyperclip.copy(current_disc_info.id)

        if upload_event == '-upload_coverart-':

            disctitle_sp = title_name if title_name else upload_values['-disctitle_input-']

            # 各項目の入力漏れ等のチェック
            if disctitle_sp == '' or upload_values['-coverartname_input-'] == '' or upload_values['-editkey_input-'] == '' or upload_values['-disctitle_input-'] == '':
                psg.popup_ok('未入力の項目があります', title = software_info.Software_Name_All(), icon = software_info.Icon_Path(), modal = True, keep_on_top = True)
            
            elif '/' in disctitle_sp or '/' in upload_values['-coverartname_input-'] or '/' in upload_values['-editkey_input-']:
                psg.popup_ok('ディスクのタイトルやカバーアートのタイプ、編集用キーに「/」を使用することは出来ません', title = software_info.Software_Name_All(), icon = software_info.Icon_Path(), modal = True, keep_on_top = True)
            
            elif '.' in upload_values['-coverartname_input-']:
                psg.popup_ok('カバーアートのタイプと「.」を使用することは出来ません', title = software_info.Software_Name_All(), icon = software_info.Icon_Path(), modal = True, keep_on_top = True)

            elif coverart_path == '':
                psg.popup_ok('カバーアートが選択されていません', title = software_info.Software_Name_All(), icon = software_info.Icon_Path(), modal = True, keep_on_top = True)

            elif upload_values['-coverartname_input-'] in coverart_type_list and title_name:
                psg.popup_ok('そのカバーアートのタイプはすでに登録されています', title = software_info.Software_Name_All(), icon = software_info.Icon_Path(), modal = True, keep_on_top = True)

            elif disctitle_sp in title_list and (not title_name):
                psg.popup_ok('そのディスクのタイトルはすでに登録されています', title = software_info.Software_Name_All(), icon = software_info.Icon_Path(), modal = True, keep_on_top = True)
            
            else:
                if psg.popup_yes_no('このカバーアートを登録しますか？', title = software_info.Software_Name_All(), icon = software_info.Icon_Path(), modal = True, keep_on_top = True) == 'Yes':
                    registration_data_name = prefix_discid_dir + "/" + current_disc_info.id + '/' + disctitle_sp + '/' + upload_values['-coverartname_input-'] + '.jpg'
                    aws_s3_client.upload_file(coverart_path, aws_info.BUCKET_NAME(), registration_data_name, ExtraArgs = {"Metadata":{"edit-key": upload_values['-editkey_input-'], "mgun": muuid.get_mgun(), "muuid": muuid.get_muuid()}})

                    psg.popup_ok('カバーアートの登録が完了しました', title = software_info.Software_Name_All(), icon = software_info.Icon_Path(), modal = True, keep_on_top = True)

                    break

        if upload_event == '-load_coverart-':

            coverart_path = psg.popup_get_file(message = 'none', title = 'none', no_window = True, multiple_files = False, file_types = (('Jpeg Image File', '.jpg'),), modal = True)

            if coverart_path != '':

                get_size_im = Image.open(coverart_path)

                if get_size_im.size[0] > 2048 or get_size_im.size[1] > 2048:
                    psg.popup_ok('画像サイズの上限を超えています\n2048x2048が最大サイズです', title = software_info.Software_Name_All(), icon = software_info.Icon_Path(), modal = True, keep_on_top = True)

                elif int(os.path.getsize(coverart_path)) > 5242880:
                    psg.popup_ok('ファイルサイズの上限を超えています\n5MBが最大ファイルサイズです', title = software_info.Software_Name_All(), icon = software_info.Icon_Path(), modal = True, keep_on_top = True)

                else:
                    ca_image_obj = util.keepAspectResizeToIo(coverart_path, (256,256))
                    upload_window['-coverart_data_key-'].update(data = ca_image_obj)
            
    upload_window.close()