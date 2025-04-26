# game.py
# Ava Heintzelman
# Updated 4/26/25 for Assignment 15 Last Assignment


def run_map(player_pos):
    """
    Runs the map interface where the player can move.
    Adds static obstacles that block movement.
    """
    global monsters, collided_monster
    pygame.init()
    screen = pygame.display.set_mode((320,320))
    pygame.display.set_caption("Map with Obstacles")
    clock = pygame.time.Clock()

    # === 1. Initialize Obstacles ===
    GRID_SIZE = 10
    NUM_OBSTACLES = 5
    obstacle_positions = set()
    forbidden = {tuple(player_pos), (0,0)}  # avoid start & town
    while len(obstacle_positions) < NUM_OBSTACLES:
        pos = (random.randrange(GRID_SIZE), random.randrange(GRID_SIZE))
        if pos not in forbidden:
            obstacle_positions.add(pos)

    # === 2. Load images ===
    try:
        player_img = pygame.image.load("player.png").convert_alpha()
    except (pygame.error, FileNotFoundError):
        player_img = None
    try:
        monster_img = pygame.image.load("monster.png").convert_alpha()
    except (pygame.error, FileNotFoundError):
        monster_img = None

    town_pos = (0, 0)
    left_town = False
    event_triggered = None

    MOVE = {
        pygame.K_UP:    (0, -1),
        pygame.K_DOWN:  (0, 1),
        pygame.K_LEFT:  (-1, 0),
        pygame.K_RIGHT: (1, 0)
    }
    move_count = 0

    # Initialize monsters if needed
    if not monsters:
        m1 = WanderingMonster.new_random_monster(exclude_positions=[player_pos, town_pos])
        m2 = WanderingMonster.new_random_monster(exclude_positions=[player_pos, town_pos, m1.position])
        monsters.extend([m1, m2])

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                event_triggered, running = "quit", False
            elif event.type == pygame.KEYDOWN and event.key in MOVE:
                dx, dy = MOVE[event.key]
                new_pos = (player_pos[0]+dx, player_pos[1]+dy)
                # === 3. Movement & Obstacle Check ===
                if 0 <= new_pos[0] < GRID_SIZE and 0 <= new_pos[1] < GRID_SIZE:
                    if new_pos in obstacle_positions:
                        print("You can't move there! An obstacle blocks the way.")
                    else:
                        player_pos = new_pos
                        move_count += 1
                        # Move monsters every other step
                        if move_count % 2 == 0:
                            for m in monsters:
                                mdx, mdy = random.choice(list(MOVE.values()))
                                m.move((mdx, mdy))
        # Check leaving/returning town & monster collisions as before...

        # === 4. Draw Everything ===
        screen.fill((255,255,255))
        # Grid
        for x in range(0, 321, 32):
            pygame.draw.line(screen, (0,0,0), (x, 0), (x, 320))
        for y in range(0, 321, 32):
            pygame.draw.line(screen, (0,0,0), (0, y), (320, y))
        # Town
        pygame.draw.circle(screen, (0,255,0), (16,16), 10)
        # Obstacles
        for ox, oy in obstacle_positions:
            pygame.draw.rect(screen, (128,128,128), pygame.Rect(ox*32, oy*32, 32, 32))
        # Monsters & Player (same as before)...
        pygame.display.flip()
        clock.tick(10)

    pygame.quit()
    return player_pos, event_triggered
