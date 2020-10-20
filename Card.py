from Constants import VALUES, SUITS


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
