import random

# --- ITEM CLASS ---
class Item:
    def __init__(self, name, description, cost, effect_type, effect_value):
        self.name = name
        self.description = description
        self.cost = cost
        self.effect_type = effect_type # "heal_hp" or "heal_mp"
        self.effect_value = effect_value

# --- QUEST CLASS ---
class Quest:
    def __init__(self, name, description, target_name, target_count, reward_gold, reward_xp):
        self.name = name
        self.description = description
        self.target_name = target_name 
        self.target_count = target_count
        self.current_count = 0
        self.reward_gold = reward_gold
        self.reward_xp = reward_xp
        self.is_completed = False
        self.is_turned_in = False

    def check_progress(self, enemy_name):
        if self.is_completed: return
        
        # Check if enemy name contains target (e.g. "Goblin Scout" matches "Goblin")
        if self.target_name.lower() in enemy_name.lower():
            self.current_count += 1
            print(f"[QUEST] {self.name}: {self.current_count}/{self.target_count}")
            if self.current_count >= self.target_count:
                self.is_completed = True
                print(f"[QUEST COMPLETED] {self.name}! Return to town.")

# --- CHARACTER BASE CLASS ---
class Character:
    def __init__(self, name, hp, attack, defense):
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.attack_stat = attack
        self.defense = defense

    def is_alive(self):
        return self.hp > 0

    def take_damage(self, dmg):
        self.hp -= dmg

# --- PLAYER CLASS & SUBCLASSES ---
class Player(Character):
    def __init__(self, name, hp, mp, str_stat, dex_stat, int_stat):
        super().__init__(name, hp, attack=0, defense=0)
        self.mp = mp 
        self.max_mp = mp
        self.str_stat = str_stat
        self.dex_stat = dex_stat
        self.int_stat = int_stat
        
        self.level = 1
        self.xp = 0
        self.xp_to_next_level = 100
        self.gold = 50
        
        self.location_x = 0
        self.location_y = 0
        
        self.inventory = []
        self.quests = []
        self.skills = {} 

    def add_item(self, item, quantity=1):
        for _ in range(quantity):
            self.inventory.append(item)

    def check_level_up(self):
        if self.xp >= self.xp_to_next_level:
            if self.level >= 10:
                self.xp = self.xp_to_next_level 
                return

            self.level += 1
            self.xp -= self.xp_to_next_level
            self.xp_to_next_level = int(self.xp_to_next_level * 1.5)
            
            # Stat Increases
            self.max_hp += 10
            self.max_mp += 10
            self.hp = self.max_hp
            self.mp = self.max_mp
            
            self.on_level_up() # Class specific boost
            print(f"\n*** LEVEL UP! YOU ARE NOW LEVEL {self.level} ***")

    def on_level_up(self):
        pass # Overridden by subclasses

    def update_quest_progress(self, enemy_name):
        for quest in self.quests:
            quest.check_progress(enemy_name)

    # For Saving/Loading
    def to_dict(self):
        return {
            "name": self.name,
            "class_type": self.__class__.__name__,
            "level": self.level,
            "xp": self.xp,
            "xp_next": self.xp_to_next_level,
            "gold": self.gold,
            "stats": {"hp": self.hp, "max_hp": self.max_hp, "mp": self.mp, "max_mp": self.max_mp, 
                      "str": self.str_stat, "dex": self.dex_stat, "int": self.int_stat},
            "location": {"x": self.location_x, "y": self.location_y},
            "inventory": [{"name": i.name, "val": i.effect_value} for i in self.inventory]
        }

class Warrior(Player):
    def __init__(self, name):
        super().__init__(name, hp=150, mp=0, str_stat=10, dex_stat=5, int_stat=2)
        self.resource_name = "Rage"
        self.add_item(Item("Health Potion", "Restores 50 HP", 20, "heal_hp", 50), 3)
        self.skills = {
            3: {"name": "Cleave", "cost": 30, "desc": "Swing wide. 150% Dmg."},
            6: {"name": "Enrage", "cost": 0, "desc": "Gain 50 Rage instantly."},
            9: {"name": "EXECUTE", "cost": 80, "desc": "Massive strike. 400% Dmg."}
        }

    def on_level_up(self):
        self.str_stat += 3
        self.dex_stat += 1

    def attack(self, enemy):
        dmg = int((8 + self.str_stat) * random.uniform(0.9, 1.1))
        self.mp = min(100, self.mp + 15) # Generate Rage
        print(f"You smash the {enemy.name} for {dmg} damage! (Gained 15 Rage)")
        enemy.take_damage(dmg)

class Rogue(Player):
    def __init__(self, name):
        super().__init__(name, hp=100, mp=100, str_stat=4, dex_stat=10, int_stat=4)
        self.resource_name = "Energy"
        self.add_item(Item("Health Potion", "Restores 50 HP", 20, "heal_hp", 50), 3)
        self.skills = {
            3: {"name": "Poison Shiv", "cost": 25, "desc": "Coat dagger. 140% Dmg."},
            6: {"name": "Blind", "cost": 40, "desc": "Enemy misses turn."},
            9: {"name": "Assassinate", "cost": 100, "desc": "Dump energy. 500% Dmg."}
        }

    def on_level_up(self):
        self.dex_stat += 3
        self.str_stat += 1
        
    def attack(self, enemy):
        dmg = int((6 + self.dex_stat) * random.uniform(0.9, 1.1))
        # Rogues regen energy naturally in combat loop usually, or small amount on hit
        print(f"You slice the {enemy.name} for {dmg} damage!")
        enemy.take_damage(dmg)

class Mage(Player):
    def __init__(self, name):
        super().__init__(name, hp=80, mp=150, str_stat=2, dex_stat=4, int_stat=12)
        self.resource_name = "Mana"
        self.add_item(Item("Health Potion", "Restores 50 HP", 20, "heal_hp", 50), 3)
        self.add_item(Item("Mana Potion", "Restores 50 MP", 25, "heal_mp", 50), 3)
        self.skills = {
            3: {"name": "Fireball", "cost": 30, "desc": "Nuke. 200% Dmg."},
            6: {"name": "Ice Lance", "cost": 20, "desc": "Fast cast. 120% Dmg."},
            9: {"name": "Apocalypse", "cost": 100, "desc": "Meteor. 500% Dmg."}
        }

    def on_level_up(self):
        self.int_stat += 3
        self.max_mp += 20

    def attack(self, enemy):
        dmg = int((4 + self.str_stat) * random.uniform(0.8, 1.0))
        print(f"You bonk the {enemy.name} with your staff for {dmg} damage.")
        enemy.take_damage(dmg)

# --- ENEMY CLASS ---
class Enemy(Character):
    def __init__(self, name, base_hp, base_attack, xp_value, level):
        # Scale stats based on player level
        scaled_hp = int(base_hp * (1 + (0.15 * (level - 1))))
        scaled_attack = int(base_attack * (1 + (0.10 * (level - 1))))
        scaled_xp = int(xp_value * (1 + (0.2 * (level - 1))))

        super().__init__(name, hp=scaled_hp, attack=scaled_attack, defense=0)
        self.xp_value = scaled_xp
        self.level = level
