# -*- coding: utf-8 -*-

# Mincar
# gui_layout.py
# (C) 2022 Cube
# cubezeero@gmail.com

import PySimpleGUI as psg

import sys
sys.path.append('../')
import software_info
import global_values as gv



def lo_home_window(icon_io_list, menu_button_bgcolor):

        upload_btn_col = [

                [psg.Button(image_data = icon_io_list[0], button_color = menu_button_bgcolor, key = '-menu_upload_btn-')],
                [psg.Text(text = 'アップロード', font = ['Meiryo',8])]
                
                ]

        download_btn_col = [

                [psg.Button(image_data = icon_io_list[1], button_color = menu_button_bgcolor, key = '-menu_download_btn-')],
                [psg.Text(text = 'ダウンロード', font = ['Meiryo',8])]
                
                ]

        edit_btn_col = [

                [psg.Button(image_data = icon_io_list[2], button_color = menu_button_bgcolor, key = '-menu_edit_btn-')],
                [psg.Text(text = '編集', font = ['Meiryo',8])]
                
                ]

        detail_btn_col = [

                [psg.Button(image_data = icon_io_list[3], button_color = menu_button_bgcolor, key = '-menu_detail_btn-')],
                [psg.Text(text = 'ディスクの詳細', font = ['Meiryo',8])]
                
                ]

        editkeyloss_btn_col = [

                [psg.Button(image_data = icon_io_list[4], button_color = menu_button_bgcolor, key = '-menu_editkeyloss_btn-')],
                [psg.Text(text = '編集キーの紛失', font = ['Meiryo',8])]
                
                ]

        setting_btn_col = [

                [psg.Button(image_data = icon_io_list[5], button_color = menu_button_bgcolor, key = '-menu_setting_btn-')],
                [psg.Text(text = '設定', font = ['Meiryo',8])]
                
                ]

        home_layout = [

                [psg.Image(filename = 'mincar_data/img/mincar_logo.png', pad = ((0,0),(40,40)))],

                [psg.Column(upload_btn_col, element_justification = 'center'),
                 psg.Column(download_btn_col, element_justification = 'center'),
                 psg.Column(edit_btn_col, element_justification = 'center'),
                 psg.Column(detail_btn_col, element_justification = 'center'),
                 psg.Column(editkeyloss_btn_col, element_justification = 'center'),
                 psg.Column(setting_btn_col, element_justification = 'center')],

                [psg.Text(text = software_info.Software_Name() + 'は同人音楽作品専用のカバーアートデータベースです', pad = ((0,0),(30,0)), key = '-announcement_text-')],
                [psg.Button(button_text = 'How To Use', font = ['Meiryo',10], size = (15,1), pad = ((0,0),(30,0)), key = '-htu_btn-')]
                
                ]

        return psg.Window(software_info.Software_Name_All(), home_layout, icon = software_info.Icon_Path(), size = (900,450), font = ['Meiryo',10], element_justification = 'c')

def lo_upload_disclist_window(disclist):

        upload_disclist_layout = [

                [psg.Listbox(values = disclist, size = (100,10), default_values = disclist[0], pad = ((0,0),(10,0)), sbar_relief = 'RELIEF_FLAT', sbar_trough_color = '#000000', sbar_background_color = '#222222', select_mode = [psg.LISTBOX_SELECT_MODE_SINGLE], key = '-listbox_titlename-')],

                [psg.Text(text = str(len(disclist)) + '件のタイトルが登録されています\n同一タイトルのカバーアートを登録する場合は同一タイトルを選択してください\n(CDの性質上、DiscIDが重複する場合があります)', pad = ((0,0),(10,0)), font = ['Meiryo',8], justification = 'center')],

                [psg.Button(button_text = 'このタイトルで登録する', font = ['Meiryo',8], size = (24,1), pad = ((0,30),(10,0)), key = '-identical_btn-'),
                 psg.Button(button_text = '別のタイトルを登録する', font = ['Meiryo',8], size = (24,1), pad = ((0,0),(10,0)), key = '-other_btn-')],

                [psg.Button(button_text = 'Cancel', font = ['Meiryo',8], size = (10,1), pad = ((0,0),(10,0)), key = '-cancel_btn-')]
                
                ]

        return psg.Window(software_info.Software_Name_All() + ' - カバーアート登録', upload_disclist_layout, icon = software_info.Icon_Path(), size = (500,380), font = ['Meiryo',10], element_justification = 'c', modal = True)

