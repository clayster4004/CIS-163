"""
Created by: Clay Beal
Date: 1/29/2023
Class: CIS 163
Professor: Woodring
"""
from npc import NPC
from item import Item


class Location:
    """
    The location class holds a blueprint for creating a location, each
    location may hold a specific name, description, visited boolean,
    neighbors dictionary, npc list, and item list.
    Attributes:
        _name (str): The name of the location
        _description (str): A description of a location
        _visited (bool): Whether this location has been visited
        _neighbors (dict): Keys being a direction, values being a
                           location of the area in that direction
        _npc_list (list): Holds instances of NPCs in this location
        _item_list (list): Holds instances of Items in this location
    """
    def __init__(self, name: str, description: str,
                 visited: bool) -> None:
        """
        Creates a new location with a name, description, and visited
        status passed in.
        Parameters:
            name (str): The name of the location
            description (str): A description of a location
            visited (bool): Whether this location has been visited
        """
        self._name = name
        self._description = description
        self._visited = visited
        self._neighbors: dict[str, Location] = {}
        self._npc_list: list[NPC] = []
        self._item_list: list[Item] = []

    def __str__(self) -> str:
        """
        String method that returns the name and description of an area
        Returns:
            (str): name and description of a location
        """
        return f'{self._name} - {self._description}'

    def set_name(self, name: str) -> None:
        """
        Setter for name variable
        Parameters:
            name (str): Passed in name
        Raises:
            ValueError: If the passed in location name is blank
        """
        # Ensures name is not blank
        if not name:
            raise ValueError('Location name cannot be blank.')
        self._name = name

    def get_name(self) -> str:
        """
        Getter for name variable
        Returns:
             _name (str): Name of a location
        """
        return self._name

    def set_description(self, description: str) -> None:
        """
        Setter for description variable
        Parameters:
            description (str): Passed in description
        Raises:
            ValueError: If the passed in location description is blank
        """
        # Ensures description is not blank
        if not description:
            raise ValueError('Location description cannot be blank.')
        self._description = description

    def get_description(self) -> str:
        """
        Getter for description variable
        Returns:
             _description (str): Description of a location
        """
        return self._description

    def set_visited(self) -> None:
        """
        Sets _visited to True
        """
        self._visited = True

    def get_visited(self) -> bool:
        """
        Getter for visited variable
        Returns:
             _visited (bool): Whether a location has been visited
        """
        return self._visited

    def get_locations(self) -> dict:
        """
        Getter for the neighbors dictionary
        Returns:
            _neighbors (dict): Keys being a direction, values being a
                               location of the area in that direction
        """
        return self._neighbors

    def add_location(self, direction: str, location: 'Location') -> None:
        """
        Adds a new key(direction), value(location) pair to the
        _neighbors dictionary
        Parameters:
            direction (str): direction of a neighboring location
            location (class): instance of a location class
        Raises:
            ValueError: If passed in direction is blank
            KeyError: If passed in direction already has a location
        """
        # Ensures direction is not blank or already in the dictionary
        if not direction:
            raise ValueError('Direction value must not be blank')
        if direction in self._neighbors:
            raise KeyError('This direction is already assigned')
        self._neighbors[direction] = location

    def add_npc(self, npc: NPC) -> None:
        """
        Adds an instance of an NPC to the _npc_list
        Parameters:
            npc (class): Instance of the NPC class
        """
        self._npc_list.append(npc)

    def get_npc(self) -> list[NPC]:
        """
        Getter for _npc_list
        Returns:
            _npc_list (list): List of class NPC instances in a location
        """
        return self._npc_list

    def add_item(self, item: Item) -> None:
        """
        Adds an instance of an Item to the _item_list
        Parameters:
            item (class): Instance of the item class
        """
        self._item_list.append(item)

    def get_items(self) -> list[Item]:
        """
        Getter for _item_list
        Returns:
            _item_list (list): List of class Item instances in a location
        """
        return self._item_list
