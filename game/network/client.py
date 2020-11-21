import socket
import sys
import pickle
import time

import pygame
from loguru import logger

from .menu import MyMenu
from .msgtype import MsgType
from .. import View


BACKGROUND_COLOR = (24, 26, 50)
BACKGROUND_COLOR = (40, 0, 40)


class GameConnection():
    def __init__(self, screen):
        self.screen = screen
        self.player_id = None
        self.is_in_lobby = False
        self.host = None
        self.port = None
        self.addr_string = None

    def connect_to_game(self, get_attrs):
        attrs = get_attrs()
        self.addr_string = attrs['addr']
        nick = attrs['nick']
        self.host, self.port = self.addr_string.split(':')
        self.port = int(self.port)

        try:
            # send nickname
            msg = pickle.dumps({
                'type': MsgType.CONNECT,
                'data': nick
                })
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.sendto(msg, (self.host, self.port))
            logger.debug('Sending {} to {}'.format(msg, self.addr_string))

            # recieving player info
            data = sock.recv(4096)
            self.player_id = pickle.loads(data)
            logger.debug('Recieved {!r} from {}'.format(self.player_id, self.addr_string))
            
            # create view to display game
            view = View(self.screen, None, None)
            while True:
                # getting list of pressed buttons
                keys = list()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        exit()
                    elif event.type == pygame.KEYDOWN:
                        keys.append(event.key)
                # get mouse position (velocity vector)
                mouse_pos = view.mouse_pos_to_polar()
                # sending velocity vector and list of pressed keys
                msg = pickle.dumps({
                    'type': MsgType.UPDATE,
                    'data': {
                        'mouse_pos': mouse_pos,
                        'keys': keys,
                        },
                    })
                sock.sendto(msg, (self.host, self.port))

                # getting current player and game model state
                data = sock.recv(2**16)
                msg = pickle.loads(data)

                # update view and redraw
                view.player = None
                view.model = msg
                for pl in view.model.players:
                    if pl.id == self.player_id:
                        view.player = pl
                        break

                if view.player is None:
                    logger.debug("Player was killed!")
                    return

                view.redraw()
                time.sleep(1/40)
        except socket.timeout:
            logger.error('Server not responding')


def start(width=900, height=600):
    socket.setdefaulttimeout(2)

    # pygame initialization
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('agar.io')
    icon = pygame.image.load('./img/logo.png')
    pygame.display.set_icon(icon)

    # init class with game connection
    gameconn = GameConnection(screen)
    # create menu
    menu = MyMenu(width*0.9, height*0.9)
    # bind connection method to menu button
    menu.update_start_menu(gameconn.connect_to_game)
    FPS = 30
    clock = pygame.time.Clock()

    # start pygame loop
    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()
        
        screen.fill(BACKGROUND_COLOR)
        
        if menu.get_main_menu().is_enabled():
            menu.get_main_menu().draw(screen)
        menu.get_main_menu().update(events)
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    start()