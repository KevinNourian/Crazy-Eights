'''
This program mimics the two-player card game, Crazy Eights. The objective is to be the first player to get rid of all cards in your hand. Multiple rounds are played and scores are kept. The player with the lowest total score when another player gets a total score of 100 points or more is the winner. A text file can be referred to if the players are not familiar with the rules.

When the game starts, the program asks for the players' names. After they enter their names, the game will refer to them by name only.

At any point during the game, the player can type "--help" and be taken to a screen where they can read the rules of the game and instructions for how to play. They will resume the game when they close the window.
'''


from random import shuffle
from random import randint
import webbrowser # To open new window -- need_help() function
from time import sleep

def intro():
    '''
    Prints introductory text and displays rules of the game.
    '''
    text = "**************************************************\n"
    text = text + "*  Welcome to Crazy Eights Card Game.            *\n"
    text = text + "*  This game is designed for two players.        *\n"
    text = text + "*  At any time, type --help to see the rules.   *\n"
    text = text + "*  Close the help window to continue.            *\n"
    text = text + "*  Good luck!!                                   *\n"
    text = text + "**************************************************"
    print(text)
    print()


def need_help():
    '''
    Opens a window to display the rules when player types --help.
    The player can close the window at will and resume the game.
    If no help is needed, the player can continue with pressing ENTER.
    '''
    text = "Type --help or press ENTER to continue \n"
    rules = input(text)
    print()
    if rules == "--help":
        webbrowser.open('Rules.txt')


class Deck:
    '''
    Contains all functions for the deck of cards.
    '''

    def shuffle_deck(self):
        '''
        Shuffles a standard 52-card deck.
        '''
        shuffled_deck = []
        tuple = ()

        deck = [1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                "K",
                "Q",
                "J"]

        suits = ["♠", "♥", "♦", "♣"]

        shuffle(deck)

        for card in deck:
            shuffle(suits)
            for suit in suits:
                tuple = card, suit
                shuffled_deck.append(tuple)
        shuffle(shuffled_deck)

        self.shuffled_deck = shuffled_deck
        self.suits = suits


    def draw_deck_creation(self, shuffled_deck):
        '''
        Creates the Draw Deck, from the remainder of cards left after dealing.
        '''
        draw_deck = []
        draw_deck = shuffled_deck

        length_draw_deck = len(draw_deck)

        self.draw_deck = draw_deck
        self.length_draw_deck = length_draw_deck


    def discard_deck_creation(self, draw_deck):
        '''
        Creates the Discard Deck, from the top card of the Draw Deck. If the top card is an 8, replaces the card in the "Draw Deck" at a random location.
        '''
        discard_deck = []

        for i in range(4):
            discard_deck.append(draw_deck[0])
            num = randint(0,37)

            if discard_deck[0][0] == '8':
                replaced_card = discard_deck[0]
                #Remove 8 card from draw_deck
                draw_deck.remove(replaced_card)
                #Insert 8 card at random location in draw_deck.
                draw_deck.insert(num, replaced_card)
                #Remove 8 card from discard_deck
                discard_deck.remove(replaced_card)
            else: #The card is not 8
                #Remove the card from draw_deck
                del draw_deck[0]
                break

        self.draw_deck = draw_deck
        self.discard_deck = discard_deck


    def count_draw_deck(self, draw_deck):
        '''
        Counts the number of cards in the Draw Deck.
        '''
        card_count_draw_deck = len(draw_deck)

        self.card_count_draw_deck = card_count_draw_deck


