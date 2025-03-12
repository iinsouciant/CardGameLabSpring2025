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

class UnitNotFoundError(Exception):
    pass

class CardNotFoundError(Exception):
    pass

class Card():
    """
    Card class that represents a card in the game. Each card has a name, a description, and a cost.
    """

    def __init__(self, name: str, description: str, cost: int):
        self.name = name
        self.cost = cost
        self.description = description
        self.owner = None

    def __str__(self) -> str:
        return f"{self.name}: {self.description}\nMana cost: {self.cost}"
    
    def popFromHand(self):
        for i, unit in enumerate(self.owner.field):
            if unit == self:
                return self.owner.hand.pop(i)
        raise CardNotFoundError

    def cast(self, target) -> None:
        """override with method that does effects based on target type"""
        raise NotImplementedError
    
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
    
    def isAlive(self) -> bool:
        return self.HP > 0
    
    def setMaxHP(self, maxHP: int) -> None:
        self.maxHP = maxHP
        self.HP = min(self.HP, self.maxHP)
    
    def popFromField(self) -> Card:
        for i, unit in enumerate(self.owner.field):
            if unit == self:
                return self.owner.field.pop(i)
        raise UnitNotFoundError
    
    def blockAttack(self, card) -> int:
        # return damage dealt back to attacker
        self.HP -= card.attack
        # on death
        if self.HP <= 0:
            # overkill damage dealt to player
            self.owner.blockAttack(-self.HP)
            # remove from play
            self.popFromField()
        return self.attack

class SpellCard(Card):
    """
    SpellCard class that represents a playable spell in the game. Each card has a name, a description, a cost, and an effect.
    """
    def __init__(self, name: str, description: str, cost: int):
        super().__init__(name, description, cost)

    def __str__(self) -> str:
        return f"{self.name}: {self.description}\nMana cost: {self.cost}"
    
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

    def cast(self, target) -> None:
        self.HP -= target.blockAttack(self)
        if self.HP <= 0:
            self.popFromField()

class Attacker(UnitCard): #  Change to Knight ?
    """
    Attacker class is a special type of UnitCard that deals large amounts of damage.
    """
    def __init__(self):
        super().__init__("Knight", "Glorious, charming, and brave combatant able to land powerful slashes.", cost = random.randint(4, 5), attack = random.randint(5, 8), maxHP = random.randint(5, 8))
    # HP 5 - 8 ; 6 or 7 - 8 HP?
    # Cost: 4 - 5
    # Attack: 5 - 8

    def cast(self, target) -> None:
        self.HP -= target.blockAttack(self)
        if self.HP <= 0:
            self.popFromField()

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
    
    def forfeit(self) -> None:
        self.HP = -1

    def generateCard(self) -> Card:
        result = random.randint(0,6)
        match result:
            case 0:
                return Wizard()
            case 1:
                return Tank()
            case 2:
                return Attacker()
            case 3:
                return HealingSpell()
            case 4:
                return DamageSpell()
            case 5:
                return ShieldSpell()
            case 6:
                return DrawCardSpell()

    def drawCards(self, numCards: int) -> None:
        for i in range(numCards):
            self.hand.append(self.generateCard())

    def playCard(self, card) -> None:
        # put unit on field or cast at target if spell
        card.owner = self
        # handle card special effects here
        if issubclass(type(card), UnitCard):
            self.field.append(card)
            card.asleep = True
            return None
        elif issubclass(type(card), SpellCard):
            # how to handle if issubclass(type(card), SpellCard)?
            raise NotImplementedError
        else: 
            raise TypeError

    def isAlive(self) -> bool:
        if self.HP <= 0:
            return False
        elif (self.deck <= 0) and (len(self.hand) == 0):
            return False
        return True

    '''
    def startTurn(self) -> None:
        # Start turn sequence
        print(f"Starting turn for {self.name}.")
        
        # draw 1 card, self.maxMana = min(10, self.maxMana + 1), self.mana = self.maxMana, attackQueue emptied
        
        self.drawCards(1)
        self.maxMana = min(10, self.maxMana + 1)
        self.mana = self.maxMana
        # self.attackQueue = [] # empty the attack que

        # awaken units
        for unit in self.field:
            unit.awake = True # unit card possesses awake 
        
        # Instructions
        #- print field
        
        pass

        #- prompt with menu:
        #-    play card from hand (print out names and atk/hp of cards in hand -> play unit from hand to field, or cast spell at a target)
        #-    use card in field (choose a card and activate ability or have attack opposite player)
        #-    print out field state again
        #-    end turn
        #-    forfeit

        while True:
            print("\nSelect one of the following actions below: ")
            print("Enter an integer value (ex. 1, 2, 3, 4, 5)")
            print("================================================")
            print("1. Play card from hand (Units placing/Spell usage)")
            print("2. Use a card on the field (Activate ability/ATK Opponent)")
            print("3. View field state")
            print("4. End turn")
            print("5. Forfeit")

            selection = input("--> ")   

            if selection == "1":
                # play card from hand
            elif selection == "2":
                # use card on field
            elif selection == "3":
                # print field
            elif selection == "4":
                print(f"{self.name} has ended their turn.")
                break # terminate loop
            elif selection == "5":
                print(f"{self.name} has forfeited the game.")
                exit() # terimate the program
            else:
                print("Option is not valid, please try again.")
    '''

    def blockAttack(self, attack) -> None:
        if issubclass(type(attack), UnitCard):
            self.HP -= attack.attack
        elif issubclass(type(attack), SpellCard):
            raise NotImplementedError
        elif issubclass(type(attack), int):
            self.HP -= attack
        else:
            raise TypeError

    def awakenField(self) -> None:
        for unit in self.field:
            unit.asleep = False

    def attackWithCard(self, card) -> None:
        self.attackQueue.append(card)


