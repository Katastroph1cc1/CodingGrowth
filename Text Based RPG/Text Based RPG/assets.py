HEADER = r"""
  /$$$$$$   /$$$$$$  /$$$$$$$  /$$$$$$$$ /$$$$$$$  /$$   /$$ /$$      
 /$$__  $$ /$$__  $$| $$__  $$| $$_____/| $$__  $$| $$  | $$| $$      
| $$  \__/| $$  \ $$| $$  \ $$| $$      | $$  \ $$| $$  | $$| $$      
| $$ /$$$$| $$  | $$| $$  | $$| $$$$$   | $$$$$$$/| $$$$$$$$| $$      
| $$|_  $$| $$  | $$| $$  | $$| $$__/   | $$__  $$| $$__  $$|__/      
| $$  \ $$| $$  | $$| $$  | $$| $$      | $$  \ $$| $$  | $$          
|  $$$$$$/|  $$$$$$/| $$$$$$$/| $$$$$$$$| $$  | $$| $$  | $$ /$$      
 \______/  \______/ |_______/ |________/|__/  |__/|__/  |__/|__/      
"""

GAME_OVER_ART = r"""
   ___   _   __  __ ___   _____   _____ ___ 
  / __| /_\ |  \/  | __| / _ \ \ / / __| _ \
 | (_ |/ _ \| |\/| | _| | (_) \ V /| _||   /
  \___/_/ \_\_|  |_|___| \___/ \_/ |___|_|_\
"""

CITY_ART = r"""
      _|_
     /   \    [THE CAPITAL CITY]
    /_____\   Safe Haven & Shops
   |  _    |
   | | |   |
   |_|_|___|
"""

FOREST_ART = r"""
      ^  ^  ^   ^      
     /|\/|\/|\ /|\    [THE DARK FOREST]
     /|\/|\/|\ /|\    Watch for Wolves
  ^^^^^^^^^^^^^^^^^^^
"""

CAVE_ART = r"""
      /---\
    /       \         [THE CAVES]
   |  O   O  |      Damp & Deadly
   |    ^    |
    \_______/
"""

RUINS_ART = r"""
    _  _   _ 
   | || | | |         [THE RUINS]
   | || |_| |       Ghosts Remain
   |__   ___|
      |_|
"""

MOUNTAINS_ART = r"""
      /\
     /  \   /\        [THE MOUNTAINS]
    /    \ /  \      Bandit Territory
   /      /    \
"""

BOSS_ART = r"""
   (    )
  ((((()))
  |o_o |||         [THE DEMON THRONE]
   \_/  ||
  / \   ||
"""

# Dictionary to map biome names to art
BIOME_ART = {
    "City": CITY_ART,
    "Forest": FOREST_ART,
    "Caves": CAVE_ART,
    "Ruins": RUINS_ART,
    "Mountains": MOUNTAINS_ART,
    "Boss": BOSS_ART
}
