#game.py
#Ava Heintzelman 
#3/18/25 (updated 3/31/25)

import random
import gamefunctions

def fight_monster(player_hp, player_gold):
    """
    Handles combat with a monster.
    The fight continues until the monster is defeated, the player runs away, or the player dies.
    
    Parameters:
        player_hp (int): The player's current HP.
        player_gold (int): The player's current gold.
    
    Returns:
        tuple: Updated (player_hp, player_gold) after combat.
    """
    monster = gamefunctions.new_random_monster()
    # Use the monster's HP if provided; otherwise, assign a default value.
    monster_hp = monster.get('hp', 20)
    print("\nA wild monster appears!")
    for key, value in monster.items():
        print(f"{key.capitalize()}: {value}")
    
    while True:
        print(f"\nYour HP: {player_hp} | Monster HP: {monster_hp}")
        print("1) Attack")
        print("2) Run away")
        fight_choice = input("Enter your choice: ")
        if fight_choice not in ['1', '2']:
            print("Invalid input. Please select 1 or 2.")
            continue
        if fight_choice == '2':
            print("You ran away!")
            return player_hp, player_gold
        
        # Simulate the attack phase with random damage values.
        player_damage = random.randint(3, 7)
        monster_damage = random.randint(2, 6)
        monster_hp -= player_damage
        print(f"You attack and deal {player_damage} damage.")
        if monster_hp <= 0:
            print("You defeated the monster!")
            player_gold += 5  # Reward for defeating the monster.
            print("You earned 5 gold!")
            return player_hp, player_gold
        
        player_hp -= monster_damage
        print(f"The monster attacks and deals {monster_damage} damage.")
        if player_hp <= 0:
            print("You have been defeated by the monster! Game Over!")
            return player_hp, player_gold

def main():
    """
    Main function for the game.
    Handles the main game loop and user input validation.
    """
    name = input("Enter your name: ")
    gamefunctions.print_welcome(name)
    
    # Initialize player's stats.
    player_hp = 30
    player_gold = 10

    # Main game loop.
    while True:
        print("\nYou are in town.")
        print(f"Current HP: {player_hp}, Current Gold: {player_gold}")
        print("What would you like to do?")
        print("1) Leave town (Fight Monster)")
        print("2) Sleep (Restore HP for 5 Gold)")
        print("3) Quit")
        
        choice = input("Enter your choice: ")
        if choice not in ['1', '2', '3']:
            print("Invalid choice. Please select 1, 2, or 3.")
            continue
        
        if choice == '3':
            print("Thanks for playing!")
            break
        
        if choice == '2':
            if player_gold < 5:
                print("Not enough gold to sleep!")
            else:
                player_gold -= 5
                player_hp = 30
                print("You slept and restored your HP to 30.")
        
        elif choice == '1':
            player_hp, player_gold = fight_monster(player_hp, player_gold)
            if player_hp <= 0:
                break

if __name__ == "__main__":
    main()
