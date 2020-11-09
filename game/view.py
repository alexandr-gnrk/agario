import math

import pygame
import pygame.gfxdraw

from model import Model
from player import Player

class Camera(object):
    """Class that converts cartesian pos to pixel pos on the screen."""

    def __init__(self, x, y, width, height, scale=1):
        # top left point of camera box
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.scale = 1

    def set_center(self, pos):
        """Change camera postion according to passed center."""
        self.x = pos[0] - self.width/2
        self.y = pos[1] + self.height/2

    def adjust(self, pos):
        """Convert cartesian pos to pos relative to the camera."""
        return  pos[0]*self.scale - self.x, self.y - pos[1]*self.scale


class View():
    """"Class that displays model state and shows HUD"""

    TEXT_COLOR = (50, 50, 50)
    HUD_BACGROUND_COLOR = (50,50,50,80)
    BACKGROUND_COLOR = (242, 251, 255)
    GRID_COLOR = (226, 234, 238)
    HUD_PADDING = (3, 3)
    FONT_SIZE = 18

    def __init__(self, width, height, model, player):
        self.width, self.height = width, height
        self.model = model
        self.player = player
        self.camera = Camera(0, 0, self.width, self.height)
        self.fps = 30
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.hud_surface = pygame.Surface((1, 1), pygame.SRCALPHA)
        self.hud_surface.fill(View.HUD_BACGROUND_COLOR)
        self.font = pygame.font.Font(pygame.font.get_default_font(), 18)

    def redraw(self):
        """Redraw screen according to model of game."""
        self.screen.fill(View.BACKGROUND_COLOR)
        self.draw_grid()
        for obj in self.model.objects:
            self.draw_object(obj)
        # self.draw_object(self.model.player)
        self.draw_hud((8, 5))
    
    def draw_grid(self, step=25):
        """Draw grid on screen with passed step."""
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
        """Draw passed object on the screen. Object could be Cell or Player."""
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
        # show nickname if obj is a Player
        if isinstance(obj, Player):
            self.draw_text(
                self.screen,
                obj.nick, 
                self.camera.adjust(obj.pos), 
                align_center=True)

    def draw_text(self, surface, text, pos, color=TEXT_COLOR, align_center=False):
        """Draw passed text on passed surface."""
        text_surface = self.font.render(text, True, color)
        pos = list(pos)
        if align_center:
            # offset pos if was passed center
            pos[0] -= text_surface.get_width() // 2
            pos[1] -= text_surface.get_height() // 2
        surface.blit(text_surface, pos)

    def draw_hud(self, padding):
        """Draw score and top players HUDs."""
        # draw score HUD item
        score_text = 'Score: {:6}'.format(int(self.player.radius))
        self.draw_hud_item(
             (15, self.height - 30 - 2*padding[1]),
             (score_text,),
             10,
             padding)
        # draw leaderboard HUD item
        lines = list()
        lines.append('Leaderboard')
        top10 = sorted(
            self.model.players,
            key=lambda pl: pl.radius,
            reverse=True)[:10]
        for i, player in enumerate(top10):
            lines.append('{}. {}'.format(i + 1, player.nick))
        self.draw_hud_item(
             (self.width - 150, 15),
             lines,
             10,
             padding)

    def draw_hud_item(self, pos, lines, maxchars, padding):
        """Draw HUD item with passed string lines."""
        # seacrh max line width
        max_width = max(map(lambda line: self.font.size(line)[0], lines))
        font_height = self.font.get_height()
        # size of HUD item background
        item_size = (
            max_width + 2*padding[0], 
            font_height*len(lines) + 2*padding[1])
        # scaling transparent HUD background
        item_surface = pygame.transform.scale(self.hud_surface, item_size)
        # draw each line
        for i, line in enumerate(lines):
            self.draw_text(
                item_surface,
                line,
                (padding[0], padding[1] + font_height*i))
        # bilt on main surface
        self.screen.blit(item_surface, pos)
    
    def start(self):
        """Start game loop."""
        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        self.model.shoot(
                            self.player,
                            self.mouse_pos_to_polar()[0])

            # print(self)
            self.model.update_velocity(
                self.player,
                *(self.mouse_pos_to_polar()))
            self.model.update()
            self.camera.set_center(self.player.pos)
            self.redraw()
            pygame.display.flip()
            self.clock.tick(self.fps)

    def mouse_pos_to_polar(self):
        """Convert mouse position to polar vector."""
        x, y = pygame.mouse.get_pos()
        # center offset 
        x -= self.width/2
        y = self.height/2 - y
        # get angle and length(speed) of vector
        angle = math.atan2(y, x)
        speed = math.sqrt(x**2 + y**2)
        # setting radius of speed change zone
        speed_bound = 0.8*min(self.width/2, self.height/2)
        # normalize speed
        speed = speed_bound if speed > speed_bound else speed/speed_bound
        return angle, speed


world_size = 1000
cell_num = 100
p = Player.make_random("Jetraid", world_size)
p._radius = 80
players = [
    p,
    Player.make_random("Sobaka", world_size),
    Player.make_random("Kit", world_size),
    Player.make_random("elohssa", world_size),
]
m = Model(players, world_size)
m.spawn_cells(cell_num)
v = View(900, 600, m, p)
v.start()