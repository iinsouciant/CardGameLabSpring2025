"""
# Libraries:
    Random library used for coin toss to decide turn order.
    Regex library to parse user inputs
    OS library used for clearing console output between turns

    https://pypi.org/project/console-menu/
    Console-menu library used to simplify displaying and executing text menu functions per turn
"""

# new updated game

import random
import re
import os
import consolemenu
from consolemenu.items import *

'''
# from https://stackoverflow.com/questions/517970/how-can-i-clear-the-interpreter-console
clear = lambda: os.system('cls' if os.name == 'nt' else 'clear')
'''

# raise error later 
class UnitNotFoundError(Exception):
    pass

class CardNotFoundError(Exception):
    pass

# LinkedList Deck
'''
Cards will be held in a linked list as a deck and be removed from the deck as the game is played (and potentially added back to the deck too).
'''

class Node:
    def __init__(self, card):
        self.card = card
        self.next = None
    
class LinkedList:
    def __init__(self):
        self.head = None
        self.__size = 0

    def isEmpty(self):
        return self.__size == 0

    def addCard(self, card): # add random card to end of linked list
        """
        Add a new card node to the end of the linked list.
        """
        newNode = Node(card)
        self.__size += 1

        if not self.head:
            self.head = newNode
            return

        current = self.head
        while current.next:
            current = current.next
        current.next = newNode

    def removeCard(self): # draws card from deck, removes from front
        """
        Remove and return the card at the front of the linked list.
        Returns None if the list is empty.
        """
        if not self.head:
            return None

        removedNode = self.head
        self.head = self.head.next
        self.__size -= 1
        return removedNode.card
    
# ==========================================================================================================================

class Card:
    """
    Basic Card class that "distinct classes" will inherit from.
    The Card class that represents a card in the game. Each card has a name and a cost. (Descriptions of UnitCards displayed removed)
    """
    def __init__(self, name, cost):
        self.name = name
        self.cost = cost
        self.owner = None

    def popFromHand(self):
        for i, unit in enumerate(self.owner.hand):
            if unit == self:
                return self.owner.hand.pop(i)
        raise CardNotFoundError

    def play(self, player, opponent):
        raise NotImplementedError

# Have AT LEAST two distinct classes that inherit from a basic Card class (example: regular cards vs wild cards in Uno)

class UnitCard(Card):
    """
    UnitCard class that represents a playable unit in the game. Each card has a name, a cost, an attack value, and health (HP). 
    Examples:
      - Wizard
      - Tank
      - Attacker (Knight?)
      More to be added...
    """
    def __init__(self, name, cost, attack, health):
        super().__init__(name, cost)
        self.ATK = attack
        self.HP = health
        self.canAttack = False # can attack
        self.canDefend = False # can defend
        self.onField = False # can defend

    def __str__(self):
        return f"{self.name} [Cost={self.cost}, ATK={self.ATK}, HP={self.HP}]"

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

    def attack(self, target) -> None:
        self.HP -= target.blockAttack(self)
        if self.HP <= 0:
            self.popFromField()

    def blockAttack(self, card) -> int:
        # return damage dealt back to attacker
        self.HP -= card.ATK
        # on death
        if self.HP <= 0:
            # overkill damage dealt to player
            self.owner.blockAttack(-self.HP)
            # remove from play
            self.popFromField()
        return self.ATK

class SpellCard(Card):
    """
    SpellCard class that represents a playable spell in the game. Each card has a name, a description, a cost, and an effect.
    Examples:
      - Damage Spell
      - Draw extra cards spell
      - Heal Spell
      More to be added...
    """
    def __init__(self, name, cost, effectType, description=""):
        super().__init__(name, cost)
        self.effectType = effectType  # function that applies some effect implemented
        self.description = description

    def __str__(self):
        return f"{self.name} [Cost={self.cost}, SPELL: {self.description}]" 

    def play(self, target=None):
        if target is None:
            target = self.owner
        self.effectType(self.owner, target) # Casts spell when called

# ==========================================================================================================================
# Player Class

