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
        self.hand = [] # contains Card objects in hand that can be played
        self.field = [] # contains UnitCard objects that can be used
        self.attackQueue = [] # used to hold what cards are being attacked with for opponent's block phase

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
        
        # draw 1 card, self.maxMana = min(10, self.maxMana + 1), self.mana = self.maxMana, attackQueue emptied
        # awaken units
        # print field
        # prompt with menu:
        #   play card from hand (print out names and atk/hp of cards in hand -> play unit from hand to field, or cast spell at a target)
        #   use card in field (choose a card and activate ability or have attack opposite player)
        #   print out field state again
        #   end turn
        #   forfeit

    def blockAttack(self, card) -> None:
        pass

    def awakenField(self) -> None:
        pass

    def attackWithCard(self, card) -> None:
        self.attackQueue.append(card)


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
    
    def cast(self, target) -> None:
        raise NotImplementedError
    
    def blockAttack(self, card) -> int:
        # return any overkill damage
        pass

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
        p1Turn = True
    else:
        print(f"{coinString} {player2.name} goes first.")
        p1Turn = False

    # Create Text Menu with consolemenu
    # menu = consolemenu.ConsoleMenu("Hearthgathering","Play your turn")


    testCard1 = UnitCard("test", "test", 3, 1, 2)
    testCard2 = UnitCard("test", "test", 3, 1, 1)
    testCard2.asleep = False
    # Main loop to proceed with turns while someone has not lost/requested for game exit
    exitCondition = False
    currentPlayer = None
    i = 0
    while exitCondition == False:
        clear()
        if p1Turn:
           currentPlayer, otherPlayer = player1, player2
        else:
            currentPlayer, otherPlayer = player2, player1

        currentPlayer.startTurn()
        currentPlayer.attackQueue.append(testCard1)
        currentPlayer.field.append(testCard2)

        # Block phase
        if len(otherPlayer.attackQueue) > 0:
            # create a menu that allows player to select and unselect any number of available units on field
            # create a menu option to confirm ending block phase
            # ending block phase computes player health then computes unit health/death
            selectableUnits = []
            for unit in currentPlayer.field:
                if unit.asleep is not True:
                    selectableUnits.append(unit)
            
            # create blocking menu
            for attacker in otherPlayer.attackQueue:
                blockMenu = consolemenu.ConsoleMenu(title="Block Menu", subtitle=f"Defend against {attacker.name}: ({attacker.attack})-({attacker.HP}/{attacker.maxHP})")
                blockMenu.exit_item.text = "Forfeit"
                blockMenu.append_item(consolemenu.items.FunctionItem(f"{currentPlayer.name}: ({currentPlayer.HP}/{currentPlayer.maxHP})",attacker.cast, args=[currentPlayer]))
                for defender in selectableUnits:
                    blockMenu.append_item(consolemenu.items.FunctionItem(f"{defender.name}: ({defender.attack})-({defender.HP}/{defender.maxHP})",attacker.cast, args=[defender]))

                blockMenu.show()
                blockMenu.join()

                if (not currentPlayer.isAlive()) or (blockMenu.exit_item.should_exit):
                    exitCondition = True

        exitCondition = True if not currentPlayer.isAlive() else False

        
        p1Turn = not p1Turn
        i += 1
        print(i)
        if i >= 500: # placeholder to prevent being stuck in infinite loop
            print("Stuck in inifinite loop. Exiting program.")
            exitCondition = True

    print(f"{currentPlayer.name} is dead! {otherPlayer.name} wins!")
            
