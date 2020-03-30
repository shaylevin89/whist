import random
import itertools


class CardGame:
    def __init__(self):
        self.final1 = []
        self.final2 = []
        self.final3 = []
        self.final4 = []
        self.club = "\u2663"
        self.spade = "\u2660"
        self.heart = "\u2665"
        self.diamond = "\u2666"
        self.suits = [self.diamond, self.club, self.heart, self.spade]
        self.cards = ['J', 'Q', 'K', 'A']
        for i in range(2, 11):
            self.cards.append(str(i))
        self.deck = []
        for i in self.suits:
            for j in self.cards:
                self.deck.append(j+i)
        random.shuffle(self.deck)
        self.player1 = self.deck[:13]
        self.player2 = self.deck[13:26]
        self.player3 = self.deck[26:39]
        self.player4 = self.deck[39:]
        self.players = [self.player1, self.player2, self.player3, self.player4]
        for player in self.players:
            for i in range(12):
                player.append([])

    def sort_suits(self, arr):
        for i in arr[:13]:
            if i[-1] == self.diamond:
                arr[13].append(i)
        for j in arr[:13]:
            if j[-1] == self.club:
                arr[14].append(j)
        for k in arr[:13]:
            if k[-1] == self.heart:
                arr[15].append(k)
        for l in arr[:13]:
            if l[-1] == self.spade:
                arr[16].append(l)

    def sort_values(self, arr, arr1, arr2):
        values = {'2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7, '9': 8, '1': 9, 'J': 10, 'Q': 11, 'K': 12,
                  'A': 13}
        rev_values = {1: '2', 2: '3', 3: '4', 4: '5', 5: '6', 6: '7', 7: '8', 8: '9', 9: '10', 10: 'J', 11: 'Q', 12: 'K',
                      13: 'A'}
        x = -1
        for suit in arr:
            x += 1
            for card in suit:
                arr1[x].append(values[card[0]])
            arr1[x].sort()
            for card1 in arr1[x]:
                arr2[x].append(rev_values[int(card1)]+arr[x][0][-1])

    def make_players(self):
        for i in self.players:
            self.sort_suits(i)
        for j in self.players:
            self.sort_values(j[13:17], j[17:21], j[21:])

    def make_final(self):
        self.make_players()
        self.final1 = list(itertools.chain.from_iterable(self.player1[21:]))
        self.final2 = list(itertools.chain.from_iterable(self.player2[21:]))
        self.final3 = list(itertools.chain.from_iterable(self.player3[21:]))
        self.final4 = list(itertools.chain.from_iterable(self.player4[21:]))

