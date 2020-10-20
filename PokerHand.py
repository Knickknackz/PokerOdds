from Constants import HAND_RANKS, VALUES
import Card


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
