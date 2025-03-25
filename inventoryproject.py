# game.py
# Ava Heintzelman 
# 3/18/25 (Updated 3/25/25)

import gamefunctions

# Global variables to track inventory and equipped weapon
inventory = []
equipped_weapon = None

def shop_menu(gold):
    """
    Displays the shop menu to purchase items.
    
    Items available:
      1) Sword: A weapon that increases damage by +2. Has limited durability.
         Cost: 15 gold.
      2) Magic Charm: A special item that can defeat a monster instantly.
         Cost: 10 gold.
    """
    shop_items = [
        {"name": "Sword", "type": "weapon", "maxDurability": 10, "currentDurability": 10, "cost": 15},
        {"name": "Magic Charm", "type": "special", "effect": "defeat_monster", "description": "Instantly defeats a monster", "cost": 10}
    ]
    
    print("\nWelcome to the Shop!")
    print(f"Your Gold: {gold}")
    for idx, item in enumerate(shop_items, start=1):
        print(f"{idx}) {item['name']} (Cost: {item['cost']} gold)")
    print("3) Exit Shop")
    
    choice = input("Select an item to purchase (1-3): ")
    while choice not in ['1', '2', '3']:
        choice = input("Invalid option. Please select (1-3): ")
    
    if choice == '3':
        return gold
    else:
        item = shop_items[int(choice)-1]
        if gold >= item['cost']:
            gold -= item['cost']
            # Remove the cost before adding to inventory
            item_copy = item.copy()
            item_copy.pop('cost')
            inventory.append(item_copy)
            print(f"You purchased {item['name']}!")
        else:
            print("You don't have enough gold!")
        return gold

def equip_item():
    """
    Allows the player to equip an item from the inventory.
    
    Currently, only items of type 'weapon' are considered for equipping.
    """
    global equipped_weapon
    # Filter inventory for weapons only
    weapons = [item for item in inventory if item.get("type") == "weapon"]
    
    if not weapons:
        print("\nYou have no weapons to equip.")
        return
    
    print("\nEquip a Weapon:")
    for idx, weapon in enumerate(weapons, start=1):
        equipped_marker = " (Equipped)" if equipped_weapon == weapon else ""
        print(f"{idx}) {weapon['name']}{equipped_marker}")
    print(f"{len(weapons)+1}) Cancel")
    
    choice = input(f"Choose a weapon to equip (1-{len(weapons)+1}): ")
    valid_choices = [str(i) for i in range(1, len(weapons)+2)]
    while choice not in valid_choices:
        choice = input(f"Invalid option. Please choose (1-{len(weapons)+1}): ")
    
    if int(choice) == len(weapons)+1:
        print("Cancelled equipping.")
    else:
        equipped_weapon = weapons[int(choice)-1]
        print(f"You have equipped {equipped_weapon['name']}.")

def fight_monster(hp, gold):
    """
    Handles the combat loop for fighting a monster.
    
    Generates a random monster via gamefunctions.new_random_monster(), then enters a loop 
    where the player can choose to attack, run away, or (if available) use a special item.
    
    Args:
        hp (int): The player's current hit points.
        gold (int): The player's current gold.
    
    Returns:
        tuple: Updated player's hit points and gold.
    """
    monster = gamefunctions.new_random_monster()
    monster_hp = monster.get('hp', 20)  # Default monster HP if not provided
    print("\nA wild monster appears!")
    print("Monster Details:")
    for key, value in monster.items():
        print(f"{key.capitalize()}: {value}")
    
    while monster_hp > 0 and hp > 0:
        print(f"\nYour HP: {hp} | Monster HP: {monster_hp}")
        print("1) Attack")
        print("2) Run away")
        # If player has a special item, offer to use it
        has_special = any(item for item in inventory if item.get("type") == "special")
        if has_special:
            print("3) Use Magic Charm (special item)")
        
        action = input("Choose an action: ")
        valid_actions = ['1', '2'] + (['3'] if has_special else [])
        while action not in valid_actions:
            action = input("Invalid option. Choose again: ")
        
        if action == '1':
            # Determine damage; increase if sword is equipped
            base_damage = 5
            bonus = 2 if equipped_weapon and equipped_weapon.get("type") == "weapon" else 0
            player_damage = base_damage + bonus
            monster_hp -= player_damage
            print(f"You attack the monster dealing {player_damage} damage.")
            
            # If a weapon is equipped, reduce its durability
            if equipped_weapon:
                equipped_weapon["currentDurability"] -= 1
                print(f"Your {equipped_weapon['name']}'s durability is now {equipped_weapon['currentDurability']}.")
                if equipped_weapon["currentDurability"] <= 0:
                    print(f"Your {equipped_weapon['name']} has broken!")
                    # Remove the broken weapon from inventory and unequip it
                    inventory.remove(equipped_weapon)
                    equipped_weapon = None
                    
            if monster_hp <= 0:
                print("You defeated the monster!")
                reward = monster.get('gold', 5)  # Default gold reward if not specified
                gold += reward
                print(f"You gained {reward} gold!")
                break
            # Monster counterattacks
            monster_damage = 3  # Fixed damage; can be randomized
            hp -= monster_damage
            print(f"The monster attacks you dealing {monster_damage} damage.")
            if hp <= 0:
                print("You have been defeated by the monster!")
                break
                
        elif action == '2':
            print("You ran away from the fight!")
            break
            
        elif action == '3' and has_special:
            # Use the first available special item
            for item in inventory:
                if item.get("type") == "special":
                    print(f"You use your {item['name']} to defeat the monster instantly!")
                    inventory.remove(item)
                    # Monster defeated without HP loss
                    reward = monster.get('gold', 5)
                    gold += reward
                    print(f"You gained {reward} gold!")
                    monster_hp = 0
                    break
    return hp, gold

def main():
    """
    Runs the main game loop.
    
    Options include:
      1) Leave town to fight a monster.
      2) Sleep (restore HP for 5 gold).
      3) Visit Shop to purchase items.
      4) Equip Items.
      5) Quit the game.
    """
    global inventory, equipped_weapon
    name = input("Enter your name: ")
    gamefunctions.print_welcome(name)
    
    hp = 30
    gold = 10
    
    while True:
        print(f"\nYou are in town.\nCurrent HP: {hp}, Current Gold: {gold}")
        print("What would you like to do?")
        print("1) Leave town (Fight Monster)")
        print("2) Sleep (Restore HP for 5 Gold)")
        print("3) Visit Shop")
        print("4) Equip Items")
        print("5) Quit")
        
        choice = input("Enter your choice (1-5): ")
        while choice not in ['1', '2', '3', '4', '5']:
            choice = input("Invalid option. Please enter a valid choice (1-5): ")
        
        if choice == '1':
            hp, gold = fight_monster(hp, gold)
            if hp <= 0:
                print("Game Over!")
                break
        elif choice == '2':
            if gold >= 5:
                gold -= 5
                hp = 30
                print("You sleep and restore your HP to 30.")
            else:
                print("You don't have enough gold to sleep!")
        elif choice == '3':
            gold = shop_menu(gold)
        elif choice == '4':
            equip_item()
        elif choice == '5':
            print("Thanks for playing. Goodbye!")
            break

if __name__ == "__main__":
    main()
