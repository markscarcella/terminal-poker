#!/usr/bin/python

""" Server code for the Hold 'Em game
"""

from card import card
import socket, sys, os, random, signal
import pokerWin

class pkrPlayer:
    """ Defines the classes that a poker player should have to be used
    by the server
    """
    def getBetDecision():
        pass

class pkrHuman(pkrPlayer):
    def __init__(self, name, clnt):
        self.name = name
        self.clnt = clnt
        self.money = 0
        self.crntBet = 0
        self.cards = []
    def resetCards(self):
        self.cards = []
    def addCard(self, card):
        self.cards.append(card)
    def getCards(self):
        return self.cards
    def resetBet(self):
        self.crntBet = 0
    def getBet(self):
        return self.crntBet
    def setBet(self, bet):
        self.money -= bet - self.crntBet
        self.crntBet = bet
    def getClient(self):
        return self.clnt
    def setMoney(self, money):
        self.money = money
    def getMoney(self):
        return self.money
    def getName(self):
        return self.name
    def addMoney(self, newMny):
        self.money += newMny
    
class pkrComputer(pkrPlayer):
    pass

class deck:
    def __init__(self):
        """ Returns a randomly sorted deck """
        # Unshuffled deck
        newDeck = [
            card("A", "H"), card("A", "D"), card("A", "S"), card("A", "C"), 
            card("2", "H"), card("2", "D"), card("2", "S"), card("2", "C"), 
            card("3", "H"), card("3", "D"), card("3", "S"), card("3", "C"), 
            card("4", "H"), card("4", "D"), card("4", "S"), card("4", "C"), 
            card("5", "H"), card("5", "D"), card("5", "S"), card("5", "C"), 
            card("6", "H"), card("6", "D"), card("6", "S"), card("6", "C"), 
            card("7", "H"), card("7", "D"), card("7", "S"), card("7", "C"), 
            card("8", "H"), card("8", "D"), card("8", "S"), card("8", "C"), 
            card("9", "H"), card("9", "D"), card("9", "S"), card("9", "C"), 
            card("T", "H"), card("T", "D"), card("T", "S"), card("T", "C"), 
            card("J", "H"), card("J", "D"), card("J", "S"), card("J", "C"), 
            card("Q", "H"), card("Q", "D"), card("Q", "S"), card("Q", "C"), 
            card("K", "H"), card("K", "D"), card("K", "S"), card("K", "C")]
        # Now shuffle
        random.seed()
        position = []
        for i in xrange(52):
            while True:
                r = random.randint(0,51)
                if r not in position:
                    position.append(r)
                    break
        self.deck = []
        for i in position:
            self.deck.append(newDeck[i])
    def nextCard(self):
        nxt = self.deck[0]
        self.deck = self.deck[1:]
        return nxt
    def printOut(self):
        for c in self.deck:
            print c.getSuit(), c.getRank()

