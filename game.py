# game.py
# Ava Heintzelman 
# 3/18/25 (updated 3/31/25, refactored)

import random
import gamefunctions

def perform_attack(player_hp, monster_hp):
    """Execute one round of combat between the player and the monster."""
    player_damage = random.randint(3, 7)
    monster_damage = random.randint(2, 6)
    print(f"You attack and deal {player_damage} damage.")
    monster_hp -= player_damage
    if monster_hp <= 0:
        print("You defeated the monster!")
        return monster_hp, player_hp, True
    print(f"The monster attacks and deals {monster_damage} damage.")
    player_hp -= monster_damage
    return monster_hp, player_hp, False

def fight_monster(player_hp, player_gold):
    """Handles combat with a monster."""
    monster = gamefunctions.new_random_monster()
    monster_hp = monster.get('hp', 20)
    print("\nA wild monster appears!")
    for key, value in monster.items():
        print(f"{key.capitalize()}: {value}")
    
    while True:
        print(f"\nYour HP: {player_hp} | Monster HP: {monster_hp}")
        print("1) Attack")
        print("2) Run away")
        choice = input("Enter your choice: ")
        if choice not in ['1', '2']:
            print("Invalid input. Please select 1 or 2.")
            continue
        if choice == '2':
            print("You ran away!")
            return player_hp, player_gold
        
        monster_hp, player_hp, defeated = perform_attack(player_hp, monster_hp)
        if defeated:
            player_gold += 5
            print("You earned 5 gold!")
            return player_hp, player_gold
        if player_hp <= 0:
            print("You have been defeated by the monster! Game Over!")
            return player_hp, player_gold

def main_menu(player_hp, player_gold):
    """Displays the main menu and returns the player's choice."""
    print("\nYou are in town.")
    print(f"Current HP: {player_hp}, Current Gold: {player_gold}")
    print("What would you like to do?")
    print("1) Leave town (Fight Monster)")
    print("2) Sleep (Restore HP for 5 Gold)")
    print("3) Quit")
    return input("Enter your choice: ")

def handle_sleep(player_hp, player_gold):
    """Handles the sleep option to restore HP in exchange for gold."""
    if player_gold < 5:
        print("Not enough gold to sleep!")
    else:
        player_gold -= 5
        player_hp = 30
        print("You slept and restored your HP to 30.")
    return player_hp, player_gold

def main():
    """Main function for the game."""
    name = input("Enter your name: ")
    gamefunctions.print_welcome(name)
    
    player_hp = 30
    player_gold = 10
    
    while True:
        choice = main_menu(player_hp, player_gold)
        if choice not in ['1', '2', '3']:
            print("Invalid choice. Please select 1, 2, or 3.")
            continue
        
        if choice == '3':
            print("Thanks for playing!")
            break
        elif choice == '2':
            player_hp, player_gold = handle_sleep(player_hp, player_gold)
        elif choice == '1':
            player_hp, player_gold = fight_monster(player_hp, player_gold)
            if player_hp <= 0:
                break

if __name__ == "__main__":
    main()
