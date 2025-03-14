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

Depicted below is the Unified Modeling Language (UML) Diagram for the Homebrew Card Game known as Hearthgathering and the division of labor documentation. Team members have communicated online and in meetings or voice calls to discuss potential ideas, implementations, clarifications, error debugging, application usage, and more!

## UML Diagram

- UML Diagram Direct Link: ...
- Used Figma to construct activity diagram (normal website): [Access here](https://www.figma.com/)
![image](https://github.com/user-attachments/assets/be77eb81-bf0e-4393-9d4e-d101e44be735)


### UML Activity Diagram Index

![image](https://github.com/user-attachments/assets/d3f1b373-eb92-4bd5-b878-666dd3e63ebc)


## Division of Labor Documentation

- Used VSCode __"Git Graph"__ Installation (Extension): [Access here](https://marketplace.visualstudio.com/items?itemName=mhutchie.git-graph)
  - _Git graph is implemented into the code (visualization example below)._
 
    ![image](https://github.com/user-attachments/assets/624e3797-4151-4496-b9af-4a10a8957a69)

 
<ins>**Both team members have worked together on various sections of the project to make it gel although primary tasks were delegated.**</ins>
- __Leo (Main task)__: Creating classes for UnitCards, SpellCards, track health, deck state, and more and also to handle drawing and playing cards.
- __Ryan (Main task)__: Game logic prompting player objects to be used for the game, names, decide player order, determine win/loss condition occurred, initiate attack/defend sequence, and more.

--------------------------------------------------------------------------------------------------------------

## Works Cited

Modules:
- https://pypi.org/project/console-menu/
- https://stackoverflow.com/questions/517970/how-can-i-clear-the-interpreter-console
- https://stackoverflow.com/questions/6824681/get-a-random-boolean-in-python
- https://docs.python.org/3/library/index.html

UML/Activity:
- https://figma.com/
- https://www.figma.com/figjam/
- https://www.geeksforgeeks.org/unified-modeling-language-uml-activity-diagrams/

Websites/Menu/Card Implementations:
- https://www.geeksforgeeks.org/python-linked-list/
- https://www.geeksforgeeks.org/linked-list-data-structure/
