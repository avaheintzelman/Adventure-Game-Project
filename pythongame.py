#game.py
#Ava Heintzelman 
#3/18/25

import gamefunctions

def fight_monster(hp, gold):
    """
    Handles the combat loop for fighting a monster.
    
    Generates a random monster via gamefunctions.new_random_monster(), then enters a loop 
    where the player can choose to attack or run away. Damage is exchanged each turn. If the 
    monster is defeated, the player earns gold. If the player runs or is defeated, control returns 
    to the town.
    
    Args:
        hp (int): The player's current hit points.
        gold (int): The player's current gold.
    
    Returns:
        tuple: Updated player's hit points and gold.
    """
    monster = gamefunctions.new_random_monster()
    # Assume the monster dictionary has keys like 'hp' and 'gold'
    monster_hp = monster.get('hp', 20)  # Default monster HP if not provided
    print("\nA wild monster appears!")
    print("Monster Details:")
    for key, value in monster.items():
        print(f"{key.capitalize()}: {value}")
    
    while monster_hp > 0 and hp > 0:
        print(f"\nYour HP: {hp} | Monster HP: {monster_hp}")
        print("1) Attack")
        print("2) Run away")
        action = input("Choose an action (1-2): ")
        while action not in ['1', '2']:
            action = input("Invalid option. Please choose (1-2): ")
        
        if action == '1':
            # Player attacks monster
            player_damage = 5  # Fixed damage value; can be modified or randomized
            monster_hp -= player_damage
            print(f"You attack the monster dealing {player_damage} damage.")
            if monster_hp <= 0:
                print("You defeated the monster!")
                reward = monster.get('gold', 5)  # Default gold reward if not specified
                gold += reward
                print(f"You gained {reward} gold!")
                break
            # Monster counterattacks
            monster_damage = 3  # Fixed damage value; can be modified or randomized
            hp -= monster_damage
            print(f"The monster attacks you dealing {monster_damage} damage.")
            if hp <= 0:
                print("You have been defeated by the monster!")
                break
        elif action == '2':
            print("You ran away from the fight!")
            break
    return hp, gold

def main():
    """
    Runs the main game loop.
    
    The loop displays a simple town menu allowing the user to:
      1) Leave town to fight a monster.
      2) Sleep (restore HP for 5 gold).
      3) Quit the game.
      
    User input is validated so that only allowed options are accepted.
    """
    name = input("Enter your name: ")
    gamefunctions.print_welcome(name)
    
    hp = 30
    gold = 10
    
    while True:
        print(f"\nYou are in town.\nCurrent HP: {hp}, Current Gold: {gold}")
        print("What would you like to do?")
        print("1) Leave town (Fight Monster)")
        print("2) Sleep (Restore HP for 5 Gold)")
        print("3) Quit")
        
        choice = input("Enter your choice (1-3): ")
        while choice not in ['1', '2', '3']:
            choice = input("Invalid option. Please enter a valid choice (1-3): ")
        
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
            print("Thanks for playing. Goodbye!")
            break

if __name__ == "__main__":
    main()