class pkrServer:
    def interrupt(self, a, b):
        for p in self.playerList:
            try:
                p.clnt.send("QUIT:")
            except socket.error:
                pass
        self.lstn.close()
        print "Terminating at admin's request..."
        os.remove("port.txt")
        sys.exit(0)
    def __init__(self, nHumans, nComputers, startMoney = 100):
        signal.signal(signal.SIGINT, self.interrupt)
        self.playerList = []
        self.startMoney = 1000
        # Set up the actual server
        port = 9000
        while True:
            port += 1
            try:
                self.lstn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.lstn.bind(('glaser', port))
                print "Server opened on port", port
                break
            except socket.error:
                self.lstn = None
        # A file for people to open to find the servers
        f = open('port.txt', 'w')
        f.write(str(port)+'\n')
        f.close()
        self.lstn.listen(nHumans+5)
        self.tableCards = []
        for i in xrange(nHumans):
            self.addHuman()
        for i in xrange(nComputers):
            self.addComputer()
        for p in self.playerList:
            p.setMoney(self.startMoney)
        self.nPlayers = len(self.playerList)
        self.crntBlinds = [5,10]
        self.nextBlindRaise = 5
        self.pot = 0
        self.buttonPlayer = 0

    def __del__(self):
        for p in self.playerList:
            p.clnt.send("QUIT:")
        self.lstn.close()

    def addHuman(self):
        # Get a connection from the player and add them to the list
        (clnt, ap) = self.lstn.accept()
        name = clnt.recv(1024)
        #clnt.setblocking(0)
        print "Adding", name+"..."
        self.playerList.append(pkrHuman(name,clnt))

    def addComputer(self):
        # Randomly set up some risk-aversion setting
        pass

    def dealHand(self, player):
        player.addCard(self.deck.nextCard())
        player.addCard(self.deck.nextCard())

    def dealFlop(self):
        self.tableCards.append(self.deck.nextCard())
        self.tableCards.append(self.deck.nextCard())
        self.tableCards.append(self.deck.nextCard())

    def dealTurn(self):
        self.tableCards.append(self.deck.nextCard())

    def dealRiver(self):
        self.tableCards.append(self.deck.nextCard())

    def bettingRound(self, actnPlyr = 0):
        lstRaise = -1
        while True:
            if lstRaise == actnPlyr:
                break
            self.sendDisplayInfo(actnPlyr)
            self.activePlayers[actnPlyr].clnt.send("ACTION:")
            action = self.activePlayers[actnPlyr].clnt.recv(1024)
            print "From", self.activePlayers[actnPlyr].getName(),
            print "received", action
            action = action.split(":")
            if action[0] == "FOLD":
                actor = self.activePlayers[actnPlyr]
                self.sendMsg(actor.getName()+" Folds!")
                self.activePlayers.remove(actor)
                self.pot += actor.getBet()                
                actor.resetBet()
                actor.resetCards()
                if lstRaise > actnPlyr:
                    lstRaise -= 1
                actnPlyr -= 1
                if len(self.activePlayers) == 1:
                    break
            elif action[0] == "CHECK":
                actor = self.activePlayers[actnPlyr]
                self.sendMsg(actor.getName()+" Checks...")
                self.activePlayers[actnPlyr].setBet(self.crntBet)
                if lstRaise < 0:
                    lstRaise = actnPlyr
            elif action[0] == "RAISE":
                amnt = int(action[1])
                actor = self.activePlayers[actnPlyr]
                self.sendMsg(actor.getName()+" Raises $"+str(amnt))
                lstRaise = actnPlyr
                self.crntBet += amnt
                self.activePlayers[actnPlyr].setBet(self.crntBet)
                if lstRaise < 0:
                    lstRaise = actnPlyr
            actnPlyr = (actnPlyr + 1) % len(self.activePlayers)
        for p in self.playerList:
            if p.getBet() > 0:
                self.pot += p.getBet()
                p.resetBet()

    def endGame(self):
        prevNonZero = False
        for p in self.playerList:
            if prevNonZero and p.getMoney() > 0:
                prevNonZero = True
            elif not prevNonZero and p.getMoney() > 0:
                return False
        return True

    def sendDisplayInfo(self, actnPlyr, finishRound=False):
        # make up a string of all the necessary info and send to
        # players. Need: players (name, cards, money, crntBet),
        # tablecards, pot, current player,
        # current button, next blind raise, current blinds
        # These items seperated by ':'
        for plyr in self.playerList:
            sendStr = "DISPLAY:"
            # players seperated by '.', items in player list seperate by ','
            for p in self.playerList:
                sendStr += p.getName()+","
                for c in p.getCards():
                    if not finishRound:
                        if p.getName() == plyr.getName():
                            sendStr += str(c)
                        else:
                            sendStr += "  "
                    else:
                        sendStr += str(c)
                sendStr += ","+str(p.getMoney())+","+str(p.getBet())+"."
            sendStr += ":"
            for c in self.tableCards:
                sendStr += c.getRank() + c.getSuit()
            sendStr += ":"+str(self.pot)+":"
            sendStr += self.playerList[self.buttonPlayer].getName()+":"
            if actnPlyr is not None:
                sendStr += self.activePlayers[actnPlyr].getName()+":"
            else:
                sendStr += ":"
            sendStr += str(self.nextBlindRaise)+":"
            sendStr += str(self.crntBlinds[0])+"/"+str(self.crntBlinds[1])
            plyr.getClient().send(sendStr)
            plyr.getClient().recv(1000)

    def sendMsg(self, msg):
        for plyr in self.playerList:
            sendStr = "MSG:"+msg
            plyr.getClient().send(sendStr)
            plyr.getClient().recv(1000)
    
    def newRound(self):
        for p in self.playerList:
            p.resetBet()
            p.resetCards()
        self.deck = deck()
        # Find the active players and set the order
        self.activePlayers = []
        orderedList = self.playerList[self.buttonPlayer+1:]+\
                      self.playerList[:self.buttonPlayer+1]
        for p in orderedList:
            if p.getMoney() > 0:
                self.activePlayers.append(p)
                self.dealHand(p)

    def findWinner(self):
        #if len(self.activePlayers) == 1:
        #    self.activePlayers[0].addMoney(self.pot)
        #    self.pot = 0
        #    return
        # Now compare best hands
        #Exit
        while len(self.activePlayers) > 1:
            c1 = self.activePlayers[0].getCards()+self.tableCards
            c2 = self.activePlayers[1].getCards()+self.tableCards
            winner = pokerWin.pokerWin(c1, c2)
            if winner == 1:
                self.activePlayers.remove(self.activePlayers[1])
            elif winner == 2: 
                self.activePlayers.remove(self.activePlayers[0])
        print str(self.activePlayers[0].getName())+" wins!"
        self.activePlayers[0].addMoney(self.pot)
        self.pot = 0
        self.sendMsg(str(self.activePlayers[0].getName())+" wins!")

    def runGame(self):
        while not self.endGame():
            self.newRound()
            # 'active'=All players that can still bet(have money&not folded)
            self.tableCards = []
            self.crntBet = self.crntBlinds[1]
            self.activePlayers[0].setBet(self.crntBlinds[0])
            self.activePlayers[1].setBet(self.crntBlinds[1])
            self.bettingRound(2 % len(self.activePlayers))
            if len(self.activePlayers) > 1:
                self.dealFlop()
                self.crntBet = 0
                self.bettingRound()
            if len(self.activePlayers) > 1:
                self.dealTurn()
                self.crntBet = 0
                self.bettingRound()
            if len(self.activePlayers) > 1:
                self.dealRiver()
                self.crntBet = 0
                self.bettingRound()
            self.findWinner()
            self.buttonPlayer = (self.buttonPlayer + 1) % self.nPlayers
            self.sendDisplayInfo(None,True)
            print 'Hit Enter to start new round'
            raw_input()

if __name__ == "__main__":
    # Setup game
    #nHumans = int(raw_input("Number of human players: "))
    #nComputers = int(raw_input("Number of computer players: "))
    #startMoney = int(raw_input("Starting cash: "))
    #svr = pkrServer(nHumans, nComputers, startMoney)
    svr = pkrServer(3,0)
    # Run the game
    newGame = True
    while newGame:
        svr.runGame()
        game = raw_input("Another Round? ")
        if game.lower() == "n" or game.lower() == "no":
            newGame = False
    os.remove('port.txt')