class Player:
    '''
    Contains all functions for the players of the game.
    '''

    def __init__(self):
        '''
        Initializes the value of the Total Score for the player.
        '''
        self.total_score = 0


    def create_name (self, name):
        '''
        Creates and saves the name of each player.
        '''
        self.name = name


    def hand(self, shuffled_deck):
        '''
        Deals 7 cards to the player.
        '''
        player_hand = []

        for i in range(7):
            player_hand.append(shuffled_deck[0])
            del shuffled_deck[0]

        self.player_hand = player_hand


    def sort_hand(self, player_hand):
        '''
        Sorts the hand of the player. 8 goes first, then the picture cards, then the numbers from large to small.
        '''

        number_of_cards = len(player_hand)
        eights = []
        pictures = []
        numbers = []
        sorted_hand = []

        for i in range (number_of_cards):
            if player_hand[i][0] == 8:
                eights.append(player_hand[i])

            elif (player_hand[i][0] == 'J') \
             or (player_hand[i][0] == 'K') \
             or (player_hand[i][0] == 'Q'):
                pictures.append(player_hand[i])

            elif (player_hand[i][0] == 1) \
             or (player_hand[i][0] == 2) \
             or (player_hand[i][0] == 3) \
             or (player_hand[i][0] == 4) \
             or (player_hand[i][0] == 5) \
             or (player_hand[i][0] == 6) \
             or (player_hand[i][0] == 7) \
             or (player_hand[i][0] == 9) \
             or (player_hand[i][0] == 10):
                numbers.append(player_hand[i])

        #Sorts by the first element of each tuple.
        numbers.sort(key=lambda tup: tup[0], reverse = True)
        sorted_hand = eights + pictures + numbers

        self.sorted_hand = sorted_hand


    def play (self, draw_deck, discard_deck, sorted_hand, suits):
        '''
        Checks the Player Hand against card in Discard Deck. If card in Player Hand has the same suit or the same value, it passes that card to the function can_play(). 8 is the wildcard. It can be used for any card.
        '''
        number_of_cards = len(sorted_hand)

        can_play = []

        check = True

        for i in range(number_of_cards):
            if sorted_hand[i][0] == 8:
                can_play.append(sorted_hand[i])
                check = False

            elif sorted_hand[i][0] == discard_deck[0][0] or sorted_hand[i][1] == discard_deck[0][1]:
                can_play.append(sorted_hand[i])
                check = False

        shuffle(can_play)
        self.can_play = can_play
        self.check = check
        self.sorted_hand = sorted_hand


    def additional_cards(self, check, sorted_hand, draw_deck, discard_deck, can_play):
        '''
        If a player does not have a card with the same suit or same number, or an 8, he can pick up to 3 cards from the Discard Deck and pass if he still cannot play. If the player draws a card that can be played, that card must be played.
        '''

        if check == True:
            additional_card_taken = 0

            while additional_card_taken < 3:
                length_draw_deck = len(draw_deck)

                if length_draw_deck > 0:
                    additional_card_taken += 1
                    print("Additional Card:", additional_card_taken)
                    print()

                    sorted_hand.append(draw_deck[0])
                    del draw_deck[0]

                    if sorted_hand[-1][0] == 8:
                        can_play.append(sorted_hand[-1])
                        break

                    elif sorted_hand[-1][0] == discard_deck[0][0] or sorted_hand[-1][1] == discard_deck[0][1]:
                        can_play.append(sorted_hand[-1])
                        break
                else:
                    break

        self.draw_deck = draw_deck
        self.sorted_hand = sorted_hand
        self.can_play = can_play


    def play_your_hand(self, discard_deck, sorted_hand, can_play):
        '''
        Creates a list with cards that can be played. Asks the user to pick a card from that list.
        '''

        print("Enter a number from 1 -", len(can_play))

        need_help()

        try:
            num = int(input("What is the number: "))

            assert num > 0
            num = num - 1
            card = can_play[num]
        except AssertionError:
            print("Integer 1 or bigger only. \n")
        except ValueError:
            print("Integers only. \n")
        except IndexError:
            print("Integer in the correct range only. \n")
        else:
            print()

            sorted_hand.remove(card)
            del discard_deck[0]
            discard_deck.append(can_play[num])
            del can_play[num]

        self.sorted_hand = sorted_hand


    def count_hand(self, sorted_hand):
        '''
        Counts the number of cards in each hand.
        '''
        card_count_hand = len(sorted_hand)

        self.card_count_hand = card_count_hand


    def set_score(self, sorted_hand):
        '''
        Calculates the score of each player when the round is finsihed.
        '''
        score = 0

        face_card_dict = {8: 50,
                          1: 1,
                          2: 2,
                          3: 3,
                          4: 4,
                          5: 5,
                          6: 6,
                          7: 7,
                          9: 9,
                          10: 10,
                          "K": 10,
                          "J": 10,
                          "Q": 10,
                          }
        for i in range(len(sorted_hand)):
          score += face_card_dict[sorted_hand[i][0]]

        self.score = score


    def set_total_score(self, score):
        '''
        Calculates the total score of each player when the game is finished.
        '''

        self.total_score = self.total_score + self.score



'''
Main Program
'''

intro()

player1 = Player()
player1.create_name  = input("First Player: ")
name1 = player1.create_name
print()

player2 = Player()
player2.create_name  = input("Second Player: ")
name2 = player2.create_name
print()

need_help()

round = 0
player1.total_score = 0
player1.total_score = 0

# Stores the names of each player and their total score in a dictionary.
total_score_dict = {}

