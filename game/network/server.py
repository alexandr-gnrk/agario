import socketserver
import pickle

from loguru import logger
import pygame

from .msgtype import MsgType
from .. import Model
from ..entities import Player


bounds = [1000, 1000]
cell_num = 150
model = Model(list(), bounds=bounds)
model.spawn_cells(cell_num)

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
            data = pickle.dumps(new_player.id)
            logger.debug('Sending {!r} to {}'.format(data, self.client_address))
            socket = self.request[1]
            socket.sendto(data, self.client_address)

            # add client to list of clients
            clients[self.client_address] = new_player
            # add player to game model
            model.add_player(new_player)
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
            data = pickle.dumps(model.copy_for_client(player.center()))
            socket = self.request[1]
            socket.sendto(data, self.client_address)


def start(host='localhost', port=9999):
    with socketserver.UDPServer((host, port), UDPHandler) as server:
        logger.info('Server started at {}:{}'.format(host, port))
        server.serve_forever()


if __name__ == '__main__':
    start()