def lo_upload_window(disc_id, disc_track_num, title_name, input_disabled_color, default_ca, gs_default_editkey):

        coverart_image_col = [

                [psg.Image(data = default_ca, pad = ((0,0),(30,0)), key = '-coverart_data_key-')],
                [psg.Button(button_text = 'カバーアート読み込み', font = ['Meiryo',8], size = (20,1), pad = ((0,0),(10,10)), key = '-load_coverart-')]

                ]

        disc_info_col = [

                [psg.Text(text = 'DiscID: ' + disc_id, pad = ((0,0),(0,0)))],
                [psg.Button(button_text = 'コピー', font = ['Meiryo',7], size = (10,1), pad = ((0,0),(5,0)), key = '-copy_discid-')],

                [psg.Text(text = 'ディスクの全曲数: ' + str(disc_track_num), pad = ((0,0),(20,0)))],

                [psg.Text(text = 'ディスクのタイトル', pad = ((0,0),(20,0)))],
                [psg.Input(default_text = title_name, disabled = bool(len(title_name)), disabled_readonly_background_color = input_disabled_color, size = (42,1), pad = ((0,0),(5,0)), key = '-disctitle_input-')],

                [psg.Text(text = 'カバーアートのタイプ(フロントカードやバックインレイなど)', pad = ((0,0),(20,0)))],
                [psg.Input(default_text = '', size = (42,1), pad = ((0,0),(5,0)), key = '-coverartname_input-')],

                [psg.Text(text = '編集用キー(カバーアートの置き換えや削除時に必要です)', pad = ((0,0),(20,0)))],
                [psg.Input(default_text = gs_default_editkey, size = (42,1), pad = ((0,0),(5,0)), key = '-editkey_input-')]

                ]

        upload_layout = [

                [psg.Frame(title = 'カバーアート', layout = coverart_image_col, size = (330,370), pad = ((0,0),(15,0)), element_justification = 'c'),
                 psg.Column(disc_info_col, element_justification = 'left', pad = ((20,0),(15,0)))],

                [psg.Button(button_text = 'キャンセル', font = ['Meiryo',8], size = (24,1), pad = ((0,50),(30,0)), key = '-cancel_btn-'),
                 psg.Button(button_text = 'カバーアートをアップロード', font = ['Meiryo',8], size = (24,1), pad = ((0,0),(30,0)), key = '-upload_coverart-')]
                
                ]

        return psg.Window(software_info.Software_Name_All() + ' - カバーアート登録', upload_layout, icon = software_info.Icon_Path(), size = (750,480), font = ['Meiryo',10], element_justification = 'c', modal = True)

def lo_download_select_window():

        download_select_layout = [

                [psg.Text(text = 'DiscIDを入力してください', pad = ((0,0),(15,0)))],

                [psg.Input(default_text = '', size = (50,1), pad = ((0,0),(15,0)), key = '-discid_input-')],

                [psg.Button(button_text = 'DiscIDで検索', font = ['Meiryo',8], size = (16,1), pad = ((0,30),(20,0)), key = '-ok_discid_btn-'),
                 psg.Button(button_text = 'ディスク本体で検索', font = ['Meiryo',8], size = (16,1), pad = ((0,30),(20,0)), key = '-ok_disc_btn-'),
                 psg.Button(button_text = 'Cancel', font = ['Meiryo',8], size = (16,1), pad = ((0,0),(20,0)), key = '-cancel_btn-')]
                
                ]

        return psg.Window(software_info.Software_Name_All() + ' - カバーアートのダウンロード', download_select_layout, icon = software_info.Icon_Path(), size = (500,150), font = ['Meiryo',10], element_justification = 'c', modal = True)

