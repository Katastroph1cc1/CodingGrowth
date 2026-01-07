import random
import time

def trigger_random_event(player, biome):
    if random.random() > 0.3: return # 30% chance

    print("\n" + "!"*30)
    print("RANDOM EVENT")
    print("!"*30)
    time.sleep(1)

    roll = random.randint(1, 100)
    if roll <= 20:
        found = random.randint(10, 40)
        print(f"You found a purse on a dead body. Looted {found} Gold.")
        player.gold += found
    elif roll <= 40:
        dmg = int(player.max_hp * 0.1)
        print(f"You stepped in a trap! Took {dmg} damage.")
        player.take_damage(dmg)
    elif roll <= 50:
        print("A wandering priest heals your wounds.")
        player.hp = min(player.max_hp, player.hp + 30)
    
    # Biome flavor
    if biome == "Forest": print("A crow caws ominously.")
    elif biome == "Caves": print("Rocks fall nearby.")
    elif biome == "Ruins": print("You hear whispering ghosts.")
    
    print("!"*30)
    time.sleep(2)
