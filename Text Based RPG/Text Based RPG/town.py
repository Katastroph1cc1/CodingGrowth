import os
import time
import models
import assets

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def visit_shop(player):
    stock = [
        models.Item("Health Potion", "Restores 50 HP", 20, "heal_hp", 50),
        models.Item("Mana Potion", "Restores 50 MP", 30, "heal_mp", 50)
    ]
    while True:
        clear()
        print("--- ALCHEMIST SHOP ---")
        for i, item in enumerate(stock):
            print(f"{i+1}. {item.name} ({item.cost}g)")
        print(f"\nGold: {player.gold} | [Q]uit")
        
        buy = input(">> ")
        if buy.lower() == 'q': break
        
        if buy.isdigit() and 1 <= int(buy) <= len(stock):
            item = stock[int(buy)-1]
            if player.gold >= item.cost:
                player.gold -= item.cost
                player.add_item(item)
                print("Bought it.")
                time.sleep(1)
            else:
                print("Not enough gold.")
                time.sleep(1)

def visit_quests(player):
    # Sample quests
    quests = [
        models.Quest("Rat Catcher", "Kill 3 Wolves", "Wolf", 3, 50, 100),
        models.Quest("Spider Bane", "Kill 2 Spiders", "Spider", 2, 100, 200),
        models.Quest("Bone Breaker", "Kill 3 Skeletons", "Skeleton", 3, 200, 400)
    ]
    
    while True:
        clear()
        print("--- QUEST BOARD ---")
        # Turn in logic
        for q in player.quests:
            if q.is_completed and not q.is_turned_in:
                print(f"[!] Turning in {q.name}. Gained {q.reward_gold}g, {q.reward_xp}xp.")
                player.gold += q.reward_gold
                player.xp += q.reward_xp
                q.is_turned_in = True
                player.check_level_up()
                time.sleep(2)

        print("\nAvailable Contracts:")
        for i, q in enumerate(quests):
            print(f"{i+1}. {q.name} - Reward: {q.reward_gold}g")
        print("[Q]uit")
        
        choice = input(">> ")
        if choice.lower() == 'q': break
        
        if choice.isdigit() and 1 <= int(choice) <= len(quests):
            sel = quests[int(choice)-1]
            import copy
            if not any(pq.name == sel.name for pq in player.quests):
                player.quests.append(copy.deepcopy(sel))
                print(f"Accepted {sel.name}.")
                time.sleep(1)
            else:
                print("Already have that quest.")
                time.sleep(1)

def visit_town(player):
    while True:
        clear()
        print(assets.CITY_ART)
        print(f"Welcome, {player.name}. Gold: {player.gold}")
        print("1. Inn (Heal - 20g)")
        print("2. Shop")
        print("3. Quest Board")
        print("4. Leave City")
        
        c = input(">> ")
        if c == '1':
            if player.gold >= 20:
                player.gold -= 20
                player.hp = player.max_hp
                player.mp = player.max_mp
                if isinstance(player, models.Warrior): player.mp = 0 # Rage reset
                print("You rested well.")
            else:
                print("Get out, broke bum.")
            time.sleep(1)
        elif c == '2':
            visit_shop(player)
        elif c == '3':
            visit_quests(player)
        elif c == '4':
            break
