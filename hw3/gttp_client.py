from socket import socket, AF_INET, SOCK_DGRAM
from argparse import ArgumentParser

# примеры сервера и клиента: https://medium.com/@pikotutorial/udp-client-server-with-python-5a5498956dd5

class GTTP_client:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.client = socket(AF_INET, SOCK_DGRAM)

    def interact_with_server(self, command, num_sends = 10):
        if command == '\n' or command == '':
            return 'Provide valid command :)' 
        if command.split()[0] == 'HELO':
            if len(command.split()) > 1:
                if float(command.split()[1]):
                    self.client.settimeout(float(command.split()[1]))
        
        for _ in range(num_sends):
            try:
                self.client.sendto(command.encode(), (self.ip, self.port))
                server_answer, _ = self.client.recvfrom(1024)
                return server_answer.decode()
            except:
                print(f'Timeout exceeded. Reconnecting attempt {_}/{num_sends}...')
        return 'Server does not respond'

parser = ArgumentParser()
parser.add_argument('--ip', '-ip', help='IP')
parser.add_argument('--port', '-p', type=int, help='Server port')
# parse command line options
args = parser.parse_args()

gttp = GTTP_client(args.ip, args.port)

while True:
    server_answer = gttp.interact_with_server(input())
    print(server_answer)
