# game.py
# Ava Heintzelman 
# Updated 4/14/25 for Assignment 13 with WanderingMonster implementation

import random, json, pygame
import gamefunctions
from wanderingMonster import WanderingMonster

# Global monsters list for persistent map state
monsters = []
# Global placeholder for a collided monster during map movement
collided_monster = None

def save_game(player_hp, player_gold, inventory, equipped_weapon, player_map_pos, filename="savegame.json"):
    data = {
        "player_hp": player_hp,
        "player_gold": player_gold,
        "inventory": inventory,
        "equipped_weapon": equipped_weapon,
        "player_map_pos": list(player_map_pos)
        # Note: Monsters state is not persisted between game sessions per assignment requirements.
    }
    with open(filename, "w") as f:
        json.dump(data, f)
    print(f"Game saved to {filename}.")

def load_game(filename="savegame.json"):
    with open(filename, "r") as f:
        data = json.load(f)
    print(f"Game loaded from {filename}.")
    return (data["player_hp"], data["player_gold"], data["inventory"],
            data["equipped_weapon"], tuple(data["player_map_pos"]))

def shop(player_gold, inventory):
    items = [
        {"name": "Sword", "type": "weapon", "price": 10, "maxDurability": 40, "currentDurability": 40, "damage_bonus": 5},
        {"name": "Magic Scroll", "type": "special", "price": 15, "description": "Instantly defeats a monster"}
    ]
    print("\nShop Menu:")
    for i, item in enumerate(items, start=1):
        print(f"{i}) {item['name']} - {item['price']} gold")
    choice = input("Enter item number (or '0' to cancel): ")
    if choice == '0' or choice not in ['1', '2']:
        print("Exiting shop." if choice=='0' else "Invalid choice.")
        return player_gold, inventory
    selected = items[int(choice)-1]
    if player_gold < selected["price"]:
        print("Not enough gold!")
        return player_gold, inventory
    player_gold -= selected["price"]
    inventory.append(selected.copy())
    print(f"You purchased a {selected['name']}!")
    return player_gold, inventory

def equip_weapon(inventory):
    weapons = [item for item in inventory if item.get("type") == "weapon"]
    if not weapons:
        print("No weapons to equip.")
        return None
    print("\nAvailable Weapons:")
    for i, w in enumerate(weapons, start=1):
        print(f"{i}) {w['name']} (Damage Bonus: {w.get('damage_bonus',0)}, Durability: {w['currentDurability']}/{w['maxDurability']})")
    choice = input("Select a weapon (or '0' to cancel): ")
    if choice == '0':
        print("No weapon equipped.")
        return None
    try:
        idx = int(choice) - 1
        if idx not in range(len(weapons)):
            print("Invalid selection.")
            return None
    except ValueError:
        print("Invalid input.")
        return None
    print(f"{weapons[idx]['name']} is now equipped.")
    return weapons[idx]

def fight_monster(player_hp, player_gold, inventory, equipped_weapon, monster=None):
    """
    Handles combat between the player and a monster.
    If a monster is provided, its 'hp' attribute is used; otherwise a new random monster is created.
    """
    if monster is None:
        monster = WanderingMonster.new_random_monster()
    print("\nA wild monster appears!")
    # Display the monster's details
    for key, value in vars(monster).items():
        # Skip the color attribute for readability
        if key != "color":
            print(f"{key.capitalize()}: {value}")
    while True:
        print(f"\nYour HP: {player_hp} | Monster HP: {monster.hp}")
        print("1) Attack\n2) Run away")
        special = [item for item in inventory if item.get("type") == "special"]
        if special:
            print("3) Use special item")
        choice = input("Enter your choice: ")
        valid = ['1', '2'] + (['3'] if special else [])
        if choice not in valid:
            print("Invalid choice. Try again.")
            continue
        if choice == '2':
            print("You ran away!")
            return player_hp, player_gold, equipped_weapon, inventory
        if choice == '3' and special:
            inventory.remove(special[0])
            print(f"You used {special[0]['name']} to defeat the monster! You earned 5 gold!")
            monster.hp = 0
            player_gold += 5
            break
        base_damage = random.randint(3, 7)
        bonus = equipped_weapon.get("damage_bonus", 0) if equipped_weapon else 0
        if equipped_weapon:
            equipped_weapon["currentDurability"] -= 1
            print(f"Your {equipped_weapon['name']} loses 1 durability.")
            if equipped_weapon["currentDurability"] <= 0:
                print(f"Your {equipped_weapon['name']} has broken!")
                inventory.remove(equipped_weapon)
                equipped_weapon = None
        total = base_damage + bonus
        monster.hp -= total
        print(f"You attack and deal {total} damage.")
        if monster.hp <= 0:
            print("You defeated the monster! You earned 5 gold!")
            player_gold += 5
            break
        m_damage = random.randint(2, 6)
        player_hp -= m_damage
        print(f"Monster attacks and deals {m_damage} damage.")
        if player_hp <= 0:
            print("You have been defeated! Game Over!")
            break
    return player_hp, player_gold, equipped_weapon, inventory

