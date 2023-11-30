#Pascu Ioan grupa 144

from LA import LA
from CFGtoPDA import CFGtoPDA
import os

itemDesc = {
    'key': 'You notice a small key under the doormat.',
    'invitation': 'An invitation with a smeared name rests on the table.',
    'chef\'s hat': 'Look like someone forgot their chef\'s hat on the chair.',
    'spoon': 'There\'s a wooden spoon on the ground.',
    'sword': 'A rusty swords is gathering dust in the corner.',
    'crown': 'The crown is shining lights on the ceiling.',
    'ancient coin': 'The glint of the ancient coin catches your eye.',
    'spell book': 'An ominous sound is coming from the spell book.',
    'magic wand': 'A magic wand slowly levitates in place.'
}

class Game:
    
    __game = None
    __rooms = {}
    __validator = None

    #when initializing the object it reads the layout of the castle as a LA
    def __init__(self):
        self.__game = LA('game.txt')
        self.__validator = CFGtoPDA('command.txt')
        self.__populateRooms()

    #nested class used for storing the items and description for each room
    class Room:
        __items = None
        __description = None
        __doors = None

        #constructor reciving a string for description, an array of items and a variable number of strings for doors
        def __init__(self, desc, items, *doors):
            self.__description = desc
            self.__items = items
            self.__doors = [*doors]

        #this function will remove an item from the room if it is present there
        def takeItem(self, item):
            if item in self.__items:
                self.__items.remove(item)
                return True
            return False
        
        #this function adds an item to the room
        def addItem(self, item):
            self.__items.append(item)

        def scanRoom(self):
            #print room description
            print('\n>>' + self.__description)
            #print description for each iteam
            for item in self.__items:
                print('>>' + itemDesc[item])
            #print available doors (varies depending on number)
            doorNum = len(self.__doors)
            if doorNum == 1:
                print('>>You see a door leading to the ' + self.__doors[0] + '.\n')
            else:
                print('>>You see ' + str(doorNum) + ' doors leading to the ', end = '')
                print(*self.__doors[0:doorNum - 1], sep = ', the ', end = '')
                print(' and the ' + self.__doors[-1] + '.\n')


    #function that will fill the __room dictionary with Room ojects containing items, descriptions and doors
    def __populateRooms(self):
        self.__rooms['Entrance Hall'] = self.Room('The grand foyer of the Castle of Illusions.', ['key'], 'Dining Room', 'Armoury')
        self.__rooms['Dining Room'] = self.Room('A room with a large table filled with an everlasting feast.', ['invitation', 'chef\'s hat'], 'Entrance Hall', 'Treasury', 'Kitchen')
        self.__rooms['Kitchen'] = self.Room('A room packed with peculiar ingredients.', ['spoon'], 'Dining Room', 'Pantry')
        self.__rooms['Pantry'] = self.Room(' A storage area for the Kitchen.', [], 'Kitchen')
        self.__rooms['Armoury'] = self.Room('A chamber filled with antiquated weapons and armour.', ['sword', 'crown'], 'Entrance Hall', 'Treasury', 'Throne Room')
        self.__rooms['Treasury'] = self.Room('A glittering room overflowing with gold and gemstones.', ['ancient coin'], 'Dining Room', 'Armoury', 'Wizard\'s Study', 'Library')
        self.__rooms['Library'] = self.Room('A vast repository of ancient and enchanted texts.', ['spell book'], 'Treasury', 'Secret Exit')
        self.__rooms['Throne Room'] = self.Room('The command center of the castle.', [], 'Armoury', 'Wizard\'s Study')
        self.__rooms['Wizard\'s Study'] = self.Room('A room teeming with mystical artifacts.', ['magic wand'], 'Throne Room', 'Treasury', 'Secret Exit')
        self.__rooms['Secret Exit'] = self.Room('The hidden passage that leads out of the Castle of Illusions.', [], 'Library', 'Wizard\'s Study')

    #functions displaying different messages
    def __helloMessage(self):
        #clear the console
        os.system('cls')
        print('>>You find yourself trapped in Castle of Illusions. Try finding any useful items and see if you can escape.')


    def __showCommands(self):
        print('>>Available commands: go [room name] | look | inventory | take [item] | drop [item]')


    def __showInventory(self, items):
        items = list(items)
        itemsNum = len(items)
        
        if itemsNum == 0:
            print('\n>>Your inventory is empty. Try looking around!\n')
            return

        print('\n>>You have ', end = '')

        #print the first item
        if items[0][0] in 'aeiou':
            print('an ' + items[0], end = '')
        else:
            print('a ' + items[0], end = '')

        #if there is only one item end the line else continue printing the other items
        if itemsNum == 1:
            print('.\n')
        else:
            for item in items[1:itemsNum - 1]:
                #depending if the first letter is a vowel or not print an/a.
                if item[0] in 'aeiou':                                                  
                    print(', an ' + item, end = '')
                else:
                    print(', a ' + item, end = '')
            if items[itemsNum - 1][0] in 'aeiou':
                print(' and an ' + items[itemsNum - 1] + '.\n')
            else:
                print(' and a ' + items[itemsNum - 1] + '.\n')

    def __endGame(self):
        print('\n>>You escaped the Castle of Illusions and I (hopefully) passed CS112!')
        print('>>Thank you for playing!')
        input()
        exit()


    #this function is called when you want to start the game
    def run(self):

        #greet the player 
        self.__helloMessage()
        self.__showCommands()
        print()

        command = None
        
        #game loop
        while(True):
            
            #check if the game ended
            if self.__game.isAccepted():
                self.__endGame()

            #get and validate player command
            command = input().strip()
            if command == '':
                continue

            #validate command
            if not self.__validator.run(command.split(maxsplit = 1)):
                print('\n>>Invalid command!\n')
                continue

            #get the command type and the potential argument
            try:
                commandType, argument = command.split(maxsplit = 1)
            except:
                commandType = command
            

            #move to the room if there is a way there
            if commandType == 'go':
                if(self.__game.step(argument)):
                    print('\n>>You enter the ' + argument + '.\n')
                else:
                    print('\n>>You can\'t go there!\n')


            #describe the surroundings
            if commandType == 'look':
                self.__rooms[self.__game.getCurrentState()].scanRoom()


            #print the inventory
            if commandType == 'inventory':
                self.__showInventory(self.__game.getSet())


            #take an item from the current room
            if commandType == 'take':
                #see if the item is present in the room
                if self.__rooms[self.__game.getCurrentState()].takeItem(argument):
                    if self.__game.step(command):
                        print('\n>>You grabbed the ' + argument + '.\n') 
                else:
                    print('\n>>That item isn\'t here!\n')

            
            #drop an item into the room
            if commandType == 'drop':
                #check if the player is able to drop the item
                if self.__game.step(command):
                    #if you have it, add it to the current room
                    self.__rooms[self.__game.getCurrentState()].addItem(argument)
                    print('\n>>You dropped the ' + argument + '.\n') 
                else:
                    print('\n>>You don\'t have that!\n')


#main
game = Game()
game.run()