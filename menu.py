from functools import partial 

import pygame_menu


class MyMenu():
    MENU_VERTICAL_MARGIN = 25
    HELP = (
        'Control keys',
        '',
        'Press "W" key to shoot',
        'Press "Space" to split into two parts')
    ABOUT = (
        'Python implementation of game agar.io',
        'Authors: @alexandr-gnrk & @vanyabondar',
        '',
        'Github: github.com/alexandr-gnrk/agario')

    def __init__(self, width, height):
        self.width = width
        self.height = height

        # creating theme for main menu
        self.theme = pygame_menu.themes.THEME_DARK.copy()
        # self.theme.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_NONE
        # self.theme.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_TITLE_ONLY_DIAGONAL  
        self.theme.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_ADAPTIVE
        self.theme.widget_selection_effect = pygame_menu.widgets.NoneSelection()

        # creating start menu
        self.start_menu = pygame_menu.Menu(
            theme=self.theme,
            height=self.height,
            width=self.width,
            onclose=pygame_menu.events.RESET,
            title='Start')
        # creating help menu
        self.help_menu = pygame_menu.Menu(
            theme=self.theme,
            height=self.height,
            width=self.width,
            onclose=pygame_menu.events.RESET,
            title='Help')
        # creating about menu
        self.about_menu = pygame_menu.Menu(
            theme=self.theme,
            height=self.height,
            width=self.width,
            onclose=pygame_menu.events.RESET,
            title='About')
        # creating main menu
        self.main_menu = pygame_menu.Menu(
            # enabled=True,
            theme=self.theme,
            height=self.height,
            width=self.width,
            onclose=pygame_menu.events.EXIT,
            title='Main menu')

        self.__init_menus_with_widgets()

    def __init_menus_with_widgets(self):
        self.update_start_menu(lambda *args: None)

        for line in MyMenu.HELP:
            self.help_menu.add_label(line)
        self.help_menu.add_vertical_margin(MyMenu.MENU_VERTICAL_MARGIN)
        self.help_menu.add_button('Back', pygame_menu.events.RESET)

        for line in MyMenu.ABOUT:
            self.about_menu.add_label(line)
        self.about_menu.add_vertical_margin(MyMenu.MENU_VERTICAL_MARGIN)
        self.about_menu.add_button('Back', pygame_menu.events.RESET)
        
        self.main_menu.add_button(self.start_menu.get_title(), self.start_menu)
        self.main_menu.add_button(self.help_menu.get_title(), self.help_menu)
        self.main_menu.add_button(self.about_menu.get_title(), self.about_menu)
        self.main_menu.add_button('Exit', pygame_menu.events.EXIT)


    def update_start_menu(self, connect_callback):
        self.start_menu.clear()

        self.start_menu.add_text_input('        Nickname:   ',
            default='user',
            maxwidth=14,
            textinput_id='nick',
            input_underline='_')
        self.start_menu.add_text_input('Server address:   ',
            default='localhost:9999',
            maxwidth=14,
            textinput_id='addr',
            input_underline='_')
        self.start_menu.add_vertical_margin(MyMenu.MENU_VERTICAL_MARGIN)
        self.start_menu.add_button(
            'Connect',
            partial(
                connect_callback, 
                self.start_menu.get_input_data))
        self.start_menu.add_button('Back', pygame_menu.events.RESET)

    def get_main_menu(self):
        return self.main_menu