def run_map(player_pos):
    """
    Runs the map interface where the player can move.
    Monster objects are drawn on the grid and move every other player move.
    A collision (player occupying the same square as a monster) triggers combat.
    """
    global monsters, collided_monster
    pygame.init()
    screen = pygame.display.set_mode((320,320))
    pygame.display.set_caption("Map")
    clock = pygame.time.Clock()
    town_pos = (0, 0)
    left_town, event_triggered = False, None
    MOVE = {pygame.K_UP:(0,-1), pygame.K_DOWN:(0,1), pygame.K_LEFT:(-1,0), pygame.K_RIGHT:(1,0)}
    move_count = 0

    # Initialize monsters if none exist
    if not monsters:
        # Ensure monsters don't spawn on the player's current position or in town
        m1 = WanderingMonster.new_random_monster(exclude_positions=[player_pos, town_pos])
        m2 = WanderingMonster.new_random_monster(exclude_positions=[player_pos, town_pos, m1.position])
        monsters.extend([m1, m2])

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                event_triggered, running = "quit", False
                break
            elif event.type == pygame.KEYDOWN and event.key in MOVE:
                dx, dy = MOVE[event.key]
                new_pos = (player_pos[0] + dx, player_pos[1] + dy)
                if 0 <= new_pos[0] < 10 and 0 <= new_pos[1] < 10:
                    player_pos = new_pos
                    move_count += 1
                    # Every other player move, let the monsters move
                    if move_count % 2 == 0:
                        for m in monsters:
                            m_dx, m_dy = random.choice(list(MOVE.values()))
                            m.move((m_dx, m_dy))
        left_town = left_town or (player_pos != town_pos)
        if left_town and player_pos == town_pos:
            event_triggered, running = "town", False
        # Check for collision with any monster
        for m in monsters:
            if m.position == player_pos:
                collided_monster = m
                event_triggered, running = "monster", False
                break

        screen.fill((255, 255, 255))
        # Draw grid lines
        for x in range(0, 321, 32):
            pygame.draw.line(screen, (0,0,0), (x, 0), (x, 320))
        for y in range(0, 321, 32):
            pygame.draw.line(screen, (0,0,0), (0, y), (320, y))
        # Draw the town (green circle)
        pygame.draw.circle(screen, (0,255,0), (16,16), 10)
        # Draw monsters with their individual colors
        for m in monsters:
            pygame.draw.circle(screen, m.color, (m.position[0]*32+16, m.position[1]*32+16), 10)
        # Draw the player (blue rectangle)
        pygame.draw.rect(screen, (0,0,255), pygame.Rect(player_pos[0]*32, player_pos[1]*32, 32, 32))
        pygame.display.flip()
        clock.tick(10)
    pygame.quit()
    return player_pos, event_triggered

def main():
    global monsters, collided_monster
    print("Welcome to the Adventure Game!")
    start = input("Press 'N' for New Game or 'L' to Load a game: ").strip().upper()
    if start == 'L':
        fname = input("Enter filename (default: savegame.json): ").strip() or "savegame.json"
        try:
            player_hp, player_gold, inventory, equipped_weapon, player_map_pos = load_game(fname)
        except FileNotFoundError:
            print("Save not found. Starting new game.")
            player_hp, player_gold, inventory, equipped_weapon, player_map_pos = 30, 10, [], None, (0, 0)
    else:
        player_hp, player_gold, inventory, equipped_weapon, player_map_pos = 30, 10, [], None, (0, 0)
    
    name = input("Enter your name: ")
    gamefunctions.print_welcome(name)
    
    while True:
        print(f"\nIn town. HP: {player_hp}, Gold: {player_gold}")
        print("1) Leave town (Map)\n2) Sleep (Restore HP for 5 Gold)\n3) Visit Shop\n4) Equip Weapon\n5) Save & Quit\n6) Quit without saving")
        choice = input("Enter choice: ")
        if choice not in ['1','2','3','4','5','6']:
            print("Invalid choice.")
            continue
        if choice == '6':
            print("Thanks for playing!")
            break
        if choice == '5':
            save_game(player_hp, player_gold, inventory, equipped_weapon, player_map_pos)
            print("Thanks for playing!")
            break
        if choice == '2':
            if player_gold < 5:
                print("Not enough gold!")
            else:
                player_gold -= 5
                player_hp = 30
                print("HP restored to 30.")
        elif choice == '3':
            player_gold, inventory = shop(player_gold, inventory)
        elif choice == '4':
            equipped_weapon = equip_weapon(inventory)
        elif choice == '1':
            player_map_pos, event = run_map(player_map_pos)
            if event == "quit":
                print("Closed map window.")
                break
            elif event == "town":
                print("Returned to town.")
            elif event == "monster":
                print("Encountered a monster!")
                # Trigger combat with the collided monster from the map
                player_hp, player_gold, equipped_weapon, inventory = fight_monster(
                    player_hp, player_gold, inventory, equipped_weapon, collided_monster)
                # Remove the defeated monster from the global list
                if collided_monster and collided_monster.hp <= 0:
                    monsters.remove(collided_monster)
                    collided_monster = None
                # Reset player position after combat (if desired)
                player_map_pos = (5, 5)
                if player_hp <= 0:
                    break

    print("Game session ended.")

if __name__ == "__main__":
    main()
