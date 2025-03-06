"""
Some description of each of the cards/classes implemented for this game
"""

import random

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
        self.hand = []

    def __str__(self):
        return f"{self.name} has {self.HP}/{self.maxHP} HP and {self.mana}/{self.maxMana} mana"

    def drawCards(self, numCards: int):
        pass

    def playCard(self):
        pass

    def isAlive(self):
        if self.HP <= 0:
            return False
        elif (self.deck <= 0) and (len(self.hand) == 0):
            return False
        return True

class Card():
    """
    Card class that represents a card in the game. Each card has a name, a description, and a cost.
    """
    def __init__(self, name: str, description: str, cost: int):
        self.name = name
        self.cost = cost
        self.description = description

    def __str__(self):
        return f"{self.name}: {self.description}\nMana cost: {self.cost}"

    def __eq__(self, other):
        return self.cost == other.cost

    def __lt__(self, other):
        return self.cost < other.cost

    def __gt__(self, other):
        return self.cost > other.cost

    def __le__(self, other):
        return self.cost <= other.cost

    def __ge__(self, other):
        return self.cost >= other.cost

    def __ne__(self, other):
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

    def __str__(self):
        return f"{self.name}: {self.description}\nMana cost: {self.cost}\nAttack: {self.attack}\nHP: {self.HP}/{self.maxHP}"
    
    def attack(self, target):
        pass
    
    def cast(self):
        raise NotImplementedError

class SpellCard(Card):
    """
    SpellCard class that represents a playable spell in the game. Each card has a name, a description, a cost, and an effect.
    """
    def __init__(self, name: str, description: str, cost: int):
        super().__init__(name, description, cost)

    def __str__(self):
        return f"{self.name}: {self.description}\nMana cost: {self.cost}"
    
    def cast(self):
        raise NotImplementedError

if __name__ == "__main__":
    pass

# Class Creation

class Wizard(UnitCard):
    """
    Wizard class is a special type of UnitCard that posseses magical abilities; a unit that boosts card spells.
    """
    def __init__(self):
        super().__init__("Wizard", "A skilled sorcerer capable of boosting attributes of spells to support allies and manipulate opponents", cost = 3, attack = random.randint(2, 5), maxHP = random.randint(5, 7)) # super().__init__(name, description, cost, attack, maxHP)
    # HP: 5 - 7
    # Cost: 3 Mana - 4?
    # Attack: 2 - 5 (Doubler on spells)

class Tank(UnitCard):
    """
    Tank class is a special type of UnitCard that is able to absorb damage.
    """
    def __init__(self):
        super().__init__(name, description, cost, attack, maxHP)
    # HP 12 - 20
    # Cost: 5-8 mana?
    # Attack: 1 - 2 or 3?

class Attacker(UnitCard): #  Change to Knight ?
    """
    Attacker class is a special type of UnitCard that deals large amounts of damage.
    """
    def __init__(self):
        super().__init__("Knight", description, cost, attack, maxHP)
    # HP 5 - 8
    # Cost: 4 - 5
    # Attack: 5 - 8

# Addition: 
'''
class Archer(UnitCard): 
    """
    Archer class is a special type of UnitCard that is able to pierce through tanks.
    """
    def __init__(self):
        super().__init__(name, description, cost, attack, maxHP)
    # HP 5 - 6
    # Cost: 3
    # Attack: 2 - 4 (Double damage when piercing tanks)

class Bandit(UnitCard):
    """
    Bandit class is a special type of UnitCard that is stealthy and powerful but is vulnerable (posseses low health).
    """
    def __init__(self):
        super().__init__(name, description, cost, attack, maxHP)
    # HP 1 - 2
    # Cost: 2
    # Attack: 4 - 8
'''

class HealingSpell(SpellCard):
    """
    A SpellCard that restores the health of UnitCards.
    """

class DamageSpell(SpellCard):
    """
    A SpellCard that deals damage to an opposing UnitCard/Player.
    """

class ShieldSpell(SpellCard):
    """
    A SpellCard that provides shield for a UnitCard, an additional way to absorb damage.
    """

class DrawCardSpell(SpellCard):
    """
    A SpellCard that allows the player to draw additional cards.
    """