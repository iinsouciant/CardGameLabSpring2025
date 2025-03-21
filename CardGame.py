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
        backlash = target.blockAttack(self)
        self.HP -= backlash
        if backlash > 0:
            print(f"{self.name} has taken {backlash} damage. HP = {self.HP}")
        if self.HP <= 0:
            self.popFromField()

    def blockAttack(self, card) -> int: # TODO fix player not taking damage
        # return damage dealt back to attacker
        self.HP -= card.ATK
        print(f"{self.name} has taken {card.ATK} damage. HP = {self.HP}")
        # on death
        if self.HP <= 0:
            # overkill damage dealt to player
            self.owner.blockAttack(-self.HP)
            # remove from play
            self.popFromField() # TODO fix unit not being removed from field
            print(f"{self.name} has died. Removing from field.\n")
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
        self.HP = 0

    def isAlive(self) -> bool:
        if self.forfeited or self.HP <= 0 or (self.deck.isEmpty() and len(self.hand) == 0 and len(self.field) == 0):
            return False
        return True

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

    def blockAttack(self, attack) -> int:
        if issubclass(type(attack), UnitCard):
            self.HP -= attack.ATK
            print(f"{self.name} has taken {attack.ATK} damage. HP = {self.HP}")
            return 0
        elif issubclass(type(attack), SpellCard):
            raise NotImplementedError
        elif issubclass(type(attack), int):
            self.HP -= attack
            print(f"{self.name} has taken {attack} damage. HP = {self.HP}")
            return 0
        else:
            raise TypeError

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
            unitAttackSubmenu = consolemenu.ConsoleMenu(title=f"Attack {self.opponent.name} with Units on Field", subtitle="Units must wait one turn to attack or defend", clear_screen=False)
            unitAttackSubmenuItem = SubmenuItem("Attack with units", submenu=unitAttackSubmenu, should_exit=True)
            for unit in self.field:
                if unit.canAttack:
                    unitAttackSubmenu.append_item(FunctionItem(f"{unit.name}: ({unit.ATK} ATK)-({unit.HP} HP)", self.unitAttack, args=[unit], should_exit=True))
            # submenu for units in hand to play (will need to validate cost on playing)
            unitPlaySubmenu = consolemenu.ConsoleMenu(title=f"Place Unit on Field", clear_screen=False)
            unitPlaySubmenuItem = SubmenuItem("Play units from hand", submenu=unitPlaySubmenu, should_exit=True)
            for card in self.hand:
                if issubclass(type(card), UnitCard):
                    unitPlaySubmenu.append_item(FunctionItem(f"{card.name} (M:{card.cost}): ({card.ATK} ATK)-({card.HP} HP)", self.playCardFromHand, args=[card],should_exit=True))
            # submenu for spells in hand to play
            spellPlaySubmenu = consolemenu.ConsoleMenu(title=f"(Mana={self.mana}/{self.maxMana}) Cast a spell from your hand then target", clear_screen=False)
            spellPlaySubmenuItem = SubmenuItem("Play spells from hand", submenu=spellPlaySubmenu, should_exit=True)
            for card in self.hand: # TODO for draw card, don't allow targeting of units
                if issubclass(type(card), SpellCard):
                    spellTargetSubmenu = consolemenu.ConsoleMenu(title=f"Pick a target to cast {card.name} on", clear_screen=False)
                    spellTargetSubmenuItem = SubmenuItem(str(card), submenu=spellTargetSubmenu, should_exit=True)
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
            fieldStateItem = FunctionItem("Print field state", self.printBoard, should_exit=False)
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
            endTurn = endTurnItem.get_return()
            if (i >= 100) or not self.isAlive() or not self.opponent.isAlive():
                break

    def blockPhase(self):
        # Block phase
        if len(self.opponent.attackQueue) > 0:
            # create a menu that allows player to select and unselect any number of available units on field
            # create a menu option to confirm ending block phase
            # ending block phase computes player health then computes unit health/death
            selectableUnits = []
            for unit in self.field:
                if unit.canDefend is True:
                    selectableUnits.append(unit)
            
            # create blocking menu
            forfeitItem = consolemenu.items.FunctionItem("Forfeit",self.forfeit,should_exit=True)
            for attacker in self.opponent.attackQueue:
                blockMenu = consolemenu.ConsoleMenu(title="Block Menu", subtitle=f"Defend against {attacker.name}: ({attacker.ATK} ATK)-({attacker.HP} HP)", show_exit_option=False, clear_screen=False)
                blockMenu.append_item(consolemenu.items.FunctionItem(f"{self.name}: ({self.HP} HP)",attacker.attack, args=[self],should_exit=True))
                for defender in selectableUnits:
                    blockMenu.append_item(consolemenu.items.FunctionItem(f"{defender.name}: ({defender.ATK} ATK)-({defender.HP} HP)",attacker.attack, args=[defender],should_exit=True))
                blockMenu.append_item(forfeitItem)
                blockMenu.show()
                blockMenu.join()
                # remove attacker once done
                self.opponent.attackQueue.pop(0)
                # check if player has died from attack or ff'ed
                if not self.isAlive():
                    return

    def unitAttack(self, unit):
        """
        Prompts an attack on the opponent's field. Attacks player's HP if no defending units; attacks random defending card. (specific implementation in the future)
        """
        self.attackQueue.append(unit)
        unit.canAttack = unit.canDefend =False
        
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
    if target.HP <= 0:
        target.popFromField()
        print(f"{target.name} has died. Removing from field.\n") 

    print(f"{target.name}'s current HP: {target.HP}") # accounts display overflow

def spellHealing(player, target):
    """ Heal 5 HP for units on the field first, then heal player if necessary. """
    healingAmount = 5
    print(f"{player.name} casts Healing Light!")

    # Apply healing/overheal to target
    if healingAmount > 0:
        target.HP += healingAmount
        print(f"  {target.name} heals for {healingAmount} HP! (Max 20 HP)")
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
        winner = checkConditions(player1, player2) # check game end conditions
        if (roundCount >= 100) or winner:
            break
        currentPlayer.startMainPhase(roundCount)

        p1Turn = not p1Turn # turn switch
        roundCount += 1 # round counter implement max amount of rounds who has the higher HP wins?
        winner = checkConditions(player1, player2) # check game end conditions again
        if (roundCount >= 100) or winner:
            break
if __name__ == "__main__":
    main()
