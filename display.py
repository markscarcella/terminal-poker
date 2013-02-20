#!/usr/bin/python

import sys
import curses
import locale
locale.setlocale(locale.LC_ALL, '')
code = locale.getpreferredencoding()
from card import card
stdscr = None

# Dictionary for selection of colors
color = None



def getColor(c):
    if c.getSuit() in ["H", "D"]:
        return color['r']
    return color[' ']
        
def printCard(cards, xPos, yPos):
    global stdscr
    offset = 0
    for c in cards:
        if c is None:
            stdscr.move(yPos,xPos+offset)
            stdscr.addstr(" ",color['felt'])
            stdscr.addstr(" ",color['felt'])
            stdscr.move(yPos+1,xPos+offset)
            stdscr.addstr(" ",color['felt'])
            stdscr.addstr(" ",color['felt'])
        elif c.getRank() == " " and c.getSuit() == " ":
            stdscr.move(yPos,xPos+offset)
            stdscr.addstr(" ",color['b'])
            stdscr.addstr(" ",color['blue'])
            stdscr.move(yPos+1,xPos+offset)
            stdscr.addstr(" ",color['blue'])
            stdscr.addstr(" ",color['b'])
        else:
            stdscr.move(yPos,xPos+offset)
            stdscr.addstr(str(c.getRank())+" ",getColor(c))
            stdscr.move(yPos+1,xPos+offset)
            stdscr.addstr(" "+str(c.getSuit()),getColor(c))
        offset += 3

def display(players, tableCards, pot, myPlayer, crntPlayer,
            crntButton, nxtBlindRaise, crntBlinds, msg):
    """ Display function for the table. Nb that if a card is face down
    u should represent it by card(" "," "). If player has folded
    (ie. no cards) represent it by None.
    """
    global stdscr
    stdscr.clear()

    for y in range(26):
        for x in range(86):
            stdscr.move(y,x)
            stdscr.addstr(" ", color['felt'])
        
    # Set up titles
    stdscr.move(1,1)
    stdscr.addstr(" "*34+"TERMINAL HOLD-EM"+" "*34,color[" "]+curses.A_BOLD)
    stdscr.move(4,1)
    stdscr.addstr("Players",color["felt"])
    stdscr.move(4,13)
    stdscr.addstr("Stack",color["felt"])
    stdscr.move(4,21)
    stdscr.addstr("Cards",color["felt"])
    stdscr.move(3,28)
    stdscr.addstr("Current",color["felt"])
    stdscr.move(4,30)
    stdscr.addstr("Bet",color["felt"])
    stdscr.move(3,40)
    stdscr.addstr("Blinds Increase in "+str(nxtBlindRaise)+" Rounds",color["felt"])
    stdscr.move(4,40)
    stdscr.addstr("Current Blinds: $"+str(crntBlinds[0])+"/$"+str(crntBlinds[1]),color["felt"])
    
    # Print out player info
    p = 6
    for (name, cards, money, bet) in players:
        stdscr.move(p,0)
        if crntButton == name:
            stdscr.addstr(" @ ", color["felt"])
        else:
            stdscr.addstr("   ", color["felt"])
        nameColor = color["felt"]
        if name == myPlayer and name == crntPlayer:
            nameColor = color["highlightCurrent"]
        elif name == myPlayer:
            nameColor = color["highlight"]
        elif name == crntPlayer:
            nameColor = color["current"]
        stdscr.move(p,3)
        stdscr.addstr(str(name)+":", nameColor)
        stdscr.move(p,13)
        stdscr.addstr("$"+str(money),color["felt"])
        printCard(cards,21,p)
        stdscr.move(p,30)
        stdscr.addstr("$"+str(bet),color["felt"])
        p += 3

    # print out pot
    stdscr.move(6,40)
    stdscr.addstr("Pot Total: $"+str(pot), color["current"])

    # print tabled cards
    stdscr.move(8,40)
    stdscr.addstr("Community Cards",color["felt"])
    printCard(tableCards,40,10)

    displayMsg(msg)
    stdscr.refresh()

def displayTurn(crntCheck, crntRaise):
    global stdscr
    # Fold button
    startX = 40
    startY = 15
    stdscr.move(startY,startX)
    stdscr.addstr(" ",color["blue"])
    stdscr.addstr("F",color["blue"]+curses.A_BOLD+curses.A_UNDERLINE)
    stdscr.addstr("old ",color["blue"])
    # Check button
    startX += len(" Fold ")+2
    stdscr.move(startY,startX)
    stdscr.addstr(" ",color["blue"])
    stdscr.addstr("C",color["blue"]+curses.A_BOLD+curses.A_UNDERLINE)
    stdscr.addstr("heck ($"+str(crntCheck)+") ",color["blue"])
    startX += len(" Check ($"+str(crntCheck)+") ")+2
    stdscr.move(startY,startX)
    stdscr.addstr(" "*20,color["felt"])
    stdscr.move(startY,startX)
    stdscr.addstr(" ",color["blue"])
    stdscr.addstr("R",color["blue"]+curses.A_BOLD+curses.A_UNDERLINE)
    stdscr.addstr("aise ($"+str(crntRaise)+") ",color["blue"])
    startX += len(" Raise ($"+str(crntRaise)+") ")+2

    startX = 40
    startY = 17
    stdscr.move(startY,startX)
    stdscr.addstr("-"*12+" Increase Raise By "+"-"*13,color["felt"])
    startY = 19
    stdscr.move(startY,startX)
    stdscr.addstr(" $1 (",color["red"])
    stdscr.addstr("1",color["red"]+curses.A_BOLD+curses.A_UNDERLINE)
    stdscr.addstr(") ",color["red"])
    startX += len(" $1 (1) ")+2
    stdscr.move(startY,startX)
    stdscr.addstr(" $5 (",color["red"])
    stdscr.addstr("2",color["red"]+curses.A_BOLD+curses.A_UNDERLINE)
    stdscr.addstr(") ",color["red"])
    startX += len(" $5 (2) ")+2
    stdscr.move(startY,startX)
    stdscr.addstr(" $10 (",color["red"])
    stdscr.addstr("3",color["red"]+curses.A_BOLD+curses.A_UNDERLINE)
    stdscr.addstr(") ",color["red"])
    startX += len(" $10 (3) ")+2
    stdscr.move(startY,startX)
    stdscr.addstr(" $50 (",color["red"])
    stdscr.addstr("4",color["red"]+curses.A_BOLD+curses.A_UNDERLINE)
    stdscr.addstr(") ",color["red"])
    startX += len(" $50 (4) ")+2
    startX = 40
    startY = 21
    stdscr.move(startY,startX)
    stdscr.addstr(" $100 (",color["red"])
    stdscr.addstr("5",color["red"]+curses.A_BOLD+curses.A_UNDERLINE)
    stdscr.addstr(") ",color["red"])
    startX += len(" $100 (5) ")+2
    stdscr.move(startY,startX)
    stdscr.addstr(" ",color["red"])
    stdscr.addstr("A",color["red"]+curses.A_BOLD+curses.A_UNDERLINE)
    stdscr.addstr("ll In ",color["red"])
    startX += len(" All In ")+2
    stdscr.move(startY,startX)
    stdscr.addstr(" R",color["red"])
    stdscr.addstr("e",color["red"]+curses.A_BOLD+curses.A_UNDERLINE)
    stdscr.addstr("set Raise ",color["red"])

