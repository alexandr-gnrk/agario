import math
import time

import pygame
import pygame.gfxdraw

from . import gameutils as gu
from .model import Model
from .entities import Player


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
    MESSAGE_COLOR = (255, 0, 0)
    GRID_COLOR = (226, 234, 238)
    HUD_PADDING = (3, 3)
    FONT_SIZE = 18
    MESSAGE_EXPIRE_TIME = 5

    DEBUG_COLOR = (255, 0, 0)

    def __init__(self, screen, model, player, debug=False):
        self.screen = screen
        self.width, self.height = self.screen.get_size()
        self.model = model
        self.player = player
        self.debug = debug
        self.camera = Camera(0, 0, self.width, self.height)
        self.fps = 30
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.hud_surface = pygame.Surface((1, 1), pygame.SRCALPHA)
        self.hud_surface.fill(View.HUD_BACGROUND_COLOR)
        self.font = pygame.font.Font(pygame.font.get_default_font(), 18)

    def redraw(self):
        """Redraw screen according to model of game."""
        self.camera.set_center(self.player.center())
        self.screen.fill(View.BACKGROUND_COLOR)
        self.draw_grid()
        for cell in self.model.cells:
            self.draw_cell(cell)
        for player in self.model.players:
            self.draw_player(player)
        # self.draw_object(self.model.player)
        self.draw_hud((8, 5))
        if self.debug:
            self.draw_debug_info()
        self.draw_messages()
        pygame.display.flip()

    def draw_messages(self):
        if time.time() - self.model.round_start <= self.MESSAGE_EXPIRE_TIME:
            self.draw_text(
                self.screen,
                "New round started!",
                [self.width // 2, self.height // 2 * 0.1],
                self.MESSAGE_COLOR,
                align_center=True)  

    def draw_grid(self, step=25):
        """Draw grid on screen with passed step."""
        world_size = self.model.bounds[0]
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

    def draw_cell(self, cell):
        """Draw passed cell on the screen"""
        # draw filled circle
        pygame.draw.circle(
            self.screen,
            cell.color,
            self.camera.adjust(cell.pos),
            cell.radius)
        
        # draw circle border
        if cell.BORDER_WIDTH != 0:
            pygame.draw.circle(
                self.screen,
                gu.make_border_color(cell.color),
                self.camera.adjust(cell.pos),
                cell.radius,
                cell.BORDER_WIDTH)

    def draw_player(self, player):
        """Draw passed player on the screen."""
        for cell in player.parts:
            # draw player part
            self.draw_cell(cell)
            # draw nickname on top of the part
            self.draw_text(
                self.screen,
                player.nick,
                self.camera.adjust(cell.pos),
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
        score_text = 'Score: {:6}'.format(int(self.player.score()))
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
            key=lambda pl: pl.score(),
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
                    elif event.key == pygame.K_SPACE:
                        self.model.split(
                            self.player,
                            self.mouse_pos_to_polar()[0])

            self.model.update_velocity(
                self.player,
                *(self.mouse_pos_to_polar()))
            self.model.update()
            self.redraw()
            self.clock.tick(self.fps)

    def draw_debug_info(self):
        """Draw debug information on the screen."""
        # draw player center
        pygame.draw.circle(
            self.screen, 
            self.DEBUG_COLOR,
            self.camera.adjust(self.player.center()), 
            5)
        # draw velocity vectors of player parts
        for cell in self.player.parts:
            dx, dy = gu.polar_to_cartesian(cell.angle, cell.speed*100)
            x, y = cell.pos
            self.draw_vector(x, y, dx, dy, self.DEBUG_COLOR)

    def draw_vector(self, x, y, dx, dy, color):
        """Draw passed vector on the screen."""
        pygame.draw.line(
            self.screen,
            color,
            self.camera.adjust([x, y]),
            self.camera.adjust([x+dx, y+dy]))
        pygame.draw.circle(
            self.screen,
            color,
            self.camera.adjust([x+dx, y+dy]),
            3)

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
        speed = 1 if speed >= speed_bound else speed/speed_bound
        return angle, speed

if __name__ == '__main__':
    bounds = [1000, 1000]
    cell_num = 100
    
    p = Player.make_random("Jetraid", bounds)
    p.parts[0].radius = 100
    players = [
        Player.make_random("Sobaka", bounds),
        Player.make_random("Kit", bounds),
        Player.make_random("elohssa", bounds),
        p,
    ]
    m = Model(players, bounds=bounds)
    m.spawn_cells(cell_num)

    pygame.init()
    screen = pygame.display.set_mode((900, 600))

    v = View(screen, m, p, debug=True)
    v.start()
