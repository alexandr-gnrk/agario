import socketserver
from loguru import logger


class UDPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = self.request[0].strip()
        socket = self.request[1]

        client_str = (self.client_address[0] + ':' 
            + str(self.client_address[1]))
        logger.info('{} received from {}'.format(data, client_str))
        
        logger.info('Sending {} to {}'.format(data, client_str))
        socket.sendto(data, self.client_address)


HOST, PORT = 'localhost', 9999
with socketserver.UDPServer((HOST, PORT), UDPHandler) as server:
    logger.info('Server started at {}:{}'.format(HOST, PORT))
    server.serve_forever()