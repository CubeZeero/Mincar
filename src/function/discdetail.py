# -*- coding: utf-8 -*-

# Mincar
# discdetail.py
# (C) 2022 Cube
# cubezeero@gmail.com

import PySimpleGUI as psg
import pyperclip
import datetime

import sys
sys.path.append('../')
import software_info
import discid

def function_discdetail(gui_layout):

    detail_tabel_header = ['Number', 'Seconds', 'Sectors', 'Length', 'Offset']
    detail_data = []

    try:
        current_disc_info = discid.read()

    except discid.DiscError:
        psg.popup_ok('ディスクの読み込み時にエラーが発生しました\nディスク本体が挿入されているか確認してください', title = software_info.Software_Name_All(), icon = software_info.Icon_Path(), modal = True, keep_on_top = True)

    else:
        for track in current_disc_info.tracks : detail_data.append([str(track.number), str(track.seconds), str(track.sectors), str(track.length), str(track.offset)])
        
        detail_window = gui_layout.lo_detail_window(current_disc_info, detail_tabel_header, detail_data, str(datetime.timedelta(seconds = current_disc_info.seconds)))

        while True:
            detail_event, detail_values = detail_window.read()

            if detail_event == psg.WIN_CLOSED or detail_event == '-ok_comp_btn-' : break

            if detail_event == '-copy_discid-' : pyperclip.copy(current_disc_info.id)

        detail_window.close()
    
    return