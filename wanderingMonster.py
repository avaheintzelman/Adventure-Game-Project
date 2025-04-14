# wanderingMonster.py
# Ava Heintzelman 
# 4/14/25

import random

class WanderingMonster:
    """
    A class representing a wandering monster in the adventure game.
    
    Attributes:
        position (tuple): The (x, y) position of the monster on the grid.
        monster_type (str): The type of the monster (e.g., 'zombie', 'slime', 'goblin').
        name (str): The name of the monster.
        hp (int): The hit points of the monster.
        gold (int): The amount of gold the monster has.
        color (tuple): The RGB color tuple representing the monster's color.
    """
    def __init__(self, position, monster_type, name, hp, gold, color):
        self.position = position
        self.monster_type = monster_type
        self.name = name
        self.hp = hp
        self.gold = gold
        self.color = color

    def move(self, direction):
        """
        Attempts to move the monster in the given direction within the grid boundaries.
        
        Parameters:
            direction (tuple): A tuple (dx, dy) representing the direction to move.
        
        The monster will not move if the new position is outside the grid or is the town square (0,0).
        """
        new_x = self.position[0] + direction[0]
        new_y = self.position[1] + direction[1]
        # Check grid boundaries (grid size: 10x10) and avoid moving into town square at (0, 0)
        if 0 <= new_x < 10 and 0 <= new_y < 10 and (new_x, new_y) != (0, 0):
            self.position = (new_x, new_y)

    @classmethod
    def new_random_monster(cls, exclude_positions=None):
        """
        Creates and returns a new random WanderingMonster.
        
        Parameters:
            exclude_positions (list): Optional list of positions (tuples) where the monster should not spawn.
        
        Returns:
            WanderingMonster: A newly created random monster instance.
        """
        if exclude_positions is None:
            exclude_positions = []
        # Define possible monster types with their attributes
        monster_options = [
            {"monster_type": "zombie", "name": "Zombie", "hp": 20, "gold": 5, "color": (255, 0, 0)},
            {"monster_type": "slime", "name": "Slime", "hp": 15, "gold": 3, "color": (0, 255, 0)},
            {"monster_type": "goblin", "name": "Goblin", "hp": 18, "gold": 4, "color": (0, 0, 255)}
        ]
        chosen = random.choice(monster_options)
        # Random position not in exclude_positions
        while True:
            x = random.randint(0, 9)
            y = random.randint(0, 9)
            if (x, y) not in exclude_positions:
                break
        return cls(position=(x, y), monster_type=chosen["monster_type"], name=chosen["name"],
                   hp=chosen["hp"], gold=chosen["gold"], color=chosen["color"])
