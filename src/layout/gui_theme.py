# -*- coding: utf-8 -*-

# Mincar
# gui_theme.py
# (C) 2022 Cube
# cubezeero@gmail.com

import sys
sys.path.append('../')
import util
import global_values as gv

def white(sg):

    white = {
		'colorname': 'white',
    	'BACKGROUND': '#ffffff',
    	'TEXT': 'black',
    	'INPUT': '#eeeeee',
    	'SCROLL': '#eeeeee',
    	'TEXT_INPUT': 'black',
    	'BUTTON': ('white', '#222222'),
    	'PROGRESS': sg.DEFAULT_PROGRESS_BAR_COLOR,
    	'BORDER': 0,
    	'SLIDER_DEPTH': 0,
    	'PROGRESS_DEPTH': 0
    }

    return white

def dark(sg):

    dark = {
		'colorname': 'dark',
    	'BACKGROUND': '#222222',
    	'TEXT': 'white',
    	'INPUT': '#1e1e1e',
    	'SCROLL': '#1e1e1e',
    	'TEXT_INPUT': '#ffffff',
    	'BUTTON': ('white', '#474747'),
    	'PROGRESS': sg.DEFAULT_PROGRESS_BAR_COLOR,
    	'BORDER': 0,
    	'SLIDER_DEPTH': 0,
    	'PROGRESS_DEPTH': 0
    }

    return dark

def theme_changer(theme_name):

	if theme_name == 'white':
		gv.menu_button_bgcolor = '#ffffff'
		gv.input_disabled_color = '#eeeeee'

		gv.default_ca = util.imageToIo('mincar_data/img/default_coverart.png')
		for iconpath in gv.icon_path_list:
			gv.icon_io_list.append(util.imageToIo(iconpath))

	else:
		gv.menu_button_bgcolor = '#222222'
		gv.input_disabled_color = '#1e1e1e'

		gv.default_ca = util.imageInvertColor('mincar_data/img/default_coverart.png')
		for iconpath in gv.icon_path_list:
			gv.icon_io_list.append(util.imageInvertColor(iconpath))
	
	return
