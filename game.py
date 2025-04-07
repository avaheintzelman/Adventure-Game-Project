# game.py
# Ava Heintzelman 
# Updated 4/7 for Assignment 12

import random, json, pygame, gamefunctions

def save_game(player_hp, player_gold, inventory, equipped_weapon, player_map_pos, filename="savegame.json"):
    data = {
        "player_hp": player_hp,
        "player_gold": player_gold,
        "inventory": inventory,
        "equipped_weapon": equipped_weapon,
        "player_map_pos": list(player_map_pos)
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

def fight_monster(player_hp, player_gold, inventory, equipped_weapon):
    monster = gamefunctions.new_random_monster()
    monster_hp = monster.get("hp", 20)
    print("\nA wild monster appears!")
    for key, value in monster.items():
        print(f"{key.capitalize()}: {value}")
    while True:
        print(f"\nYour HP: {player_hp} | Monster HP: {monster_hp}")
        print("1) Attack\n2) Run away")
        special = [item for item in inventory if item.get("type") == "special"]
        if special:
            print("3) Use special item")
        choice = input("Enter your choice: ")
        valid = ['1', '2'] + (['3'] if special else [])
        if choice not in valid:
            print("Invalid choice. Try again."); continue
        if choice == '2':
            print("You ran away!"); return player_hp, player_gold, equipped_weapon, inventory
        if choice == '3' and special:
            inventory.remove(special[0])
            print(f"You used {special[0]['name']} to defeat the monster! You earned 5 gold!")
            return player_hp, player_gold + 5, equipped_weapon, inventory
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
        monster_hp -= total
        print(f"You attack and deal {total} damage.")
        if monster_hp <= 0:
            print("You defeated the monster! You earned 5 gold!")
            return player_hp, player_gold + 5, equipped_weapon, inventory
        m_damage = random.randint(2, 6)
        player_hp -= m_damage
        print(f"Monster attacks and deals {m_damage} damage.")
        if player_hp <= 0:
            print("You have been defeated! Game Over!")
            return player_hp, player_gold, equipped_weapon, inventory

def run_map(player_pos):
    pygame.init()
    screen = pygame.display.set_mode((320,320))
    pygame.display.set_caption("Map")
    clock = pygame.time.Clock()
    town_pos, monster_pos = (0, 0), (5, 5)
    left_town, event_triggered = False, None
    MOVE = {pygame.K_UP:(0,-1), pygame.K_DOWN:(0,1), pygame.K_LEFT:(-1,0), pygame.K_RIGHT:(1,0)}
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                event_triggered, running = "quit", False; break
            elif event.type == pygame.KEYDOWN and event.key in MOVE:
                dx, dy = MOVE[event.key]
                new_pos = (player_pos[0] + dx, player_pos[1] + dy)
                if 0 <= new_pos[0] < 10 and 0 <= new_pos[1] < 10:
                    player_pos = new_pos
        left_town = left_town or (player_pos != town_pos)
        if left_town and player_pos == town_pos: event_triggered, running = "town", False
        if player_pos == monster_pos: event_triggered, running = "monster", False
        screen.fill((255, 255, 255))
        for x in range(0, 321, 32):
            pygame.draw.line(screen, (0,0,0), (x, 0), (x, 320))
        for y in range(0, 321, 32):
            pygame.draw.line(screen, (0,0,0), (0, y), (320, y))
        pygame.draw.circle(screen, (0,255,0), (16,16), 10)
        pygame.draw.circle(screen, (255,0,0), (monster_pos[0]*32+16, monster_pos[1]*32+16), 10)
        pygame.draw.rect(screen, (0,0,255), pygame.Rect(player_pos[0]*32, player_pos[1]*32, 32, 32))
        pygame.display.flip()
        clock.tick(10)
    pygame.quit()
    return player_pos, event_triggered

def main():
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
            print("Invalid choice."); continue
        if choice == '6':
            print("Thanks for playing!"); break
        if choice == '5':
            save_game(player_hp, player_gold, inventory, equipped_weapon, player_map_pos)
            print("Thanks for playing!"); break
        if choice == '2':
            if player_gold < 5:
                print("Not enough gold!")
            else:
                player_gold -= 5; player_hp = 30; print("HP restored to 30.")
        elif choice == '3':
            player_gold, inventory = shop(player_gold, inventory)
        elif choice == '4':
            equipped_weapon = equip_weapon(inventory)
        elif choice == '1':
            player_map_pos, event = run_map(player_map_pos)
            if event == "quit":
                print("Closed map window."); break
            elif event == "town":
                print("Returned to town.")
            elif event == "monster":
                print("Encountered a monster!")
                player_map_pos = (5, 5)
                player_hp, player_gold, equipped_weapon, inventory = fight_monster(player_hp, player_gold, inventory, equipped_weapon)
                if player_hp <= 0:
                    break

if __name__ == "__main__":
    main()
