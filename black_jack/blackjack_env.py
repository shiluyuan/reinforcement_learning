import random
# cards on table, J, Q, K are viewed as 10

class Deck():
    def __init__(self):
        self.cards = [1,2,3,4,5,6,7,8,9,10,10,10,10] * 4 * 4
        
    def shuffle(self):
        random.shuffle(self.cards)
    
    def draw_hand(self):
        self.hand = self.cards[:2]
        self.cards = self.cards[2:]
        
    def draw_card(self):
        self.hand = self.cards[0]
        self.cards = self.cards[1:]
## 
def compare_hand(a,b):
    if a>b:
        return 1
    elif a<b:
        return -1
    else:
        return 0 
    
def usable_ace(hand):
    # hand: [1,7,2], return true
    return 1 in hand and sum(hand) + 10 <= 21

def sum_hand(hand):
    if usable_ace(hand):
        return sum(hand) + 10
    else:
        return sum(hand)

def is_bust(hand):
    return sum_hand(hand) > 21

def score(hand):
    return 0 if is_bust(hand) else sum_hand(hand)

def is_natural_blackjack(hand):
    return sorted(hand) == [1,10]

# defince enviornment 
class blackjack_env():
    
    def __init__(self,natural=False):
        self.natural = natural
        
    def get_state(self):
        return (sum_hand(self.player), self.dealer[0], usable_ace(self.player))
    
    def reset(self):
        self.deck = Deck()
        # shuffle the cards
        self.deck.shuffle()
        # draw hand for player
        self.deck.draw_hand()
        self.player = self.deck.hand
        # to see whether the player got natural blackjack
        if is_natural_blackjack(self.player):
            self.natural = True
        # draw hand for dealer 
        self.deck.draw_hand()
        self.dealer = self.deck.hand
        # auto draw card for player if sum is less than 11
        while sum_hand(self.player) <= 11:
            self.deck.draw_card()
            self.player.append(self.deck.hand)
        return self.get_state()
    
    def step(self,action):
        # action true: player hit a card
        if action and sum_hand(self.player) < 21:
            self.deck.draw_card()
            self.player.append(self.deck.hand)
            if is_bust(self.player):
                done = True
                reward = -1
            else:
                done = False
                reward = 0
        else: #stick with cards
            done = True
            while sum_hand(self.dealer) < 17:
                # dealer must get a card when the sum is less than 17
                self.deck.draw_card()
                self.dealer.append(self.deck.hand)
            reward = compare_hand(score(self.player), score(self.dealer))
            if self.natural:
                reward = 1.5
        return self.get_state(), reward, done
    
            

    
    