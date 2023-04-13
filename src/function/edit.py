# -*- coding: utf-8 -*-

# Mincar
# edit.py
# (C) 2022 Cube
# cubezeero@gmail.com

import PySimpleGUI as psg
from PIL import Image
import os
import io
import json

import sys
sys.path.append('../')
import muuid
import aws_info
import software_info
import discid
import global_values as gv
import util

def function_edit(aws_s3_client, gui_layout):

    disc_id = ''
    coverart_download_list = []
    coverart_download_bytedata = []
    coverart_download_bytedata_rs = []
    coverart_type_list = []
    title_list = []
    title_name = ''
    current_coverart_index = 0

    prefix_discid_dir = "discid_dir"

    if muuid.check_mbl(muuid.get_muuid(), aws_s3_client, aws_info.BUCKET_NAME()):
        psg.popup_ok('サーバ側からブロックされました', title = software_info.Software_Name_All(), icon = software_info.Icon_Path(), modal = True, keep_on_top = True)
        return
    
    aws_s3_response = aws_s3_client.get_object(Bucket = aws_info.BUCKET_NAME(), Key = '03_maintenance/maintenance_info.db')
    maintenance_info = json.loads(aws_s3_response["Body"].read())

    if maintenance_info['maintenance'] == 1:
        psg.popup_ok(maintenance_info['info_massage'], title = software_info.Software_Name_All(), icon = software_info.Icon_Path(), modal = True, keep_on_top = True)
        return

    #---------------------------------------------------------------------------------
    # Edit DiscID Search Window
    #---------------------------------------------------------------------------------


    edit_select_window = gui_layout.lo_edit_select_window()

    while True:
        edit_select_event, edit_select_values = edit_select_window.read()
                        
        if edit_select_event == psg.WIN_CLOSED or edit_select_event == '-cancel_btn-':
            edit_select_window.close()
            return
                    
        if edit_select_event == '-ok_discid_btn-':
            if edit_select_values['-discid_input-'] != '':
                disc_id = edit_select_values['-discid_input-']
                break
            
            else:
                psg.popup_ok('DiscIDを入力してください', title = software_info.Software_Name_All(), icon = software_info.Icon_Path(), modal = True, keep_on_top = True)
        
        if edit_select_event == '-ok_disc_btn-':
            try:
                current_disc_info = discid.read()
                disc_id = current_disc_info.id
                break

            except discid.DiscError:
                psg.popup_ok('ディスクの読み込み時にエラーが発生しました\nディスク本体が挿入されているか確認してください', title = software_info.Software_Name_All(), icon = software_info.Icon_Path(), modal = True, keep_on_top = True)
            
    edit_select_window.close()

    aws_s3_response = aws_s3_client.list_objects_v2(Bucket = aws_info.BUCKET_NAME(), Prefix = prefix_discid_dir + "/" + disc_id + '/')
    
    if "Contents" not in aws_s3_response:
        psg.popup_ok('このディスクのカバーアートはまだ登録されていません', title = software_info.Software_Name_All(), icon = software_info.Icon_Path(), modal = True, keep_on_top = True)
        return

    # DiscIDと一致したタイトルの取得
    for aws_s3_obj in aws_s3_response['Contents']:
        if aws_s3_obj['Key'].split('/')[2] not in title_list:
            title_list.append(aws_s3_obj['Key'].split('/')[2])


    #---------------------------------------------------------------------------------
    # Edit TitleList Window
    #---------------------------------------------------------------------------------


    edit_disclist_window = gui_layout.lo_edit_disclist_window(title_list)

    while True:
        edit_disclist_event, edit_disclist_values = edit_disclist_window.read()
                
        if edit_disclist_event == psg.WIN_CLOSED or edit_disclist_event == '-cancel_btn-':
            edit_disclist_window.close()
            return
            
        elif edit_disclist_event == '-ok_btn-':
            title_name = edit_disclist_values['-listbox_titlename-'][0]
            break
    
    edit_disclist_window.close()


    #---------------------------------------------------------------------------------
    # Edit plzwait Window
    #---------------------------------------------------------------------------------


    edit_pw_window = gui_layout.lo_getca_pw_window()

    while True:
        edit_pw_event, edit_pw_values = edit_pw_window.read(timeout = 100)

        # 各カバーアートのダウンロード
        for aws_s3_obj in aws_s3_response['Contents']:
            if aws_s3_obj['Key'].split('/')[2] == title_name:
                coverart_download_list.append(aws_s3_obj['Key'])
                coverart_download_bytedata.append(io.BytesIO(aws_s3_client.get_object(Bucket = aws_info.BUCKET_NAME(), Key = aws_s3_obj['Key'])['Body'].read()))
                coverart_download_bytedata_rs.append(util.keepAspectResizeToIo(coverart_download_bytedata[-1], (200,200)))
                coverart_type_list.append(aws_s3_obj['Key'].split('/')[3].split('.')[0])
        
        break

    edit_pw_window.close()


    #---------------------------------------------------------------------------------
    # Edit Main Window
    #---------------------------------------------------------------------------------


    edit_window = gui_layout.lo_edit_window(coverart_type_list, coverart_download_bytedata_rs, gv.general_setting_dict['editkey'])

    while True:
        edit_event, edit_values = edit_window.read()

        if edit_event == psg.WIN_CLOSED or edit_event == '-cancel_btn-' : break
        
        # カバーアートプレビューの切り替え
        if edit_event == '-coverarttype_list-':
            current_coverart_index = int(coverart_type_list.index(edit_values['-coverarttype_list-'][0]))
            edit_window['-coverart_data_key-'].update(data = coverart_download_bytedata_rs[current_coverart_index])
        
        if edit_event == '-delete_btn-':
            if psg.popup_yes_no('このカバーアートを削除しますか？', title = software_info.Software_Name_All(), icon = software_info.Icon_Path(), modal = True, keep_on_top = True) == 'Yes':
                
                current_coverart_index = int(coverart_type_list.index(edit_values['-coverarttype_list-'][0]))
                object_editkey = aws_s3_client.head_object(Bucket = aws_info.BUCKET_NAME(), Key = coverart_download_list[current_coverart_index])['Metadata']['edit-key']

                if object_editkey == edit_values['-editkey_input-']:
                    current_coverart_index = int(coverart_type_list.index(edit_values['-coverarttype_list-'][0]))
                    aws_s3_client.delete_object(Bucket = aws_info.BUCKET_NAME(), Key = coverart_download_list[current_coverart_index])

                    psg.popup_ok('カバーアートを削除しました', title = software_info.Software_Name_All(), icon = software_info.Icon_Path(), modal = True, keep_on_top = True)

                    del coverart_type_list[current_coverart_index]
                    del coverart_download_list[current_coverart_index]
                    del coverart_download_bytedata[current_coverart_index]
                    del coverart_download_bytedata_rs[current_coverart_index]

                    if not coverart_type_list : break

                    edit_window['-coverarttype_list-'].update(values = coverart_type_list, set_to_index = 0)
                    edit_window['-coverart_data_key-'].update(data = coverart_download_bytedata_rs[0])
                
                else:
                    psg.popup_ok('編集キーが違います', title = software_info.Software_Name_All(), icon = software_info.Icon_Path(), modal = True, keep_on_top = True)
        
        if edit_event == '-load_coverart-':

            coverart_path = psg.popup_get_file(message = 'none', title = 'none', no_window = True, multiple_files = False, file_types = (('Jpeg Image File', '.jpg'),), modal = True)

            if coverart_path != '':

                get_size_im = Image.open(coverart_path)

                if get_size_im.size[0] > 2048 or get_size_im.size[1] > 2048:
                    psg.popup_ok('画像サイズの上限を超えています\n2048x2048が最大サイズです', title = software_info.Software_Name_All(), icon = software_info.Icon_Path(), modal = True, keep_on_top = True)

                elif int(os.path.getsize(coverart_path)) > 5242880:
                    psg.popup_ok('ファイルサイズの上限を超えています\n5MBが最大ファイルサイズです', title = software_info.Software_Name_All(), icon = software_info.Icon_Path(), modal = True, keep_on_top = True)

                else:
                    if psg.popup_yes_no('このカバーアートを更新しますか？', title = software_info.Software_Name_All(), icon = software_info.Icon_Path(), modal = True, keep_on_top = True) == 'Yes':

                        current_coverart_index = int(coverart_type_list.index(edit_values['-coverarttype_list-'][0]))
                        object_editkey = aws_s3_client.head_object(Bucket = aws_info.BUCKET_NAME(), Key = coverart_download_list[current_coverart_index])['Metadata']['edit-key']

                        if object_editkey == edit_values['-editkey_input-']:

                            coverart_download_bytedata_rs[current_coverart_index] = util.keepAspectResizeToIo(coverart_path, (200,200))
                            aws_s3_client.upload_file(coverart_path, aws_info.BUCKET_NAME(), coverart_download_list[current_coverart_index], ExtraArgs = {"Metadata":{"edit-key": object_editkey, "mgun": muuid.get_mgun(), "muuid": muuid.get_muuid()}})

                            edit_window['-coverart_data_key-'].update(data = coverart_download_bytedata_rs[current_coverart_index])

                            psg.popup_ok('カバーアートを更新しました', title = software_info.Software_Name_All(), icon = software_info.Icon_Path(), modal = True, keep_on_top = True)
                        
                        else:
                            psg.popup_ok('編集キーが違います', title = software_info.Software_Name_All(), icon = software_info.Icon_Path(), modal = True, keep_on_top = True)
    
    edit_window.close()
    return