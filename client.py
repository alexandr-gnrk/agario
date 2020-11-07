import socket
import sys

import pygame
from loguru import logger

import menu


WIDTH, HEIGHT = 900, 600
BACKGROUND_COLOR = (24, 26, 50)
BACKGROUND_COLOR = (40, 0, 40)

def connect(addr_string):
    host, port = addr_string.split(':')
    port = int(port)
    print(host, port)

# pygame initialization
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('agar.io')
# icon = pygame.image.load('./src/logo.png')
# pygame.display.set_icon(icon)

main_menu = menu.create_menu(WIDTH*0.9, HEIGHT*0.9, connect)

while True:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            exit()
        # elif event.type == pygame.KEYDOWN:
        #     if event.key == pygame.K_ESCAPE:
        #         main_menu.toggle()
    
    screen.fill(BACKGROUND_COLOR)
    
    if main_menu.is_enabled():
        main_menu.draw(screen)

    main_menu.update(events)
    pygame.display.flip()
