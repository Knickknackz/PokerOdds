import OddsObjects
from Card import Card

class HoldEmHand:
    def __init__(self, cards):
        cards = cards.split(' ')
        self.cards = [Card(x) for x in cards]
        card_set = {repr(card) for card in cards}
        if len(card_set) < len(cards):
            raise ValueError
        self.cards = sorted(self.cards)

    def __repr__(self):
        card_strings = (str(card) for card in self)
        return '<HoldEmHand object ({})>'.format(', '.join(card_strings))

    def __str__(self):
        result = ''
        for card in self.cards:
            result += str(card) + ' '
        return result[:-1]

    def __iter__(self):
        return iter(self.cards)

    def winChance(self, players):
        if self.cards[0].suit == self.cards[1].suit:
            suited = 's'
        elif self.cards[0].value == self.cards[1].value:
            suited = ''
        else:
            suited = 'o'
        return OddsObjects.full[self.cards[1].value + self.cards[0].value + suited][players-2]