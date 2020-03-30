from tkinter import *
import socket
from threading import Thread


class GameBoard:
    def __init__(self):
        self.root = Tk()
        self.root.resizable(False, False)
        self.root.geometry("1000x650")
        self.root.configure(bg="green")
        self.root.title("ShayaWhist")
        self.places = [0.17, 0.222, 0.274, 0.326, 0.378, 0.43, 0.482, 0.534, 0.586, 0.638, 0.69, 0.742, 0.794]
        self.player2 = Label(self.root, text='player 1', padx=200, pady=30, font=('arial', 18)).pack()
        self.name_label = Label(self.root, text='player 3', padx=50, pady=30, font=('arial', 18), bg='green')
        self.name_label.place(relx=0.4, rely=0.905)
        self.canvas = Canvas(width=80, height=340)
        self.canvas.create_text(40, 180, font=('arial', 18), text="player 4", angle=90)
        self.canvas.place(relx=0, rely=0.2)
        self.canvas2 = Canvas(width=80, height=340)
        self.canvas2.create_text(40, 180, font=('arial', 18), text="player 2", angle=270)
        self.canvas2.place(relx=0.92, rely=0.2)
        self.butt0 = Button()
        self.butt1 = Button()
        self.butt2 = Button()
        self.butt3 = Button()
        self.butt4 = Button()
        self.butt5 = Button()
        self.butt6 = Button()
        self.butt7 = Button()
        self.butt8 = Button()
        self.butt9 = Button()
        self.butt10 = Button()
        self.butt11 = Button()
        self.butt12 = Button()
        self.butts = []
        self.check = [0, '']
        self.pbutt = Button(self.root, text='PUT', width=3, heigh=1,
                            font=('arial', 15), command=lambda: self.push()).place(relx=0.55, rely=0.65)
        self.cards = []
        self.takes = 0
        self.takeslbl = Label(self.root, text='Takes: \n' + str(self.takes), font=('arial', 14))
        self.takeslbl.place(relx=0.1, rely=0.85)
        self.takes1 = 0
        self.takeslbl1 = Label(self.root, text='Takes: \n' + str(self.takes), font=('arial', 14))
        self.takeslbl1.place(relx=0.008, rely=0.6)
        self.takes2 = 0
        self.takeslbl2 = Label(self.root, text='Takes: \n' + str(self.takes), font=('arial', 14))
        self.takeslbl2.place(relx=0.3, rely=0.03)
        self.takes3 = 0
        self.takeslbl3 = Label(self.root, text='Takes: \n' + str(self.takes), font=('arial', 14))
        self.takeslbl3.place(relx=0.93, rely=0.6)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = ('SERVER IP HERE', 15432)
        self.sock.connect(self.server_address)
        self.name = '2'
        self.check2 = 0
        self.reds = ["\u2665", "\u2666"]
        self.startbtn = Button(self.root, text='start', command=lambda: self.start(self.startbtn))
        self.startbtn.place(relx=0.85, rely=0.75)
        self.thr = Thread(target=self.first_connect)
        self.thr.start()
        self.root.mainloop()

    def back_place(self, btn, player):
        self.check[0] -= 1
        btn.place(relx=self.places[player.index((btn.config('text')[-1]))], rely=0.8)
        btn.config(command=lambda: self.put_in_middle(btn, player))

    def start(self, btn):
        self.make_butts(self.cards)
        self.sock.send(self.name.encode())
        btn.destroy()
        # btn.config(command=self.nothing)

    def put_in_middle(self, btn, player):
        if self.check[0] == 0 and self.check2 == 0:
            self.check[0] += 1
            self.check[1] = btn['text']
            btn.place(relx=0.482, rely=0.6)
            btn.config(command=lambda: self.back_place(btn, player))

    def make_reds(self, btn):
        if btn['text'][-1] in self.reds:
            btn['fg'] = 'red'

    def make_red_lbl(self,text):
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

    def first_connect(self):
        while True:
            try:
                data = self.sock.recv(258).decode()
                # print(data)
                if len(data) > 10:
                    self.cards = data.split(' ')[26:39]
                    print(self.cards)
                elif data[-1] == '2':
                    played_card0 = Label(self.root, text=data[:-1], fg=self.make_red_lbl(data[:-1]), width=3, heigh=3,
                                         font=('arial', 18))
                    played_card0.place(relx=0.482, rely=0.5)
                elif data[-1] == '3':
                    played_card1 = Label(self.root, text=data[:-1], fg=self.make_red_lbl(data[:-1]), width=3, heigh=3,
                                         font=('arial', 18))
                    played_card1.place(relx=0.364, rely=0.35)
                elif data[-1] == '0':
                    played_card2 = Label(self.root, text=data[:-1], fg=self.make_red_lbl(data[:-1]), width=3, heigh=3,
                                         font=('arial', 18))
                    played_card2.place(relx=0.482, rely=0.2)
                elif data[-1] == '1':
                    played_card3 = Label(self.root, text=data[:-1], fg=self.make_red_lbl(data[:-1]), width=3, heigh=3,
                                         font=('arial', 18))
                    played_card3.place(relx=0.6, rely=0.35)
                elif data[-1] == '5':
                    self.check2 = 0
                    if data[0] == '3':
                        self.takes += 1
                        self.takeslbl['text'] = 'Takes: \n' + str(self.takes)
                    elif data[0] == '4':
                        self.takes1 += 1
                        self.takeslbl1['text'] = 'Takes: \n' + str(self.takes1)
                    elif data[0] == '1':
                        self.takes2 += 1
                        self.takeslbl2['text'] = 'Takes: \n' + str(self.takes2)
                    elif data[0] == '2':
                        self.takes3 += 1
                        self.takeslbl3['text'] = 'Takes: \n' + str(self.takes3)
                    try:
                        played_card0.destroy()
                        played_card1.destroy()
                        played_card2.destroy()
                        played_card3.destroy()
                    except:
                        continue
            except:
                print('except')
                break

    def push(self):
        if self.check[0] == 1:
            self.check2 = 1
            self.sock.send(self.check[1].encode() + self.name.encode())
            for i in self.butts:
                if self.check[1] == i['text']:
                    self.butts.remove(i)
                    i.destroy()
                    self.check[0] -= 1


try1 = GameBoard()