class Player:
    """
    Player class that represents a player in the game. Each player has a hand of cards, mana...
    """
    def __init__(self, name, deck):
        self.name = name
        #self.shield = shield (to be implemented in the future)
        self.HP = 20 # All players hp 20 (adjust if needed)
        self.mana = 0 
        self.maxMana = 2 # Start with 3 mana max (adjust if needed)
        self.deck = deck  # Deck held in a LinkedList
        self.hand = []  # List of cards in the player's hand
        self.field = []  # List of UnitCards on the field
        self.attackQueue = []
        self.forfeited = False
        self.opponent = None

    def forfeit(self) -> None:
        self.forfeited = True

    def setOpponent(self, opponent) -> None:
        if type(opponent) is Player:
            self.opponent = opponent
        else:
            raise TypeError

    def drawCards(self, amount = 1): 
        """
        Used to draw an "amount" of cards from deck into hand.
        """
        for i in range(amount):
            if self.deck.isEmpty():
                return  # Check if deck is empty, Can't draw if deck is empty
            cardDrawn = self.deck.removeCard()
            if cardDrawn:
                self.hand.append(cardDrawn)

    def incrementMana(self): # self.maxMana = min(10, self.maxMana + 1)
        """
        Increase max mana per turn by 1 (max mana is 10). Will keep refreshing mana to full.
        """
        if self.maxMana < 10:
            self.maxMana += 1
        self.mana = self.maxMana # Start with 3 mana max

    def playCardFromHand(self, card, target=None) -> None:
        """
        Put unit on field or cast at target if spell; attempts to play a card from the hand.
        """
        if card.cost <= self.mana:
            card.owner = self
            self.mana -= card.cost
            card.popFromHand()
            # handle card special effects here
            if issubclass(type(card), UnitCard) or (type(card) is UnitCard):
                self.field.append(card)
                print(f"{self.name} played unit: {card.name}")
                return
            elif issubclass(type(card), SpellCard) or (type(card) is SpellCard):
                card.play(target)
                print(f"{self.name} played spell: {card.name}")
                return
            else: 
                raise TypeError
        print("Insufficient mana.")
        
    def endTurn(self) -> bool:
        return True
    
    def printBoard(self) -> None:
        print(
            f"\n{self.name}'s TURN (HP={self.HP}, Mana={self.mana}/{self.maxMana})")
        print(f"{self.name} hand: {[str(c) for c in self.hand]}")
        print(f"{self.name} field: {[str(u) for u in self.field]}")
        print(f"{self.opponent.name} field: {[str(u) for u in self.opponent.field]}")

    def startMainPhase(self, roundCount: int):
        """
        Simplified turn seq:
        #-    play card from hand (print out names and atk/hp of cards in hand -> play unit from hand to field, or cast spell at a target)
        #-    use card in field (choose a card and activate ability or have attack opposite player, skip, etc)
        #-    print out field state again
        #-    end turn
        #-    forfeit
        """
        self.incrementMana()
        self.resetActions()
        self.drawCards(1) # free draw per turn
        print(f"{self.name} has attempted to draw 1 card.")

        endTurn = False
        i = 0

        while not endTurn:
            mainTurnMenu = consolemenu.ConsoleMenu(title=f"Main Phase - Round {roundCount}", subtitle=f"{self.name}'s TURN (HP={self.HP}, Mana={self.mana}/{self.maxMana})\
            \n{self.name}\'s field: {[str(u) for u in self.field]}\
            \n{self.name} hand: {[str(c) for c in self.hand]}", show_exit_option=False, clear_screen=False)

            # submenu for available units in field to attack with
            unitAttackSubmenu = consolemenu.ConsoleMenu(title=f"Attack {self.opponent.name} with Units on Field")
            unitAttackSubmenuItem = SubmenuItem("Attack with units", submenu=unitAttackSubmenu, should_exit=True)
            for unit in self.field:
                if unit.canAttack:
                    unitAttackSubmenu.append_item(FunctionItem(f"{unit.name}: ({unit.ATK} ATK)-({unit.HP} HP)", self.unitAttack, args=[unit], should_exit=True))
            # submenu for units in hand to play (will need to validate cost on playing)
            unitPlaySubmenu = consolemenu.ConsoleMenu(title=f"Place Unit on Field")
            unitPlaySubmenuItem = SubmenuItem("Play units from hand", submenu=unitPlaySubmenu, should_exit=True)
            for card in self.hand:
                if issubclass(type(card), UnitCard):
                    unitPlaySubmenu.append_item(FunctionItem(f"{card.name} (M:{card.cost}): ({card.ATK} ATK)-({card.HP} HP)", self.playCardFromHand, args=[card],should_exit=True))
            # submenu for spells in hand to play
            spellPlaySubmenu = consolemenu.ConsoleMenu(title=f"Cast a spell from your hand then target", clear_screen=False)
            spellPlaySubmenuItem = SubmenuItem("Play spells from hand", submenu=spellPlaySubmenu, should_exit=True)
            for card in self.hand:
                if issubclass(type(card), SpellCard):
                    spellTargetSubmenu = consolemenu.ConsoleMenu(title=f"Pick a target to cast {card.name} on", clear_screen=False)
                    spellTargetSubmenuItem = SubmenuItem(str(card), submenu=spellTargetSubmenu)
                    # target self
                    spellTargetSubmenu.append_item(FunctionItem(f"{self.name}: ({self.HP} HP)", self.playCardFromHand, args=[card,self],should_exit=True))
                    # target opponent
                    spellTargetSubmenu.append_item(FunctionItem(f"{self.opponent.name}: ({self.opponent.HP} HP)", self.playCardFromHand, args=[card,self.opponent],should_exit=True))
                    # target units on field
                    for unit in self.field:
                        spellTargetSubmenu.append_item(FunctionItem(f"{self.name}\'s {unit.name}: ({unit.ATK} ATK)-({unit.HP} HP)", self.playCardFromHand, args=[card,unit],should_exit=True))
                    for unit in self.opponent.field:
                        spellTargetSubmenu.append_item(FunctionItem(f"{self.opponent.name}\'s {unit.name}: ({unit.ATK} ATK)-({unit.HP} HP)", self.playCardFromHand, args=[card,unit],should_exit=True))
                    spellPlaySubmenu.append_item(spellTargetSubmenuItem)
            # print field state
            fieldStateItem = FunctionItem("Print field state", self.printBoard, should_exit=True)
            # end turn
            endTurnItem = FunctionItem("End turn", self.endTurn, should_exit=True)
            # ff 
            forfeitItem = FunctionItem("Forfeit", self.forfeit, should_exit=True)

            # append all menus
            mainTurnMenu.append_item(unitAttackSubmenuItem)
            mainTurnMenu.append_item(unitPlaySubmenuItem)
            mainTurnMenu.append_item(spellPlaySubmenuItem)
            mainTurnMenu.append_item(fieldStateItem)
            mainTurnMenu.append_item(endTurnItem)
            mainTurnMenu.append_item(forfeitItem)

            mainTurnMenu.show()
            mainTurnMenu.join()
            '''
            while True:
                choice = input(f"[{self.name}'s Turn] Unit {unit.name} (Atk={unit.ATK}, HP={unit.HP}) action?\n"
                            "(1) Attack\n(2) Defend\n(3) Skip\n"
                            "Enter choice --> ") # simplified, actions for units
                if choice == '1':
                    if unit.canAttack:
                        self.unitAttack(unit, opponent)
                        unit.canAttack = False  # Used up its attack
                        return
                    else:
                        print(f"{unit.name} cannot attack this turn.")
                        return
                elif choice == '2':
                    if unit.canDefend:
                        print(f"{unit.name} is set to defend next attack.")
                        unit.canDefend = False  # Unit now in "defending" mode
                        return
                    else:
                        print(f"{unit.name} cannot defend this turn.")
                        return
                elif choice == '3':
                    print(f"{unit.name} does nothing.")
                    return
                else:
                    print("Invalid choice. Try again.") # If not valid int is entered 
            break if loops exceeded or if end turn/forfeit selected'''
            endTurn = endTurnItem.get_return()
            winner = checkConditions(self, self.opponent) # check game end conditions again
            if (i >= 100) or winner:
                break

    def blockPhase(self):
        # Block phase
        if len(self.opponent.attackQueue) > 0:
            # create a menu that allows player to select and unselect any number of available units on field
            # create a menu option to confirm ending block phase
            # ending block phase computes player health then computes unit health/death
            selectableUnits = []
            for unit in self.field:
                if unit.asleep is not True:
                    selectableUnits.append(unit)
            
            # create blocking menu
            forfeitItem = consolemenu.items.FunctionItem("Forfeit",self.forfeit,should_exit=True)
            for attacker in self.opponent.attackQueue:
                blockMenu = consolemenu.ConsoleMenu(title="Block Menu", subtitle=f"Defend against {attacker.name}: ({attacker.ATK} ATK)-({attacker.HP} HP)", show_exit_option=False, clear_screen=False)
                blockMenu.append_item(consolemenu.items.FunctionItem(f"{self.name}: ({self.HP} HP)",attacker.cast, args=[self],should_exit=True))
                for defender in selectableUnits:
                    blockMenu.append_item(consolemenu.items.FunctionItem(f"{defender.name}: ({defender.ATK} ATK)-({defender.HP} HP)",attacker.cast, args=[defender],should_exit=True))
                blockMenu.append_item(forfeitItem)
                blockMenu.show()
                blockMenu.join()
                # remove attacker once done
                self.opponent.attackQueue.pop(0)
                # check if player has died from attack or ff'ed
                winner = checkConditions(self, self.opponent) # check game end conditions again
                if winner:
                    print(f"Game Over! Winner: {winner}")
                    return

    def unitAttack(self, unit):
        """
        Prompts an attack on the opponent's field. Attacks player's HP if no defending units; attacks random defending card. (specific implementation in the future)
        """
        self.attackQueue.append(unit)
        unit.canAttack = unit.canDefend =False
        '''# Filter out units that have chosen to defend (or we can pick them).
        defendingUnits = [u for u in opponent.field if not u.canDefend]
        if defendingUnits:
            # We just pick the first 'defending' unit for demonstration
            defender = defendingUnits[0]
            print(f"{unit.name} (ATK={unit.ATK}) attacks {defender.name} (HP={defender.HP}).")

            defender.HP -= unit.ATK # compare/damage

            # Remove unit from the field if dead
            if defender.HP <= 0:
                overflowDamage = abs(defender.HP) # can't have negative HP
                print(f"{defender.name} is destroyed! Overflow damage = {overflowDamage}")
                opponent.field.remove(defender)
                opponent.HP -= overflowDamage # applies to player
            else:
                print(f"{defender.name} survives with {defender.HP} HP.")
        else:
            print(f"{unit.name} hits {opponent.name} directly for {unit.ATK} damage!")
            opponent.HP -= unit.ATK # if no defending units played

        # Edit: (Print updated HP of both players) - to keep track better
        print(f"{opponent.name}'s HP: {opponent.HP}")
        print(f"{self.name}'s HP: {self.HP}")'''
        
    def resetActions(self): # resets the unit actions
        """
        Changed for simplicity, everything just defends and attacks reset (asleep may be implemented in the future)
        """
        for unit in self.field:
            unit.canAttack = True
            unit.canDefend = True
    
