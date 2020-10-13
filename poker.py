import bisect

VALUES = '23456789TJQKA'
SUITS = 'HDSC'
HAND_RANKS = [
    'High Card',
    'Pair',
    'Two Pair',
    'Three of a Kind',
    'Straight',
    'Flush',
    'Full House',
    'Four of a Kind',
    'Straight Flush',
    'Royal Flush'
]

card_strings = {
    'A': 'Ace',
    '2': 'Two',
    '3': 'Three',
    '4': 'Four',
    '5': 'Five',
    '6': 'Six',
    '7': 'Seven',
    '8': 'Eight',
    '9': 'Nine',
    'T': 'Ten',
    'J': 'Jack',
    'Q': 'Queen',
    'K': 'King'
}

FULL_DECK = ['AS', '2S', '3S', '4S', '5S', '6S', '7S', '8S', '9S', 'TS', 'JS', 'QS', 'KS',
                    'AD', '2D', '3D', '4D', '5D', '6D', '7D', '8D', '9D', 'TD', 'JD', 'QD', 'KD',
                    'AH', '2H', '3H', '4H', '5H', '6H', '7H', '8H', '9H', 'TH', 'JH', 'QH', 'KH',
                    'AC', '2C', '3C', '4C', '5C', '6C', '7C', '8C', '9C', 'TC', 'JC', 'QC', 'KC'
                    ]


class Card:
    def __init__(self, value_suit):
        value, suit = value_suit
        if value not in VALUES:
            raise ValueError
        if suit not in SUITS:
            raise ValueError
        self.value = value
        self.suit = suit

    def __repr__(self):
        return '<Card object {}>'.format(self)

    def __str__(self):
        return '{}{}'.format(self.value, self.suit)

    def __eq__(self, other):
        if self.value_index != other.value_index:
            return self.value == other.value
        else:
            return self.suit_index == other.suit_index

    def __lt__(self, other):
        if self.value_index != other.value_index:
            return self.value_index < other.value_index
        else:
            return self.suit_index < other.suit_index

    def __gt__(self, other):
        if self.value_index != other.value_index:
            return self.value_index > other.value_index
        else:
            return self.suit_index > other.suit_index

    @property
    def value_index(self):
        return VALUES.index(self.value)

    @property
    def suit_index(self):
        return SUITS.index(self.suit)


class PokerHand:
    def __init__(self, cards):
        cards = cards.split(' ')
        self.cards = [Card(x) for x in cards]
        card_set = {repr(card) for card in cards}
        if len(card_set) < len(cards):
            raise ValueError
        self.cards = sorted(self.cards)

    def __repr__(self):
        card_strings = (str(card) for card in self)
        return '<PokerHand object ({})>'.format(', '.join(card_strings))

    def __str__(self):
        result = ''
        for card in self.cards:
            result += str(card) + ' '
        return result[:-1]

    def __iter__(self):
        return iter(self.cards)

    def __gt__(self, other):
        if self.rank_index != other.rank_index:
            return self.rank_index > other.rank_index
        else:
            self_rank = self.rank[1]
            other_rank = other.rank[1]
            while self_rank and self_rank[-1] == other_rank[-1]:
                self_rank.pop()
                other_rank.pop()
            if not self_rank:
                return False
            else:
                return VALUES.index(self_rank[-1]) > VALUES.index(other_rank[-1])

    def __lt__(self, other):
        if self.rank_index != other.rank_index:
            return self.rank_index < other.rank_index
        else:
            self_rank = self.rank[1]
            other_rank = other.rank[1]
            while self_rank and self_rank[-1] == other_rank[-1]:
                self_rank.pop()
                other_rank.pop()
            if not self_rank:
                return False
            else:
                return VALUES.index(self_rank[-1]) < VALUES.index(other_rank[-1])

    def __eq__(self, other):
        if self.rank_index != other.rank_index:
            return self.rank_index == other.rank_index
        else:
            self_rank = self.rank[1]
            other_rank = other.rank[1]
            while self_rank and self_rank[-1] == other_rank[-1]:
                self_rank.pop()
                other_rank.pop()
            if not self_rank:
                return True
            else:
                return False

    def checkStraight(self):
        start = self.cards[0].value_index
        for i in range(1, len(self.cards) - 1):
            if self.cards[i].value_index != start + 1:
                return False
            else:
                start += 1
        if self.cards[-1].value_index != start + 1:
            if self.cards[-1].value == 'A' and self.cards[0].value == '2':
                return 'A'
            else:
                return False
        return self.cards[0].value

    def checkFlush(self):
        suit_to_check = self.cards[0].suit
        for i in range(1, len(self.cards) - 1):
            if self.cards[i].suit != suit_to_check:
                return False
        return max(self.cards)

    def checkPairs(self):
        d = {}
        for card in self.cards:
            if card.value in d:
                d[card.value] += 1
            else:
                d[card.value] = 1
        pairs = []
        tiebreak = []
        for c in d:
            if d[c] != 1:
                pairs.append([d[c], c])
            else:
                tiebreak.append(c)
        tiebreak.sort(key=VALUES.index)
        if len(pairs) == 1:
            if pairs[0][0] == 2:
                return ['Pair', tiebreak + [pairs[0][1]]]
            elif pairs[0][0] == 3:
                return ['Three of a Kind', tiebreak + [pairs[0][1]]]
            elif pairs[0][0] == 4:
                return ['Four of a Kind', tiebreak + [pairs[0][1]]]
        elif len(pairs) == 2:
            pairs.sort()
            if pairs[1][0] == 2:
                if VALUES.index(pairs[0][1]) > VALUES.index(pairs[1][1]):
                    return ['Two Pair', tiebreak + [pairs[1][1], pairs[0][1]]]
                else:
                    return ['Two Pair', tiebreak + [pairs[0][1], pairs[1][1]]]
            elif pairs[1][0] == 3:
                return ['Full House', tiebreak + [pairs[0][1], pairs[1][1]]]
        else:
            return ['High Card', tiebreak]

    @property
    def rank_index(self):
        return HAND_RANKS.index(self.rank[0])

    @property
    def rank(self):
        straight = self.checkStraight()
        flush = self.checkFlush()
        if straight and flush:
            if straight == 'T':
                return ['Royal Flush', [straight]]
            else:
                return ['Straight Flush', [straight]]

        if straight:
            return ['Straight', [straight]]
        if flush:
            return ['Flush', [x.value for x in self.cards]]

        pairs = self.checkPairs()
        return pairs


