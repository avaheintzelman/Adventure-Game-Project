#game.py
#Ava Heintzelman 
#3/18/25 (updated 3/31/25)

import random
import gamefunctions

def shop(player_gold, inventory):
    """
    Displays the shop menu and allows the player to purchase items.
    
    Parameters:
        player_gold (int): The player's current gold.
        inventory (list): The player's inventory list.
    
    Returns:
        tuple: Updated (player_gold, inventory).
    """
    shop_items = [
        {"name": "Sword", "type": "weapon", "price": 10, "maxDurability": 40, "currentDurability": 40, "damage_bonus": 5},
        {"name": "Magic Scroll", "type": "special", "price": 15, "description": "Instantly defeats a monster"}
    ]
    print("\nShop Menu:")
    for i, item in enumerate(shop_items, start=1):
        print(f"{i}) {item['name']} - {item['price']} gold")
    choice = input("Enter the number of the item you wish to purchase (or '0' to cancel): ")
    if choice == '0':
        print("Exiting shop.")
        return player_gold, inventory
    if choice not in ['1', '2']:
        print("Invalid choice.")
        return player_gold, inventory
    selected = shop_items[int(choice) - 1]
    if player_gold < selected["price"]:
        print("Not enough gold!")
        return player_gold, inventory
    player_gold -= selected["price"]
    # Add a copy of the item to the inventory.
    inventory.append(selected.copy())
    print(f"You purchased a {selected['name']}!")
    return player_gold, inventory

def equip_weapon(inventory):
    """
    Allows the player to equip a weapon from their inventory.
    
    Parameters:
        inventory (list): The player's inventory list.
    
    Returns:
        dict or None: The equipped weapon if one is chosen, else None.
    """
    weapons = [item for item in inventory if item.get("type") == "weapon"]
    if not weapons:
        print("You have no weapons to equip.")
        return None
    print("\nAvailable Weapons:")
    for i, weapon in enumerate(weapons, start=1):
        print(f"{i}) {weapon['name']} (Damage Bonus: {weapon.get('damage_bonus', 0)}, Durability: {weapon['currentDurability']}/{weapon['maxDurability']})")
    choice = input("Select a weapon to equip (or '0' to cancel): ")
    if choice == '0':
        print("No weapon equipped.")
        return None
    try:
        index = int(choice) - 1
        if index < 0 or index >= len(weapons):
            print("Invalid selection.")
            return None
    except ValueError:
        print("Invalid input.")
        return None
    equipped = weapons[index]
    print(f"{equipped['name']} is now equipped.")
    return equipped

def fight_monster(player_hp, player_gold, inventory, equipped_weapon):
    """
    Handles combat with a monster.
    The player can attack (using an equipped weapon if available),
    run away, or use a special item (if available) to defeat the monster instantly.
    
    Parameters:
        player_hp (int): The player's current HP.
        player_gold (int): The player's current gold.
        inventory (list): The player's inventory.
        equipped_weapon (dict or None): The currently equipped weapon.
    
    Returns:
        tuple: Updated (player_hp, player_gold, equipped_weapon, inventory).
    """
    monster = gamefunctions.new_random_monster()
    monster_hp = monster.get("hp", 20)
    print("\nA wild monster appears!")
    for key, value in monster.items():
        print(f"{key.capitalize()}: {value}")
    
    while True:
        print(f"\nYour HP: {player_hp} | Monster HP: {monster_hp}")
        print("1) Attack")
        print("2) Run away")
        # Offer option to use a special item if one exists in the inventory.
        special_items = [item for item in inventory if item.get("type") == "special"]
        if special_items:
            print("3) Use special item to defeat the monster")
        
        fight_choice = input("Enter your choice: ")
        valid_choices = ['1', '2']
        if special_items:
            valid_choices.append('3')
        if fight_choice not in valid_choices:
            print("Invalid input. Please try again.")
            continue
        
        if fight_choice == '2':
            print("You ran away!")
            return player_hp, player_gold, equipped_weapon, inventory
        
        if fight_choice == '3' and special_items:
            used_item = special_items[0]
            inventory.remove(used_item)
            print(f"You used {used_item['name']} to defeat the monster instantly!")
            player_gold += 5
            print("You earned 5 gold!")
            return player_hp, player_gold, equipped_weapon, inventory
        
        # Attack action
        base_damage = random.randint(3, 7)
        bonus_damage = 0
        if equipped_weapon:
            bonus_damage = equipped_weapon.get("damage_bonus", 0)
            # Reduce durability for each attack.
            equipped_weapon["currentDurability"] -= 1
            print(f"Your {equipped_weapon['name']} loses 1 durability.")
            if equipped_weapon["currentDurability"] <= 0:
                print(f"Your {equipped_weapon['name']} has broken!")
                inventory.remove(equipped_weapon)
                equipped_weapon = None
        
        total_damage = base_damage + bonus_damage
        monster_hp -= total_damage
        print(f"You attack and deal {total_damage} damage.")
        if monster_hp <= 0:
            print("You defeated the monster!")
            player_gold += 5
            print("You earned 5 gold!")
            return player_hp, player_gold, equipped_weapon, inventory
        
        # Monster counterattack
        monster_damage = random.randint(2, 6)
        player_hp -= monster_damage
        print(f"The monster attacks and deals {monster_damage} damage.")
        if player_hp <= 0:
            print("You have been defeated by the monster! Game Over!")
            return player_hp, player_gold, equipped_weapon, inventory

def main():
    """
    Main function for the game.
    Manages the game loop, which includes options to fight monsters,
    sleep to restore HP, visit the shop to purchase items, equip weapons, or quit.
    """
    name = input("Enter your name: ")
    gamefunctions.print_welcome(name)
    
    # Initialize player stats and inventory.
    player_hp = 30
    player_gold = 10
    inventory = []
    equipped_weapon = None

    while True:
        print("\nYou are in town.")
        print(f"Current HP: {player_hp}, Current Gold: {player_gold}")
        print("What would you like to do?")
        print("1) Leave town (Fight Monster)")
        print("2) Sleep (Restore HP for 5 Gold)")
        print("3) Visit Shop")
        print("4) Equip Weapon")
        print("5) Quit")
        
        choice = input("Enter your choice: ")
        if choice not in ['1', '2', '3', '4', '5']:
            print("Invalid choice. Please try again.")
            continue
        
        if choice == '5':
            print("Thanks for playing!")
            break
        
        if choice == '2':
            if player_gold < 5:
                print("Not enough gold to sleep!")
            else:
                player_gold -= 5
                player_hp = 30
                print("You slept and restored your HP to 30.")
        elif choice == '3':
            player_gold, inventory = shop(player_gold, inventory)
        elif choice == '4':
            equipped_weapon = equip_weapon(inventory)
        elif choice == '1':
            player_hp, player_gold, equipped_weapon, inventory = fight_monster(
                player_hp, player_gold, inventory, equipped_weapon
            )
            if player_hp <= 0:
                break

if __name__ == "__main__":
    main()
