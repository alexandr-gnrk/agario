import argparse


parser = argparse.ArgumentParser(
    description="Python implementation of game agar.io")
parser.add_argument(
    '-wt', '--width',
    dest='width',
    type=int,
    default=900,
    help='screen width')
parser.add_argument(
    '-ht', '--height',
    dest='height',
    type=int,
    default=600,
    help='screen height')
parser.add_argument(
    '-s', '--server',
    action='store_true',
    dest='server',
    help='start game server')
parser.add_argument(
    '-p', '--port',
    dest='port',
    type=int,
    default=9999,
    help='port number for server')

args = parser.parse_args()

if args.server:
    import game.network.server as server
    server.start(host='0.0.0.0', port=args.port)
else:
    import game.network.client as client
    client.start(args.width, args.height)