import math

import pygame
import pygame.gfxdraw

from model import Model
from player import Player

class Camera(object):
    def __init__(self, x, y, width, height, scale=1):
        # top left point of camera box
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.scale = 1

    def set_center(self, pos):
        self.x = pos[0] - self.width/2
        self.y = pos[1] + self.height/2
        # return pos[0]*self.scale - self.width//2, pos[1]*self.scale + self.height/2  

    def adjust(self, pos):
        # return self.x - pos[0]*self.scale, self.y - pos[1]*self.scale  
        return  pos[0]*self.scale - self.x, self.y - pos[1]*self.scale


class View():
    TEXT_COLOR = (0, 0, 0)
    BACKGROUND_COLOR = (242, 251, 255)
    GRID_COLOR = (226, 234, 238)
    def __init__(self, width, height, model):
        self.width, self.height = width, height
        self.model = model
        self.camera = Camera(0, 0, self.width, self.height)
        self.fps = 30
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.width, self.height))

    def redraw(self):
        self.screen.fill(View.BACKGROUND_COLOR)
        self.draw_grid()
        for cell in self.model.cells:
            self.draw_object(cell)
        self.draw_object(self.model.player)

    def draw_grid(self, step=25):
        world_size = self.model.world_size
        for i in range(-world_size, world_size+step, step):
            start_coord = (-world_size, i)
            end_coord = (world_size, i)
            pygame.draw.line(
                self.screen, 
                View.GRID_COLOR, 
                self.camera.adjust(start_coord), 
                self.camera.adjust(end_coord), 
                2)
            pygame.draw.line(
                self.screen, 
                View.GRID_COLOR, 
                self.camera.adjust(start_coord[::-1]), 
                self.camera.adjust(end_coord[::-1]), 
                2)

    def draw_object(self, obj):
        # draw filled circle
        pygame.draw.circle(
            self.screen,
            obj.color,
            self.camera.adjust(obj.pos),
            obj.radius)
        # draw circle border
        pygame.draw.circle(
            self.screen,
            obj.border_color,
            self.camera.adjust(obj.pos),
            obj.radius,
            obj.BORDER_WIDTH)
        # show nickname
        if isinstance(obj, Player):
            self.draw_text(
                obj.nick, 
                self.camera.adjust(obj.pos), 
                align_center=True)

    def draw_text(self, text, pos, color=TEXT_COLOR, font_size=18, align_center=False):
        # select font
        font = pygame.font.Font(pygame.font.get_default_font(), font_size)
        # render text
        surface = font.render(text, True, color)
        pos = list(pos)
        if align_center:
            # define the center
            pos[0] -= surface.get_width() // 2
            pos[1] -= surface.get_height() // 2
        self.screen.blit(surface, pos)
        
    def start(self):
        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    exit()

            # print(self)
            self.model.move(*(self.mouse_pos_to_polar()))
            self.camera.set_center(self.model.player.pos)
            self.redraw()
            pygame.display.flip()
            self.clock.tick(self.fps)

    def mouse_pos_to_polar(self):
        # convert mouse position to polar vector
        x, y = pygame.mouse.get_pos()
        # center offset 
        x -= self.width/2
        y = self.height/2 - y

        angle = math.atan2(y, x)
        speed = math.sqrt(x**2 + y**2)
        # setting radius of speed change zone
        speed_bound = 0.8*min(self.width/2, self.height/2)
        # normalize speed
        speed = speed_bound if speed > speed_bound else speed / speed_bound
        return angle, speed


world_size = 400
cell_num = 100
p = Player.make_random("Jetraid", world_size)
m = Model(p, world_size)
m.spawn_cells(cell_num)
v = View(900, 600, m)
v.start()