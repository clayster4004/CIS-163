"""
Created by: Clay Beal
Date: 1/29/2023
Class: CIS 163
Professor: Woodring
"""


class NPC:
    """
    The NPC class holds a blueprint for creating an NPC, each having a
    name, description, message number, and list of messages
    Attributes:
        _name (str): The name of an NPC
        _description (str): A description of the NPC
        _message_num (int): Holds an index for what message
                            the NPC is on
        _messages (list): Holds a list of messages the NPC can say
    """
    def __init__(self, name: str, description: str) -> None:
        """
        Creates a new item with a name, description, message_num and
        list of messages
         Parameters:
            name (str): The name of the NPC
            description (str): A description of the NPC
        """
        self._name = name
        self._description = description
        self._message_num = 0
        self._messages: list[str] = []

    def __str__(self) -> str:
        """
        String method that returns the name of the NPC
        Returns:
            (str): name of the NPC
        """
        return f'{self._name}'

    def set_name(self, name: str) -> None:
        """
        Setter for name variable
        Parameters:
            name (str): Passed in name
        Raises:
            ValueError: If the passed in NPC name is blank
        """
        # Ensures name is not blank
        if not name:
            raise ValueError('NPC name cannot be blank.')
        self._name = name

    def get_name(self) -> str:
        """
        Getter for name variable
        Returns:
             _name (str): Name of an NPC
        """
        return self._name

    def set_description(self, description: str) -> None:
        """
        Setter for description variable
        Parameters:
            description (str): Passed in description
        Raises:
            ValueError: If the passed in NPC description is blank
        """
        # Ensures description is not blank
        if not description:
            raise ValueError('NPC description cannot be blank.')
        self._description = description

    def get_description(self) -> str:
        """
        Getter for description variable
        Returns:
             _description (str): Description of an NPC
        """
        return self._description

    def add_message(self, message: str) -> None:
        """
        Appends a message (str) to the list of _messages an NPC has
        Parameters:
            message (str): Message an NPC can say
        """
        self._messages.append(message)

    def get_message(self) -> str:
        """
        Getter for a message in the NPC list cycling through
        the messages
        Returns:
            (str): a message from the _message_list of an NPC
        """
        # Increments message number and gets the remainder from the len
        # of the list to cycle through messages
        self._message_num = (self._message_num + 1) % len(self._messages)
        return self._messages[self._message_num]