def displayMsg(msg):
    stdscr.move(13,40)
    stdscr.addstr(" "*45, color["felt"])
    stdscr.move(13,40)
    stdscr.addstr(">> "+msg, color["felt"])

def getAction(maxBet, myBet, myStack):
    myRaise = 0
    displayTurn((maxBet - myBet), myRaise)
    while 1:
        key = stdscr.getch()

        #for buttons
        if key == ord('f'):
            return 'FOLD:'
        if key == ord('c'):
            return 'CHECK:'
        if key == ord('r'):
            return 'RAISE:'+str(myRaise)

        #for raises:
        if key == ord('1') and myRaise + 1 <= myStack - (maxBet - myBet):
            myRaise += 1
            displayTurn((maxBet - myBet), myRaise)
        if key == ord('2') and myRaise + 5 <= myStack - (maxBet - myBet):
            myRaise += 5
            displayTurn((maxBet - myBet), myRaise)
        if key == ord('3') and myRaise + 10 <= myStack - (maxBet - myBet):
            myRaise += 10
            displayTurn((maxBet - myBet), myRaise)
        if key == ord('4') and myRaise + 50 <= myStack - (maxBet - myBet):
            myRaise += 50
            displayTurn((maxBet - myBet), myRaise)
        if key == ord('5') and myRaise + 100 <= myStack - (maxBet - myBet):
            myRaise += 100
            displayTurn((maxBet - myBet), myRaise)
        if key == ord('a') and myRaise <= myStack - (maxBet - myBet):
            myRaise = myStack - (maxBet - myBet)
            displayTurn((maxBet - myBet), myRaise)
        if key == ord('e'):
            myRaise = 0
            displayTurn((maxBet - myBet), myRaise)


def setup():
    # Set up the viewscreen
    global stdscr
    locale.setlocale(locale.LC_ALL,"")
    try:
        stdscr = curses.initscr()
        curses.curs_set(0)
        stdscr.keypad(1)
    except curses.error:
        curses.endwin()
        print "Could not load curses"
        sys.exit(1)
    curses.start_color()
    curses.mousemask(curses.BUTTON1_PRESSED)
    
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_WHITE)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_RED)
    curses.init_pair(10, curses.COLOR_RED, curses.COLOR_WHITE)
    curses.init_pair(4, curses.COLOR_BLUE, curses.COLOR_RED)
    curses.init_pair(5, curses.COLOR_RED, curses.COLOR_GREEN)
    curses.init_pair(6, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(7, curses.COLOR_WHITE, curses.COLOR_BLUE)
    curses.init_pair(8, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(9, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(11, curses.COLOR_BLACK, curses.COLOR_GREEN)
    curses.cbreak()
    curses.noecho()
    global color
    color = {
    ' ' : curses.color_pair(1),
    'b' : curses.color_pair(2),
    'red' : curses.color_pair(3),
    'r' : curses.color_pair(10),
    'B' : curses.color_pair(4),
    'current' : curses.color_pair(5),
    'blue' : curses.color_pair(7),
    'highlight' : curses.color_pair(11)+curses.A_BOLD,
    'highlightCurrent' : curses.color_pair(5)+curses.A_BOLD,
    'invFelt' : curses.color_pair(9),
    'felt' : curses.color_pair(11),
    }
    

def exit():
    global stdscr
    stdscr.keypad(0)
    curses.endwin()    
                      
if __name__=="__main__":
    setup()
    player = [("Mark", [card(" "," "), card(" "," ")], 200, 00),
              ("Ian", [card("A","S"), card("K","H")], 80, 20),
              ("Cameron",  [card(" "," "), card(" "," ")], 90, 10),
              ("Nik",  [card(" "," "), card(" "," ")], 100, 0)]
    tableCards = [card("A","H"), card("7","D"), card("9","S"),
                  card(" "," "), card (" "," ")]
    displayMsg("Test message")
    display(player, tableCards, 30, "Ian", "Nik", "Mark", 2, [20,10],"MSG")
    getAction(20, 10, 200)
    stdscr.getch()
    exit()
