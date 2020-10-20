import bisect
import OddsObjects
import PokerHand
import HoldEmHand
from Constants import FULL_DECK


def bestHand(cards):
    best = PokerHand('2S 3C 4H 5C 7H')  # Weakest Poker Hand
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


def postFlopOdds(hand, flop):
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

def preFlopOdds(hand, players = 2):
    hand = HoldEmHand(hand)
    win, loss, expected = hand.rank
    print('Odds for ' + str(hand) + ' before the Flop for a ' + str(players) + 'Player Round:')
    print('Chance to Win or Tie: ' + str(win) + '%')
    print('Chance to Lose:       ' + str(loss) + '%')
    print('Expected Value:       ' + str(expected) + '%')

preFlopOdds('2S 5C')
h1 = PokerHand('4H 7S 9C AS AC')
h2 = PokerHand('4H 7S 9C AC AS')

win, tie, loss = turnOdds('AC 6S', '2S 3C 4H 5D')
total = win + tie + loss
print(win, tie, loss, total)
print("Win: " + ' ' + str(round(win / total * 100, 2)))
print("Tie: " + ' ' + str(round(tie / total * 100, 2)))
print("Loss: " + ' ' + str(round(loss / total * 100, 2)))
"""
riverOdds('AC 6S', '2S 3C 4H 7S 9C')
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
