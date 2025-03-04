#gamefunctions.py
#Ava Heintzelman
#2/20/25

"""Game Functions Module.

This module provides a collection of functions for an adventure game.
Functions include purchasing items, generating random monsters, and utility
functions for printing messages and menus.

Typical usage example:

  from gamefunctions import purchase_item, new_random_monster, sorta_sum
  quantity, balance = purchase_item(3.5, 20, 4)
  monster = new_random_monster()
  print(sorta_sum(5, 7))
"""

import random

def purchase_item(itemPrice: float, startingMoney: float,
                  quantityToPurchase: int = 1) -> tuple:
    """
    Determine how many items can be bought given available funds.

    Args:
        itemPrice (float): The price of a single item.
        startingMoney (float): The available funds.
        quantityToPurchase (int, optional): Desired number of items to buy.
            Defaults to 1.

    Returns:
        tuple: A tuple containing the quantity purchased (int) and the
            remaining money (float).
    """
    max_affordable = int(startingMoney // itemPrice)
    quantity_purchased = min(max_affordable, quantityToPurchase)
    remaining_money = startingMoney - (quantity_purchased * itemPrice)
    return quantity_purchased, remaining_money

def new_random_monster() -> dict:
    """
    Generate a random monster with various attributes.

    Returns:
        dict: A dictionary representing a monster with keys:
            'name', 'description', 'health', 'power', and 'money'.
    """
    monster_types = [
        {"name": "George", "description": "A sneaky goblin lurks in the shadows, ready to attack.",
         "health_range": (10, 20), "power_range": (5, 10), "money_range": (5, 15)},
        {"name": "King", "description": "A towering King wields a giant club, snarling at you.",
         "health_range": (20, 40), "power_range": (10, 20), "money_range": (15, 50)},
        {"name": "Vulture", "description": "A vulture picks at a carcass but eyes you suspiciously.",
         "health_range": (1, 5), "power_range": (2, 5), "money_range": (50, 150)}
    ]
    
    chosen_monster = random.choice(monster_types)
    monster = {
        "name": chosen_monster["name"],
        "description": chosen_monster["description"],
        "health": random.randint(*chosen_monster["health_range"]),
        "power": random.randint(*chosen_monster["power_range"]),
        "money": round(random.uniform(*chosen_monster["money_range"]), 2)
    }
    return monster

def sorta_sum(a: int, b: int) -> int:
    """
    Compute the sum of two integers, with a special rule.

    Args:
        a (int): The first integer.
        b (int): The second integer.

    Returns:
        int: The sum of a and b. However, if the sum is between 10 and 19
            inclusive, the function returns 20.
    """
    total = a + b
    if 10 <= total <= 19:
        return 20
    return total

def print_welcome(name: str, width: int = 20) -> None:
    """
    Print a welcome message centered within a given width.

    Args:
        name (str): The name to include in the welcome message.
        width (int, optional): The width of the printed message.
            Defaults to 20.
    """
    print(f"{'Hello, ' + name + '!':^{width}}")

def print_shop_menu(item1Name: str, item1Price: float,
                    item2Name: str, item2Price: float) -> None:
    """
    Print a shop menu displaying two items and their corresponding prices.

    Args:
        item1Name (str): The name of the first item.
        item1Price (float): The price of the first item.
        item2Name (str): The name of the second item.
        item2Price (float): The price of the second item.
    """
    print("/----------------------\\")
    print(f"| {item1Name:<12}${item1Price:7.2f} |")
    print(f"| {item2Name:<12}${item2Price:7.2f} |")
    print("\\----------------------/")

def test_functions():
    """Test all functions in the module."""
    print("Testing purchase_item()")
    print(purchase_item(1.23, 10, 3))  # expected: (3, remaining money)
    print(purchase_item(1.23, 2.01, 3))  # expected: (1, remaining money)
    print(purchase_item(3.41, 21.12))  # expected: (1, remaining money)
    print(purchase_item(31.41, 21.12))  # expected: (0, 21.12)

    print("\nTesting new_random_monster()")
    print(new_random_monster())
    print(new_random_monster())
    print(new_random_monster())

    print("\nTesting sorta_sum()")
    print(sorta_sum(3, 4))   # → 7
    print(sorta_sum(9, 4))   # → 20
    print(sorta_sum(10, 11)) # → 21

    print("\nTesting print_welcome()")
    print_welcome("Jeff")
    print_welcome("Audrey")
    print_welcome("Chris")

    print("\nTesting print_shop_menu()")
    print_shop_menu("Apple", 31, "Pear", 1.234)
    print_shop_menu("Egg", 0.23, "Bag of Oats", 12.34)
    print_shop_menu("Milk", 2.5, "Bread", 3.0)

if __name__ == "__main__":
    test_functions()
