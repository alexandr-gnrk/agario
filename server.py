import socketserver
import pickle

from loguru import logger
import pygame

from game import Model
from game.entities import Player
from msgtype import MsgType


bounds = [1000, 1000]
cell_num = 100
players = list()
model = Model(players, bounds)
model.spawn_cells(cell_num)
last_id = 0

clients = dict()

p = Player.make_random("Jetraid", bounds)

class UDPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        # getting request
        msg = pickle.loads(self.request[0])
        msgtype = msg['type']
        data = msg['data']

        global clients
        global model
        global bounds

        if msgtype == MsgType.CONNECT:
            nick = data
            logger.debug('Recieved {!r} from {}'.format(nick, self.client_address))
            
            # make new player with recievd nickname
            new_player = Player.make_random(nick, bounds)

            # sending created player to client
            data = pickle.dumps(new_player)
            logger.debug('Sending {!r} to {}'.format(data, self.client_address))
            socket = self.request[1]
            socket.sendto(data, self.client_address)

            # add client to list of clients
            clients[self.client_address] = new_player
            # add player to game model
            model.players.append(new_player)
        elif msgtype == MsgType.UPDATE:
            mouse_pos = data['mouse_pos']
            keys = data['keys']

            # define player according to client address
            player = clients[self.client_address]

            # simulate player actions
            for key in keys:
                if key == pygame.K_w:
                    model.shoot(
                        player,
                        mouse_pos[0])
                elif key == pygame.K_SPACE:
                    model.split(
                        player,
                        mouse_pos[0])
            # update player velocity and update model state
            model.update_velocity(player, *mouse_pos)
            model.update()

            # send player state and game model state to client
            data = pickle.dumps({
                'player': player,
                'model': model
            })
            socket = self.request[1]
            socket.sendto(data, self.client_address)


HOST, PORT = 'localhost', 9999
with socketserver.UDPServer((HOST, PORT), UDPHandler) as server:
    logger.info('Server started at {}:{}'.format(HOST, PORT))
    server.serve_forever()