# ================================================================================================================

# Spell functions (more to be implemented later)
def spellDrawCards(player, target):
    """ Draw 2 cards from own deck. """
    if target.deck.isEmpty():
        print("No cards in deck!")
        return
    print(f"{target.name} attempts to draw 2 cards from the deck.")
    for i in range(2):
        if target.deck.isEmpty():
            print("No more cards left in the deck!")
            break
        target.drawCards(1)

def spellFireball(player, target):
    """ Deal 3 damage directly to opponent's HP or overflow to their units first. """
    damage = 3
    print(f"\n{player.name} casts Fireball!")

    # Apply damage to target
    print(f"  {target.name} takes {damage} direct damage!")
    target.HP -= damage

    print(f"{target.name}'s current HP: {target.HP}")

def spellHealing(player, target):
    """ Heal 5 HP for units on the field first, then heal player if necessary. """
    healingAmount = 5
    print(f"{player.name} casts Healing Light!")

    # Apply healing/overheal to target
    if healingAmount > 0:
        target.HP += healingAmount
        print(f"  {target.name} heals for {healingAmount} HP!")
        # Ensure HP doesn't exceed 20 (or any desired max HP)
        if target.HP > 20:
            target.HP = 20
        print(f"{target.name}'s current HP: {target.HP}")

