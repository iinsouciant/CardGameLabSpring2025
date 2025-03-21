**Information about (Game)**

<ins>**NOTE**: Anything listed in this brainstorm is theoretical and provides an idea for the developing game. Some fundamentals, features, and units or spells may have not been added yet but will potentially be implemented in the future.</ins>

----------------------------------------------------

Main Parent: Card 

Board/Field Class: ? --> Play class that tracks cards for Player 1 and Player 2

**Classes: Unit Cards**
- Constructor: Name, Attack Dmg, HP Stat, Mana, Description
Wizards, 
Tanks, 
Attackers, 

**Spells: Spell Cards**
- Constructor: Name, Mana, Description
Healing, 
Damage, 
Shield, 
Draw Card, 

Cost of resource:
- Mana

========================================================================

Game Fundamentals:

- Flip a coin/roll a die 50/50 chance to see which Player goes first
- Each player is given 25 cards in their deck randomly (Spells and Unit Cards RNG)
- First turn each player draws 5 on first turn; draw 1 random card per turn (some spell cards can draw more cards)
- Use as many units on the field as the player wants per turn 
- Mana system (should get full energy each turn) like elixir system card; each card has a certain cost
- Max mana starts 2 first turn, increases by 1 every subsequent turn to a maximum of 10.
- Each player starts with **20 HP** (Temporary)
- Each unit can only do one action (attack/defend) per turn
- Overflow damage, difference of damage taken goes to user; For instance: Player 1 deals 20 damage and Player 2 Defends with 16 HP, Player 2 will have 4 HP deducted from their total HP

- No AI playing, just two individuals playing back and forth
- IMPORTANT: "Before the end of each round, the player can choose to attack with their played units. Their opponent can defend with their own units, but defending units cannot attack the next turn"

Winning Conditions:

- No more cards to draw by player when no more cards in their hands
- Nothing on the field placed by them
- No more HP

Additional Condition: Player A wins by default if a forfeit is called by a Player B. 

Player Actions per Turn (PRINTS OUT EACH TURN):
- Can choose one action per unit
- Attack
- Defend
- Check what both players HPs are (Field)
- What each player has on the field (being played) ; (Field)
- What you the player has in their hand (ONLY SEEN BY EACH INDIVIDUAL)
- Remaining Mana/Max Mana
