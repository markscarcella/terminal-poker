#!/usr/bin/python

from copy import deepcopy
from card import card

single = 0
pair = 1
twoPair = 2
threeKind = 3
straight = 4
flush = 5
fullHouse = 6
fourKind = 7
straightFlush = 8
order = ['A','K','Q','J','T','9','8','7','6','5','4','3','2']
handType = ["single",
            "pair",
            "twoPair",
            "threeKind",
            "straight",
            "flush",
            "fullHouse",
            "fourKind",
            "straightFlush",
            ]


def cardOrder(c1,c2):
    if order.index(c1[0]) > order.index(c2[0]):
        return 1
    if order.index(c1[0]) < order.index(c2[0]):
        return -1
    else:
        return 0

def sortCards(hand):
    hand.sort(cardOrder)

def isSingle(hand):
    return (single, [[hand[i][0] for i in range(5)]])

def isPair(hand):
    cardKind = [i[0] for i in hand]
    for kind in order:
        if cardKind.count(kind) == 2:
            others = []
            for j in cardKind:
                if j != kind:
                    others.append(j)
            return (pair, [[kind],others])

def isTwoPair(hand):
    cardKind = [i[0] for i in hand]
    for kind in order:
        for kind2 in order:
            for kind3 in order:
                if cardKind.count(kind) == 2 and cardKind.count(kind2)\
                       == 2  and kind != kind2 and cardKind.count(kind3) == 1:
                    return (twoPair, [[kind, kind2], [kind3]])
    return None

def isThreeKind(hand):
    cardKind = [i[0] for i in hand]
    for kind in order:
        if cardKind.count(kind) == 3:
            others = []
            for j in cardKind:
                if j != kind:
                    others.append(j)
            return (threeKind, [[kind],others])
    return None

def isFullHouse(hand):
    cardKind = [i[0] for i in hand]
    for kind in order:
        for kind2 in order:
            if cardKind.count(kind) == 3 and cardKind.count(kind2) == 2 and kind != kind2:
                    return (fullHouse, [[kind, kind2]])
    return None

def isFourKind(hand):
    cardKind = [i[0] for i in hand]
    for kind in order:
        if cardKind.count(kind) == 4:
            for j in cardKind:
                if j != kind:
                    return (fourKind, [[kind],[j]])
    return None

def isStraight(hand):
    if [card[0] for card in hand] !=\
           order[order.index(hand[0][0]):order.index(hand[0][0])+5]:
        return None
    return (straight, [hand[0][0]])
    
def isFlush(hand):
    suit = hand[0][1]
    for card in hand:
        if card[1] != suit:
            return None
    return (flush, [[hand[i][0] for i in range(5)]])
    
def isStraightFlush(hand):
    if isStraight(hand) != None and isFlush(hand) != None:
        return (straightFlush, [[hand[i][0] for i in range(5)]])

def classify(hand):
    hand.sort(cardOrder)
    types = [isStraightFlush, isFourKind, isFullHouse, isFlush, isStraight, isThreeKind, isTwoPair, isPair, isSingle]
    for f in types:
        if f(hand) != None:
            return f(hand)

def compareCard(c1, c2):
    if order.index(c1) < order.index(c2):
        return c1
    return c2

def compareNext(cards1, cards2):
    if len(cards1) == 0:
        return None
    for i in range(len(cards1)):
        if order.index(cards1[i]) < order.index(cards2[i]):
            return 1
        if order.index(cards1[i]) > order.index(cards2[i]):
            return 2
    compareNext(cards1[1:], cards2[:1])

def compareHands(h1, h2):
    if (h1 and h2):
        (h1Type, c1) = classify(h1)
        (h2Type, c2) = classify(h2)
        if h1Type > h2Type:
            return h1
        if h1Type < h2Type:
            return h2
        else:
            for i in range(len(c1)):
                if compareNext(c1[i], c2[i]) == 1:
                    return h1
                if compareNext(c1[i], c2[i]) == 2:
                    return h2

def comb(l,n):
    if n == 0:
        return [[]]
    if n > len(l):
        return []
    combs = []
    for i,elt in enumerate(l):
        tmpCombs = comb(l[i+1:],n-1)
        for j in tmpCombs:
            j.append(elt)
            combs.append(j)
    return combs

def findBestHand(pokerCards):
    cards = convertHand(pokerCards)[:]
    combs = comb(cards, 5)
    tmpWinHand = combs[0]
    for i in range(1,len(combs)):
        tmpWinHand = compareHands(tmpWinHand, combs[i])
        if tmpWinHand == None:
            tmpWinHand = combs[i]
    return tmpWinHand

def convertHand(pokerHand):
    hand = []
    for c in pokerHand:
        hand.append(str(c.getRank())+str(c.getSuit()))
        sortCards(hand)
    return hand

def pokerWin(cards1, cards2):
    print convertHand(cards1), convertHand(cards2)
    h1 = findBestHand(cards1)
    h2 = findBestHand(cards2)
    if compareHands(h1, h2) == h1:
        return 1
    if compareHands(h1, h2) == h2:
        return 2
    return 0
    

if __name__=="__main__":
    cards1 = [card('4','D'),card('K','S'),card('4','C'),card('T','C'),card('6','C'),card('4','S'),card('3','C')]
    cards2 = [card('A','C'),card('K','C'),card('4','C'),card('T','C'),card('6','C'),card('4','S'),card('3','C')]

    #['KD', 'KS', 'JC', 'TC', '6C', '4S', '3C'] ['AS', 'KS', 'TC', '7C', '6C', '4S', '3C']

    print comb(cards1, 5)
    
    print handType[classify(deepcopy(cards1))[0]], findBestHand(deepcopy(cards1))
    print handType[classify(findBestHand(deepcopy(cards2)))[0]], findBestHand(deepcopy(cards2))
    
    print pokerWin(cards1, cards2)
