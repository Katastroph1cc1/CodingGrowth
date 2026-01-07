import random
import time
import os
import models

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_bars(entity):
    percent = entity.hp / entity.max_hp
    bar = '=' * int(20 * percent) + '-' * (20 - int(20 * percent))
    print(f"{entity.name:<15} [{bar}] {int(entity.hp)}/{entity.max_hp} HP", end="")
    if hasattr(entity, 'mp'):
        print(f" | {entity.mp}/{entity.max_mp} {getattr(entity, 'resource_name', 'MP')}")
    else:
        print("")

def enemy_taunt(enemy_name):
    taunts = [
        f"The {enemy_name} screams: 'I'm going to eat your face!'",
        f"The {enemy_name} laughs: 'You fight like a damn coward.'",
        f"The {enemy_name} grunts: 'Bleed for me, bitch!'"
    ]
    print(f"\n> {random.choice(taunts)}")

def start_encounter(player, enemy):
    clear()
    print(f"*** BATTLE: {player.name} VS {enemy.name} ***")
    if random.random() < 0.5: enemy_taunt(enemy.name)

    while player.is_alive() and enemy.is_alive():
        print("-" * 50)
        print_bars(player)
        print_bars(enemy)
        print("-" * 50)
        
        # --- PLAYER TURN ---
        action = input("[A]ttack | [S]kill | [I]nventory | [R]un: ").lower()
        
        if action == 'a':
            player.attack(enemy)
            
        elif action == 's':
            avail = {k: v for k, v in player.skills.items() if player.level >= k}
            if not avail:
                print("You don't know any skills yet.")
                continue
            for lvl, s in avail.items():
                print(f"[Lv{lvl}] {s['name']} (Cost: {s['cost']})")
            
            choice = input("Skill Name: ").title()
            chosen = next((s for s in avail.values() if s['name'] == choice), None)
            
            if chosen and player.mp >= chosen['cost']:
                player.mp -= chosen['cost']
                # Simple skill damage calc
                stat = player.str_stat if isinstance(player, models.Warrior) else (player.dex_stat if isinstance(player, models.Rogue) else player.int_stat)
                dmg = int(stat * 3.5)
                print(f"You used {chosen['name']}! Dealt {dmg} damage.")
                enemy.take_damage(dmg)
            else:
                print("Invalid skill or not enough resource!")
                continue

        elif action == 'i':
            potions = [i for i in player.inventory if "Potion" in i.name]
            if not potions:
                print("You have no potions, idiot.")
                continue
            print(f"Using {potions[0].name}...")
            player.inventory.remove(potions[0])
            if potions[0].effect_type == "heal_hp":
                player.hp = min(player.max_hp, player.hp + potions[0].effect_value)
            elif potions[0].effect_type == "heal_mp":
                player.mp = min(player.max_mp, player.mp + potions[0].effect_value)
                
        elif action == 'r':
            if random.random() < 0.4:
                print("You ran away like a baby!")
                return "fled"
            else:
                print("Failed to run!")
        else:
            print("Do something valid!")
            continue

        # --- ENEMY TURN ---
        if enemy.is_alive():
            time.sleep(1)
            dmg = max(1, int(enemy.attack_stat - (player.dex_stat * 0.1)))
            print(f"\nThe {enemy.name} hits you for {dmg} damage!")
            player.take_damage(dmg)
            
            # Resource regen for Rogue/Warrior
            if isinstance(player, models.Rogue): player.mp = min(player.max_mp, player.mp + 10)

    if player.is_alive():
        print(f"\nVICTORY! The {enemy.name} is dead.")
        return "victory"
    else:
        return "defeat"