# ================================================================================================================

# Game functions 
def buildDeck(numCards=30): # default size in deck
    """
    - Builds a random deck (LinkedList) of 25 cards (for each player minimum).
    """
    randomUnits = [
        ("Wizard", 4, 4, 6),
        ("Tank", 6, 2, 12),
        ("Knight", 5, 5, 7),
        ("Archer", 3, 3, 5),
        ("Bandit", 2, 4, 2)
    ]
    """
    Wizard class is a special type of UnitCard that posseses magical abilities. (Future Implementation ex: a unit that boosts card spells.)

    Tank class is a special type of UnitCard that is able to absorb damage.

    Attacker (Knight) class is a special type of UnitCard that deals large amounts of damage.

    Archer class is a special type of UnitCard that is able to deal moderate damage from afar. (Future Implementation ex: pierce through tanks, 2x damage.)

    Bandit class is a special type of UnitCard that is stealthy and powerful but is vulnerable (posseses low health).

    """

    randomSpells = [
        ("Draw Spell", 3, spellDrawCards, "Draw 2 cards"),
        ("Fireball", 4, spellFireball, "Deal 3 damage to opponent"),
        ("Heal", 3, spellHealing, "Heal 5 HP")
    ]

    """
    Heal: A SpellCard that restores the health of UnitCards.

    Damage (Fireball): A SpellCard that deals damage to an opposing UnitCard/Player.

    Draw: A SpellCard that allows the player to draw additional cards.
    """

    deck = LinkedList()
    for i in range(numCards):
        if random.random() < 0.5: # making it a 50/50 chance of picking a unit or a spell
            name, cost, atk, hp = random.choice(randomUnits)
            deck.addCard(UnitCard(name, cost, atk, hp))
        else:
            name, cost, effect, desc = random.choice(randomSpells)
            deck.addCard(SpellCard(name, cost, effect, desc))

    return deck