def lo_download_disclist_window(disclist):

        download_disclist_layout = [

                [psg.Listbox(values = disclist, size = (100,10), default_values = disclist[0], pad = ((0,0),(20,0)), sbar_relief = 'RELIEF_FLAT', sbar_trough_color = '#000000', sbar_background_color = '#222222', select_mode = [psg.LISTBOX_SELECT_MODE_SINGLE], key = '-listbox_titlename-')],

                [psg.Text(text = str(len(disclist)) + '件のタイトルが登録されています\n取得したいカバーアートのタイトルを選択してください\n(CDの性質上、DiscIDが重複する場合があります)', pad = ((0,0),(10,0)), font = ['Meiryo',8], justification = 'center')],

                [psg.Button(button_text = 'OK', font = ['Meiryo',8], size = (12,1), pad = ((0,30),(10,0)), key = '-ok_btn-'),
                 psg.Button(button_text = 'Cancel', font = ['Meiryo',8], size = (12,1), pad = ((0,0),(10,0)), key = '-cancel_btn-')]
                
                ]

        return psg.Window(software_info.Software_Name_All() + ' - カバーアートのダウンロード', download_disclist_layout, icon = software_info.Icon_Path(), size = (500,360), font = ['Meiryo',10], element_justification = 'c', modal = True)

def lo_getca_pw_window():

        download_pw_layout = [

                [psg.Text(text = 'カバーアートリストを取得中', text_color = '#000000', background_color = '#2de27f', pad = ((0,0),(5,0)))]
                
                ]

        return psg.Window(software_info.Software_Name_All() + ' - カバーアートのダウンロード', download_pw_layout, no_titlebar = True, size = (200,40), font = ['Meiryo',10], background_color = '#2de27f', element_justification = 'c', modal = True)

def lo_download_window(coverart_type_list, coverart_rs_bytedata):

        coverart_image = [

                [psg.Image(data = coverart_rs_bytedata[0], pad = ((0,0),(40,0)), key = '-coverart_data_key-')],

                ]

        download_layout = [

                [psg.Listbox(values = coverart_type_list, size = (30,15), default_values = coverart_type_list[0], pad = ((0,0),(20,0)), enable_events = True, sbar_relief = 'RELIEF_FLAT', sbar_trough_color = '#000000', sbar_background_color = '#222222', select_mode = [psg.LISTBOX_SELECT_MODE_SINGLE], key = '-coverarttype_list-'),
                        psg.Frame(title = 'カバーアート', layout = coverart_image, size = (330,320), pad = ((10,0),(20,0)), element_justification = 'c')],

                [psg.Text(text = str(len(coverart_type_list)) + '件のカバーアートが登録されています', pad = ((0,0),(20,0)))],

                [psg.Button(button_text = 'このカバーアートをダウンロード', font = ['Meiryo',8], size = (26,1), pad = ((0,30),(10,0)), key = '-download_btn-'),
                 psg.Button(button_text = 'Cancel', font = ['Meiryo',8], size = (12,1), pad = ((0,0),(10,0)), key = '-cancel_btn-')]
                
                ]

        return psg.Window(software_info.Software_Name_All() + ' - カバーアートのダウンロード', download_layout, icon = software_info.Icon_Path(), size = (700,440), font = ['Meiryo',10], element_justification = 'c', modal = True)

