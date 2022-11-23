# -*- coding: utf-8 -*-

# Mincar
# mincar_gui.py
# (C) 2022 Cube
# cubezeero@gmail.com

#---------------------------------------------------------------------------------

# Library

#---------------------------------------------------------------------------------

import PySimpleGUI as psg
import boto3
import discid
import pyperclip
from PIL import Image, ImageOps
import io
import re
import os
import datetime
import webbrowser
import json
from packaging.version import Version, parse

import aws_info
import version
from layout import gui_layout, gui_theme
import util
import mgun

#---------------------------------------------------------------------------------

# System init

#---------------------------------------------------------------------------------

aws_info_ak = aws_info.ACCESS_KEY()
aws_info_sak = aws_info.SECRET_ACCESS_KEY()
aws_info_rn = aws_info.REGION_NAME()
aws_info_bn = aws_info.BUCKET_NAME()

aws_s3_client = boto3.client('s3', aws_access_key_id = aws_info_ak, aws_secret_access_key = aws_info_sak, region_name = aws_info_rn)

software_version = version.VERSION()
window_title_raw = 'Mincar'
version_all = software_version[0] + software_version[1] + software_version[2]
window_title = 'Mincar v' + version_all

icon_path = 'mincar_data/img/mincar_logo.ico'

with open('mincar_data/setting.json', encoding = 'UTF-8') as file:
    general_setting_dict = json.load(file)

gs_theme_name = general_setting_dict['themename']
gs_default_editkey = general_setting_dict['editkey']
gs_default_savefolder = general_setting_dict['savefolder']
gs_startupdate_check = bool(general_setting_dict['start_update_check'])

psg.LOOK_AND_FEEL_TABLE['theme'] = gui_theme.white(psg) if gs_theme_name == 'Light' else gui_theme.dark(psg)

psg.theme('theme')

icon_path_list = ['mincar_data/img/button_icon/button_icon_upload.png',
                  'mincar_data/img/button_icon/button_icon_download.png',
                  'mincar_data/img/button_icon/button_icon_edit.png',
                  'mincar_data/img/button_icon/button_icon_detail.png',
                  'mincar_data/img/button_icon/button_icon_editkeyloss.png',
                  'mincar_data/img/button_icon/button_icon_setting.png']

icon_io_list = []

if psg.LOOK_AND_FEEL_TABLE['theme']['colorname'] == 'white':
    menu_button_bgcolor = '#ffffff'
    input_disabled_color = '#eeeeee'

    default_ca = util.imageToIo(Image, io, 'mincar_data/img/default_coverart.png')
    for iconpath in icon_path_list:
        icon_io_list.append(util.imageToIo(Image, io, iconpath))

else:
    menu_button_bgcolor = '#222222'
    input_disabled_color = '#1e1e1e'

    default_ca = util.imageInvertColor(Image, ImageOps, io, 'mincar_data/img/default_coverart.png')
    for iconpath in icon_path_list:
        icon_io_list.append(util.imageInvertColor(Image, ImageOps, io, iconpath))

window_layout = gui_layout.window_layout(psg, window_title, icon_path)

if gs_startupdate_check:
    aws_s3_response = aws_s3_client.get_object(Bucket = aws_info_bn, Key = '00_latest_software_vesion/latest_version.db')
    update_info = json.loads(aws_s3_response["Body"].read())

    if parse(update_info['version']) > parse(software_version[0]):
        update_info_all = update_info['version'] + update_info['version_space'] + update_info['version_prerelease']
        if psg.popup_yes_no('Mincarの新しいバージョンが利用可能です\n\n現在のバージョン: v' + version_all + '\n最新バージョン: v' + update_info_all + '\n\n最新バージョンをダウンロードしますか？', title = window_title, icon = icon_path, modal = True, keep_on_top = True) == 'Yes':
            webbrowser.open(update_info['url'])

#---------------------------------------------------------------------------------

# Home Window

#---------------------------------------------------------------------------------

home_window = window_layout.lo_home_window(icon_io_list, menu_button_bgcolor, window_title_raw)

