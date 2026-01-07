import random
import models

BOSS_LOCATION = (0, -10) # 10 steps South

class MapTile:
    def __init__(self, x, y, player_level):
        self.x = x
        self.y = y
        self.player_level = player_level
        self.description = ""
        self.enemy = None
        self.biome = ""
        self.generate_tile()

    def generate_tile(self):
        # 1. The City
        if self.x == 0 and self.y == 0:
            self.biome = "City"
            self.description = "The Capital City. Roads lead in all directions."
            return

        # 2. The Boss (South)
        if (self.x, self.y) == BOSS_LOCATION:
            self.biome = "Boss"
            self.description = "THE GATES OF HELL. The Demon King awaits."
            self.enemy = models.Enemy("Demon King", base_hp=800, base_attack=30, xp_value=50000, level=15)
            return

        # 3. Biomes by Direction
        if self.y < 0: # South
            self.biome = "Forest"
            self.description = "The Dark Forest. Trees block the sun."
            if random.random() < 0.5: self.enemy = self.spawn_scaled_enemy("Forest")

        elif self.y > 0: # North
            self.biome = "Caves"
            self.description = "The damp Caves. Smells of rot."
            if random.random() < 0.5: self.enemy = self.spawn_scaled_enemy("Caves")

        elif self.x > 0: # East
            self.biome = "Ruins"
            self.description = "Ancient Ruins. Shadows move here."
            if random.random() < 0.5: self.enemy = self.spawn_scaled_enemy("Ruins")

        elif self.x < 0: # West
            self.biome = "Mountains"
            self.description = "Jagged Mountains. The wind howls."
            if random.random() < 0.5: self.enemy = self.spawn_scaled_enemy("Mountains")

    def spawn_scaled_enemy(self, biome_type):
        lvl = self.player_level
        options = []
        if biome_type == "Forest":
            options = [("Dire Wolf", 30, 4, 20), ("Orc Scout", 40, 5, 25), ("Bear", 60, 6, 30)]
        elif biome_type == "Caves":
            options = [("Giant Spider", 35, 6, 25), ("Troll", 70, 8, 40), ("Bat", 20, 5, 15)]
        elif biome_type == "Ruins":
            options = [("Skeleton", 40, 5, 20), ("Ghost", 30, 8, 30), ("Dark Knight", 80, 10, 60)]
        elif biome_type == "Mountains":
            options = [("Bandit", 50, 6, 30), ("Harpy", 30, 9, 35), ("Golem", 100, 4, 50)]

        choice = random.choice(options)
        return models.Enemy(choice[0], choice[1], choice[2], choice[3], level=lvl)

class World:
    def __init__(self):
        self.map_grid = {} 

    def is_movement_allowed(self, target_x, target_y, player_level):
        if (target_x, target_y) == BOSS_LOCATION:
            if player_level < 10:
                print(f"\n[BLOCKED] A dark barrier blocks the path South.")
                print("Voice: 'ONLY THOSE OF LEVEL 10 MAY ENTER!'")
                return False
            else:
                print("\n[UNLOCKED] The barrier shatters. The King awaits.")
                return True
        return True

    def get_tile(self, x, y, player_level):
        if (x, y) not in self.map_grid:
            self.map_grid[(x, y)] = MapTile(x, y, player_level)
        return self.map_grid[(x, y)]
