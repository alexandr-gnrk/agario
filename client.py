import socket
import sys
import pickle
import time

import pygame
from loguru import logger

from menu import MyMenu
from game import View
from msgtype import MsgType


WIDTH, HEIGHT = 900, 600
#WIDTH, HEIGHT = 450, 300
BACKGROUND_COLOR = (24, 26, 50)
BACKGROUND_COLOR = (40, 0, 40)


class Game():
    def __init__(self, screen):
        self.screen = screen
        self.player = None
        self.is_in_lobby = False
        self.host = None
        self.port = None
        self.addr_string = None

    def connect_to_game(self, nick, addr_string):
        self.addr_string = addr_string
        self.host, self.port = addr_string.split(':')
        self.port = int(self.port)


        try:
            # making protobuf message
            msg = pickle.dumps({
                'type': MsgType.CONNECT,
                'data': nick
                })
            # sending connect request to server
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.sendto(msg, (self.host, self.port))
            logger.debug('Sending {} to {}'.format(msg, self.addr_string))

            # getting player info from server
            data = sock.recv(4096)
            self.player = pickle.loads(data)
            logger.debug('Recieved {!r} from {}'.format(self.player, self.addr_string))
            
            view = View(self.screen, None, self.player)
            while True:
                keys = list()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        exit()
                    elif event.type == pygame.KEYDOWN:
                        keys.append(event.key)
                mouse_pos = view.mouse_pos_to_polar()
                msg = pickle.dumps({
                    'type': MsgType.UPDATE,
                    'data': {
                        'mouse_pos': mouse_pos,
                        'keys': keys,
                        },
                    })
                sock.sendto(msg, (self.host, self.port))
                data = sock.recv(2**16)
                msg = pickle.loads(data)
                view.player = msg['player']
                view.model = msg['model']
                view.redraw()
                time.sleep(1/40)



        except socket.timeout:
            logger.error('Server not responding')




socket.setdefaulttimeout(2)

# pygame initialization
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('agar.io')
# icon = pygame.image.load('./src/logo.png')
# pygame.display.set_icon(icon)

game = Game(screen)
menu = MyMenu(WIDTH*0.9, HEIGHT*0.9)
menu.update_start_menu(game.connect_to_game)
FPS = 30
clock = pygame.time.Clock()
while True:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            exit()
        # elif event.type == pygame.KEYDOWN:
        #     if event.key == pygame.K_ESCAPE:
        #         main_menu.toggle()
    
    screen.fill(BACKGROUND_COLOR)
    
    # game.update()
    if menu.get_main_menu().is_enabled():
        menu.get_main_menu().draw(screen)

    menu.get_main_menu().update(events)
    pygame.display.flip()
    clock.tick(FPS)
