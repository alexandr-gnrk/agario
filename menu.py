from functools import partial 

import pygame_menu


def create_menu(width, height, connect_func):
    MENU_WIDTH, MENU_HEIGHT = width, height
    MENU_VERTICAL_MARGIN = 25
    HELP = (
        '*Some useful information*',
        '*Another useful information*',
        '*Press smth to kill me*')
    ABOUT = (
        'Python implementation of game agar.io',
        'Authors: @alexandr-gnrk & @vanyabondar',
        '',
        'Github: github.com/alexandr-gnrk/agario')
    # creating theme for main menu
    main_theme = pygame_menu.themes.THEME_DARK.copy()
    # main_theme.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_NONE
    # main_theme.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_TITLE_ONLY_DIAGONAL  
    main_theme.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_ADAPTIVE
    main_theme.widget_selection_effect = pygame_menu.widgets.NoneSelection()


    # creating start menu
    start_menu = pygame_menu.Menu(
        theme=main_theme,
        height=MENU_HEIGHT,
        width=MENU_WIDTH,
        onclose=pygame_menu.events.RESET,
        title='Start')
    start_menu.add_text_input('Server address:   ',
        default='localhost:9999',
        maxwidth=14,
        textinput_id='addr',
        input_underline='_')
    start_menu.add_vertical_margin(MENU_VERTICAL_MARGIN)
    start_menu.add_button(
        'Connect', 
        partial(
            connect_func, 
            start_menu.get_input_data()['addr']))
    start_menu.add_button('Back', pygame_menu.events.RESET)


    # creating help menu
    help_menu = pygame_menu.Menu(
        theme=main_theme,
        height=MENU_HEIGHT,
        width=MENU_WIDTH,
        onclose=pygame_menu.events.RESET,
        title='Help')
    for line in HELP:
        help_menu.add_label(line)
    help_menu.add_vertical_margin(MENU_VERTICAL_MARGIN)
    help_menu.add_button('Back', pygame_menu.events.RESET)


    # creating about menu
    about_menu = pygame_menu.Menu(
        theme=main_theme,
        height=MENU_HEIGHT,
        width=MENU_WIDTH,
        onclose=pygame_menu.events.RESET,
        title='About')
    for line in ABOUT:
        about_menu.add_label(line)
    about_menu.add_vertical_margin(MENU_VERTICAL_MARGIN)
    about_menu.add_button('Back', pygame_menu.events.RESET)


    # creating main menu
    main_menu = pygame_menu.Menu(
        enabled=True,
        theme=main_theme,
        height=MENU_HEIGHT,
        width=MENU_WIDTH,
        onclose=pygame_menu.events.EXIT,
        title='Main menu')
    main_menu.add_button(start_menu.get_title(), start_menu)
    main_menu.add_button(help_menu.get_title(), help_menu)
    main_menu.add_button(about_menu.get_title(), about_menu)
    main_menu.add_button('Exit', pygame_menu.events.EXIT)

    return main_menu