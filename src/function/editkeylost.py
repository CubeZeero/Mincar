# -*- coding: utf-8 -*-

# Mincar
# editkeylost.py
# (C) 2022 Cube
# cubezeero@gmail.com

import PySimpleGUI as psg
import json

import sys
sys.path.append('../')
import muuid
import aws_info
import software_info

def function_editkeylost(aws_s3_client, gui_layout):

    if muuid.check_mbl(muuid.get_muuid(), aws_s3_client, aws_info.BUCKET_NAME()):
                psg.popup_ok('サーバ側からブロックされました', title = software_info.Software_Name_All(), icon = software_info.Icon_Path(), modal = True, keep_on_top = True)
            
    else:
        
        editkeyloss_window = gui_layout.lo_editkeyloss_window()

        while True:
            editkeyloss_event, editkeyloss_values = editkeyloss_window.read()

            if editkeyloss_event == psg.WIN_CLOSED or editkeyloss_event == '-cancel_btn-' : break

            if editkeyloss_event == '-ok_btn-':
                if editkeyloss_values['-ekl_discid_input-'] == '' or editkeyloss_values['-ekl_title_input-'] == '' or editkeyloss_values['-ekl_email_input-'] == '':
                    psg.popup_ok('未入力の項目があります', title = software_info.Software_Name_All(), icon = software_info.Icon_Path(), modal = True, keep_on_top = True)
                
                elif psg.popup_yes_no('このフォームを送信しますか？', title = software_info.Software_Name_All(), icon = software_info.Icon_Path(), modal = True, keep_on_top = True) == 'Yes':
                    ekl_form_dict = {
                        'discid': str(editkeyloss_values['-ekl_discid_input-']),
                        'disctitle': str(editkeyloss_values['-ekl_title_input-']),
                        'catype': str(editkeyloss_values['-ekl_catype_input-']),
                        'email': str(editkeyloss_values['-ekl_email_input-']),
                        'mgun': muuid.get_mgun(),
                        'muuid': muuid.get_muuid()
                    }

                    ekl_key_name = '01_ekl_form_data/' + editkeyloss_values['-ekl_discid_input-'].replace('/','_') + '-' + editkeyloss_values['-ekl_title_input-'].replace('/','_') + '-' + editkeyloss_values['-ekl_catype_input-'].replace('/','_') + '.db'

                    aws_s3_client.put_object(Body = json.dumps(ekl_form_dict, ensure_ascii = False, indent = 4), Bucket = aws_info.BUCKET_NAME(), Key = ekl_key_name)

                    psg.popup_ok('フォームの送信が完了しました', title = software_info.Software_Name_All(), icon = software_info.Icon_Path(), modal = True, keep_on_top = True)
                    break

        editkeyloss_window.close()
