#!/usr/bin/python

""" Client code for the Hold 'Em game
"""

import socket, sys
import display
from card import card

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
f = None
try:
    f = open('port.txt', 'r')
except IOError:
    print "No server found"
    sys.exit(1)

port = int(f.readline())
f.close()
s.connect(('glaser', port))

name = raw_input("Enter your name: ")
s.send(name)

act = None; plyrs = None; tblCards = None; pot = None;
btn = None; actPlyr = None; nxtBlndRs = None; blnds=None; msg = ''
display.setup()
while True:
    nxtMsg = s.recv(4096).split(":")
    #print "Recieved", nxtMsg
    myMny = 0; myBet = 0; maxBet = 0
    if nxtMsg[0] == "ACTION":
        for p in plyrs:
            if p == "":
                continue
            pName, cards, mny, bet = p.split(",")
            if name == pName:
                myMny = int(mny)
                myBet = int(bet)
            if int(bet) > maxBet:
                maxBet = int(bet)
        #print maxBet, myBet
        myAct = display.getAction(int(maxBet),int(myBet),int(myMny))
        st = s.send(myAct)
    elif nxtMsg[0] == "DISPLAY":
        try:
            act, plyrs, tblCards, pot, btn, actPlyr, nxtBlndRs, blnds = nxtMsg
        except ValueError:
            display.exit()
            print nxtMsg
        # Parse players
        plyrs = plyrs.split(".")
        dispPlyrs = []
        for p in plyrs:
            if p == "":
                continue
            pName, cards, mny, bet = p.split(",")
            if len(cards) == 0:
                cards = (None,None)
            else:
                cards = [card(cards[0], cards[1]),
                         card(cards[2], cards[3])]
            dispPlyrs.append((pName, cards,int(mny),int(bet)))
        i = 0
        print tblCards
        dispTblCards = []
        while i < len(tblCards):
            dispTblCards.append(card(tblCards[i],tblCards[i+1]))
            i += 2
        display.display(dispPlyrs, dispTblCards, int(pot), name, actPlyr,
                        btn, nxtBlndRs,
                        [int(b) for b in blnds.split('/')], msg)
        s.send("OK")
    elif nxtMsg[0] == "MSG":
        display.displayMsg(nxtMsg[1])
        msg = nxtMsg[1]
        s.send("OK")
    elif nxtMsg[0] == "QUIT":
        break

s.close()
display.exit()
