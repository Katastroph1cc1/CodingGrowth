import json
import os
import models

SAVE_FILE = "save_game.json"

def save_game(player):
    data = player.to_dict()
    try:
        with open(SAVE_FILE, 'w') as f:
            json.dump(data, f, indent=4)
        print("[SYSTEM] Game Saved.")
    except Exception as e:
        print(f"Error saving: {e}")

def load_game():
    if not os.path.exists(SAVE_FILE):
        print("No save file found.")
        return None
    
    try:
        with open(SAVE_FILE, 'r') as f:
            data = json.load(f)
            
        name = data['name']
        ctype = data['class_type']
        
        if ctype == "Warrior": player = models.Warrior(name)
        elif ctype == "Rogue": player = models.Rogue(name)
        elif ctype == "Mage": player = models.Mage(name)
        else: return None
        
        player.level = data['level']
        player.xp = data['xp']
        player.xp_to_next_level = data['xp_next']
        player.gold = data['gold']
        player.hp = data['stats']['hp']
        player.max_hp = data['stats']['max_hp']
        player.mp = data['stats']['mp']
        player.max_mp = data['stats']['max_mp']
        player.str_stat = data['stats']['str']
        player.dex_stat = data['stats']['dex']
        player.int_stat = data['stats']['int']
        player.location_x = data['location']['x']
        player.location_y = data['location']['y']
        
        player.inventory = []
        for i in data['inventory']:
            # Reconstruct basic potions
            effect = "heal_hp" if "Health" in i['name'] else "heal_mp"
            player.inventory.append(models.Item(i['name'], "Restored", 0, effect, i['val']))
            
        print("Game Loaded.")
        return player
    except Exception as e:
        print(f"Corrupt save: {e}")
        return None
