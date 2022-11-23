# -*- coding: utf-8 -*-

# Mincar
# gui_layout.py
# (C) 2022 Cube
# cubezeero@gmail.com

class window_layout:

    def __init__(self, psg, window_title, icon_path):

        self.psg = psg
        self.window_title = window_title
        self.icon_path = icon_path

    def lo_home_window(self, icon_io_list, menu_button_bgcolor, window_title_raw):

        upload_btn_col = [

                [self.psg.Button(image_data = icon_io_list[0], button_color = menu_button_bgcolor, key = '-menu_upload_btn-')],
                [self.psg.Text(text = 'アップロード', font = ['Meiryo',8])]
                
                ]

        download_btn_col = [

                [self.psg.Button(image_data = icon_io_list[1], button_color = menu_button_bgcolor, key = '-menu_download_btn-')],
                [self.psg.Text(text = 'ダウンロード', font = ['Meiryo',8])]
                
                ]
        
        edit_btn_col = [

                [self.psg.Button(image_data = icon_io_list[2], button_color = menu_button_bgcolor, key = '-menu_edit_btn-')],
                [self.psg.Text(text = '編集', font = ['Meiryo',8])]
                
                ]
        
        detail_btn_col = [

                [self.psg.Button(image_data = icon_io_list[3], button_color = menu_button_bgcolor, key = '-menu_detail_btn-')],
                [self.psg.Text(text = 'ディスクの詳細', font = ['Meiryo',8])]
                
                ]

        setting_btn_col = [

                [self.psg.Button(image_data = icon_io_list[4], button_color = menu_button_bgcolor, key = '-menu_setting_btn-')],
                [self.psg.Text(text = '設定', font = ['Meiryo',8])]
                
                ]

        home_layout = [

                [self.psg.Image(filename = 'mincar_data/img/mincar_logo.png', pad = ((0,0),(40,40)))],

                [self.psg.Column(upload_btn_col, element_justification = 'center'),
                 self.psg.Column(download_btn_col, element_justification = 'center'),
                 self.psg.Column(edit_btn_col, element_justification = 'center'),
                 self.psg.Column(detail_btn_col, element_justification = 'center'),
                 self.psg.Column(setting_btn_col, element_justification = 'center')],

                [self.psg.Text(text = window_title_raw + 'は同人音楽作品専用のカバーアートデータベースです', pad = ((0,0),(30,0)), key = '-announcement_text-')],
                [self.psg.Button(button_text = 'How To Use', font = ['Meiryo',10], size = (15,1), pad = ((0,0),(30,0)), key = '-htu_btn-')]
                
                ]

        return self.psg.Window(self.window_title, home_layout, icon = self.icon_path, size = (800,450), font = ['Meiryo',10], element_justification = 'c')

    def lo_upload_disclist_window(self, disclist):

        upload_disclist_layout = [

                [self.psg.Listbox(values = disclist, size = (100,10), default_values = disclist[0], pad = ((0,0),(10,0)), sbar_relief = 'RELIEF_FLAT', sbar_trough_color = '#000000', sbar_background_color = '#222222', select_mode = [self.psg.LISTBOX_SELECT_MODE_SINGLE], key = '-listbox_titlename-')],

                [self.psg.Text(text = str(len(disclist)) + '件のタイトルが登録されています\n同一タイトルのカバーアートを登録する場合は同一タイトルを選択してください\n(CDの性質上、DiscIDが重複する場合があります)', pad = ((0,0),(10,0)), font = ['Meiryo',8], justification = 'center')],

                [self.psg.Button(button_text = 'このタイトルで登録する', font = ['Meiryo',8], size = (24,1), pad = ((0,30),(10,0)), key = '-identical_btn-'),
                 self.psg.Button(button_text = '別のタイトルを登録する', font = ['Meiryo',8], size = (24,1), pad = ((0,0),(10,0)), key = '-other_btn-')],

                [self.psg.Button(button_text = 'Cancel', font = ['Meiryo',8], size = (10,1), pad = ((0,0),(10,0)), key = '-cancel_btn-')]
                
                ]

        return self.psg.Window(self.window_title + ' - カバーアート登録', upload_disclist_layout, icon = self.icon_path, size = (500,380), font = ['Meiryo',10], element_justification = 'c', modal = True)

    def lo_upload_window(self, disc_id, disc_track_num, title_name, input_disabled_color, default_ca, gs_default_editkey):

        coverart_image_col = [

                [self.psg.Image(data = default_ca, pad = ((0,0),(30,0)), key = '-coverart_data_key-')],
                [self.psg.Button(button_text = 'カバーアート読み込み', font = ['Meiryo',8], size = (20,1), pad = ((0,0),(10,10)), key = '-load_coverart-')]

                ]
        
        disc_info_col = [

                [self.psg.Text(text = 'DiscID: ' + disc_id, pad = ((0,0),(0,0)))],
                [self.psg.Button(button_text = 'コピー', font = ['Meiryo',7], size = (10,1), pad = ((0,0),(5,0)), key = '-copy_discid-')],

                [self.psg.Text(text = 'ディスクの全曲数: ' + str(disc_track_num), pad = ((0,0),(20,0)))],

                [self.psg.Text(text = 'ディスクのタイトル', pad = ((0,0),(20,0)))],
                [self.psg.Input(default_text = title_name, disabled = bool(len(title_name)), disabled_readonly_background_color = input_disabled_color, size = (42,1), pad = ((0,0),(5,0)), key = '-disctitle_input-')],

                [self.psg.Text(text = 'カバーアートのタイプ(フロントカードやバックインレイなど)', pad = ((0,0),(20,0)))],
                [self.psg.Input(default_text = '', size = (42,1), pad = ((0,0),(5,0)), key = '-coverartname_input-')],

                [self.psg.Text(text = '編集用キー(カバーアートの置き換えや削除時に必要です)', pad = ((0,0),(20,0)))],
                [self.psg.Input(default_text = gs_default_editkey, size = (42,1), pad = ((0,0),(5,0)), key = '-editkey_input-')]

                ]

        upload_layout = [

                [self.psg.Frame(title = 'カバーアート', layout = coverart_image_col, size = (330,370), pad = ((0,0),(15,0)), element_justification = 'c'),
                 self.psg.Column(disc_info_col, element_justification = 'left', pad = ((20,0),(15,0)))],

                [self.psg.Button(button_text = 'キャンセル', font = ['Meiryo',8], size = (24,1), pad = ((0,50),(30,0)), key = '-cancel_btn-'),
                 self.psg.Button(button_text = 'カバーアートをアップロード', font = ['Meiryo',8], size = (24,1), pad = ((0,0),(30,0)), key = '-upload_coverart-')]
                
                ]

        return self.psg.Window(self.window_title + ' - カバーアート登録', upload_layout, icon = self.icon_path, size = (750,480), font = ['Meiryo',10], element_justification = 'c', modal = True)

    def lo_download_select_window(self):

        download_select_layout = [

                [self.psg.Text(text = 'DiscIDを入力してください', pad = ((0,0),(15,0)))],

                [self.psg.Input(default_text = '', size = (50,1), pad = ((0,0),(15,0)), key = '-discid_input-')],

                [self.psg.Button(button_text = 'DiscIDで検索', font = ['Meiryo',8], size = (16,1), pad = ((0,30),(20,0)), key = '-ok_discid_btn-'),
                 self.psg.Button(button_text = 'ディスク本体で検索', font = ['Meiryo',8], size = (16,1), pad = ((0,30),(20,0)), key = '-ok_disc_btn-'),
                 self.psg.Button(button_text = 'Cancel', font = ['Meiryo',8], size = (16,1), pad = ((0,0),(20,0)), key = '-cancel_btn-')]
                
                ]

        return self.psg.Window(self.window_title + ' - カバーアートのダウンロード', download_select_layout, icon = self.icon_path, size = (500,150), font = ['Meiryo',10], element_justification = 'c', modal = True)
    
    def lo_download_disclist_window(self, disclist):

        download_disclist_layout = [

                [self.psg.Listbox(values = disclist, size = (100,10), default_values = disclist[0], pad = ((0,0),(20,0)), sbar_relief = 'RELIEF_FLAT', sbar_trough_color = '#000000', sbar_background_color = '#222222', select_mode = [self.psg.LISTBOX_SELECT_MODE_SINGLE], key = '-listbox_titlename-')],

                [self.psg.Text(text = str(len(disclist)) + '件のタイトルが登録されています\n取得したいカバーアートのタイトルを選択してください\n(CDの性質上、DiscIDが重複する場合があります)', pad = ((0,0),(10,0)), font = ['Meiryo',8], justification = 'center')],

                [self.psg.Button(button_text = 'OK', font = ['Meiryo',8], size = (12,1), pad = ((0,30),(10,0)), key = '-ok_btn-'),
                 self.psg.Button(button_text = 'Cancel', font = ['Meiryo',8], size = (12,1), pad = ((0,0),(10,0)), key = '-cancel_btn-')]
                
                ]

        return self.psg.Window(self.window_title + ' - カバーアートのダウンロード', download_disclist_layout, icon = self.icon_path, size = (500,360), font = ['Meiryo',10], element_justification = 'c', modal = True)
    
    def lo_getca_pw_window(self):

        download_pw_layout = [

                [self.psg.Text(text = 'カバーアートリストを取得中', text_color = '#000000', background_color = '#2de27f', pad = ((0,0),(5,0)))]
                
                ]

        return self.psg.Window(self.window_title + ' - カバーアートのダウンロード', download_pw_layout, no_titlebar = True, size = (200,40), font = ['Meiryo',10], background_color = '#2de27f', element_justification = 'c', modal = True)
    
    def lo_download_window(self, coverart_type_list, coverart_rs_bytedata):

        coverart_image = [

                [self.psg.Image(data = coverart_rs_bytedata[0], pad = ((0,0),(40,0)), key = '-coverart_data_key-')],

                ]

        download_layout = [

                [self.psg.Listbox(values = coverart_type_list, size = (30,15), default_values = coverart_type_list[0], pad = ((0,0),(20,0)), enable_events = True, sbar_relief = 'RELIEF_FLAT', sbar_trough_color = '#000000', sbar_background_color = '#222222', select_mode = [self.psg.LISTBOX_SELECT_MODE_SINGLE], key = '-coverarttype_list-'),
                 self.psg.Frame(title = 'カバーアート', layout = coverart_image, size = (330,320), pad = ((10,0),(20,0)), element_justification = 'c')],

                [self.psg.Text(text = str(len(coverart_type_list)) + '件のカバーアートが登録されています', pad = ((0,0),(20,0)))],

                [self.psg.Button(button_text = 'このカバーアートをダウンロード', font = ['Meiryo',8], size = (26,1), pad = ((0,30),(10,0)), key = '-download_btn-'),
                 self.psg.Button(button_text = 'Cancel', font = ['Meiryo',8], size = (12,1), pad = ((0,0),(10,0)), key = '-cancel_btn-')]
                
                ]

        return self.psg.Window(self.window_title + ' - カバーアートのダウンロード', download_layout, icon = self.icon_path, size = (700,440), font = ['Meiryo',10], element_justification = 'c', modal = True)

    def lo_edit_select_window(self):

        edit_select_layout = [

                [self.psg.Text(text = 'DiscIDを入力してください', pad = ((0,0),(15,0)))],

                [self.psg.Input(default_text = '', size = (50,1), pad = ((0,0),(15,0)), key = '-discid_input-')],

                [self.psg.Button(button_text = 'DiscIDで検索', font = ['Meiryo',8], size = (16,1), pad = ((0,30),(20,0)), key = '-ok_discid_btn-'),
                 self.psg.Button(button_text = 'ディスク本体で検索', font = ['Meiryo',8], size = (16,1), pad = ((0,30),(20,0)), key = '-ok_disc_btn-'),
                 self.psg.Button(button_text = 'Cancel', font = ['Meiryo',8], size = (16,1), pad = ((0,0),(20,0)), key = '-cancel_btn-')]
                
                ]

        return self.psg.Window(self.window_title + ' - カバーアートの編集', edit_select_layout, icon = self.icon_path, size = (500,150), font = ['Meiryo',10], element_justification = 'c', modal = True)

    def lo_edit_disclist_window(self, disclist):

        edit_disclist_layout = [

                [self.psg.Listbox(values = disclist, size = (100,10), default_values = disclist[0], pad = ((0,0),(20,0)), sbar_relief = 'RELIEF_FLAT', sbar_trough_color = '#000000', sbar_background_color = '#222222', select_mode = [self.psg.LISTBOX_SELECT_MODE_SINGLE], key = '-listbox_titlename-')],

                [self.psg.Text(text = str(len(disclist)) + '件のタイトルが登録されています\n取得したいカバーアートのタイトルを選択してください\n(CDの性質上、DiscIDが重複する場合があります)', pad = ((0,0),(10,0)), font = ['Meiryo',8], justification = 'center')],

                [self.psg.Button(button_text = 'OK', font = ['Meiryo',8], size = (12,1), pad = ((0,30),(10,0)), key = '-ok_btn-'),
                 self.psg.Button(button_text = 'Cancel', font = ['Meiryo',8], size = (12,1), pad = ((0,0),(10,0)), key = '-cancel_btn-')]
                
                ]

        return self.psg.Window(self.window_title + ' - カバーアートの編集', edit_disclist_layout, icon = self.icon_path, size = (500,360), font = ['Meiryo',10], element_justification = 'c', modal = True)

    def lo_edit_window(self, coverart_type_list, coverart_rs_bytedata, gs_default_editkey):

        coverart_image = [

                [self.psg.Image(data = coverart_rs_bytedata[0], pad = ((0,0),(40,0)), key = '-coverart_data_key-')]

                ]
        
        coverart_col = [

                [self.psg.Frame(title = 'カバーアート', layout = coverart_image, size = (330,320), element_justification = 'c')],
                [self.psg.Button(button_text = 'カバーアートの更新', font = ['Meiryo',8], size = (20,1), pad = ((0,0),(10,0)), key = '-load_coverart-')]

                ]

        edit_layout = [

                [self.psg.Listbox(values = coverart_type_list, size = (30,18), pad = ((0,0),(20,0)), default_values = coverart_type_list[0], enable_events = True, sbar_relief = 'RELIEF_FLAT', sbar_trough_color = '#000000', sbar_background_color = '#222222', select_mode = [self.psg.LISTBOX_SELECT_MODE_SINGLE], key = '-coverarttype_list-'),
                 self.psg.Column(coverart_col, element_justification = 'center', pad = ((20,0),(20,0)))],

                [self.psg.Text(text = str(len(coverart_type_list)) + '件のカバーアートが登録されています', pad = ((0,0),(20,0)))],

                [self.psg.Text(text = '編集キー', pad = ((0,0),(15,0)), font = ['Meiryo',8], justification = 'center')],
                [self.psg.Input(default_text = gs_default_editkey, size = (30,1), pad = ((0,0),(5,0)), key = '-editkey_input-')],

                [self.psg.Button(button_text = 'このカバーアートを削除', font = ['Meiryo',8], size = (26,1), pad = ((0,30),(20,0)), key = '-delete_btn-'),
                 self.psg.Button(button_text = 'Cancel', font = ['Meiryo',8], size = (12,1), pad = ((0,0),(20,0)), key = '-cancel_btn-')]
                
                ]

        return self.psg.Window(self.window_title + ' - カバーアートの編集', edit_layout, icon = self.icon_path, size = (700,580), font = ['Meiryo',10], element_justification = 'c', modal = True)

    def lo_detail_window(self, disc_info, detail_tabel_header, detail_data, all_seconds):

        detail_layout = [

                [self.psg.Text(text = 'ディスクの詳細', font = ['Meiryo',12], pad = ((0,0),(10,10)))],

                [self.psg.Text(text = 'DiscID: ' + disc_info.id, pad = ((0,0),(10,0)))],
                [self.psg.Button(button_text = 'コピー', font = ['Meiryo',7], size = (10,1), pad = ((0,0),(5,10)), key = '-copy_discid-')],
                [self.psg.Text(text = '合計セクタ: ' + str(disc_info.sectors), pad = ((0,0),(10,0)))],
                [self.psg.Text(text = '合計再生時間: ' + all_seconds, pad = ((0,0),(10,0)))],
                [self.psg.Text(text = '合計再生時間(秒): ' + str(disc_info.seconds) + 's', pad = ((0,0),(10,0)))],

                [self.psg.Table(detail_data, headings = detail_tabel_header, auto_size_columns = False, font = ['Meiryo',10], size = (24,12), pad = ((0,0),(20,0)), key = '-ok_btn-')],

                [self.psg.Button(button_text = 'OK', font = ['Meiryo',8], size = (16,1), pad = ((0,0),(20,0)), key = '-ok_comp_btn-')]
                
                ]

        return self.psg.Window(self.window_title + ' - ディスクの詳細', detail_layout, icon = self.icon_path, size = (600,570), font = ['Meiryo',10], element_justification = 'c', modal = True)

    def lo_setting_window(self, window_title_raw, software_version, setting_menu_list, library_list, setting_theme_list, general_setting_dict):

        setting_general_frame = [

                [self.psg.Text(text = 'テーマ (再起動時に適用されます)', font = ['Meiryo',8], pad = ((0,0),(90,0))),
                 self.psg.Combo(setting_theme_list, default_value = general_setting_dict['themename'], font = ['Meiryo',8], size = (12,1), pad = ((10,0),(90,0)), readonly = True, key = '-theme_combo-')],

                [self.psg.Text(text = 'デフォルトの編集キー', font = ['Meiryo',8], pad = ((0,0),(15,0))),
                 self.psg.Input(default_text = general_setting_dict['editkey'], size = (24,1), pad = ((10,0),(13,0)), key = '-default_editkey_input-')],

                [self.psg.Text(text = '保存先を指定', font = ['Meiryo',8], pad = ((0,0),(30,0)))],
                [self.psg.Input(default_text = general_setting_dict['savefolder'], size = (40,1), pad = ((0,0),(5,0)), key = '-get_folder_input-')],
                [self.psg.Button(button_text = '参照', font = ['Meiryo',8], size = (8,1), pad = ((0,0),(10,0)), key = '-get_folder_btn-')],

                [self.psg.Checkbox(text = '起動時に自動でアップデートを確認する', default = bool(general_setting_dict['start_update_check']), font = ['Meiryo',8], auto_size_text = True, pad = ((0,0),(30,0)), key = '-start_update_check-')]

                ]

        setting_info_frame = [

                [self.psg.Image(filename = 'mincar_data/img/mincar_logo_info.png', pad = ((0,0),(65,5)))],
                [self.psg.Text(text = window_title_raw, font = ['Meiryo',12], pad = ((0,0),(10,0)))],
                [self.psg.Text(text = 'version ' + software_version, font = ['Meiryo',8], pad = ((0,0),(2,0)))],
                [self.psg.Text(text = 'Developed by Cube', font = ['Meiryo',10], pad = ((0,0),(10,0)))],
                [self.psg.Text(text = library_list, font = ['Meiryo',8], pad = ((0,0),(10,0)))],
                [self.psg.Text(text = 'https://github.com/CubeZeero/Mincar', enable_events = True, font = ['Meiryo',8,'underline'], pad = ((0,0),(10,0)), key = '-homepage-')],
                [self.psg.Button(button_text = 'アップデートの確認', font = ['Meiryo',8], size = (24,1), pad = ((0,0),(20,0)), key = '-update_check_btn-')]

                ]

        setting_layout = [

                [self.psg.Listbox(values = setting_menu_list, size = (20,20), default_values = setting_menu_list[0], sbar_relief = 'RELIEF_FLAT', sbar_trough_color = '#000000', sbar_background_color = '#222222', enable_events = True, select_mode = [self.psg.LISTBOX_SELECT_MODE_SINGLE], key = '-listbox_menu-'),
                 self.psg.Frame('一般設定', setting_general_frame, title_location = self.psg.TITLE_LOCATION_TOP, size = (450,420), element_justification = 'center', key = setting_menu_list[0], visible = True),
                 self.psg.Frame('情報', setting_info_frame, title_location = self.psg.TITLE_LOCATION_TOP, size = (450,420), element_justification = 'center', key = setting_menu_list[1], visible = False)],

                [self.psg.Button(button_text = 'OK', font = ['Meiryo',8], size = (12,1), pad = ((0,30),(15,0)), key = '-ok_btn-'),
                 self.psg.Button(button_text = 'Cancel', font = ['Meiryo',8], size = (12,1), pad = ((0,0),(15,0)), key = '-cancel_btn-')]
                
                ]

        return self.psg.Window(self.window_title + ' - 設定', setting_layout, icon = self.icon_path, size = (600,490), font = ['Meiryo',10], element_justification = 'c', modal = True)