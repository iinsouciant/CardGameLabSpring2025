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
    
# Note: Can Adjust VALUES of cards later on as the game runs to see fit, balance changes 

class Wizard(UnitCard):
    """
    Wizard class is a special type of UnitCard that posseses magical abilities; a unit that boosts card spells.
    """
    def __init__(self):
        super().__init__("Wizard", "A skilled sorcerer capable of boosting attributes of spells to support allies and manipulate opponents. Spells recieve double effects when casted.", cost = 3, attack = random.randint(2, 5), maxHP = random.randint(5, 7)) # super().__init__(name, description, cost, attack, maxHP)
    # HP: 5 - 7 or 4 HP?
    # Cost: 3 Mana - 4?
    # Attack: 2 - 5 (Doubler on spells)

class Tank(UnitCard):
    """
    Tank class is a special type of UnitCard that is able to absorb damage.
    """
    def __init__(self):
        super().__init__("Tank", "Armored unit possessing high health attributes that provides cover for the team.", cost = random.randint(5, 8), attack = random.randint(1, 2), maxHP = random.randint(12, 20))
    # HP 12 - 20
    # Cost: 5-8 mana?
    # Attack: 1 - 2 or 3?

class Attacker(UnitCard): #  Change to Knight ?
    """
    Attacker class is a special type of UnitCard that deals large amounts of damage.
    """
    def __init__(self):
        super().__init__("Knight", "Glorious, charming, and brave combatant able to land powerful slashes.", cost = random.randint(4, 5), attack = random.randint(5, 8), maxHP = random.randint(5, 8))
    # HP 5 - 8 ; 6 or 7 - 8 HP?
    # Cost: 4 - 5
    # Attack: 5 - 8

# Addition: 
'''
class Archer(UnitCard): 
    """
    Archer class is a special type of UnitCard that is able to pierce through tanks.
    """
    def __init__(self):
        super().__init__("Archer", "An artillery unit able to snipe enemies within a distance. Arrows will pierce tanks and do double damage from a range.", cost = 3, attack = random.randint(2, 4), maxHP = random.randint(5, 6))
    # HP 5 - 6
    # Cost: 3
    # Attack: 2 - 4 (Double damage when piercing tanks) if tank, 2x

class Bandit(UnitCard):
    """
    Bandit class is a special type of UnitCard that is stealthy and powerful but is vulnerable (posseses low health).
    """
    def __init__(self):
        super().__init__("Bandit", "A stealthy unit able to sneak behind enemy territories and infiltrate backlines while dealing massive damage if uncaught.", cost = 2, attack = random.randint(4, 8), maxHP = random.randint(1, 2))
    # HP 1 - 2
    # Cost: 2
    # Attack: 4 - 8
'''

# Fix spell implementation

class HealingSpell(SpellCard):
    """
    A SpellCard that restores the health of UnitCards.
    """
    def __init__(self, name = "Heal", description = "Heals a UnitCard", cost = 2):
        super().__init__(name, description, cost)
    # Heals 1 or 2 - 4 HP?

class DamageSpell(SpellCard):
    """
    A SpellCard that deals damage to an opposing UnitCard/Player.
    """
    def __init__(self, name = "Fireball", description = "Deals damage to an enemy unit", cost=3):
        super().__init__(name, description, cost)
        self.damage = random.randint(3, 4)

class ShieldSpell(SpellCard):
    """
    A SpellCard that provides shield for a UnitCard, an additional way to absorb damage.
    """
    def __init__(self, name = "Shield Cast", description = "Grants unit cards with an applicable shield that is capable of absorbing damage.", cost = random.randint(1, 2)):
        super().__init__(name, description, cost)
        self.shield = random.randint(1, 3) # Shields are set at 0 initially, applied when spell is casted
    # MANA 1 - 2?
    # Shield health random 1 - 3?

class DrawCardSpell(SpellCard):
    """
    A SpellCard that allows the player to draw additional cards.
    """
    def __init__(self, name = "Card Draw", description = "Player is allowed to draw addition cards.", cost = 2):
        super().__init__(name, description, cost)
        #self.drawRand = random.randint(1, 2)
    # Randomly generate a number of cards 1 - 2? 

'''
Requirements (Updated):
- Deck at least 25 cards, 2 players taking turns (lose if no HP and or no more cards in hand)
- Multiple types of cards, distinct classes that inherit from a basic Card class
- Cards WILL BE HELD in a linked list as a deck (be removed from the deck as the game is played)
'''
class Node:
    def __init__(self, card):
        self.card = card
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None
        self.size = 0

    def draw(self): 
        if not self.head:
            return None

    # "Potentially added back to the deck too" if needed
    def append(self, card): 
        current = self.head
        if not current: # Case #1 : If Empty
            self.head = Node(card)
        else:
            while current.next: # Case #2 : If list is not empty
                current = current.next
            current.next = Node(card)
        self.size += 1
        
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
            