def coinToss(): # same as ? return random.choice([True, False]) 
    '''
    Coin flip simplification:
    https://stackoverflow.com/questions/6824681/get-a-random-boolean-in-python
    '''
    return random.choice([True, False])
    # Same implementation as old coin flip, automized

def checkConditions(player1, player2):
    """
    Check if either player: 
    - no more hp
    - no cards in hand + deck
    - forfeit.
    """
    if player1.forfeited: # Check forfeit 
        print(f"{player2.name} wins because {player1.name} forfeited the game!")
        return "Player2"
    if player2.forfeited:
        print(f"{player1.name} wins because {player2.name} forfeited the game!")
        return "Player1"
    if player1.HP <= 0: # Check HP
        print(f"\n{player2.name} wins because {player1.name} has no more HP!")
        return "Player2"
    if player2.HP <= 0:
        print(f"\n{player1.name} wins because {player2.name} has no more HP!")
        return "Player1"
    if player1.deck.isEmpty() and len(player1.hand) == 0 and len(player1.field) == 0: # Deck/Hand check: if a player's deck is empty AND their hand is empty AND they have no units on field results in a loss
        print(f"\n{player2.name} wins because {player1.name} has no more cards to play!")
        return "Player2"
    if player2.deck.isEmpty() and len(player2.hand) == 0 and len(player2.field) == 0:
        print(f"\n{player1.name} wins because {player2.name} has no more cards to play!")
        return "Player1"
    return None

# Future
# Create Text Menu with consolemenu
# menu = consolemenu.ConsoleMenu("Hearthgathering","Play your turn")

def main():
    print("=========================================")
    print("Welcome to the Hearthgathering Card Game")
    print("A simple digital collectible card game...!")
    print("=========================================")
    p1Deck = buildDeck(30) # How many cards in deck setter (deck at least 25 cards), random deck build
    p2Deck = buildDeck(30) # If set at 6 for example, no cards will be drawn empty deck, # 1 or 0 to test if no cards and no deck error
    player1 = Player(input("Enter name for player 1 (P1): "), p1Deck)
    player2 = Player(input("Enter name for player 2 (P2): "), p2Deck)
    player1.drawCards(5) # adjust if needed start with 5 as in brainstorms
    player2.drawCards(5)
    player1.setOpponent(player2)
    player2.setOpponent(player1)

    # Coin toss
    p1Turn = coinToss()
    if p1Turn:
        print("Player1 won the coin toss! Player1 goes first.")
    else:
        print("Player2 won the coin toss! Player2 goes first.")

    # Start the main game loop
    roundCount = 1
    while True:
        print(f"\n=== ROUND {roundCount} ===\n")
        currentPlayer = player1 if p1Turn else player2
        opponentPlayer = player2 if p1Turn else player1
        currentPlayer.blockPhase()
        currentPlayer.startMainPhase(roundCount)

        '''# Menu dusplay simplified 
        print(
            f"\n{currentPlayer.name}'s TURN (HP={currentPlayer.HP}, Mana={currentPlayer.mana}/{currentPlayer.maxMana})")
        print(f"{currentPlayer.name} hand: {[str(c) for c in currentPlayer.hand]}")
        print(f"{currentPlayer.name} field: {[str(u) for u in currentPlayer.field]}")
        print(f"{opponentPlayer.name} field: {[str(u) for u in opponentPlayer.field]}")
        print(f"Type 'play <index>' (starts at 0) to play a card from your hand, 'forfeit' to give up, or 'end' to end your turn.")
        while True:
            command = input(f"{currentPlayer.name}, enter command: ").strip().lower()
            if command.startswith("play"): # parse index
                parts = command.split()
                if len(parts) == 2 and parts[1].isdigit():
                    cardIndex = int(parts[1])
                    currentPlayer.playCard(cardIndex, opponentPlayer)
                else:
                    print("Usage: play <hand index>")
            elif command == "forfeit":
                print(f"{currentPlayer.name} forfeits the game!")
                currentPlayer.forfeited = True
                break
            elif command == "end":
                break
            else:
                print("Unknown command. Options: 'play <index>', 'end', 'forfeit'.")

            winner = checkConditions(player1, player2) # check game end conditions again
            if winner:
                print(f"Game Over! Winner: {winner}")
                return

        # Menu to choose actions for units on field
        print(f"\n{currentPlayer.name} is deciding actions for their Units...")
        for unit in currentPlayer.field:
            if unit.HP > 0:
                currentPlayer.startTurn(unit, opponentPlayer)
            else:
                currentPlayer.field.remove(unit) # "Remove dead units if any slipped through"

        winner = checkConditions(player1, player2) # check game end conditions again
        if winner:
            print(f"Game Over! Winner: {winner}")
            return'''
        
        p1Turn = not p1Turn # turn switch
        roundCount += 1 # round counter implement max amount of rounds who has the higher HP wins?
        winner = checkConditions(player1, player2) # check game end conditions again
        if (roundCount >= 100) or winner:
            break