while True:
    home_event, home_values = home_window.read()

    if home_event == psg.WIN_CLOSED : break

    if home_event == '-htu_btn-' : webbrowser.open('https://cubezeero.notion.site/cubezeero/Mincar-fa40bb8295074f67b9b6f8ffde1313e7')


    #---------------------------------------------------------------------------------

    # Upload Window

    #---------------------------------------------------------------------------------


    if home_event == '-menu_upload_btn-':
        coverart_path = ''
        title_list = []
        coverart_type_list = []
        title_name = ''

        cancel_sw = 0

        psg.popup_ok('カバーアートの登録は著作権者(作曲者)本人による登録を推奨します\n\nまた本データベースは「同人音楽作品」専用です\nメジャー作品などの一般流通作品の登録はお控えください', title = window_title, icon = icon_path, modal = True, keep_on_top = True)

        try:
            current_disc_info = discid.read()

            aws_s3_response = aws_s3_client.list_objects_v2(Bucket = aws_info_bn, Prefix = current_disc_info.id + '/')
            
            # DiscIDと一致したタイトルの取得
            if "Contents" in aws_s3_response:
                for aws_s3_obj in aws_s3_response['Contents']:
                    if aws_s3_obj['Key'].split('/')[1] not in title_list:
                        title_list.append(aws_s3_obj['Key'].split('/')[1])
                

                #---------------------------------------------------------------------------------
                # Upload TitleList Window
                #---------------------------------------------------------------------------------


                upload_dl_window = window_layout.lo_upload_disclist_window(title_list)

                while True:
                    upload_dl_event, upload_dl_values = upload_dl_window.read()
                    
                    if upload_dl_event == psg.WIN_CLOSED or upload_dl_event == '-cancel_btn-':
                        cancel_sw = 1
                        break

                    if upload_dl_event == '-identical_btn-':
                        title_name = upload_dl_values['-listbox_titlename-'][0]
                        break
                    
                    if upload_dl_event == '-other_btn-' : break
                
                upload_dl_window.close()

            if cancel_sw == 0:

                # DiscIDが存在する場合のみ一致したタイトルの取得
                if "Contents" in aws_s3_response:
                    for aws_s3_obj in aws_s3_response['Contents']:
                        if aws_s3_obj['Key'].split('/')[1] == title_name:
                            coverart_type_list.append(aws_s3_obj['Key'].split('/')[2].split('.')[0])


                #---------------------------------------------------------------------------------
                # Upload Main Window
                #---------------------------------------------------------------------------------


                upload_window = window_layout.lo_upload_window(current_disc_info.id, current_disc_info.last_track_num, title_name, input_disabled_color, default_ca, gs_default_editkey)

                while True:
                    upload_event, upload_values = upload_window.read()
                            
                    if upload_event == psg.WIN_CLOSED or upload_event == '-cancel_btn-' : break

                    if upload_event == '-copy_discid-' : pyperclip.copy(current_disc_info.id)

                    if upload_event == '-upload_coverart-':

                        disctitle_sp = title_name if title_name else upload_values['-disctitle_input-']

                        # 各項目の入力漏れ等のチェック
                        if disctitle_sp == '' or upload_values['-coverartname_input-'] == '' or upload_values['-editkey_input-'] == '' or upload_values['-disctitle_input-'] == '':
                            psg.popup_ok('未入力の項目があります', title = window_title, icon = icon_path, modal = True, keep_on_top = True)
                        
                        elif '/' in disctitle_sp or '/' in upload_values['-coverartname_input-'] or '/' in upload_values['-editkey_input-']:
                            psg.popup_ok('ディスクのタイトルやカバーアートのタイプ、編集用キーに「/」を使用することは出来ません', title = window_title, icon = icon_path, modal = True, keep_on_top = True)
                        
                        elif '.' in upload_values['-coverartname_input-']:
                            psg.popup_ok('カバーアートのタイプと「.」を使用することは出来ません', title = window_title, icon = icon_path, modal = True, keep_on_top = True)

                        elif coverart_path == '':
                            psg.popup_ok('カバーアートが選択されていません', title = window_title, icon = icon_path, modal = True, keep_on_top = True)

                        elif upload_values['-coverartname_input-'] in coverart_type_list and title_name:
                            psg.popup_ok('そのカバーアートのタイプはすでに登録されています', title = window_title, icon = icon_path, modal = True, keep_on_top = True)

                        elif disctitle_sp in title_list and (not title_name):
                            psg.popup_ok('そのディスクのタイトルはすでに登録されています', title = window_title, icon = icon_path, modal = True, keep_on_top = True)
                        
                        else:
                            if psg.popup_yes_no('このカバーアートを登録しますか？', title = window_title, icon = icon_path, modal = True, keep_on_top = True) == 'Yes':
                                registration_data_name = current_disc_info.id + '/' + disctitle_sp + '/' + upload_values['-coverartname_input-'] + '.jpg'
                                aws_s3_client.upload_file(coverart_path, aws_info_bn, registration_data_name, ExtraArgs = {"Metadata":{"edit-key": upload_values['-editkey_input-'], "mgun": mgun.mgun()}})

                                psg.popup_ok('カバーアートの登録が完了しました', title = window_title, icon = icon_path, modal = True, keep_on_top = True)

                                break

                    if upload_event == '-load_coverart-':

                        coverart_path = psg.popup_get_file(message = 'none', title = 'none', no_window = True, multiple_files = False, file_types = (('Jpeg Image File', '.jpg'),), modal = True)

                        if coverart_path != '':

                            get_size_im = Image.open(coverart_path)

                            if get_size_im.size[0] > 2048 or get_size_im.size[1] > 2048:
                                psg.popup_ok('画像サイズの上限を超えています\n2048x2048が最大サイズです', title = window_title, icon = icon_path, modal = True, keep_on_top = True)

                            elif int(os.path.getsize(coverart_path)) > 5242880:
                                psg.popup_ok('ファイルサイズの上限を超えています\n5MBが最大ファイルサイズです', title = window_title, icon = icon_path, modal = True, keep_on_top = True)

                            else:
                                ca_image_obj = util.keepAspectResizeToIo(Image, io, coverart_path, (256,256))
                                upload_window['-coverart_data_key-'].update(data = ca_image_obj)
                        
                upload_window.close()

        except discid.DiscError:
            psg.popup_ok('ディスクの読み込み時にエラーが発生しました\nディスク本体が挿入されているか確認してください', title = window_title, icon = icon_path, modal = True, keep_on_top = True)


    #---------------------------------------------------------------------------------

    # Download Window

    #---------------------------------------------------------------------------------


    if home_event == '-menu_download_btn-':
        disc_id = ''
        coverart_download_list = []
        coverart_download_bytedata = []
        coverart_download_bytedata_rs = []
        coverart_type_list = []
        title_list = []
        title_name = ''
        current_coverart_index = 0
        cancel_sw = 0


        #---------------------------------------------------------------------------------
        # Download DiscID Search Window
        #---------------------------------------------------------------------------------


        download_select_window = window_layout.lo_download_select_window()

        while True:
            download_select_event, download_select_values = download_select_window.read()
                            
            if download_select_event == psg.WIN_CLOSED or download_select_event == '-cancel_btn-':
                cancel_sw = 1
                break
                        
            if download_select_event == '-ok_discid_btn-':
                if download_select_values['-discid_input-'] != '':
                    disc_id = download_select_values['-discid_input-']
                    break
                
                else:
                    psg.popup_ok('DiscIDを入力してください', title = window_title, icon = icon_path, modal = True, keep_on_top = True)
            
            if download_select_event == '-ok_disc_btn-':
                try:
                    current_disc_info = discid.read()
                    disc_id = current_disc_info.id
                    break

                except discid.DiscError:
                    psg.popup_ok('ディスクの読み込み時にエラーが発生しました\nディスク本体が挿入されているか確認してください', title = window_title, icon = icon_path, modal = True, keep_on_top = True)
                
        download_select_window.close()

        if cancel_sw == 0:

            aws_s3_response = aws_s3_client.list_objects_v2(Bucket = aws_info_bn, Prefix = disc_id + '/')
            
            if "Contents" not in aws_s3_response:
                psg.popup_ok('このディスクのカバーアートはまだ登録されていません', title = window_title, icon = icon_path, modal = True, keep_on_top = True)

            else:
                # DiscIDと一致したタイトルの取得
                for aws_s3_obj in aws_s3_response['Contents']:
                    if aws_s3_obj['Key'].split('/')[1] not in title_list:
                        title_list.append(aws_s3_obj['Key'].split('/')[1])


                #---------------------------------------------------------------------------------
                # Download TitleList Window
                #---------------------------------------------------------------------------------
                

                download_disclist_window = window_layout.lo_download_disclist_window(title_list)

                while True:
                    download_disclist_event, download_disclist_values = download_disclist_window.read()
                            
                    if download_disclist_event == psg.WIN_CLOSED or download_disclist_event == '-cancel_btn-':
                        cancel_sw = 1
                        break
                        
                    elif download_disclist_event == '-ok_btn-':
                        title_name = download_disclist_values['-listbox_titlename-'][0]
                        break
                
                download_disclist_window.close()

                if cancel_sw == 0:


                    #---------------------------------------------------------------------------------
                    # Download plzwait Window
                    #---------------------------------------------------------------------------------


                    download_pw_window = window_layout.lo_getca_pw_window()

                    while True:
                        download_pw_event, download_pw_values = download_pw_window.read(timeout = 100)

                        # 各カバーアートのダウンロード
                        for cnt, aws_s3_obj in enumerate(aws_s3_response['Contents']):
                            if aws_s3_obj['Key'].split('/')[1] == title_name:
                                coverart_download_list.append(aws_s3_obj['Key'])
                                coverart_download_bytedata.append(io.BytesIO(aws_s3_client.get_object(Bucket = aws_info_bn, Key = aws_s3_obj['Key'])['Body'].read()))
                                coverart_download_bytedata_rs.append(util.keepAspectResizeToIo(Image, io, coverart_download_bytedata[-1], (200,200)))
                                coverart_type_list.append(aws_s3_obj['Key'].split('/')[2].split('.')[0])
                        
                        break

                    download_pw_window.close()


                    #---------------------------------------------------------------------------------
                    # Download Main Window
                    #---------------------------------------------------------------------------------
                    

                    download_window = window_layout.lo_download_window(coverart_type_list, coverart_download_bytedata_rs)

                    while True:
                        download_event, download_values = download_window.read()

                        if download_event == psg.WIN_CLOSED or download_event == '-cancel_btn-' : break
                        
                        # カバーアートプレビューの切り替え
                        if download_event == '-coverarttype_list-':
                            current_coverart_index = int(coverart_type_list.index(download_values['-coverarttype_list-'][0]))
                            download_window['-coverart_data_key-'].update(data = coverart_download_bytedata_rs[current_coverart_index])

                        if download_event == '-download_btn-':
                            dl_default_path_raw = title_name + ' - ' + coverart_type_list[current_coverart_index]

                            # Windowsでファイル名に使用できない文字列をアンダーバーへ置き換え
                            dl_default_path = re.sub(r'[\\|/|:|?|"|<|>|\|]', '_', dl_default_path_raw)

                            if os.path.isdir(gs_default_savefolder) == True and gs_default_savefolder != '':
                                with open(gs_default_savefolder + '/' + dl_default_path + '.jpg', mode = 'wb') as save_ca:
                                    save_ca.write(coverart_download_bytedata[current_coverart_index].getvalue())

                                    psg.popup_ok('カバーアートのダウンロードが完了しました', title = window_title, icon = icon_path, modal = True, keep_on_top = True)

                            else:
                                coverart_dl_path = psg.popup_get_file(message = 'none', title = 'none', default_path = dl_default_path, no_window = True, save_as = True, default_extension = '.jpg', multiple_files = False, file_types = (('Jpeg Image File', '.jpg'),), modal = True)
                            
                                if coverart_dl_path != '':

                                    # すでに取得済みのバイトデータを保存
                                    with open(coverart_dl_path, mode = 'wb') as save_ca:
                                        save_ca.write(coverart_download_bytedata[current_coverart_index].getvalue())
                                    
                                    psg.popup_ok('カバーアートのダウンロードが完了しました', title = window_title, icon = icon_path, modal = True, keep_on_top = True)
                    
                    download_window.close()


    #---------------------------------------------------------------------------------

    # Edit Window

    #---------------------------------------------------------------------------------


    if home_event == '-menu_edit_btn-':
        disc_id = ''
        coverart_download_list = []
        coverart_download_bytedata = []
        coverart_download_bytedata_rs = []
        coverart_type_list = []
        title_list = []
        title_name = ''
        current_coverart_index = 0
        cancel_sw = 0


        #---------------------------------------------------------------------------------
        # Edit DiscID Search Window
        #---------------------------------------------------------------------------------


        edit_select_window = window_layout.lo_edit_select_window()

        while True:
            edit_select_event, edit_select_values = edit_select_window.read()
                            
            if edit_select_event == psg.WIN_CLOSED or edit_select_event == '-cancel_btn-':
                cancel_sw = 1
                break
                        
            if edit_select_event == '-ok_discid_btn-':
                if edit_select_values['-discid_input-'] != '':
                    disc_id = edit_select_values['-discid_input-']
                    break
                
                else:
                    psg.popup_ok('DiscIDを入力してください', title = window_title, icon = icon_path, modal = True, keep_on_top = True)
            
            if edit_select_event == '-ok_disc_btn-':
                try:
                    current_disc_info = discid.read()
                    disc_id = current_disc_info.id
                    break

                except discid.DiscError:
                    psg.popup_ok('ディスクの読み込み時にエラーが発生しました\nディスク本体が挿入されているか確認してください', title = window_title, icon = icon_path, modal = True, keep_on_top = True)
                
        edit_select_window.close()

        if cancel_sw == 0:

            aws_s3_response = aws_s3_client.list_objects_v2(Bucket = aws_info_bn, Prefix = disc_id + '/')
            
            if "Contents" not in aws_s3_response:
                psg.popup_ok('このディスクのカバーアートはまだ登録されていません', title = window_title, icon = icon_path, modal = True, keep_on_top = True)
                cancel_sw = 1

            else:
                # DiscIDと一致したタイトルの取得
                for aws_s3_obj in aws_s3_response['Contents']:
                    if aws_s3_obj['Key'].split('/')[1] not in title_list:
                        title_list.append(aws_s3_obj['Key'].split('/')[1])


                #---------------------------------------------------------------------------------
                # Edit TitleList Window
                #---------------------------------------------------------------------------------


                edit_disclist_window = window_layout.lo_edit_disclist_window(title_list)

                while True:
                    edit_disclist_event, edit_disclist_values = edit_disclist_window.read()
                            
                    if edit_disclist_event == psg.WIN_CLOSED or edit_disclist_event == '-cancel_btn-':
                        cancel_sw = 1
                        break
                        
                    elif edit_disclist_event == '-ok_btn-':
                        title_name = edit_disclist_values['-listbox_titlename-'][0]
                        break
                
                edit_disclist_window.close()

            if cancel_sw == 0:


                #---------------------------------------------------------------------------------
                # Edit plzwait Window
                #---------------------------------------------------------------------------------


                edit_pw_window = window_layout.lo_getca_pw_window()

                while True:
                    edit_pw_event, edit_pw_values = edit_pw_window.read(timeout = 100)

                    # 各カバーアートのダウンロード
                    for cnt, aws_s3_obj in enumerate(aws_s3_response['Contents']):
                        if aws_s3_obj['Key'].split('/')[1] == title_name:
                            coverart_download_list.append(aws_s3_obj['Key'])
                            coverart_download_bytedata.append(io.BytesIO(aws_s3_client.get_object(Bucket = aws_info_bn, Key = aws_s3_obj['Key'])['Body'].read()))
                            coverart_download_bytedata_rs.append(util.keepAspectResizeToIo(Image, io, coverart_download_bytedata[-1], (200,200)))
                            coverart_type_list.append(aws_s3_obj['Key'].split('/')[2].split('.')[0])
                    
                    break

                edit_pw_window.close()


                #---------------------------------------------------------------------------------
                # Edit Main Window
                #---------------------------------------------------------------------------------


                edit_window = window_layout.lo_edit_window(coverart_type_list, coverart_download_bytedata_rs, gs_default_editkey)

                while True:
                    edit_event, edit_values = edit_window.read()

                    if edit_event == psg.WIN_CLOSED or edit_event == '-cancel_btn-' : break
                    
                    # カバーアートプレビューの切り替え
                    if edit_event == '-coverarttype_list-':
                        current_coverart_index = int(coverart_type_list.index(edit_values['-coverarttype_list-'][0]))
                        edit_window['-coverart_data_key-'].update(data = coverart_download_bytedata_rs[current_coverart_index])
                    
                    if edit_event == '-delete_btn-':
                        if psg.popup_yes_no('このカバーアートを削除しますか？', title = window_title, icon = icon_path, modal = True, keep_on_top = True) == 'Yes':
                            object_editkey = aws_s3_client.head_object(Bucket = aws_info_bn, Key = coverart_download_list[0])['Metadata']['edit-key']

                            if object_editkey == edit_values['-editkey_input-']:
                                current_coverart_index = int(coverart_type_list.index(edit_values['-coverarttype_list-'][0]))
                                aws_s3_client.delete_object(Bucket = aws_info_bn, Key = coverart_download_list[current_coverart_index])

                                psg.popup_ok('カバーアートを削除しました', title = window_title, icon = icon_path, modal = True, keep_on_top = True)

                                del coverart_type_list[current_coverart_index]
                                del coverart_download_list[current_coverart_index]
                                del coverart_download_bytedata[current_coverart_index]
                                del coverart_download_bytedata_rs[current_coverart_index]

                                if not coverart_type_list : break

                                edit_window['-coverarttype_list-'].update(values = coverart_type_list, set_to_index = 0)
                                edit_window['-coverart_data_key-'].update(data = coverart_download_bytedata_rs[0])
                            
                            else:
                                psg.popup_ok('編集キーが違います', title = window_title, icon = icon_path, modal = True, keep_on_top = True)
                    
                    if edit_event == '-load_coverart-':

                        coverart_path = psg.popup_get_file(message = 'none', title = 'none', no_window = True, multiple_files = False, file_types = (('Jpeg Image File', '.jpg'),), modal = True)

                        if coverart_path != '':

                            get_size_im = Image.open(coverart_path)

                            if get_size_im.size[0] > 2048 or get_size_im.size[1] > 2048:
                                psg.popup_ok('画像サイズの上限を超えています\n2048x2048が最大サイズです', title = window_title, icon = icon_path, modal = True, keep_on_top = True)

                            elif int(os.path.getsize(coverart_path)) > 5242880:
                                psg.popup_ok('ファイルサイズの上限を超えています\n5MBが最大ファイルサイズです', title = window_title, icon = icon_path, modal = True, keep_on_top = True)

                            else:
                                if psg.popup_yes_no('このカバーアートを更新しますか？', title = window_title, icon = icon_path, modal = True, keep_on_top = True) == 'Yes':
                                    object_editkey = aws_s3_client.head_object(Bucket = aws_info_bn, Key = coverart_download_list[0])['Metadata']['edit-key']

                                    if object_editkey == edit_values['-editkey_input-']:
                                        current_coverart_index = int(coverart_type_list.index(edit_values['-coverarttype_list-'][0]))

                                        coverart_download_bytedata_rs[current_coverart_index] = util.keepAspectResizeToIo(Image, io, coverart_path, (200,200))
                                        aws_s3_client.upload_file(coverart_path, aws_info_bn, coverart_download_list[current_coverart_index], ExtraArgs = {"Metadata":{"edit-key": object_editkey}})

                                        edit_window['-coverart_data_key-'].update(data = coverart_download_bytedata_rs[current_coverart_index])

                                        psg.popup_ok('カバーアートを更新しました', title = window_title, icon = icon_path, modal = True, keep_on_top = True)
                                    
                                    else:
                                        psg.popup_ok('編集キーが違います', title = window_title, icon = icon_path, modal = True, keep_on_top = True)
                
                edit_window.close()


    #---------------------------------------------------------------------------------

    # Disc Detail Window

    #---------------------------------------------------------------------------------


    if home_event == '-menu_detail_btn-':

        detail_tabel_header = ['Number', 'Seconds', 'Sectors', 'Length', 'Offset']
        detail_data = []

        try:
            current_disc_info = discid.read()

            for track in current_disc_info.tracks:
                detail_data.append([str(track.number), str(track.seconds), str(track.sectors), str(track.length), str(track.offset)])
            
            detail_window = window_layout.lo_detail_window(current_disc_info, detail_tabel_header, detail_data, str(datetime.timedelta(seconds = current_disc_info.seconds)))

            while True:
                detail_event, detail_values = detail_window.read()

                if detail_event == psg.WIN_CLOSED or detail_event == '-ok_comp_btn-' : break

                if detail_event == '-copy_discid-' : pyperclip.copy(current_disc_info.id)

            detail_window.close()

        except discid.DiscError:
            psg.popup_ok('ディスクの読み込み時にエラーが発生しました\nディスク本体が挿入されているか確認してください', title = window_title, icon = icon_path, modal = True, keep_on_top = True)

    
    #---------------------------------------------------------------------------------

    # Editkey Loss Window

    #---------------------------------------------------------------------------------


    if home_event == '-menu_editkeyloss_btn-':
            
        editkeyloss_window = window_layout.lo_editkeyloss_window()

        while True:
            editkeyloss_event, editkeyloss_values = editkeyloss_window.read()

            if editkeyloss_event == psg.WIN_CLOSED or editkeyloss_event == '-cancel_btn-' : break

            if editkeyloss_event == '-ok_btn-':
                if editkeyloss_values['-ekl_discid_input-'] == '' or editkeyloss_values['-ekl_title_input-'] == '' or editkeyloss_values['-ekl_email_input-'] == '':
                    psg.popup_ok('未入力の項目があります', title = window_title, icon = icon_path, modal = True, keep_on_top = True)
                
                elif psg.popup_yes_no('このフォームを送信しますか？', title = window_title, icon = icon_path, modal = True, keep_on_top = True) == 'Yes':
                    ekl_form_dict = {
                        'discid': str(editkeyloss_values['-ekl_discid_input-']),
                        'disctitle': str(editkeyloss_values['-ekl_title_input-']),
                        'catype': str(editkeyloss_values['-ekl_catype_input-']),
                        'email': str(editkeyloss_values['-ekl_email_input-']),
                        "mgun": mgun.mgun()
                    }

                    ekl_key_name = '01_ekl_form_data/' + editkeyloss_values['-ekl_discid_input-'].replace('/','_') + '-' + editkeyloss_values['-ekl_title_input-'].replace('/','_') + '-' + editkeyloss_values['-ekl_catype_input-'].replace('/','_') + '.db'

                    aws_s3_client.put_object(Body = json.dumps(ekl_form_dict, ensure_ascii = False, indent = 4), Bucket = aws_info_bn, Key = ekl_key_name)

                    psg.popup_ok('フォームの送信が完了しました', title = window_title, icon = icon_path, modal = True, keep_on_top = True)
                    break

        editkeyloss_window.close()


    #---------------------------------------------------------------------------------

    # Setting Window

    #---------------------------------------------------------------------------------


    if home_event == '-menu_setting_btn-':

        setting_menu_list = ['一般', '情報']
        setting_theme_list = ['Light', 'Dark']
        library_list = 'boto3,pysimplegui,libdiscid,python-discid,pyperclip,pillow'

        setting_window = window_layout.lo_setting_window(window_title_raw, version_all, setting_menu_list, library_list, setting_theme_list, general_setting_dict)

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
                aws_s3_response = aws_s3_client.get_object(Bucket = aws_info_bn, Key = '00_latest_software_vesion/latest_version.db')
                update_info = json.loads(aws_s3_response["Body"].read())

                if parse(update_info['version']) > parse(software_version[0]):
                    update_info_all = update_info['version'] + update_info['version_space'] + update_info['version_prerelease']
                    if psg.popup_yes_no('Mincarの新しいバージョンが利用可能です\n\n現在のバージョン: v' + version_all + '\n最新バージョン: v' + update_info_all + '\n\n最新バージョンをダウンロードしますか？', title = window_title, icon = icon_path, modal = True, keep_on_top = True) == 'Yes':
                        webbrowser.open(update_info['url'])

                else:
                    psg.popup_ok('お使いのMincarは最新バージョンです', title = window_title, icon = icon_path, modal = True, keep_on_top = True)
            
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

                with open('mincar_data/setting.json', 'w', encoding = 'UTF-8') as file:
                    json.dump(general_setting_dict, file, ensure_ascii = False, indent = 4)

                break

        setting_window.close()

home_window.close()