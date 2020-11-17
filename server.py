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
            
            new_player = Player.make_random(nick, bounds)

            data = pickle.dumps(new_player)
            logger.debug('Sending {!r} to {}'.format(data, self.client_address))
            socket = self.request[1]
            socket.sendto(data, self.client_address)

            clients[self.client_address] = new_player
            model.players.append(new_player)
        elif msgtype == MsgType.UPDATE:
            mouse_pos = data['mouse_pos']
            keys = data['keys']
            player = clients[self.client_address]

            for key in keys:
                if key == pygame.K_w:
                    model.shoot(
                        player,
                        mouse_pos[0])
                elif key == pygame.K_SPACE:
                    model.split(
                        player,
                        mouse_pos[0])
            model.update_velocity(player, *mouse_pos)
            model.update()

            data = pickle.dumps({
                'player': player,
                'model': model
            })
            socket = self.request[1]
            socket.sendto(data, self.client_address)
            

    def connect_player(self, message):
        # making new player
        global last_id
        global players
        last_id += 1
        new_player = pb.Player()
        new_player.id = last_id
        new_player.nick = message.nick
        new_player.status = pb.LobbyStatus.NOT_READY
        players.append(new_player)
        print(players)

        # response to the client with new player
        socket = self.request[1]
        data = new_player.SerializeToString()
        logger.debug('Sending {} to {}'.format(data, self.client_address))
        socket.sendto(data, self.client_address)

    def update_lobby(self, message):
        global players
        print(players)
        lobby = pb.Lobby()
        for player in players:
            player_pb = lobby.players.add()
            player_pb = player

        print(lobby)

        # response to the client with lobby
        socket = self.request[1]
        data = lobby.SerializeToString()
        print(data)
        logger.debug('Sending {} to {}'.format(data, self.client_address))
        socket.sendto(data, self.client_address)

HOST, PORT = 'localhost', 9999
with socketserver.UDPServer((HOST, PORT), UDPHandler) as server:
    logger.info('Server started at {}:{}'.format(HOST, PORT))
    server.serve_forever()