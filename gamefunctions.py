#gamefunctions.py
#Ava Heintzelman
#2/20/25

#adventure funtion a funtion for purchasing items and generating random monsters

import random

def purchase_item(itemPrice: float, startingMoney: float, quantityToPurchase: int = 1):
    #determines how many items can be bought given the available funds and returns the quantity bought and remaining balance.
    max_affordable = int(startingMoney // itemPrice)
    quantity_purchased = min(max_affordable, quantityToPurchase)
    remaining_money = startingMoney - (quantity_purchased * itemPrice)
    return quantity_purchased, remaining_money

def new_random_monster():
    #creation of a random monster with describing words that include name, description, health, power, and money.
    monster_types = [
        {"name": "George", "description": "A sneaky goblin lurks in the shadows, ready to attack.", "health_range": (10, 20), "power_range": (5, 10), "money_range": (5, 15)},
        {"name": "King", "description": "A towering King wields a giant club, snarling at you.", "health_range": (20, 40), "power_range": (10, 20), "money_range": (15, 50)},
        {"name": "Vulture", "description": "A vulture picks at a carcass but eyes you suspiciously.", "health_range": (1, 5), "power_range": (2, 5), "money_range": (50, 150)}
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

#demonstration of functions
print("Testing purchase_item()")
print(purchase_item(1.23, 10, 3))  #expected: (3, remaining money)
print(purchase_item(1.23, 2.01, 3))  #expected: (1, remaining money)
print(purchase_item(3.41, 21.12))  #expected: (1, remaining money)
print(purchase_item(31.41, 21.12))  #expected: (0, 21.12)

print("\nTesting new_random_monster()")
print(new_random_monster())
print(new_random_monster())
print(new_random_monster())

def sorta_sum(a, b):
    """
    Given 2 ints, a and b, return their sum. However, sums in the range 10..19 inclusive, are forbidden, so in that case just return 20.
    """
    total = a + b
    if 10 <= total <= 19:
        return 20
    return total

def print_welcome(name, width=20):
    """
    Prints a welcome for the supplied 'name' parameter. The output is centered within a field of given 'width'.
    """
    print(f"{'Hello, ' + name + '!':^{width}}")

def print_shop_menu(item1Name, item1Price, item2Name, item2Price):
    """
    Prints a sign that contains a list of two items and their corresponding prices.
    Items are left-aligned, and prices are right-aligned with two decimal places.
    """
    print("/----------------------\\")
    print(f"| {item1Name:<12}${item1Price:7.2f} |")
    print(f"| {item2Name:<12}${item2Price:7.2f} |")
    print("\\----------------------/")

#example test cases
print(sorta_sum(3, 4))  # → 7
print(sorta_sum(9, 4))  # → 20
print(sorta_sum(10, 11))  # → 21

#example test cases for print_welcome
print_welcome("Jeff")
print_welcome("Audrey")
print_welcome("Chris")

#example test cases for print_shop_menu
print_shop_menu("Apple", 31, "Pear", 1.234)
print_shop_menu("Egg", 0.23, "Bag of Oats", 12.34)
print_shop_menu("Milk", 2.5, "Bread", 3.0)

