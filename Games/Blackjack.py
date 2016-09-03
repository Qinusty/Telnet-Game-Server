from Games import Game
import random

class Blackjack(Game.Game):
    def __init__(self):
        ## Anything that needs to happen when game first created
        self.user_hand = []
        self.dealer_hand = []
        self.gameover = True
        self.cards = ['AD','2D','3D','4D','5D','6D','7D','8D','9D','TD','JD','QD','KD',
         'AC','2C','3C','4C','5C','6C','7C','8C','9C','TC','JC','QC','KC',
         'AS','2S','3S','4S','5S','6S','7S','8S','9S','TS','JS','QS','KS',
         'AH','2H','3H','4H','5H','6H','7H','8H','9H','TH','JH','QH','KH']
        self.deck_place = 0
        self.name = 'blackjack'
        random.shuffle(self.cards)
        
    def draw_card(self):
        card = self.cards[self.deck_place]
        self.deck_place += 1
        return card
    
    def handle(self, userID, data, queue):
        """ 
        Do everything in this function
        userID is the unique identifier for the user.
        data is the variable containing text sent by the client to the server.
        """
        if "help" in data.lower():
            return self.help()
        elif "draw" in data.lower() and self.gameover:
            self.gameover = False
            self.user_hand = []
            self.dealer_hand = []
            self.user_hand.append(self.draw_card())
            self.user_hand.append(self.draw_card())
            self.dealer_hand.append(self.draw_card())
            self.dealer_hand.append(self.draw_card())
            return ["New game:",
                    "You drew: {0}".format(", ".join(self.user_hand)),
                    "This has a value of: {0}".format(self.get_score(self.user_hand)),
                    "Dealer drew: {0}".format(self.dealer_hand[0]),
                    "This has a value of: {0}".format(self.get_score([self.dealer_hand[0]])),
                    "Do you wish to hit or stay?"]
        elif "stay" in data.lower() and not self.gameover:
            self.gameover = True
            user_score = self.get_score(self.user_hand)
            if user_score <= 21:
                dealer_score = self.get_score(self.dealer_hand)
                while (dealer_score < 17 or dealer_score > 21) \
                        and dealer_score < user_score \
                        and user_score != 21:
                    card = self.draw_card()
                    self.dealer_hand.append(card)
                    dealer_score = self.get_score(self.dealer_hand)
                dealer_str = "The dealer finished with a hand of: " + ", ".join(self.dealer_hand)
                if dealer_score > 21:
                    self.gameover = True
                    return [dealer_str, "The dealer is bust! You win!", "Send draw to play again!"]
                elif user_score > dealer_score:
                    return [dealer_str, "You win!"]
                elif user_score == dealer_score:
                    return [dealer_str, "You draw..."]
                else:
                    return [dealer_str, "You lose!"]
            else:
                return ["You went bust!", "Send draw to play again!"]
            
        elif "hit" in data.lower() and not self.gameover:
            self.user_hand.append(self.draw_card())
            user_score = self.get_score(self.user_hand)
            new_hand = "You have: " + ", ".join(self.user_hand)
            valueof = "with a value of: " + str(self.get_score(self.user_hand))
            if user_score > 21:
                self.gameover = True
                return [new_hand, valueof, "You went bust!", "Send draw to play again"]
            else:
                return [new_hand, valueof, "Send hit to draw again"]
        else:
            print("WRONG: " + data)
            return ["Something went wrong... Probably dodgy cases, I got...", str(data)]

    def welcome(self):
        return "Welcome to blackjack"

    def get_score(self, cards):
        score = 0
        aces = []
        for card in cards:
            cardslist = list(card)
            if 'J' in card:
                score = score + 10
            elif 'Q' in card:
                score = score + 10
            elif 'K' in card:
                score = score + 10
            elif 'T' in card:
                score = score + 10
            elif 'A' in card:
                aces.append(card)
            else:
                score = score + int(card[0])
        for card in aces:
            if score <= 10:
                score = score + 11
            else:
                score = score + 1
        return score
        

    def help(self):
        return ["Draw: Start the game", "Stay: Stays", "Hit: Draws another card"]
