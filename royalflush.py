#! /usr/bin/python2

from pcards import Deck, Card
from itertools import chain, combinations
from joblib import Parallel, delayed
import multiprocessing

# https://docs.python.org/2.7/library/itertools.html#recipes
def powerset(iterable):
    #"powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

def drawInitial(deck):
    return deck.draw(5)

def holdCards(hand):
    high_cards = [card for card in hand if card.rank() >= 10]
    handPowerset = [list(subset) for subset in powerset(high_cards)]
    bestHand = []
    for potentialHand in handPowerset:
        if len(potentialHand) <= 0:
            continue
        suit = potentialHand[0].suit()
        if all(card.suit() == suit for card in potentialHand):
            if len(potentialHand) > len(bestHand):
                bestHand = potentialHand
    return bestHand

def drawMissing(deck, hand):
    return hand + deck.draw(5 - len(hand))

def isRoyalFlush(hand):
    if all(card.rank() >= 10 for card in hand):
        suit = hand[0].suit()
        if all(card.suit() == suit for card in hand):
            return True
    return False

def step(deck):
    firstDraw = drawInitial(deck)
    heldCards = holdCards(firstDraw)
    secondDraw = drawMissing(deck, heldCards)
    return secondDraw

def getNumberOfTries(job):
    i = 0
    while True:
        i = i + 1
        deck = Deck()
        deck.shuffle()
        hand = step(deck)
        if isRoyalFlush(hand):
            print job, "done"
            break
    return i

def runSimulation(n = 100, numCores = multiprocessing.cpu_count()):
    print "Run", n, "simulations on", numCores, "cores:"
    results = Parallel(n_jobs=numCores)(delayed(getNumberOfTries)(i) for i in range(0, n))
    total=0
    for item in results:
        total+=item
    total=total/len(results)
    print "Average: " + str(total)

user_input = raw_input("How many instances of the simulation would you like to run?\nDefault: 10000 ")

try:
    f = int(user_input)
except ValueError:
    f = 10000

runSimulation(n = f)
