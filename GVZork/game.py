"""
Created by: Clay Beal
Date: 1/29/2023
Class: CIS 163
Professor: Woodring
"""
import random
import datetime
import typing
import time
from location import Location
from item import Item
from npc import NPC


class Game:
    """
    The game class holds a blueprint for creating the GVZork game. It
    holds a list of commands the user can give in a dictionary, keys
    being commands and values being function names. It also holds a
    list of item instances, current weight of the user, locations,
    current_location of the user, how many calories the elf needs,
    a game over variable, and calls a function to create the world,
    consisting of locations, items, and NPCs.
    Attributes:
        _commands (dict): calls a function to create a command's dict
        _items (list): items held by the player
        _current_weight (int): weight of a player based on items weight
        _locations (list): list of locations in game
        _current_location (class): Instance of location class you are in
        _elf_needed_calories (int): Number of calories the elf needs
        _game_over (bool): Holds false until win condition is met
    """

    def __init__(self) -> None:
        """
        Creates a game instance with attributes, as well as creates
        the world
        """
        self._commands = self.setup_commands()
        self._items: list[Item] = []
        self._current_weight = 0
        self._locations: list[Location] = []
        self.create_world()
        self._current_location = self.random_location()
        self._elf_needed_calories = 500
        self._game_over = False

    def setup_commands(self) -> dict[str, typing.Callable]:
        """
        Sets of the commands in a dictionary format, commands (keys),
        and function names (values)
        Returns:
            (dict): commands (keys) with function names (values)
        """
        return {'help': self.print_help,
                '?': self.print_help,
                'go': self.go,
                'talk': self.talk,
                'meet': self.meet,
                'take': self.take,
                'give': self.give,
                'inventory': self.show_items,
                'look': self.look,
                'scream': self.scream,
                'quit': self.quit
                }

    def create_world(self) -> None:
        """
        This function creates all the locations, NPCs, and items,
        as well as puts all the NPCs and items in specific locations.
        """
        # SETS UP ALL THE INSTANCES OF LOCATION, ITEM, AND NPC
        # Locations
        ravines = Location('Woods', 'Home to the elf that froze GVSU',
                           False)
        holton_hooker = Location('Holton-Hooker', 'Freshman Dorms',
                                 False)
        kleiner = Location('Kleiner', 'Home to the award winning Dish'
                                      ' (5 star Dining)', False)
        mackinac = Location('Mackinac', 'The school of computing is '
                                        'located here', False)
        manitou = Location('Manitou', 'Older building with '
                           'lecture halls left and right', False)
        kindschi = Location('Kindschi', 'Laboratories'
                            ' on laboratories for 3 floors', False)
        rec = Location('Rec', 'Let\'s pump some iron',
                       False)
        kirkhof = Location('Kirkhof', 'Hub for college student'
                           ' (and a Panda Express)', False)
        lake_ontario = Location('Lake Ontario', 'Basic building'
                                ' with basic classrooms', False)

        # Items
        laker_bowl = Item('Laker Bowl', 'Mashed Potatoes, Chicken,'
                          ' Corn, and Gravy', 150, 8)
        apple = Item('Apple', 'Sour, Juicy, Delicious',
                     50, 4)
        pizza = Item('Pizza', 'One hot and ready slice '
                     'of supreme pizza!', 100, 6)
        burrito = Item('Burrito', 'One of the biggest '
                       'burritos you\'ve ever seen', 125, 8)
        bio_textbook = Item('Biology Textbook', '7th edition '
                            'Introductory Biology Textbook, lots of '
                            'provocative pictures drawn inside the'
                            ' cover', 0, 8)
        celsius = Item('Celsius', '200 milligrams of'
                       ' pure energy', 75, 5)
        speaker = Item('Speaker', 'Produces great sound for '
                       'such a small speaker', 0, 6)
        protein_bar = Item('Protein Bar', 'Mint Chocolate '
                           'with a whopping 20g of protein', 100, 8)
        chocolate_bar = Item('Chocolate', 'Classic Dove chocolate'
                             ' bar, looks delicious!', 75, 5)
        banana = Item('Banana', 'Perfectly ripe, perfectly delicious',
                      50, 3)

        # NPCs
        elf = NPC('Elf', 'Apparently freezing college campuses '
                         'is a hobby?')
        elf.add_message('"I still need food!"\n'
                        'Kinda annoying huh?')
        elf.add_message('"I still need food!"\n'
                        'We get it...')
        elf.add_message('"I still need food!"\n'
                        'Yeah, yeah, yeah...')

        mantella = NPC('Mantella', 'GVSU\'s one and only president')
        mantella.add_message('"Remember to study!"\n'
                             'Yeah, yeah, yeah...')
        mantella.add_message('"I\'m the president here at Grand '
                             'Valley."\n'
                             'Well she seems nice enough...')
        mantella.add_message('"Lakers always do their best!"\n'
                             'Well that\'s good I guess...')

        louie = NPC('Louie', 'Gotta give it to him,'
                             ' man\'s got spirit')
        louie.add_message('"Are you going to the football game this'
                          ' friday?"\n'
                          'Only if they are playing Ferris, heh...')
        louie.add_message('"I\'m proud to be a laker!"\n'
                          'Me too buddy, me too...')
        louie.add_message('"If anyone here has spirit, it\'s me!"\n'
                          'Not as much as me, heh...')

        woodring = NPC('Woodring', 'Appears to be a CIS instructor')
        woodring.add_message('"A little word of advice, always '
                             'start your coding projects early."\n'
                             'Best advice I\'ve heard all day...')
        woodring.add_message('"I\'m in my office most mornings if '
                             'you need coding help."\n'
                             'I\'ll definitely be taking you up '
                             'on that offer...')
        woodring.add_message('"Howdy, how are ya?"\n'
                             'Pretty good I guess...')

        clay = NPC('Clay', 'Seems to be a student at GVSU')

        zach = NPC('Zach', 'Seems to be a student at GVSU')
        zach.add_message('"Hey amigo!"\n'
                         'Howdy partner... heh...')
        zach.add_message('"What are you up to today?"\n'
                         'Oh ya know, trying to save campus,'
                         ' nothing much...')
        zach.add_message('"Ramen is the go-to meal for me at night."\n'
                         'Hm, is it now...?')

        # ADDS NPCs AND ITEMS, AND NEIGHBORS TO LOCATIONS
        # Ravines Setup
        ravines.add_npc(elf)
        ravines.add_location('south', holton_hooker)

        # Holton-Hooker Setup
        holton_hooker.add_item(apple)
        holton_hooker.add_location('north', ravines)
        holton_hooker.add_location('east', kleiner)
        holton_hooker.add_location('south', lake_ontario)
        holton_hooker.add_location('west', mackinac)

        # Kleiner Setup
        kleiner.add_item(laker_bowl)
        kleiner.add_location('west', holton_hooker)

        # Mackinac Setup
        mackinac.add_npc(woodring)
        mackinac.add_item(pizza)
        mackinac.add_location('east', holton_hooker)
        mackinac.add_location('south', kirkhof)
        mackinac.add_location('west', manitou)

        # Manitou Setup
        manitou.add_npc(clay)
        manitou.add_item(burrito)
        manitou.add_location('east', mackinac)
        manitou.add_location('south', kindschi)

        # Kindschi Setup
        kindschi.add_item(bio_textbook)
        kindschi.add_item(celsius)
        kindschi.add_location('north', manitou)
        kindschi.add_location('east', kirkhof)
        kindschi.add_location('west', rec)

        # Rec Setup
        rec.add_npc(louie)
        rec.add_item(speaker)
        rec.add_item(protein_bar)
        rec.add_location('east', kindschi)

        # Kirkhof Setup
        kirkhof.add_npc(mantella)
        kirkhof.add_item(chocolate_bar)
        kirkhof.add_location('north', mackinac)
        kirkhof.add_location('east', lake_ontario)
        kirkhof.add_location('west', kindschi)

        # Lake Ontario Setup
        lake_ontario.add_npc(zach)
        lake_ontario.add_item(banana)
        lake_ontario.add_location('north', holton_hooker)
        lake_ontario.add_location('west', kirkhof)

        self._locations = [ravines, holton_hooker, kleiner, mackinac,
                           manitou, kindschi, rec,
                           kirkhof, lake_ontario]

    def random_location(self) -> Location:
        """
        This function uses the random library to pick a random location
        instance from the list of locations and returns it
        Returns:
             (class): An instance of the location class
        """
        return random.choice(self._locations)

    def print_help(self) -> None:
        """
        This function prints the available commands and gives basic
        directions to the user, it also prints the current time
        """
        # Prints the commands
        print('Directions')
        print('Available Commands:')
        commands = self._commands
        for key in commands:
            print(key)
        print()
        # Prints examples for the user
        print('Commands such as "go", "talk", "meet", "take", and "give"\n'
              'require a target word after them.\n\n'
              'Example: "go north" or "take apple"\n\n'
              'Type in the "look" command to get a better idea of\n'
              'where you are as well as the surrounding areas.\n')
        # Prints the current time
        current_time = datetime.datetime.now()
        print(f'Time: {current_time.strftime("%H:%M:%S")}')

    def go(self, direction) -> None:
        """
        This function takes a user inputted direction and uses a
        locations neighbor dictionary to change your current location
        to the location provided by the direction the user wants to
        travel
        direction (str): direction inputted by the user in which they
                         want to travel
        Returns:
            (None): To break out of the function if they are carrying
                    more than 30 lbs.
        """
        # Sets the location you are currently in to visited
        self._current_location.set_visited()
        # Sets neighbor_dict to the current locations neighbors
        neighbor_dict = self._current_location.get_locations()
        # If you weigh more than 30lbs. you cannot move
        if self._current_weight >= 30:
            print('You are carrying more than the max weight (30 lbs)')
            return
        # If passed in direction is a key in the neighbor dictionary,
        # set that to the new current location
        if direction in neighbor_dict:
            self._current_location = neighbor_dict[direction]
            print(f'You have entered {self._current_location}')

    def talk(self, target) -> None:
        """
        Takes in a user inputted target (name of an NPC) and gets
        a message from a specific NPCs list of messages. If the user
        talks to clay, then they will add a teleportation orb to
        their inventory
        Parameters:
            target (str): Name of the NPC in which they'd like to speak
        """
        # Cycles through each npc in the location you are in
        for npc in self._current_location.get_npc():
            # If the npc named 'clay' is there, a teleportation orb is
            # given to the user and 'clay' disappears from that location
            if target.lower() == npc.get_name().lower() and \
                    npc.get_name().lower() == 'clay':
                orb = Item('Orb', 'Teleportation orb used to travel'
                                  ' anywhere instantly', 0, 5)
                self._items.append(orb)
                self._current_location._npc_list.clear()
                print("Hey my name is Clay, Here's a little something\n"
                      "that'll make your travels a little easier!\n")
                print('You have found the teleportation orb, use it '
                      'to travel anywhere instantly\nwith the'
                      ' "teleport" command!')
                # Adds teleport to the list of commands
                self._commands['teleport'] = self.teleport
            # If the target isn't 'clay' print a normal message
            elif target.lower() == npc.get_name().lower():
                # Splits message at the newline
                the_message = npc.get_message().split('\n')
                for i in range(2):
                    # Prints each letter with a slight delay
                    for letter in the_message[i]:
                        print(letter, end='')
                        time.sleep(0.05)
                    # Print "..." with a longer delay on its own line
                    # after the first line is printed out in the message
                    if i == 0:
                        print()
                        for j in range(3):
                            print('.', end='')
                            time.sleep(.8)
                    print()

    def meet(self, target) -> None:
        """
        Takes in a user inputted target (name of an NPC) and gets
        a description of a specific NPC
        Parameters:
            target (str): Name of the NPC in which they'd like to meet
        """
        # Cycles through the NPCs in a location and prints their desc
        for npc in self._current_location.get_npc():
            if target.lower() == npc.get_name().lower():
                print(npc.get_description())

    def take(self, target) -> None:
        """
        Takes a user inputted target (item name) and adds it to the
        users item list as well as removes it from the locations item
        list
        target (str): Name of an item in which the NPC would like to
                      pick up
        """
        # Cycles through the items in the location you are in
        for item in self._current_location.get_items():
            # Checks to see if the user input is an items name
            # If so removes the item from the location, adds it to
            # the user and adds the weight to the user
            if target == item.get_name().lower():
                self._current_location._item_list.remove(item)
                self._items.append(item)
                self._current_weight += item.get_weight()
                print(f'You picked up - {item.get_name()} - and added'
                      f' it to your inventory.')

    def give(self, target) -> None:
        """
        Takes in user inputted target (name of an item) and if dropped
        in the woods subtracts its calories from that the elf needs.
        Or if you gave the elf an item that has 0 calories, you are
        teleported to a different random location on the map. Or if
        you are not in the woods you drop the target in at the location
        you are currently at.
        Parameters:
            target (str): Name of an instance of an item
        """
        # Cycles through the items in the users item list
        for item in self._items:
            # Checks if the user input is the name of an item
            if target == item.get_name().lower():
                # Checks to see if the user location is the woods
                # If so the item weight is taken off the calories the
                # elf requires
                if self._current_location.get_name() == 'Woods':
                    self._items.remove(item)
                    self._current_weight -= item.get_weight()

                    if item.get_calories() > 0 and\
                            self._elf_needed_calories - \
                            item.get_calories() > 0:
                        self._elf_needed_calories -= item.get_calories()
                        print('You still need ' + str(self._elf_needed_calories)
                              + ' calories to satisfy me!')
                    elif item.get_calories() > 0 and\
                            self._elf_needed_calories - \
                            item.get_calories() <= 0:
                        self._elf_needed_calories -= item.get_calories()
                    # If the item had no calories the user is
                    # teleported to a random location
                    else:
                        self._current_location = self.random_location()
                        print('I don\'t want that! Teleportation Activate!')
                # If user is not in the woods the item is added to the
                # new location and taken off users items
                elif self._current_location.get_name() != 'Woods':
                    self._current_location.add_item(item)
                    self._items.remove(item)
                    self._current_weight -= item.get_weight()
                    print(f'You set down - {item.get_name()}.')
                else:
                    pass

    def show_items(self, args: str = None) -> None:
        """
        Prints off the items you currently have with you
        Parameters:
            args (str): Converts any str input to NoneType, the function
                        will run if user inputs a str post command
        """
        # Goes through the users list of items and prints weight
        total_weight = 0
        for item in self._items:
            total_weight += item.get_weight()
            print(item)
        print()
        print(f'{total_weight} total lbs.')

    def look(self, args: str = None) -> None:
        """
        Prints the current items in the location you are in, the NPCs
        in that location, and the surrounding locations
        Parameters:
            args (str): Converts any str input to NoneType, the function
                        will run if user inputs a str post command
        """
        # Check to see if there are any items and NPCs in the room.
        # Prints them off
        if self._current_location.get_items() and \
                self._current_location.get_npc():
            print()
            print(f'{self._current_location}\n')
            print('Items here:')
            for item in self._current_location.get_items():
                print(str(item))
            print()
            print('People here:')
            for npc in self._current_location.get_npc():
                print(str(npc) + '\n')
        # Check to see if there are any items in the room
        # Prints them off
        elif self._current_location.get_items():
            print()
            print(f'{self._current_location}\n')
            print('Items here:')
            for item in self._current_location.get_items():
                print(str(item))
            print()
            print('You are alone.\n')
        # Checks to see if there are NPCs in the room
        # Prints them off
        elif self._current_location.get_npc():
            print()
            print(f'{self._current_location}\n\n'
                  f'There are no items here.\n')
            print('People here:')
            for npc in self._current_location.get_npc():
                print(str(npc) + '\n')
        # If there are no NPCs or items, just prints the location
        else:
            print()
            print(f'{self._current_location}\n\n'
                  f'There are no items here.\n\n'
                  f'You are alone.\n')

        # Cycles through the neighbors of a location and lets the user
        # know what direction they can travel
        neighbor_dict = self._current_location.get_locations()
        for key in neighbor_dict:
            # Only tells the user the location name if they have
            # visited it previously
            if neighbor_dict[key].get_visited():
                print(f'You could go {key} to {neighbor_dict[key]}')
            else:
                print(f'You could go {key}')
        print()

    def play(self) -> None:
        """
        Main game loop. Prints a header that explains the game and
        gets user input, calls an input_validity function to ensure
        the input is valid.
        """
        # Prints welcome rules and help function with delays
        print('Welcome to GVZork!\n')
        time.sleep(1.5)
        print('Grand Valley is frozen solid and can only be unfrozen\n'
              'if you feed the elf living in the woods behind campus\n'
              '500 calories worth of food.\n')
        time.sleep(4)
        print('You can find food along the way in various locations\n'
              'and carry up to 30 lbs.\n')
        time.sleep(3)
        print('Talk to some of the NPCs, they might have items or\n'
              'wisdom to share with you.')
        time.sleep(3)
        print()
        input('Press Enter For The Directions...')
        print()
        self.print_help()

        # Loops until game over is True
        while not self._game_over:
            found = False
            # Loops until found = True (until user input is good)
            while not found:
                # Gets user input, splits it at the spaces
                user_input = input('>>>').lower()
                tokens = user_input.split()
                # Sets command as the first typed word and deleted it
                command = tokens[0]
                del tokens[0]
                # Joins the following words into one word
                target = ' '.join(tokens)
                # If just a command is inputted it is tried, if it
                # requires a target the user is notified
                if command in self._commands and not target:
                    try:
                        self._commands[command]()
                        found = True
                    except TypeError:
                        print('Commands like that require a target...')
                # Calls function to check validity of the command
                # and target
                elif self.input_validity(command, target):
                    self._commands[command](target)
                else:
                    if target:
                        print(f'"{command} {target}" doesn\'t'
                              f' exactly work here...')
                    else:
                        print(f'I don\'t know what "{command}" means...')

                # If the elf has 0 calories or fewer, quit the game
                # And print a win message
                if self._elf_needed_calories <= 0:
                    print('Oh my.. oh my gosh..')
                    time.sleep(2)
                    print('It\'s happening...')
                    time.sleep(2)
                    print('Grand Valley is unfrozen!')
                    time.sleep(2)
                    print('Congratulations.. until next time...')
                    exit(0)

    def input_validity(self, command: str, target: str) -> bool:
        """
        Takes in a command and a target and makes sure the input is
        valid, returns true if so.
        Parameters:
            command (str): User inputted command
            target (str): User inputted target
        Returns:
            True (bool): if the input is valid (in the commands dictionary
                  and the item or npc is in the location you are in)
        """
        # Returns True if commands are single word commands
        if command.lower() in ['look', 'inventory', 'scream', 'quit']:
            return True
        # Returns true if command is valid and target is a location
        if command == 'go' and target in \
                self._current_location.get_locations():
            return True
        # Returns true if command is valid and target is an NPC
        for npc in self._current_location.get_npc():
            if command == 'talk' and target == \
                    str(npc).lower():
                return True
        # Returns true if command is valid and target is an item
        # (in a location)
        for item in self._current_location.get_items():
            if command == 'take' and target == \
                    item.get_name().lower():
                return True
        # Returns true if command is valid and target is an item
        # (in the users items)
        for item in self._items:
            if command == 'give' and target == \
                    item.get_name().lower():
                return True
        # Returns true if command is valid and target is a location
        # (checks all locations for the teleport() function)
        for location in self._locations:
            if command == 'teleport' and target == \
                    location.get_name().lower():
                return True
        return False

    def teleport(self, place: str) -> None:
        """
        This function is used to teleport the user's location to a
        location of their choice (place)
        Parameters:
            place (str): passed in location name from the user that
                         they want to teleport to
        """
        # Looks through the list of locations and sets the users
        # current location to the user inputted 'place'
        for location in self._locations:
            if place.lower() == location.get_name().lower():
                self._current_location = location
                print(f'You have successfully teleported to '
                      f'{location.get_name()}')

    def scream(self, args: str = None) -> None:
        """
        Used to print a screaming message from the user and print
        a comedic message if an NPC is in the room
        Parameters:
            args (str): Converts any str input to NoneType, the function
                        will run if user inputs a str post command
        """
        # Checks if an NPC is in the room and prints message
        if self._current_location.get_npc():
            for npc in self._current_location.get_npc():
                print('AAAAAAAHHHHHHHHHHHHHHH!')
                print(f'The only person that can hear you is '
                      f'{npc.get_name()} and they\'d like '
                      f'it if you shh!')
        else:
            print('AAAAAAAHHHHHHHHHHHHHHH!')
            print('Nobody can hear you, nobody can see you,'
                  ' you are alone...')

    def quit(self, args: str = None) -> None:
        """
        Prints off message thanking the user for playing and exits
        the game
        Parameters:
            args (str): Converts any str input to NoneType, the function
                        will run if user inputs a str post command
        """
        # Prints a thanks for playing message with a delay
        print('Thanks for playing...')
        for i in range(3):
            print('.', end='')
            time.sleep(1)
        print()
        print('But you lose...')
        exit(0)
