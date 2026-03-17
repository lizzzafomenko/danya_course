import asyncio 

from argparse import ArgumentParser


# https://docs.python.org/3/library/asyncio-protocol.html

import zlib
import random
import math
import hashlib

class GuessingGame:
    def __init__(self, IP):
        # init the game
        self.IP = IP
        self.crc32 = zlib.crc32(str(IP).encode())
        random.seed(self.crc32)
        self.upper_bound = random.randint(100, 1000)
        self.target = random.randint(1, self.upper_bound)
        self.num_tries = int(math.log2(self.upper_bound)) + 1
        self.win_key = self.IP + str(self.target)
        self.win_key = hashlib.sha256(self.win_key.encode()).hexdigest()
        self.winner = False

    def get_range(self):
        return f'WLCM {1} {self.upper_bound}'
    
    def check(self, number):
        try:
            number = int(number)
        except:
            return f'Invalid guess {number}'
        if self.winner:
            return "You're already a winner bro"
        if number == self.target:
            self.winner = True
            return f'BING {self.win_key}'
        self.num_tries -= 1
        if self.num_tries == 0:
            return 'FAIL'
        if number > self.target:
            return 'LESS'
        return 'MORE'


class GTTP_server:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.active_games = {}
        self.transport = None
    
    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, data, client_address):
        command = data.decode()
        server_answer = self._get_client_command(command, client_address)
        self.transport.sendto(server_answer.encode(), client_address)

    def _get_client_command(self, command, client_address):
        client_address = f"{client_address[0]}:{client_address[1]}"
        if client_address in self.active_games:
            answer = self._command_parser(command, client_address)
            return answer
        else:
            if command.split()[0] == 'HELO':
                game = GuessingGame(client_address)
                self.active_games[client_address] = game
                return game.get_range()
            else:
                return f'Invalid command {command}'
    
    def _command_parser(self, command, client_address): 
        try:
            message, guess = command.split()
            if message == 'GUES':
                answer = self.active_games[client_address].check(guess)
                if answer == 'FAIL':
                    del self.active_games[client_address]
                return answer
            return f'Invalid command {command}'
        except:
            return f'Invalid command {command}'
        

async def serverok(ip, port):
    loop = asyncio.get_running_loop()

    transport, protocol = await loop.create_datagram_endpoint(
        lambda: GTTP_server(ip, port),
        local_addr=(ip, port))
    try:
        # await asyncio.sleep(3600)  # Serve for 1 hour. 
        await asyncio.Future()
    finally:
        transport.close()

parser = ArgumentParser()
parser.add_argument('--ip', '-ip', help='IP')
parser.add_argument('--port', '-p', type=int, help='Server port')
args = parser.parse_args()

asyncio.run(serverok(args.ip, args.port))