def lo_edit_select_window():

        edit_select_layout = [

                [psg.Text(text = 'DiscIDを入力してください', pad = ((0,0),(15,0)))],

                [psg.Input(default_text = '', size = (50,1), pad = ((0,0),(15,0)), key = '-discid_input-')],

                [psg.Button(button_text = 'DiscIDで検索', font = ['Meiryo',8], size = (16,1), pad = ((0,30),(20,0)), key = '-ok_discid_btn-'),
                 psg.Button(button_text = 'ディスク本体で検索', font = ['Meiryo',8], size = (16,1), pad = ((0,30),(20,0)), key = '-ok_disc_btn-'),
                 psg.Button(button_text = 'Cancel', font = ['Meiryo',8], size = (16,1), pad = ((0,0),(20,0)), key = '-cancel_btn-')]
                
                ]

        return psg.Window(software_info.Software_Name_All() + ' - カバーアートの編集', edit_select_layout, icon = software_info.Icon_Path(), size = (500,150), font = ['Meiryo',10], element_justification = 'c', modal = True)

def lo_edit_disclist_window(disclist):

        edit_disclist_layout = [

                [psg.Listbox(values = disclist, size = (100,10), default_values = disclist[0], pad = ((0,0),(20,0)), sbar_relief = 'RELIEF_FLAT', sbar_trough_color = '#000000', sbar_background_color = '#222222', select_mode = [psg.LISTBOX_SELECT_MODE_SINGLE], key = '-listbox_titlename-')],

                [psg.Text(text = str(len(disclist)) + '件のタイトルが登録されています\n取得したいカバーアートのタイトルを選択してください\n(CDの性質上、DiscIDが重複する場合があります)', pad = ((0,0),(10,0)), font = ['Meiryo',8], justification = 'center')],

                [psg.Button(button_text = 'OK', font = ['Meiryo',8], size = (12,1), pad = ((0,30),(10,0)), key = '-ok_btn-'),
                 psg.Button(button_text = 'Cancel', font = ['Meiryo',8], size = (12,1), pad = ((0,0),(10,0)), key = '-cancel_btn-')]
                
                ]

        return psg.Window(software_info.Software_Name_All() + ' - カバーアートの編集', edit_disclist_layout, icon = software_info.Icon_Path(), size = (500,360), font = ['Meiryo',10], element_justification = 'c', modal = True)

def lo_edit_window(coverart_type_list, coverart_rs_bytedata, gs_default_editkey):

        coverart_image = [

                [psg.Image(data = coverart_rs_bytedata[0], pad = ((0,0),(40,0)), key = '-coverart_data_key-')]

                ]

        coverart_col = [

                [psg.Frame(title = 'カバーアート', layout = coverart_image, size = (330,320), element_justification = 'c')],
                [psg.Button(button_text = 'カバーアートの更新', font = ['Meiryo',8], size = (20,1), pad = ((0,0),(10,0)), key = '-load_coverart-')]

                ]

        edit_layout = [

                [psg.Listbox(values = coverart_type_list, size = (30,18), pad = ((0,0),(20,0)), default_values = coverart_type_list[0], enable_events = True, sbar_relief = 'RELIEF_FLAT', sbar_trough_color = '#000000', sbar_background_color = '#222222', select_mode = [psg.LISTBOX_SELECT_MODE_SINGLE], key = '-coverarttype_list-'),
                 psg.Column(coverart_col, element_justification = 'center', pad = ((20,0),(20,0)))],

                [psg.Text(text = str(len(coverart_type_list)) + '件のカバーアートが登録されています', pad = ((0,0),(20,0)))],

                [psg.Text(text = '編集キー', pad = ((0,0),(15,0)), font = ['Meiryo',8], justification = 'center')],
                [psg.Input(default_text = gs_default_editkey, size = (30,1), pad = ((0,0),(5,0)), key = '-editkey_input-')],

                [psg.Button(button_text = 'このカバーアートを削除', font = ['Meiryo',8], size = (26,1), pad = ((0,30),(20,0)), key = '-delete_btn-'),
                 psg.Button(button_text = 'Cancel', font = ['Meiryo',8], size = (12,1), pad = ((0,0),(20,0)), key = '-cancel_btn-')]
                
                ]

        return psg.Window(software_info.Software_Name_All() + ' - カバーアートの編集', edit_layout, icon = software_info.Icon_Path(), size = (700,580), font = ['Meiryo',10], element_justification = 'c', modal = True)

