"""
Created by: Clay Beal
Date: 1/29/2023
Class: CIS 163
Professor: Woodring
"""


class Item:
    """
    The item class holds a blueprint for creating an item, each having
    a name, description, calories, and weight
    Attributes:
        _name (str): The name of the item
        _description (str): A description of the item
        _calories (int): Number of calories an item has
        _weight (int): Number of lbs an item weighs
    """
    def __init__(self, name: str, description: str,
                 calories: int, weight: int) -> None:
        """
        Creates a new item with a name, description, calories,
        and weight
        Parameters:
            name (str): The name of the item
            description (str): A description of an item
            calories (int): Number of calories an item has
            weight (int): Number of lbs an item weighs
        """
        self._name = name
        self._description = description
        self._calories = calories
        self._weight = weight

    def __str__(self) -> str:
        """
        String method that returns the name and description of an item
        Returns:
            (str): name, weight, and description of an item
        """
        return f'{self._name} - {self._weight}lbs. - {self._description}'

    def set_name(self, name: str) -> None:
        """
        Setter for name variable
        Parameters:
            name (str): Passed in name
        Raises:
            ValueError: If the passed in item name is blank
        """
        # Ensures name is not blank
        if not name:
            raise ValueError('Item name cannot be blank.')
        self._name = name

    def get_name(self) -> str:
        """
        Getter for name variable
        Returns:
             _name (str): Name of an item
        """
        return self._name

    def set_description(self, description: str) -> None:
        """
        Setter for description variable
        Parameters:
            description (str): Passed in description
        Raises:
            ValueError: If the passed in item description is blank
        """
        # Ensures description is not blank
        if not description:
            raise ValueError('Item description cannot be blank.')
        self._description = description

    def get_description(self) -> str:
        """
        Getter for description variable
        Returns:
             _description (str): Description of an item
        """
        return self._description

    def set_calories(self, calories: int) -> None:
        """
        Setter for calories variable
        Parameters:
            calories (int): Passed in calories
        Raises:
            ValueError: If the passed in item calories isn't between
                        0 and 1000 inclusive
        """
        if 0 <= calories <= 1000:
            self._calories = calories
        else:
            raise ValueError('Calorie must be between 0 and 1000 inclusive.')

    def get_calories(self) -> int:
        """
        Getter for calories variable
        Returns:
             _calories (int): Number of calories an item has
        """
        return self._calories

    def set_weight(self, weight: int) -> None:
        """
        Setter for weight variable
        Parameters:
            weight (int): Passed in weight
        Raises:
            ValueError: If the passed in item weight isn't between
                        0 and 500 exclusive
        """
        if 0 < weight < 500:
            self._weight = weight
        else:
            raise ValueError('Weight must be between 0 and 500')

    def get_weight(self) -> int:
        """
        Getter for weight variable
        Returns:
             _weight (int): Weight of an item
        """
        return self._weight
