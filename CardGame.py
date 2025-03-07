"""
# Libraries:
    Random library used for coin toss to decide turn order.
    Regex library to parse user inputs
    OS library used for clearing console output between turns

    https://pypi.org/project/console-menu/
    Console-menu library used to simplify displaying and executing text menu functions per turn
"""

import random
import re
import os
import consolemenu

class Player():
    """
    Player class that represents a player in the game. Each player has a hand of cards, mana...
    """
    def __init__(self, name: str, deck=25, maxHP=20, maxMana=0, shield=0):
        self.name = name
        self.shield = shield
        self.maxHP = maxHP
        self.HP = maxHP
        self.maxMana = maxMana
        self.mana = maxMana
        self.deck = deck
        self.incomingAttack = 0
        self.hand = [] # contains Card objects in hand that can be played
        self.field = [] # contains UnitCard objects that can be used

    def __str__(self) -> str:
        return f"{self.name} has {self.HP}/{self.maxHP} HP and {self.mana}/{self.maxMana} mana"

    def drawCards(self, numCards: int) -> None:
        pass

    def playCard(self) -> None:
        pass

    def isAlive(self) -> bool:
        if self.HP <= 0:
            return False
        elif (self.deck <= 0) and (len(self.hand) == 0):
            return False
        return True
    
    def startTurn(self) -> None:
        # Start turn sequence
        print(f"Starting turn for {self.name}.")
        
        # draw 1 card, self.maxMana = min(10, self.maxMana + 1), self.mana = self.maxMana, print field
        # prompt with menu:
        #   play card from hand (print out names and atk/hp of cards in hand -> play unit from hand to field, or cast spell at a target)
        #   use card in field (choose a card and activate ability or have attack opposite player)
        #   print out field state again
        #   end turn
        #   forfeit

    def defendDamage(self, dmg: int) -> None:
        pass

    def awakenField(self) -> None:
        pass

class Card():
    """
    Card class that represents a card in the game. Each card has a name, a description, and a cost.
    """
    def __init__(self, name: str, description: str, cost: int):
        self.name = name
        self.cost = cost
        self.description = description

    def __str__(self) -> str:
        return f"{self.name}: {self.description}\nMana cost: {self.cost}"

    def __eq__(self, other) -> bool:
        return self.cost == other.cost

    def __lt__(self, other) -> bool:
        return self.cost < other.cost

    def __gt__(self, other) -> bool:
        return self.cost > other.cost

    def __le__(self, other) -> bool:
        return self.cost <= other.cost

    def __ge__(self, other) -> bool:
        return self.cost >= other.cost

    def __ne__(self, other) -> bool:
        return self.cost != other.cost
    
class UnitCard(Card):
    """
    UnitCard class that represents a playable unit in the game. Each card has a name, a description, a cost, an attack value, and health.
    """
    def __init__(self, name: str, description: str, cost: int, attack: int, maxHP: int):
        super().__init__(name, description, cost)
        self.attack = attack
        self.maxHP = maxHP
        self.HP = maxHP
        self.asleep = True # unit is asleep first turn. cannot block or attack. Awaken on next turn

    def __str__(self) -> str:
        return f"{self.name}: {self.description}\nMana cost: {self.cost}\nAttack: {self.attack}\nHP: {self.HP}/{self.maxHP}"
    
    def attack(self, target) -> None:
        pass
    
    def cast(self) -> None:
        raise NotImplementedError

class SpellCard(Card):
    """
    SpellCard class that represents a playable spell in the game. Each card has a name, a description, a cost, and an effect.
    """
    def __init__(self, name: str, description: str, cost: int):
        super().__init__(name, description, cost)

    def __str__(self) -> str:
        return f"{self.name}: {self.description}\nMana cost: {self.cost}"
    
    def cast(self) -> None:
        raise NotImplementedError

# from https://stackoverflow.com/questions/517970/how-can-i-clear-the-interpreter-console
clear = lambda: os.system('cls' if os.name == 'nt' else 'clear')

if __name__ == "__main__":
    print("Starting game...\n")
    player1 = Player(input("Enter name for player 1 (P1): "))
    player2 = Player(input("Enter name for player 2 (P2): "))
    player1.drawCards(5)
    player2.drawCards(5)

    # Determine player order and validate input
    response = ""
    while ((re.search(r"(?i)h(?:eads)?", response) is None) and (re.search(r"(?i)t(?:ails)?", response) is None)):
        print(response)
        response = input("P1 choose heads or tails: ")
    heads = (re.search(r"(?i)h(?:eads)?", response) is None)
    # Coin toss
    coin = random.randint(0,1)
    coinString = "Tails!" if coin else "Heads!"

    if (heads and not coin) and (not heads and coin):
        print(f"{coinString} {player1.name} goes first.")
        p1Start = True
    else:
        print(f"{coinString} {player2.name} goes first.")
        p1Start = False

    # Main loop to proceed with turns while someone has not lost/requested for game exit
    exitCondition = False
    while exitCondition == False:
        clear()
        if p1Start:
            # Start turn sequence
            print(f"Starting turn for {player1.name}.")
            player1.startTurn()

            # Block incoming damage
            if (player1.incomingAttack > 0):
                player1.blockAttack()
            
