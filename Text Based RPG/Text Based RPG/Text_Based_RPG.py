import os
import sys
import models
import world
import combat
import town
import events
import save_manager
import assets

player = None
game_world = world.World()

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def create_character():
    clear()
    print("Enter your name:")
    name = input(">> ")
    print("Choose Class: \n1. Warrior (Str/HP)\n2. Rogue (Dex/Crit)\n3. Mage (Int/Mana)")
    while True:
        c = input(">> ")
        if c == '1': return models.Warrior(name)
        elif c == '2': return models.Rogue(name)
        elif c == '3': return models.Mage(name)

def move_player(dx, dy):
    global player
    tx, ty = player.location_x + dx, player.location_y + dy
    
    if game_world.is_movement_allowed(tx, ty, player.level):
        player.location_x += dx
        player.location_y += dy
        
        tile = game_world.get_tile(player.location_x, player.location_y, player.level)
        clear()
        print(f"LOCATION: ({player.location_x}, {player.location_y}) - {tile.biome}")
        print(tile.description)
        if tile.biome in assets.BIOME_ART: print(assets.BIOME_ART[tile.biome])
        
        if tile.enemy:
            res = combat.start_encounter(player, tile.enemy)
            if res == "victory":
                player.xp += tile.enemy.xp_value
                player.gold += int(tile.enemy.xp_value / 2)
                player.check_level_up()
                player.update_quest_progress(tile.enemy.name)
                tile.enemy = None # Enemy killed
            elif res == "defeat":
                print(assets.GAME_OVER_ART)
                sys.exit()
        else:
            if tile.biome != "City":
                events.trigger_random_event(player, tile.biome)

def main():
    global player
    clear()
    print(assets.HEADER)
    print("1. New Game\n2. Load Game")
    if input(">> ") == '2':
        player = save_manager.load_game()
        if not player: player = create_character()
    else:
        player = create_character()
    
    # Game Loop
    while True:
        if player.location_x == 0 and player.location_y == 0:
            town.visit_town(player)
            print("\nYou are at the City Gates.")

        print(f"\nPlayer: {player.name} [Lv {player.level}] HP: {player.hp}/{player.max_hp}")
        print("COMPASS: [N]orth | [S]outh | [E]ast | [W]est")
        print("[I]nventory | [Q]uests | [Save] | [Quit]")
        
        cmd = input(">> ").lower()
        
        if cmd == 'n': move_player(0, 1)
        elif cmd == 's': move_player(0, -1)
        elif cmd == 'e': move_player(1, 0)
        elif cmd == 'w': move_player(-1, 0)
        elif cmd == 'i':
            print(f"Items: {', '.join([i.name for i in player.inventory])}")
            input("Press Enter...")
        elif cmd == 'q':
            for q in player.quests:
                print(f"{q.name}: {q.current_count}/{q.target_count}")
            input("Press Enter...")
        elif cmd == 'save': save_manager.save_game(player)
        elif cmd == 'quit': sys.exit()

if __name__ == "__main__":
    main()