if __name__ == "__main__":
    main()

# Old Template
'''
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
        self.ATK = attack
        self.maxHP = maxHP
        self.HP = maxHP
        self.asleep = True # unit is asleep first turn. cannot block or attack. Awaken on next turn

    def __str__(self) -> str:
        return f"{self.name}: {self.description}\nMana cost: {self.cost}\nAttack: {self.ATK}\nHP: {self.HP}/{self.maxHP}"
    
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
        self.HP -= card.ATK
        # on death
        if self.HP <= 0:
            # overkill damage dealt to player
            self.owner.blockAttack(-self.HP)
            # remove from play
            self.popFromField()
        return self.ATK

class SpellCard(Card):
    """
    SpellCard class that represents a playable spell in the game. Each card has a name, a description, a cost, and an effect.
    """
    def __init__(self, name: str, description: str, cost: int):
        super().__init__(name, description, cost)

    def __str__(self) -> str:
        return f"{self.name}: {self.description}\nMana cost: {self.cost}"
    
# Note: Can Adjust VALUES of cards later on as the game runs to see fit, balance changes 

# Change
units = [
        ("Wizard", 4, 4, 6),
        ("Tank", 6, 2, 12),
        ("Knight", 5, 5, 7),
        ("Archer", 3, 3, 5),
        ("Bandit", 2, 4, 2)
    ]
'''
'''
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
    # Randomly generate a number of cards 1 - 2? '''
'''

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
        self.deck = deck # LinkedList
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
    def blockAttack(self, attack) -> None:
        if issubclass(type(attack), UnitCard):
            self.HP -= attack.ATK
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

'''
Requirements (Updated):
# Create the Player class to track health, deck state, etc and handle drawing and playing cards.

- Deck at least 25 cards, 2 players taking turns (lose if no HP and or no more cards in hand)
- Multiple types of cards, distinct classes that inherit from a basic Card class
- Cards WILL BE HELD in a linked list as a deck (be removed from the deck as the game is played)
# null (none) to indicate end of the list'
'''

'''
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
                blockMenu = consolemenu.ConsoleMenu(title="Block Menu", subtitle=f"Defend against {attacker.name}: ({attacker.ATK} ATK)-({attacker.HP}/{attacker.maxHP} HP)", show_exit_option=False)
                blockMenu.append_item(consolemenu.items.FunctionItem(f"{currentPlayer.name}: ({currentPlayer.HP}/{currentPlayer.maxHP} HP)",attacker.cast, args=[currentPlayer],should_exit=True))
                for defender in selectableUnits:
                    blockMenu.append_item(consolemenu.items.FunctionItem(f"{defender.name}: ({defender.ATK} ATK)-({defender.HP}/{defender.maxHP} HP)",attacker.cast, args=[defender],should_exit=True))
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
'''
"""
# Libraries:
    Random library used for coin toss to decide turn order.
    Regex library to parse user inputs
    (deleted) OS library used for clearing console output between turns

    https://pypi.org/project/console-menu/
    Inspriation: Console-menu library used to simplify displaying and executing text menu functions per turn
"""