def bestHand(cards):
    best = PokerHand('2S 3C 4H 5C 7H')
    cards = cards.split(' ')
    for one in range(len(cards)):
        for two in range(one + 1, len(cards)):
            for three in range(two + 1, len(cards)):
                for four in range(three + 1, len(cards)):
                    for five in range(four + 1, len(cards)):
                        test = PokerHand(
                            cards[one] + ' ' + cards[two] + ' ' + cards[three] + ' ' + cards[four] + ' ' + cards[five])
                        if test > best or test == best:
                            best = test
    return best

def riverOdds(hand, board):
    board_arr = board.split(' ') + hand.split(' ')
    river_deck = FULL_DECK[:]
    your_best_hand = bestHand(hand + ' ' + board)
    win, tie, loss = (0, 0, 0)
    for card in board_arr:
        river_deck.remove(card)
    for i in range(len(river_deck)):
        for j in range(i + 1, len(river_deck)):
            check_hand = bestHand(board + ' ' + river_deck[i] + ' ' + river_deck[j])
            if your_best_hand > check_hand:
                win += 1
            elif your_best_hand == check_hand:
                tie += 1
            else:
                loss += 1
    return [win, tie, loss]

def turnOdds(hand, board):
    board_arr = board.split(' ') + hand.split(' ')
    turn_deck = FULL_DECK[:]
    win, tie, loss = (0, 0, 0)
    for card in board_arr:
        turn_deck.remove(card)
    for i in range(len(turn_deck)):
        odds = riverOdds(hand, board + ' ' + turn_deck[i])
        win += odds[0]
        tie += odds[1]
        loss += odds[2]
    return [win, tie, loss]

def flopOdds(hand, flop):
    board_arr = flop.split(' ') + hand.split(' ')
    turn_deck = FULL_DECK[:]
    win, tie, loss = (0, 0, 0)
    for card in board_arr:
        turn_deck.remove(card)
    for i in range(len(turn_deck)):
        odds = turnOdds(hand, flop + ' ' + turn_deck[i])
        win += odds[0]
        tie += odds[1]
        loss += odds[2]
    total = win + tie + loss
    print(win, tie, loss, total)
    print("Win: " + ' ' + str(round(win / total * 100, 2)))
    print("Tie: " + ' ' + str(round(tie / total * 100, 2)))
    print("Loss: " + ' ' + str(round(loss / total * 100, 2)))
    return [win, tie, loss]

h1 = PokerHand('4H 7S 9C AS AC')
h2 = PokerHand('4H 7S 9C AC AS')

turnOdds('AC AS', '2S 3C 4H 7S')

"""
riverOdds('AC AS', '2S 3C 4H 7S 9C')
Loss:  13.69
Tie:  0.56
Win:  85.75

ranked_hands = []
for i in range(len(deck)):
    for j in range(i + 1, len(deck)):
        for k in range(j + 1, len(deck)):
            for l in range(k + 1, len(deck)):
                    hand = PokerHand('KC' + ' ' + deck[j] + ' ' + deck[k] + ' ' + deck[l] + ' ' + deck[i])
                    bisect.insort(ranked_hands, hand)

f = open("Hands", 'w')
f.write('[\n')
for hand in ranked_hands:
    f.write("'" + str(hand) + "',\n")
f.write(']')
f.close()
"""
