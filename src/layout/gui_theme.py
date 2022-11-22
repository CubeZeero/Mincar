# -*- coding: utf-8 -*-

# Mincar
# gui_theme.py
# (C) 2022 Cube
# cubezeero@gmail.com

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
