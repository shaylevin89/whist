import socket
from whist import CardGame
import select
from threading import Thread
from time import sleep


# עד פה זה יחסית עבד!!!!
# TODO מתחיל לעבוד על הצ'אט החדש. אחרי שעבדתי על צ'אט ישן עם באגים. כרגע ידיים חולקו לפעמים כמו שצריך ולפעמים לא.

class Merkazia:
    def __init__(self):
        self.game = CardGame()
        self.game.make_final()
        self.playerlst = [self.game.final1, self.game.final2, self.game.final3, self.game.final4]
        self.deck = []
        for i in range(4):
            self.deck.extend(self.playerlst[i])
        self.sdeck = ' '.join(self.deck)
        self.addresses = {}  # new chat
        self.clients = {}  # List of connected clients - socket as a key, user header and name as data
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a TCP/IP socket
        self.server_address = ('', 15432)  # Bind the socket to the port
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(self.server_address)
        self.sock.listen(8)  # Listen for incoming connections
        # self.sockets_list = [self.sock]

        self.thr = Thread(target=self.listening)
        self.thr.start()
        self.thr.join()     # what??
        self.sock.close()
        self.identify = ['0', '1', '2', '3']
        # self.read_sockets, _, self.exception_sockets = select.select(self.sockets_list, [], self.sockets_list)

    def listening(self):
        while True:
            csocket, caddress = self.sock.accept()
            print("%s:%s has connected." % caddress)
            csocket.send(self.sdeck.encode())
            Thread(target=self.receive_card, args=(csocket,)).start()

    def receive_card(self, csocket):
        name = csocket.recv(1).decode()
        print(name)
        self.clients[csocket] = name
        while True:
            gcard = csocket.recv(32).decode()
            # self.clients[csocket] = gcard[-1]

            if len(gcard) >= 1:
                print(gcard)
                self.broadcast(gcard)

    def broadcast(self, card):
        for sock in self.clients:
            sock.send(card.encode())
            print(f'{card} sended')

mer = Merkazia()
# mer.listening()