def lo_detail_window(disc_info, detail_tabel_header, detail_data, all_seconds):

        detail_layout = [

                [psg.Text(text = 'ディスクの詳細', font = ['Meiryo',12], pad = ((0,0),(10,10)))],

                [psg.Text(text = 'DiscID: ' + disc_info.id, pad = ((0,0),(10,0)))],
                [psg.Button(button_text = 'コピー', font = ['Meiryo',7], size = (10,1), pad = ((0,0),(5,10)), key = '-copy_discid-')],
                [psg.Text(text = '合計セクタ: ' + str(disc_info.sectors), pad = ((0,0),(10,0)))],
                [psg.Text(text = '合計再生時間: ' + all_seconds, pad = ((0,0),(10,0)))],
                [psg.Text(text = '合計再生時間(秒): ' + str(disc_info.seconds) + 's', pad = ((0,0),(10,0)))],

                [psg.Table(detail_data, headings = detail_tabel_header, auto_size_columns = False, font = ['Meiryo',10], size = (24,12), pad = ((0,0),(20,0)), key = '-ok_btn-')],

                [psg.Button(button_text = 'OK', font = ['Meiryo',8], size = (16,1), pad = ((0,0),(20,0)), key = '-ok_comp_btn-')]
                
                ]

        return psg.Window(software_info.Software_Name_All() + ' - ディスクの詳細', detail_layout, icon = software_info.Icon_Path(), size = (600,570), font = ['Meiryo',10], element_justification = 'c', modal = True)

def lo_editkeyloss_window():

        editkeyloss_layout = [

                [psg.Text(text = '編集キー紛失時用の確認フォーム', font = ['Meiryo',12], pad = ((0,0),(15,0)))],
                [psg.Text(text = '編集キーを紛失、忘れた場合はこちらのフォームでお問い合わせください', font = ['Meiryo',8], pad = ((0,0),(10,0)))],

                [psg.Text(text = '編集キーを設定したDiscID (必須)', font = ['Meiryo',8], pad = ((0,0),(40,0)))],
                [psg.Input(default_text = '', size = (42,1), pad = ((0,0),(5,0)), key = '-ekl_discid_input-')],

                [psg.Text(text = '編集キーを設定したタイトル (必須)', font = ['Meiryo',8], pad = ((0,0),(20,0)))],
                [psg.Input(default_text = '', size = (42,1), pad = ((0,0),(5,0)), key = '-ekl_title_input-')],

                [psg.Text(text = '編集キーを設定したカバーアートのタイプ', font = ['Meiryo',8], pad = ((0,0),(20,0)))],
                [psg.Input(default_text = '', size = (42,1), pad = ((0,0),(5,0)), key = '-ekl_catype_input-')],

                [psg.Text(text = 'メールアドレス (必須)', font = ['Meiryo',8], pad = ((0,0),(20,0)))],
                [psg.Input(default_text = '', size = (42,1), pad = ((0,0),(5,0)), key = '-ekl_email_input-')],

                [psg.Button(button_text = '送信', font = ['Meiryo',8], size = (12,1), pad = ((0,30),(40,0)), key = '-ok_btn-'),
                 psg.Button(button_text = 'Cancel', font = ['Meiryo',8], size = (12,1), pad = ((0,0),(40,0)), key = '-cancel_btn-')]
                
                ]

        return psg.Window(software_info.Software_Name_All() + ' - ディスクの詳細', editkeyloss_layout, icon = software_info.Icon_Path(), size = (600,450), font = ['Meiryo',10], element_justification = 'c', modal = True)