'''
Requirements (Updated):
# Create the Player class to track health, deck state, etc and handle drawing and playing cards.

- Deck at least 25 cards, 2 players taking turns (lose if no HP and or no more cards in hand)
- Multiple types of cards, distinct classes that inherit from a basic Card class
- Cards WILL BE HELD in a linked list as a deck (be removed from the deck as the game is played)
'''

# null (none) to indicate end of the list
class Node: 
    def __init__(self, card):
        self.card = card
        self.next = None

class LinkedList:
    def __init__(self, maxCards = 50): # Can change amount of cards maximum in deck later, each player starts wtih 25 cards
        self.head = None
        self.size = 0
        self.maxCards = maxCards

    def drawCard(self): 
        if not self.head: # Check If the deck is empty
            return None 
        drawn = self.head.card
        self.head = self.head.next
        self.size -= 1
        return drawn

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
        
def playerOrder() -> bool:
    """Determine player order and validate input. Return True if P1 first"""
    response = ""
    heads = re.search(r"(?i)h(?:eads)?$", response)
    tails = re.search(r"(?i)t(?:ails)?$", response)
    player = re.search(r"(?i)p(?:layer)?[ ]?(1|2)$", response)
    while ((heads is None) and (tails is None) and (player is None)):
        print(response)
        response = input("P1 choose \"heads\" or \"tails\": ")
        heads = re.search(r"(?i)h(?:eads)?$", response)
        tails = re.search(r"(?i)t(?:ails)?$", response)
        player = re.search(r"(?i)p(?:layer)?[ ]?(1|2)$", response)
    
    # if specified player start
    if player is not None:
        playerNum = player.group(1)
        if playerNum == "1":
            return True
        return False
    
    resultIsTails = (tails is not None)
    # Coin toss
    coinIsTails = random.randint(0,1)
    coinString = "Tails!" if coinIsTails else "Heads!"

    if (resultIsTails and coinIsTails) or (not resultIsTails and not coinIsTails):
        print(f"{coinString} {player1.name} goes first.")
        return True
    print(f"{coinString} {player2.name} goes first.")
    return False

# from https://stackoverflow.com/questions/517970/how-can-i-clear-the-interpreter-console
clear = lambda: os.system('cls' if os.name == 'nt' else 'clear')

if __name__ == "__main__":
    print("Starting game...\n")
    player1 = Player(input("Enter name for player 1 (P1): "))
    player2 = Player(input("Enter name for player 2 (P2): "))
    player1.drawCards(5)
    player2.drawCards(5)

    p1Turn = playerOrder()

    # Create Text Menu with consolemenu
    # menu = consolemenu.ConsoleMenu("Hearthgathering","Play your turn")


    testCard1 = Attacker()
    testCard2 = Tank()
    testCard3 = Attacker()
    testCard2.setMaxHP(1)
    testCard4 = Tank()
    # Main loop to proceed with turns while someone has not lost/requested for game exit
    exitCondition = False
    currentPlayer = None
    turnCount = 0
    while exitCondition == False:
        if p1Turn:
           currentPlayer, otherPlayer = player1, player2
        else:
            currentPlayer, otherPlayer = player2, player1

        currentPlayer.startTurn()
        if not turnCount:
            otherPlayer.attackQueue.append(testCard1)
            otherPlayer.field.append(testCard1)
            otherPlayer.attackQueue.append(testCard3)
            otherPlayer.field.append(testCard3)
            currentPlayer.playCard(testCard4)
            currentPlayer.playCard(testCard2)
            currentPlayer.awakenField()

        # turn swap after player turn ends
        p1Turn = not p1Turn
        if p1Turn:
           currentPlayer, otherPlayer = player1, player2
        else:
            currentPlayer, otherPlayer = player2, player1
        clear()
        exitCondition = True if not currentPlayer.isAlive() else False
        turnCount += 1
        print(f"Turn {turnCount}")
        if turnCount >= 100: 
            print("Reached turn limit. Exiting program.")
            exit()

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
            forfeitItem = consolemenu.items.FunctionItem("Forfeit",currentPlayer.forfeit,should_exit=True)
            for attacker in otherPlayer.attackQueue:
                blockMenu = consolemenu.ConsoleMenu(title="Block Menu", subtitle=f"Defend against {attacker.name}: ({attacker.attack} ATK)-({attacker.HP}/{attacker.maxHP} HP)", show_exit_option=False)
                blockMenu.append_item(consolemenu.items.FunctionItem(f"{currentPlayer.name}: ({currentPlayer.HP}/{currentPlayer.maxHP} HP)",attacker.cast, args=[currentPlayer],should_exit=True))
                for defender in selectableUnits:
                    blockMenu.append_item(consolemenu.items.FunctionItem(f"{defender.name}: ({defender.attack} ATK)-({defender.HP}/{defender.maxHP} HP)",attacker.cast, args=[defender],should_exit=True))
                blockMenu.append_item(forfeitItem)
                blockMenu.show()
                blockMenu.join()
                # remove attacker once done
                otherPlayer.attackQueue.pop(0)
                # check if player has died from attack or ff'ed
                exitCondition = True if not currentPlayer.isAlive() else False


    # Win message
    if currentPlayer.isAlive():
        loser, winner = otherPlayer, currentPlayer
    else:
        winner, loser = otherPlayer, currentPlayer
    print(f"{loser.name} is dead! {winner.name} wins!")
            