while player1.total_score <= 100 and player2.total_score <= 100:

        round += 1

        print("*******************")
        print("ROUND:",round)
        print("CARDS ARE SHUFFLED")
        print("*******************")
        print()

        deck = Deck()
        deck.shuffle_deck()

        player1.hand(deck.shuffled_deck)
        player1.sort_hand(player1.player_hand)

        player2.hand(deck.shuffled_deck)
        player2.sort_hand(player2.player_hand)

        deck.draw_deck_creation(deck.shuffled_deck)
        draw_deck = deck.draw_deck

        deck.count_draw_deck(deck.draw_deck)
        print("Number of cards in Draw Deck:")
        print(deck.card_count_draw_deck)
        print()

        deck.discard_deck_creation(deck.draw_deck)
        print("Discard Deck")
        discard_deck = deck.discard_deck
        print(discard_deck)
        print()

        player1.count_hand(player1.sorted_hand)
        player1.card_count_hand

        player2.count_hand(player2.sorted_hand)
        player2.card_count_hand

        deck.count_draw_deck(deck.draw_deck)
        deck.card_count_draw_deck


        player = player1


        while player.card_count_hand > 0:
            if deck.card_count_draw_deck > 0:

                if player == player1:
                    name = name1

                    player.sort_hand(player.sorted_hand)
                    sorted_hand = player.sorted_hand
                    print(name + "'s Hand")
                    print(sorted_hand)
                    print()

                    player.play(deck.draw_deck, deck.discard_deck, player.sorted_hand, deck.suits)
                    check = player.check

                    if player.check == True:
                        player.additional_cards(player.check, player.sorted_hand, deck.draw_deck, deck.discard_deck, player.can_play)

                    can_play = player.can_play
                    print("Can Play")
                    print(can_play)
                    print()

                    if len(player.can_play) > 0:

                        player.play_your_hand(deck.discard_deck, player.sorted_hand, player.can_play)
                        sorted_hand = player.sorted_hand

                        discard_deck = deck.discard_deck
                        print("Discard Deck")
                        print(discard_deck)
                        print()

                        player.sort_hand(player.sorted_hand)

                    else:
                        print("No cards to play.")
                        print()

                    player.count_hand(player.sorted_hand)
                    card_count_hand = player.card_count_hand
                    if card_count_hand == 0:
                        break

                    deck.count_draw_deck(deck.draw_deck)
                    card_count_draw_deck = deck.card_count_draw_deck
                    if card_count_draw_deck == 0:
                        break

                    player = player2


                if player == player2:
                    name = name2

                    player.sort_hand(player.sorted_hand)
                    sorted_hand = player.sorted_hand
                    print(name + "'s Hand")
                    print(sorted_hand)
                    print()

                    player.play(deck.draw_deck, deck.discard_deck, player.sorted_hand, deck.suits)
                    check = player.check

                    if player.check == True:
                        player.additional_cards(player.check, player.sorted_hand, deck.draw_deck, deck.discard_deck, player.can_play)

                    can_play = player.can_play
                    print("Can Play")
                    print(can_play)
                    print()

                    if len(player.can_play) > 0:

                        player.play_your_hand(deck.discard_deck, player.sorted_hand, player.can_play)
                        sorted_hand = player.sorted_hand

                        discard_deck = deck.discard_deck
                        print("Discard Deck")
                        print(discard_deck)
                        print()

                        player.sort_hand(player.sorted_hand)

                    else:
                        print("No cards to play.")
                        print()

                    player.count_hand(player.sorted_hand)
                    card_count_hand = player.card_count_hand
                    if card_count_hand == 0:
                        break

                    deck.count_draw_deck(deck.draw_deck)
                    card_count_draw_deck = deck.card_count_draw_deck
                    if card_count_draw_deck == 0:
                        break

                    player = player1


        print("***************")
        print("SCORES ROUND:", round)
        print("***************")
        print()


        player1.set_score(player1.sorted_hand)
        print("Score: " + name1)
        print(player1.score)

        player1.set_total_score(player1.score)
        print("Total score: " + name1)
        print(player1.total_score)

        player2.set_score(player2.sorted_hand)
        print("Score: " + name2)
        print(player2.score)

        player2.set_total_score(player2.score)
        print("Total score: " + name2)
        print(player2.total_score)

        deck.count_draw_deck(deck.draw_deck)
        print("Number of cards left in Draw Deck:")
        print(deck.card_count_draw_deck)


# Creates a dictionary with key as the player name and value as the Total Score.
total_score_dict[name1] = player1.total_score
total_score_dict[name2] = player2.total_score

# Determines the minimum value of values in the dictionary.
min_value = min(total_score_dict, key=lambda k: total_score_dict[k])

# Displays the winner of the game.
print("\nTHE WINNER IS: " + min_value)