def lo_setting_window(window_title_raw, software_version, setting_menu_list, library_list, setting_theme_list, general_setting_dict):

        setting_general_frame = [

                [psg.Text(text = 'テーマ (再起動時に適用されます)', font = ['Meiryo',8], pad = ((0,0),(90,0))),
                 psg.Combo(setting_theme_list, default_value = general_setting_dict['themename'], font = ['Meiryo',8], size = (12,1), pad = ((10,0),(90,0)), readonly = True, key = '-theme_combo-')],

                [psg.Text(text = 'デフォルトの編集キー', font = ['Meiryo',8], pad = ((0,0),(15,0))),
                 psg.Input(default_text = general_setting_dict['editkey'], size = (24,1), pad = ((10,0),(13,0)), key = '-default_editkey_input-')],

                [psg.Text(text = '保存先を指定', font = ['Meiryo',8], pad = ((0,0),(30,0)))],
                [psg.Input(default_text = general_setting_dict['savefolder'], size = (40,1), pad = ((0,0),(5,0)), key = '-get_folder_input-')],
                [psg.Button(button_text = '参照', font = ['Meiryo',8], size = (8,1), pad = ((0,0),(10,0)), key = '-get_folder_btn-')],

                [psg.Checkbox(text = '起動時に自動でアップデートを確認する', default = bool(general_setting_dict['start_update_check']), font = ['Meiryo',8], auto_size_text = True, pad = ((0,0),(30,0)), key = '-start_update_check-')]

                ]

        setting_info_frame = [

                [psg.Image(filename = 'mincar_data/img/mincar_logo_info.png', pad = ((0,0),(65,5)))],
                [psg.Text(text = window_title_raw, font = ['Meiryo',12], pad = ((0,0),(10,0)))],
                [psg.Text(text = 'version ' + software_version, font = ['Meiryo',8], pad = ((0,0),(2,0)))],
                [psg.Text(text = 'Developed by Cube', font = ['Meiryo',10], pad = ((0,0),(10,0)))],
                [psg.Text(text = library_list, font = ['Meiryo',8], pad = ((0,0),(10,0)))],
                [psg.Text(text = 'https://github.com/CubeZeero/Mincar', enable_events = True, font = ['Meiryo',8,'underline'], pad = ((0,0),(10,0)), key = '-homepage-')],
                [psg.Button(button_text = 'アップデートの確認', font = ['Meiryo',8], size = (24,1), pad = ((0,0),(20,0)), key = '-update_check_btn-')]

                ]

        setting_layout = [

                [psg.Listbox(values = setting_menu_list, size = (20,20), default_values = setting_menu_list[0], sbar_relief = 'RELIEF_FLAT', sbar_trough_color = '#000000', sbar_background_color = '#222222', enable_events = True, select_mode = [psg.LISTBOX_SELECT_MODE_SINGLE], key = '-listbox_menu-'),
                 psg.Frame('一般設定', setting_general_frame, title_location = psg.TITLE_LOCATION_TOP, size = (450,420), element_justification = 'center', key = setting_menu_list[0], visible = True),
                 psg.Frame('情報', setting_info_frame, title_location = psg.TITLE_LOCATION_TOP, size = (450,420), element_justification = 'center', key = setting_menu_list[1], visible = False)],

                [psg.Button(button_text = 'OK', font = ['Meiryo',8], size = (12,1), pad = ((0,30),(15,0)), key = '-ok_btn-'),
                 psg.Button(button_text = 'Cancel', font = ['Meiryo',8], size = (12,1), pad = ((0,0),(15,0)), key = '-cancel_btn-')]
                
                ]

        return psg.Window(software_info.Software_Name_All() + ' - 設定', setting_layout, icon = software_info.Icon_Path(), size = (600,490), font = ['Meiryo',10], element_justification = 'c', modal = True)