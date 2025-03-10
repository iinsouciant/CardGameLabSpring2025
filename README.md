# Homebrew Card Game
For this lab, you will be joining with a new group to create a homebrewed card game of your own in the style of games like Magic: The Gathering and Hearthstone. This card game will familiarize you with the use of inheritance and polymorphism in python, as well as implementing a linked list data structure.

###  The Card Game
The card game will consist of two players, each with a deck of at least 25 cards, taking turns playing cards until they have reduced their opponent's HP to 0 at which point they win. Each player will draw a hand of cards at the start of the game, and continue drawing at the start of their turn.

There must be a deck of cards of multiple, distinct classes that inherit from a basic Card class. The child classes should extend the Card class with real differences between the classes (regular cards vs wild cards in Uno for example).

The deck of cards will be implemented as a linked list and consist of two major card types: Unit Cards and Spell Cards. All cards will posses a name, description, and some cost of resource which prevents a player from playing all of their hand at once (at least at the start of the game).

- Additionally, Unit cards will have an Attack and HP stat
- Before the end of each round, the player can choose to attack with their played units. Their opponent can defend with their own units, but defending units cannot attack the next turn
- Spell cards will have some effect that changes the game state. This can be instant damage, health regeneration, or altering unit stats
 

### Extra Requirements
1. A log keeping track of all actions taken in the game should be displayed
2. An AI opponent is not required, you can assume the computer will be passed back and forth while playing the game.

# Submission
Each person will submit the code indiviudally, but leave a comment on who you worked with for the lab.

--------------------------------------------------------------------------------------------------------------

# Planning Write Up

Depicted below is the Unified Modeling Language (UML) Diagram for the Homebrew Card Game known as Hearthgathering... ; 

## UML Diagram

- TBD

### UML Activity Diagram Index

![image](https://github.com/user-attachments/assets/d3f1b373-eb92-4bd5-b878-666dd3e63ebc)


## Division of Labor Documentation

- Used VSCode "Git Graph" Installation (Extension): https://marketplace.visualstudio.com/items?itemName=mhutchie.git-graph
- TBD
