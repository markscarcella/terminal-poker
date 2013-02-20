
class card:
    """ Simple container for cards
    """
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
    def getSuit(self):
        return self.suit
    def __repr__(self):
        return self.getRank()+self.getSuit() 
    def __str__(self):
        return self.getRank()+self.getSuit()
    def getRank(self):
        return self.rank
    def __getitem__(self, n):
        """ For  backward compatibility with mark's code:
        For card c: (nb c[n] == c.__getitem__(n))
        c[0] returns rank
        c[1] return suit
        """
        if n == 0:
            return self.rank
        elif n == 1:
            return self.suit
        else:
            raise IndexError

