# -*- coding: utf-8 -*-

# Mincar
# download.py
# (C) 2022 Cube
# cubezeero@gmail.com

import PySimpleGUI as psg
import os
import io
import re

import sys
sys.path.append('../')
import muuid
import aws_info
import software_info
import discid
import util

def function_download(aws_s3_client, gui_layout, gs_default_savefolder):

    disc_id = ''
    coverart_download_list = []
    coverart_download_bytedata = []
    coverart_download_bytedata_rs = []
    coverart_type_list = []
    title_list = []
    title_name = ''
    current_coverart_index = 0
    cancel_sw = 0

    if muuid.check_mbl(muuid.get_muuid(), aws_s3_client, aws_info.BUCKET_NAME()):
        psg.popup_ok('サーバ側からブロックされました', title = software_info.Software_Name_All(), icon = software_info.Icon_Path(), modal = True, keep_on_top = True)

    else:


        #---------------------------------------------------------------------------------
        # Download DiscID Search Window
        #---------------------------------------------------------------------------------


        download_select_window = gui_layout.lo_download_select_window()

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
                    psg.popup_ok('DiscIDを入力してください', title = software_info.Software_Name_All(), icon = software_info.Icon_Path(), modal = True, keep_on_top = True)
            
            if download_select_event == '-ok_disc_btn-':
                try:
                    current_disc_info = discid.read()
                    disc_id = current_disc_info.id
                    break

                except discid.DiscError:
                    psg.popup_ok('ディスクの読み込み時にエラーが発生しました\nディスク本体が挿入されているか確認してください', title = software_info.Software_Name_All(), icon = software_info.Icon_Path(), modal = True, keep_on_top = True)
                
        download_select_window.close()

        if cancel_sw == 0:

            aws_s3_response = aws_s3_client.list_objects_v2(Bucket = aws_info.BUCKET_NAME(), Prefix = disc_id + '/')
            
            if "Contents" not in aws_s3_response:
                psg.popup_ok('このディスクのカバーアートはまだ登録されていません', title = software_info.Software_Name_All(), icon = software_info.Icon_Path(), modal = True, keep_on_top = True)

            else:
                # DiscIDと一致したタイトルの取得
                for aws_s3_obj in aws_s3_response['Contents']:
                    if aws_s3_obj['Key'].split('/')[1] not in title_list:
                        title_list.append(aws_s3_obj['Key'].split('/')[1])


                #---------------------------------------------------------------------------------
                # Download TitleList Window
                #---------------------------------------------------------------------------------
                

                download_disclist_window = gui_layout.lo_download_disclist_window(title_list)

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


                    download_pw_window = gui_layout.lo_getca_pw_window()

                    while True:
                        download_pw_event, download_pw_values = download_pw_window.read(timeout = 100)

                        # 各カバーアートのダウンロード
                        for cnt, aws_s3_obj in enumerate(aws_s3_response['Contents']):
                            if aws_s3_obj['Key'].split('/')[1] == title_name:
                                coverart_download_list.append(aws_s3_obj['Key'])
                                coverart_download_bytedata.append(io.BytesIO(aws_s3_client.get_object(Bucket = aws_info.BUCKET_NAME(), Key = aws_s3_obj['Key'])['Body'].read()))
                                coverart_download_bytedata_rs.append(util.keepAspectResizeToIo(coverart_download_bytedata[-1], (200,200)))
                                coverart_type_list.append(aws_s3_obj['Key'].split('/')[2].split('.')[0])
                        
                        break

                    download_pw_window.close()


                    #---------------------------------------------------------------------------------
                    # Download Main Window
                    #---------------------------------------------------------------------------------
                    

                    download_window = gui_layout.lo_download_window(coverart_type_list, coverart_download_bytedata_rs)

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

                                    psg.popup_ok('カバーアートのダウンロードが完了しました', title = software_info.Software_Name_All(), icon = software_info.Icon_Path(), modal = True, keep_on_top = True)

                            else:
                                coverart_dl_path = psg.popup_get_file(message = 'none', title = 'none', default_path = dl_default_path, no_window = True, save_as = True, default_extension = '.jpg', multiple_files = False, file_types = (('Jpeg Image File', '.jpg'),), modal = True)
                            
                                if coverart_dl_path != '':

                                    # すでに取得済みのバイトデータを保存
                                    with open(coverart_dl_path, mode = 'wb') as save_ca:
                                        save_ca.write(coverart_download_bytedata[current_coverart_index].getvalue())
                                    
                                    psg.popup_ok('カバーアートのダウンロードが完了しました', title = software_info.Software_Name_All(), icon = software_info.Icon_Path(), modal = True, keep_on_top = True)
                    
                    download_window.close()