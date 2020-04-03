from tkinter import *
import socket
from threading import Thread


class GameBoard:
    def __init__(self):
        # ask for player number:
        self.name = '1'
        # initial host and port setting
        self.host = '127.0.0.1'
        self.port = 15432
        # tkinter setting
        self.club, self.spade, self.heart, self.diamond = "\u2663", "\u2660", "\u2665", "\u2666"
        self.suits = [self.diamond, self.club, self.heart, self.spade]
        self.root = Tk()
        self.players_names = ['Player 1', 'Player 2', 'Player 3', 'Player 4']
        self.root.resizable(False, False)
        self.root.geometry("1000x650")
        self.root.configure(bg="green")
        self.root.title("ShayaWhist")
        # card places and other players widgets
        self.places = [0.17, 0.222, 0.274, 0.326, 0.378, 0.43, 0.482, 0.534, 0.586, 0.638, 0.69, 0.742, 0.794]
        self.orders = [0, 1, 2, 3], [1, 2, 3, 0], [2, 3, 0, 1], [3, 0, 1, 2]
        self.player2 = Label(self.root, text=self.players_names[self.orders[int(self.name)][2]], padx=200, pady=30,
                             font=('arial', 18)).pack()
        self.name_label = Label(self.root, text=self.players_names[self.orders[int(self.name)][0]], padx=50, pady=30,
                                font=('arial', 18), bg='green')
        self.name_label.place(relx=0.4, rely=0.905)
        self.canvas = Canvas(width=80, height=340)
        self.canvas.create_text(40, 180, font=('arial', 18), text=self.players_names[self.orders[int(self.name)][1]],
                                angle=90)
        self.canvas.place(relx=0, rely=0.2)
        self.canvas2 = Canvas(width=80, height=340)
        self.canvas2.create_text(40, 180, font=('arial', 18), text=self.players_names[self.orders[int(self.name)][3]],
                                 angle=270)
        self.canvas2.place(relx=0.92, rely=0.2)
        self.butt0, self.butt1, self.butt2, self.butt3, self.butt4, self.butt5, self.butt6, self.butt7, self.butt8, \
            self.butt9, self.butt10, self.butt11, self.butt12 = [Button() for x in range(13)]
        self.butts = []
        # put button:
        self.pbutt = Button(self.root, text='PUT', width=3, heigh=1,
                            font=('arial', 15), command=lambda: self.push()).place(relx=0.55, rely=0.65)
        self.cards = []  # player card
        self.cards2 = []
        self.check = [0, '']  # card button place configuration - [true or false, card str]
        self.round_bank = [[0, '', '0'], [0, '', '1'], [0, '', '2'], [0, '', '3']]  # [value, card, player]

        self.check_for_clean = 0
        self.trump = ''
        self.firs_card = ' '

        self.cut_places = [(0, 13), (13, 26), (26, 39), (39, 52)]
        # the takes labels for all the player:
        self.takes = 0
        self.takeslbl = Label(self.root, text='Takes: \n' + str(self.takes), font=('arial', 14))
        self.takeslbl.place(relx=0.1, rely=0.85)
        self.takes1 = 0
        self.takeslbl1 = Label(self.root, text='Takes: \n' + str(self.takes), font=('arial', 14))
        self.takeslbl1.place(relx=0.008, rely=0.6)
        self.takes2 = 0
        self.takeslbl2 = Label(self.root, text='Takes: \n' + str(self.takes), font=('arial', 14))
        self.takeslbl2.place(relx=0.65, rely=0.03)
        self.takes3 = 0
        self.takeslbl3 = Label(self.root, text='Takes: \n' + str(self.takes), font=('arial', 14))
        self.takeslbl3.place(relx=0.93, rely=0.6)

        self.inputbet = StringVar(self.root)
        self.entry = Entry(self.root, textvariable=self.inputbet, width=3, font=('arial', 14))
        self.entry.place(relx=0.03, rely=0.887)
        self.betbtn = Button(self.root, text='bet', height=1, font=('arial', 12), command=self.bet_func)
        self.betbtn.place(relx=0.032, rely=0.835)

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = (self.host, self.port)
        self.sock.connect(self.server_address)

        self.took_card = 1
        self.when_pushed = 0
        self.reds = ["\u2665", "\u2666"]
        self.startbtn = Button(self.root, text='start', command=lambda: self.start(self.startbtn))
        self.startbtn.place(relx=0.85, rely=0.75)
        self.cleanbtn1 = Button(self.root, text='take cards', font=('arial', 14),
                                command=lambda: self.clean_table(str(int(self.name))))
        self.cleanbtn1.place(relx=0.85, rely=0.85)

        self.thr = Thread(target=self.first_connect)
        self.thr.start()

        self.root.mainloop()

    def send_sign(self, sign):
        self.sock.send(sign.encode() + '7'.encode())

    def bet_func(self):
        try:
            if 14 > int(self.inputbet.get()) >= 0:
                data = str(self.inputbet.get())
                self.betbtn.destroy()
                self.entry.destroy()
                self.sock.send(data.encode() + self.name.encode() + '6'.encode())
        except:
            pass

    def i_won(self):
        trumps_list = []
        firsts_list = []
        for i in self.round_bank:
            if i[1][-1] == self.trump:
                trumps_list.append(i[0])
            elif i[1][-1] == self.firs_card[-1]:
                firsts_list.append(i[0])
        if len(trumps_list) == 0:
            if max(firsts_list) == self.round_bank[int(self.name)][0]:
                if self.firs_card[-1] == self.round_bank[int(self.name)][1][-1]:
                    return True
        else:
            if max(trumps_list) == self.round_bank[int(self.name)][0]:
                if self.trump == self.round_bank[int(self.name)][1][-1]:
                    return True

    def clean_table(self, player):
        if self.check_for_clean == 4 and self.i_won():
            self.sock.send(player.encode() + '5'.encode())
            self.check_for_clean = 0
            self.took_card = 1

    def get_sign(self, sign):
        signlbl = Label(self.root, text=self.suits[int(sign)], bg='green', font=('arial', 36))
        signlbl.place(relx=0.49, rely=0.36)
        self.trump = self.suits[int(sign)]

    def back_place(self, btn, player):
        self.check[0] = 0
        btn.place(relx=self.places[player.index((btn.config('text')[-1]))], rely=0.8)
        btn.config(command=lambda: self.put_in_middle(btn, player))

    def start(self, btn):
        self.make_butts(self.cards)
        self.sock.send(self.name.encode())
        btn.destroy()

    def check_suit(self, btn):
        if self.took_card == 1:
            return True
        elif self.firs_card != ' ':
            if btn['text'][-1] == self.firs_card[-1] or (self.firs_card[-1] not in [x[-1] for x in self.cards2]):
                return True

    def put_in_middle(self, btn, player):
        if self.check[0] == 0 and self.when_pushed == 0 and self.check_suit(btn):
            self.check[0] = 1
            self.check[1] = btn['text']
            btn.place(relx=0.482, rely=0.6)
            btn.config(command=lambda: self.back_place(btn, player))

    def make_reds(self, btn):
        if btn['text'][-1] in self.reds:
            btn['fg'] = 'red'

    def make_red_lbl(self, text):
        if text[-1] in self.reds:
            return 'red'

    def make_butts(self, lsttxt):
        self.butt0 = Button(self.root, text=lsttxt[0], width=3, heigh=3,
                            font=('arial', 18), command=lambda: self.put_in_middle(self.butt0, lsttxt))
        self.make_reds(self.butt0)
        self.butt0.place(relx=self.places[0], rely=0.8)
        self.butt1 = Button(self.root, text=lsttxt[1], width=3, heigh=3,
                            font=('arial', 18), command=lambda: self.put_in_middle(self.butt1, lsttxt))
        self.make_reds(self.butt1)
        self.butt1.place(relx=self.places[1], rely=0.8)
        self.butt2 = Button(self.root, text=lsttxt[2], width=3, heigh=3,
                            font=('arial', 18), command=lambda: self.put_in_middle(self.butt2, lsttxt))
        self.make_reds(self.butt2)
        self.butt2.place(relx=self.places[2], rely=0.8)
        self.butt3 = Button(self.root, text=lsttxt[3], width=3, heigh=3,
                            font=('arial', 18), command=lambda: self.put_in_middle(self.butt3, lsttxt))
        self.make_reds(self.butt3)
        self.butt3.place(relx=self.places[3], rely=0.8)
        self.butt4 = Button(self.root, text=lsttxt[4], width=3, heigh=3,
                            font=('arial', 18), command=lambda: self.put_in_middle(self.butt4, lsttxt))
        self.make_reds(self.butt4)
        self.butt4.place(relx=self.places[4], rely=0.8)
        self.butt5 = Button(self.root, text=lsttxt[5], width=3, heigh=3,
                            font=('arial', 18), command=lambda: self.put_in_middle(self.butt5, lsttxt))
        self.make_reds(self.butt5)
        self.butt5.place(relx=self.places[5], rely=0.8)
        self.butt6 = Button(self.root, text=lsttxt[6], width=3, heigh=3,
                            font=('arial', 18), command=lambda: self.put_in_middle(self.butt6, lsttxt))
        self.make_reds(self.butt6)
        self.butt6.place(relx=self.places[6], rely=0.8)
        self.butt7 = Button(self.root, text=lsttxt[7], width=3, heigh=3,
                            font=('arial', 18), command=lambda: self.put_in_middle(self.butt7, lsttxt))
        self.make_reds(self.butt7)
        self.butt7.place(relx=self.places[7], rely=0.8)
        self.butt8 = Button(self.root, text=lsttxt[8], width=3, heigh=3,
                            font=('arial', 18), command=lambda: self.put_in_middle(self.butt8, lsttxt))
        self.make_reds(self.butt8)
        self.butt8.place(relx=self.places[8], rely=0.8)
        self.butt9 = Button(self.root, text=lsttxt[9], width=3, heigh=3,
                            font=('arial', 18), command=lambda: self.put_in_middle(self.butt9, lsttxt))
        self.make_reds(self.butt9)
        self.butt9.place(relx=self.places[9], rely=0.8)
        self.butt10 = Button(self.root, text=lsttxt[10], width=3, heigh=3,
                             font=('arial', 18), command=lambda: self.put_in_middle(self.butt10, lsttxt))
        self.make_reds(self.butt10)
        self.butt10.place(relx=self.places[10], rely=0.8)
        self.butt11 = Button(self.root, text=lsttxt[11], width=3, heigh=3,
                             font=('arial', 18), command=lambda: self.put_in_middle(self.butt11, lsttxt))
        self.make_reds(self.butt11)
        self.butt11.place(relx=self.places[11], rely=0.8)
        self.butt12 = Button(self.root, text=lsttxt[12], width=3, heigh=3,
                             font=('arial', 18), command=lambda: self.put_in_middle(self.butt12, lsttxt))
        self.make_reds(self.butt12)
        self.butt12.place(relx=self.places[12], rely=0.8)
        self.butts = [self.butt0, self.butt1, self.butt2, self.butt3, self.butt4, self.butt5, self.butt6, self.butt7,
                      self.butt8, self.butt9, self.butt10, self.butt11, self.butt12]

    def check_if_first(self, card):
        tmp = 0
        for player in self.round_bank:
            if player[0] == 0:
                tmp += 1
        if tmp == 3:
            self.firs_card = card

    def first_connect(self):
        values = {'2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7, '9': 8, '1': 9, 'J': 10, 'Q': 11, 'K': 12,
                  'A': 13}
        while True:
            try:
                data = self.sock.recv(280).decode()
                if len(data) > 10:
                    self.cards = data.split(' ')[self.cut_places[int(self.name)][0]:self.cut_places[int(self.name)][1]]
                    self.cards2 = data.split(' ')[self.cut_places[int(self.name)][0]:self.cut_places[int(self.name)][1]]
                    print(self.cards)
                elif data[-1] == self.name:
                    played_card0 = Label(self.root, text=data[:-1], fg=self.make_red_lbl(data[:-1]), width=3, heigh=3,
                                         font=('arial', 18))
                    played_card0.place(relx=0.482, rely=0.5)
                    self.took_card = 0
                    self.check_for_clean += 1
                    self.round_bank[int(data[-1])][1] = data[:-1]
                    self.round_bank[int(data[-1])][0] = values[data[0]]
                    self.check_if_first(data[:-1])
                elif data[-1] == str(self.orders[int(self.name)][1]):
                    played_card1 = Label(self.root, text=data[:-1], fg=self.make_red_lbl(data[:-1]), width=3, heigh=3,
                                         font=('arial', 18))
                    played_card1.place(relx=0.364, rely=0.35)
                    self.took_card = 0
                    self.check_for_clean += 1
                    self.round_bank[int(data[-1])][1] = data[:-1]
                    self.round_bank[int(data[-1])][0] = values[data[0]]
                    self.check_if_first(data[:-1])
                elif data[-1] == str(self.orders[int(self.name)][2]):
                    played_card2 = Label(self.root, text=data[:-1], fg=self.make_red_lbl(data[:-1]), width=3, heigh=3,
                                         font=('arial', 18))
                    played_card2.place(relx=0.482, rely=0.2)
                    self.took_card = 0
                    self.check_for_clean += 1
                    self.round_bank[int(data[-1])][1] = data[:-1]
                    self.round_bank[int(data[-1])][0] = values[data[0]]
                    self.check_if_first(data[:-1])
                elif data[-1] == str(self.orders[int(self.name)][3]):
                    played_card3 = Label(self.root, text=data[:-1], fg=self.make_red_lbl(data[:-1]), width=3, heigh=3,
                                         font=('arial', 18))
                    played_card3.place(relx=0.6, rely=0.35)
                    self.took_card = 0
                    self.check_for_clean += 1
                    self.round_bank[int(data[-1])][1] = data[:-1]
                    self.round_bank[int(data[-1])][0] = values[data[0]]
                    self.check_if_first(data[:-1])
                elif data[-1] == '5':
                    self.when_pushed = 0
                    self.check_for_clean = 0
                    self.firs_card = ' '
                    self.round_bank = [[0, '', '0'], [0, '', '1'], [0, '', '2'], [0, '', '3']]
                    if data[0] == str(self.orders[int(self.name)][0]):
                        self.takes += 1
                        self.takeslbl['text'] = 'Takes: \n' + str(self.takes)
                    elif data[0] == str(self.orders[int(self.name)][1]):
                        self.takes1 += 1
                        self.takeslbl1['text'] = 'Takes: \n' + str(self.takes1)
                    elif data[0] == str(self.orders[int(self.name)][2]):
                        self.takes2 += 1
                        self.takeslbl2['text'] = 'Takes: \n' + str(self.takes2)
                    elif data[0] == str(self.orders[int(self.name)][3]):
                        self.takes3 += 1
                        self.takeslbl3['text'] = 'Takes: \n' + str(self.takes3)
                    try:
                        played_card0.destroy()
                        played_card1.destroy()
                        played_card2.destroy()
                        played_card3.destroy()
                    except:
                        continue
                elif data[-1] == '6':
                    if data[-2] == str(self.orders[int(self.name)][0]):
                        bet = Label(self.root, text='bet\n' + data[:-2], font=('arial', 14))
                        bet.place(relx=0.02, rely=0.85)
                    elif data[-2] == str(self.orders[int(self.name)][1]):
                        bet = Label(self.root, text='bet ' + data[:-2], font=('arial', 14))
                        bet.place(relx=0.008, rely=0.68)
                    elif data[-2] == str(self.orders[int(self.name)][2]):
                        bet = Label(self.root, text='bet\n' + data[:-2], font=('arial', 14))
                        bet.place(relx=0.3, rely=0.03)
                    elif data[-2] == str(self.orders[int(self.name)][3]):
                        bet = Label(self.root, text='bet ' + data[:-2], font=('arial', 14))
                        bet.place(relx=0.93, rely=0.68)
                elif data[-1] == '7':
                    self.get_sign(data[0])
                    self.trump = self.suits[int(data[0])]

            except NameError as msg:
                print(msg)

    def push(self):
        if self.check[0] == 1 and (self.took_card == 1 or self.round_bank[self.orders[int(self.name)][3]][0] > 0):
            self.when_pushed = 1
            self.sock.send(self.check[1].encode() + self.name.encode())
            self.cards2.remove(self.check[1])
            for i in self.butts:
                if self.check[1] == i['text']:
                    self.butts.remove(i)
                    i.destroy()
                    self.check[0] -= 1


try1 = GameBoard()
