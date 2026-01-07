import pygame
import sys
import random
import math
import os

pygame.init()

# -------------------- SCREEN SETUP --------------------
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("The Adventures of Mr.Landa")
clock = pygame.time.Clock()

# -------------------- LOAD IMAGES --------------------
def load_image(image_data, size=None):
    """Load image from data"""
    try:
        img = pygame.image.load(image_data)
        if size:
            img = pygame.transform.scale(img, size)
        return img
    except:
        return None

# Load background
try:
    background_img = pygame.image.load("hallway.png")
    background_img = pygame.transform.scale(background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
    print("Loaded hallway.png")
except:
    print("Could not load hallway.png")
    background_img = None

# Load heart images
try:
    full_heart_img = pygame.image.load("Heart.png")
    full_heart_img = pygame.transform.scale(full_heart_img, (40, 40))
    print("Loaded Heart.png")
except:
    print("Could not load Heart.png")
    full_heart_img = None

try:
    broken_heart_img = pygame.image.load("Broken heart.png")
    broken_heart_img = pygame.transform.scale(broken_heart_img, (40, 40))
    print("Loaded Broken heart.png")
except:
    print("Could not load Broken heart.png")
    broken_heart_img = None

# Load player image
try:
    player_img = pygame.image.load("landa.png")
    player_img = pygame.transform.scale(player_img, (70, 90))
    print("Loaded landa.png")
except:
    print("Could not load landa.png")
    player_img = None

# Load student image
try:
    student_img = pygame.image.load("pngegg.png")
    student_img = pygame.transform.scale(student_img, (60, 80))
    print("Loaded pngegg.png")
except:
    print("Could not load pngegg.png")
    student_img = None

# Load monster can image
try:
    monster_img = pygame.image.load("monster.png")
    monster_img = pygame.transform.scale(monster_img, (40, 70))
    print("Loaded monster.png")
except:
    print("Could not load monster.png")
    monster_img = None

# Load bagel image
try:
    bagel_img = pygame.image.load("bagel.png")
    bagel_img = pygame.transform.scale(bagel_img, (50, 50))
    print("Loaded bagel.png")
except:
    print("Could not load bagel.png")
    bagel_img = None

# Load coin image
try:
    coin_img = pygame.image.load("coin.png")
    coin_img = pygame.transform.scale(coin_img, (40, 40))
    print("Loaded coin.png")
except:
    print("Could not load coin.png")
    coin_img = None

# Load Minecraft inventory image
minecraft_inv_img = None
inventory_files = ["minecraft_inventory.png", "minecraft_inventory.jpg", "inventory.jpg", "inventory.png"]
for filename in inventory_files:
    try:
        minecraft_inv_img = pygame.image.load(filename)
        minecraft_inv_img = pygame.transform.scale(minecraft_inv_img, (700, 600))
        print(f"Loaded {filename}")
        break
    except:
        continue

if not minecraft_inv_img:
    print("Could not load Minecraft inventory")
    print("   Tried files:", inventory_files)

# -------------------- AUDIO SETUP --------------------
pygame.mixer.init()

# Background music
try:
    pygame.mixer.music.load("background_music.mp3")
    pygame.mixer.music.set_volume(0.1)
    pygame.mixer.music.play(-1)
    print("Loaded background_music.mp3")
except:
    print("Background music not found")

# Load sound effects
drink_sound = None
try:
    drink_sound = pygame.mixer.Sound("drink.mp3")
    drink_sound.set_volume(0.4)
    print("Loaded drink.mp3")
except:
    print("Could not load drink.mp3")

eat_sound = None
try:
    eat_sound = pygame.mixer.Sound("eat.mp3")
    eat_sound.set_volume(0.4)
    print("Loaded eat.mp3")
except:
    print("Could not load eat.mp3")

pickup_sound = None
try:
    pickup_sound = pygame.mixer.Sound("pickup.mp3")
    pickup_sound.set_volume(0.3)
    print("Loaded pickup.mp3")
except:
    print("Could not load pickup.mp3")

coin_sound = None
try:
    coin_sound = pygame.mixer.Sound("coin.mp3")
    coin_sound.set_volume(0.3)
    print("Loaded coin.mp3")
except:
    print("Could not load coin.mp3")

# -------------------- COLORS --------------------
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (100, 150, 255)
GRAY = (128, 128, 128)
LIGHT_GRAY = (200, 200, 200)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
DARK_GRAY = (80, 80, 80)
BROWN = (139, 69, 19)
GOLD = (255, 215, 0)

# -------------------- FONTS --------------------
font_large = pygame.font.SysFont(None, 60)
font_medium = pygame.font.SysFont(None, 40)
font_small = pygame.font.SysFont(None, 30)

# -------------------- GAME CONSTANTS (CHANGEABLE VARIABLES) --------------------
# Core Game Settings
LANE_WIDTH = SCREEN_WIDTH // 3
LANES = [LANE_WIDTH // 2, SCREEN_WIDTH // 2, SCREEN_WIDTH - LANE_WIDTH // 2]
GAME_TIME = 1200  # 20 minutes in seconds
GOAL_DISTANCE = 1000  # 1000 meters to win
MAX_INVENTORY_SIZE = 40  # Maximum items in inventory

# Speed Settings
BASE_SPEED = 5
BOOST_SPEED = 12
BOOST_DURATION = 180  # 3 seconds at 60 FPS

# Spawn Rate Settings (frames between spawns)
INITIAL_SPAWN_RATE = 80  # Start slower
MIN_SPAWN_RATE = 25  # Fastest spawn rate
SPAWN_RATE_DECREASE = 0.5  # How much to decrease spawn rate per spawn

# Spawn Probabilities (must add up to 1.0)
STUDENT_SPAWN_CHANCE = 0.55  # 55% students (obstacles)
COIN_SPAWN_CHANCE = 0.30     # 30% coins (common)
MONSTER_SPAWN_CHANCE = 0.10  # 10% monsters (rare boost)
BAGEL_SPAWN_CHANCE = 0.05    # 5% bagels (very rare healing)

# Score Values
DODGE_POINTS = 10      # Points for dodging a student
MONSTER_POINTS = 50    # Points for collecting monster
BAGEL_POINTS = 75      # Points for collecting bagel
COIN_VALUE = 1         # Value of each coin

# Player Settings
MAX_LIVES = 3
INVINCIBILITY_FRAMES = 60  # 1 second of invincibility after hit

# Helper function for centered text
def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)

# Helper function for left-aligned text
def draw_text_left(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

# -------------------- PLAYER CLASS --------------------
class Player:
    def __init__(self):
        self.lane = 1  # Start in middle lane (0, 1, 2)
        self.width = 70
        self.height = 90
        self.x = LANES[self.lane]
        self.y = SCREEN_HEIGHT - 150
        self.color = BLUE
        self.move_cooldown = 0
        self.image = player_img
        
    def move_left(self):
        if self.lane > 0 and self.move_cooldown == 0:
            self.lane -= 1
            self.move_cooldown = 10
            
    def move_right(self):
        if self.lane < 2 and self.move_cooldown == 0:
            self.lane += 1
            self.move_cooldown = 10
            
    def update(self):
        # Smooth movement to lane position
        target_x = LANES[self.lane]
        if self.x < target_x:
            self.x = min(self.x + 15, target_x)
        elif self.x > target_x:
            self.x = max(self.x - 15, target_x)
            
        if self.move_cooldown > 0:
            self.move_cooldown -= 1
            
    def draw(self, boosted=False):
        # Draw boost glow effect
        if boosted:
            for i in range(3):
                pygame.draw.rect(screen, YELLOW, 
                    (self.x - self.width//2 - 10 + i*2, 
                     self.y - self.height//2 - 10 + i*2, 
                     self.width + 20 - i*4, 
                     self.height + 20 - i*4), 2)
        
        # Draw player image or fallback to rectangle
        if self.image:
            img_rect = self.image.get_rect(center=(self.x, self.y))
            screen.blit(self.image, img_rect)
        else:
            pygame.draw.rect(screen, self.color, 
                            (self.x - self.width//2, self.y - self.height//2, 
                             self.width, self.height))
            # Draw face
            pygame.draw.circle(screen, WHITE, (int(self.x - 10), int(self.y - 20)), 5)
            pygame.draw.circle(screen, WHITE, (int(self.x + 10), int(self.y - 20)), 5)
            pygame.draw.rect(screen, WHITE, (self.x - 10, self.y, 20, 5))

# -------------------- OBSTACLE CLASS (Students) --------------------
class Student:
    def __init__(self, lane, speed):
        self.lane = lane
        self.x = LANES[lane]
        self.y = -100
        self.width = 60
        self.height = 80
        self.speed = speed
        self.color = RED
        self.image = student_img
        
    def update(self):
        self.y += self.speed
        
    def draw(self):
        # Draw student image or fallback
        if self.image:
            img_rect = self.image.get_rect(center=(self.x, self.y))
            screen.blit(self.image, img_rect)
        else:
            pygame.draw.rect(screen, self.color,
                            (self.x - self.width//2, self.y - self.height//2,
                             self.width, self.height))
            pygame.draw.circle(screen, (255, 200, 180),
                              (int(self.x), int(self.y - self.height//2 - 15)), 15)
        
    def is_off_screen(self):
        return self.y > SCREEN_HEIGHT + 100
        
    def collides_with(self, player):
        px = player.x
        py = player.y
        pw = player.width
        ph = player.height
        
        return (abs(self.x - px) < (self.width + pw) // 2 and
                abs(self.y - py) < (self.height + ph) // 2)

# -------------------- COLLECTIBLE CLASS (Monster) --------------------
class Monster:
    def __init__(self, lane, speed):
        self.lane = lane
        self.x = LANES[lane]
        self.y = -100
        self.width = 40
        self.height = 70
        self.speed = speed
        self.color = GREEN
        self.image = monster_img
        
    def update(self):
        self.y += self.speed
        
    def draw(self):
        # Draw monster can image or fallback
        if self.image:
            img_rect = self.image.get_rect(center=(self.x, self.y))
            screen.blit(self.image, img_rect)
        else:
            pygame.draw.rect(screen, self.color,
                            (self.x - self.width//2, self.y - self.height//2,
                             self.width, self.height))
            draw_text("M", font_small, BLACK, self.x, self.y)
        
    def is_off_screen(self):
        return self.y > SCREEN_HEIGHT + 100
        
    def collides_with(self, player):
        px = player.x
        py = player.y
        pw = player.width
        ph = player.height
        
        return (abs(self.x - px) < (self.width + pw) // 2 and
                abs(self.y - py) < (self.height + ph) // 2)

# -------------------- COLLECTIBLE CLASS (Bagel) --------------------
class Bagel:
    def __init__(self, lane, speed):
        self.lane = lane
        self.x = LANES[lane]
        self.y = -100
        self.width = 50
        self.height = 50
        self.speed = speed
        self.color = ORANGE
        self.image = bagel_img
        
    def update(self):
        self.y += self.speed
        
    def draw(self):
        # Draw bagel image or fallback
        if self.image:
            img_rect = self.image.get_rect(center=(self.x, self.y))
            screen.blit(self.image, img_rect)
        else:
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), 25)
            pygame.draw.circle(screen, (200, 150, 100), (int(self.x), int(self.y)), 10)
        
    def is_off_screen(self):
        return self.y > SCREEN_HEIGHT + 100
        
    def collides_with(self, player):
        px = player.x
        py = player.y
        pw = player.width
        ph = player.height
        
        return (abs(self.x - px) < (self.width + pw) // 2 and
                abs(self.y - py) < (self.height + ph) // 2)

# -------------------- COLLECTIBLE CLASS (Coin) --------------------
class Coin:
    def __init__(self, lane, speed):
        self.lane = lane
        self.x = LANES[lane]
        self.y = -100
        self.width = 40
        self.height = 40
        self.speed = speed
        self.color = GOLD
        self.image = coin_img
        self.rotation = 0  # For spinning animation
        
    def update(self):
        self.y += self.speed
        self.rotation = (self.rotation + 5) % 360  # Spin animation
        
    def draw(self):
        # Draw coin image or fallback
        if self.image:
            # Rotate coin for spinning effect
            rotated_img = pygame.transform.rotate(self.image, self.rotation)
            img_rect = rotated_img.get_rect(center=(self.x, self.y))
            screen.blit(rotated_img, img_rect)
        else:
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), 20)
            pygame.draw.circle(screen, ORANGE, (int(self.x), int(self.y)), 15)
            draw_text("$", font_small, BLACK, self.x, self.y)
        
    def is_off_screen(self):
        return self.y > SCREEN_HEIGHT + 100
        
    def collides_with(self, player):
        px = player.x
        py = player.y
        pw = player.width
        ph = player.height
        
        return (abs(self.x - px) < (self.width + pw) // 2 and
                abs(self.y - py) < (self.height + ph) // 2)

# -------------------- GAME CLASS --------------------
class Game:
    def __init__(self):
        self.player = Player()
        self.students = []
        self.monsters = []
        self.bagels = []
        self.coins = []
        self.lives = MAX_LIVES
        self.max_lives = MAX_LIVES
        self.inventory = []
        self.coin_count = 0  # Separate coin counter
        self.score = 0
        self.spawn_timer = 0
        self.spawn_rate = INITIAL_SPAWN_RATE
        self.game_timer = GAME_TIME
        self.start_ticks = pygame.time.get_ticks()
        self.paused = False
        self.invincible_timer = 0
        self.game_over = False
        self.victory = False
        self.distance = 0
        self.current_speed = BASE_SPEED
        self.boost_timer = 0
        self.scroll_offset = 0
        
    def use_boost(self):
        """Use a monster from inventory to activate speed boost"""
        if self.boost_timer == 0:
            for i, item in enumerate(self.inventory):
                if item == "Monster Energy":
                    self.inventory.pop(i)
                    self.boost_timer = BOOST_DURATION
                    self.current_speed = BOOST_SPEED
                    if drink_sound:
                        drink_sound.play()
                    return
    
    def use_bagel(self):
        """Use a bagel from inventory to restore health"""
        for i, item in enumerate(self.inventory):
            if item == "Bagel":
                if self.lives < self.max_lives:
                    self.inventory.pop(i)
                    self.lives += 1
                    if eat_sound:
                        eat_sound.play()
                    return
            
    def spawn_obstacle(self):
        lane = random.randint(0, 2)
        rand = random.random()
        
        # Use changeable spawn probabilities
        if rand < STUDENT_SPAWN_CHANCE:
            self.students.append(Student(lane, self.current_speed))
        elif rand < STUDENT_SPAWN_CHANCE + COIN_SPAWN_CHANCE:
            self.coins.append(Coin(lane, self.current_speed))
        elif rand < STUDENT_SPAWN_CHANCE + COIN_SPAWN_CHANCE + MONSTER_SPAWN_CHANCE:
            self.monsters.append(Monster(lane, self.current_speed))
        else:  # Bagels (very rare)
            self.bagels.append(Bagel(lane, self.current_speed))
            
    def update(self):
        if self.paused or self.game_over:
            return
            
        # Update timer
        elapsed = (pygame.time.get_ticks() - self.start_ticks) / 1000
        self.game_timer = max(0, GAME_TIME - elapsed)
        
        # Check if time ran out (LOSE condition)
        if self.game_timer <= 0:
            self.game_over = True
            self.victory = False
            return
            
        # Update boost timer
        if self.boost_timer > 0:
            self.boost_timer -= 1
            if self.boost_timer == 0:
                self.current_speed = BASE_SPEED
                
        # Update distance (speed affects distance traveled)
        distance_gain = self.current_speed / 60.0
        self.distance += distance_gain
        
        # Update scroll offset for moving background effect
        self.scroll_offset += self.current_speed
        if self.scroll_offset >= 100:
            self.scroll_offset = 0
        
        # Check if reached goal (WIN condition)
        if self.distance >= GOAL_DISTANCE:
            self.victory = True
            self.game_over = True
            return
            
        # Update player
        self.player.update()
        
        # Update invincibility
        if self.invincible_timer > 0:
            self.invincible_timer -= 1
        
        # Spawn obstacles with increasing difficulty
        self.spawn_timer += 1
        if self.spawn_timer >= self.spawn_rate:
            self.spawn_obstacle()
            self.spawn_timer = 0
            # Gradually increase difficulty by decreasing spawn rate
            if self.spawn_rate > MIN_SPAWN_RATE:
                self.spawn_rate = max(MIN_SPAWN_RATE, self.spawn_rate - SPAWN_RATE_DECREASE)
                
        # Update students
        for student in self.students[:]:
            student.speed = self.current_speed
            student.update()
            if student.is_off_screen():
                self.students.remove(student)
                self.score += DODGE_POINTS
            elif student.collides_with(self.player) and self.invincible_timer == 0:
                self.students.remove(student)
                self.lives -= 1
                self.invincible_timer = INVINCIBILITY_FRAMES
                if self.lives <= 0:
                    self.game_over = True
                    self.victory = False
                    
        # Update monsters
        for monster in self.monsters[:]:
            monster.speed = self.current_speed
            monster.update()
            if monster.is_off_screen():
                self.monsters.remove(monster)
            elif monster.collides_with(self.player):
                self.monsters.remove(monster)
                # Check inventory size before adding
                if len(self.inventory) < MAX_INVENTORY_SIZE:
                    self.inventory.append("Monster Energy")
                self.score += MONSTER_POINTS
                if pickup_sound:
                    pickup_sound.play()
                
        # Update bagels
        for bagel in self.bagels[:]:
            bagel.speed = self.current_speed
            bagel.update()
            if bagel.is_off_screen():
                self.bagels.remove(bagel)
            elif bagel.collides_with(self.player):
                self.bagels.remove(bagel)
                # Check inventory size before adding
                if len(self.inventory) < MAX_INVENTORY_SIZE:
                    self.inventory.append("Bagel")
                self.score += BAGEL_POINTS
                if pickup_sound:
                    pickup_sound.play()
        
        # Update coins
        for coin in self.coins[:]:
            coin.speed = self.current_speed
            coin.update()
            if coin.is_off_screen():
                self.coins.remove(coin)
            elif coin.collides_with(self.player):
                self.coins.remove(coin)
                self.coin_count += COIN_VALUE
                self.score += COIN_VALUE * 5  # Coins also add to score
                if coin_sound:
                    coin_sound.play()
                
    def draw(self):
        # Draw scrolling background for movement effect
        if background_img:
            y_offset = self.scroll_offset % SCREEN_HEIGHT
            screen.blit(background_img, (0, y_offset))
            screen.blit(background_img, (0, y_offset - SCREEN_HEIGHT))
        else:
            screen.fill(BLACK)
            # Draw lanes
            for i in range(4):
                x = i * LANE_WIDTH
                pygame.draw.line(screen, GRAY, (x, 0), (x, SCREEN_HEIGHT), 2)
                
            # Draw animated lane markers
            for y in range(-20, SCREEN_HEIGHT + 100, 100):
                for i in range(1, 3):
                    x = i * LANE_WIDTH
                    marker_y = (y + self.scroll_offset) % SCREEN_HEIGHT
                    pygame.draw.rect(screen, WHITE, (x - 5, marker_y, 10, 40))
                
        # Draw obstacles
        for student in self.students:
            student.draw()
            
        for monster in self.monsters:
            monster.draw()
            
        for bagel in self.bagels:
            bagel.draw()
        
        for coin in self.coins:
            coin.draw()
            
        # Draw player (flashing if invincible)
        if self.invincible_timer == 0 or (self.invincible_timer // 5) % 2 == 0:
            self.player.draw(self.boost_timer > 0)
            
        # Draw HUD
        self.draw_hud()
        
        # Draw pause menu if paused
        if self.paused:
            self.draw_inventory()
            
        # Draw game over screen
        if self.game_over:
            self.draw_game_over()
            
    def draw_hud(self):
        # Draw semi-transparent background for HUD
        hud_surface = pygame.Surface((SCREEN_WIDTH, 100))
        hud_surface.set_alpha(180)
        hud_surface.fill(BLACK)
        screen.blit(hud_surface, (0, 0))
        
        # Draw hearts
        heart_x = 20
        for i in range(self.max_lives):
            if i < self.lives:
                if full_heart_img:
                    screen.blit(full_heart_img, (heart_x + i * 50, 15))
                else:
                    pygame.draw.circle(screen, RED, (heart_x + i * 40, 30), 15)
            else:
                if broken_heart_img:
                    screen.blit(broken_heart_img, (heart_x + i * 50, 15))
                else:
                    pygame.draw.circle(screen, GRAY, (heart_x + i * 40, 30), 15, 2)
                
        # Draw distance progress bar
        distance_percent = min(self.distance / GOAL_DISTANCE, 1.0)
        bar_width = 400
        bar_height = 30
        bar_x = SCREEN_WIDTH // 2 - bar_width // 2
        bar_y = 20
        
        pygame.draw.rect(screen, GRAY, (bar_x, bar_y, bar_width, bar_height))
        progress_color = YELLOW if self.boost_timer > 0 else GREEN
        pygame.draw.rect(screen, progress_color, 
                        (bar_x, bar_y, int(bar_width * distance_percent), bar_height))
        pygame.draw.rect(screen, WHITE, (bar_x, bar_y, bar_width, bar_height), 3)
        
        distance_text = f"{int(self.distance)}m / {GOAL_DISTANCE}m"
        draw_text(distance_text, font_small, WHITE, SCREEN_WIDTH // 2, bar_y + bar_height // 2)
        
        # Draw timer
        minutes = int(self.game_timer // 60)
        seconds = int(self.game_timer % 60)
        timer_text = f"Time: {minutes:02d}:{seconds:02d}"
        timer_color = RED if self.game_timer < 60 else WHITE
        draw_text_left(timer_text, font_small, timer_color, SCREEN_WIDTH - 200, 25)
        
        # Draw coin count with icon
        coin_x = 20
        coin_y = 70
        if coin_img:
            small_coin = pygame.transform.scale(coin_img, (30, 30))
            screen.blit(small_coin, (coin_x, coin_y - 5))
            draw_text_left(f"x {self.coin_count}", font_small, GOLD, coin_x + 35, coin_y)
        else:
            draw_text_left(f"Coins: {self.coin_count}", font_small, GOLD, coin_x, coin_y)
        
        # Draw inventory count
        monster_count = self.inventory.count("Monster Energy")
        bagel_count = self.inventory.count("Bagel")
        inv_text = f"M:{monster_count} B:{bagel_count} ({len(self.inventory)}/{MAX_INVENTORY_SIZE})"
        draw_text_left(inv_text, font_small, GREEN, 200, 70)
        
        # Draw boost status
        if self.boost_timer > 0:
            boost_text = f"BOOST! {self.boost_timer // 60 + 1}s"
            draw_text(boost_text, font_medium, ORANGE, SCREEN_WIDTH // 2, 70)
        else:
            draw_text_left("SPACE: Boost | TAB: Inventory", font_small, LIGHT_GRAY, 450, 70)
        
    def get_inventory_slot_rects(self):
        """Get the rectangles for each inventory slot for click detection"""
        inv_width = 700
        inv_height = 600
        inv_x = (SCREEN_WIDTH - inv_width) // 2
        inv_y = (SCREEN_HEIGHT - inv_height) // 2
        
        # Match Minecraft inventory layout from the image
        # Main inventory: 3 rows x 9 columns (27 slots)
        # Hotbar: 1 row x 9 columns (9 slots)
        # Total: 36 slots to match Minecraft, but we'll add 4 more for 40
        slot_rects = []
        slot_size = 64
        spacing = 8  # Space between slots
        
        # Main inventory grid (3 rows x 9 columns) = 27 slots
        main_grid_x = inv_x + 52
        main_grid_y = inv_y + 320
        
        for row in range(3):
            for col in range(9):
                x = main_grid_x + col * (slot_size + spacing)
                y = main_grid_y + row * (slot_size + spacing)
                slot_rects.append(pygame.Rect(x, y, slot_size, slot_size))
        
        # Hotbar (1 row x 9 columns) = 9 slots
        hotbar_y = inv_y + 525
        for col in range(9):
            x = main_grid_x + col * (slot_size + spacing)
            y = hotbar_y
            slot_rects.append(pygame.Rect(x, y, slot_size, slot_size))
        
        # Extra 4 slots to reach 40 (placed in top area)
        extra_slot_x = inv_x + 52
        extra_slot_y = inv_y + 80
        for col in range(4):
            x = extra_slot_x + col * (slot_size + spacing)
            y = extra_slot_y
            slot_rects.append(pygame.Rect(x, y, slot_size, slot_size))
        
        return slot_rects, inv_x, inv_y
    
    def draw_inventory(self):
        # Draw semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))
        
        inv_width = 700
        inv_height = 600
        inv_x = (SCREEN_WIDTH - inv_width) // 2
        inv_y = (SCREEN_HEIGHT - inv_height) // 2
        
        # Draw inventory background
        if minecraft_inv_img:
            screen.blit(minecraft_inv_img, (inv_x, inv_y))
        else:
            pygame.draw.rect(screen, (139, 87, 66), (inv_x, inv_y, inv_width, inv_height))
            pygame.draw.rect(screen, (50, 50, 50), (inv_x, inv_y, inv_width, inv_height), 5)
            draw_text("Inventory", font_large, WHITE, SCREEN_WIDTH // 2, inv_y + 30)
        
        # Get slot rectangles
        slot_rects, _, _ = self.get_inventory_slot_rects()
        
        # Draw inventory slots (only if not using background image)
        if not minecraft_inv_img:
            for slot in slot_rects:
                pygame.draw.rect(screen, DARK_GRAY, slot)
                pygame.draw.rect(screen, (150, 150, 150), slot, 2)
        
        # Draw items in inventory slots
        for i, item in enumerate(self.inventory[:MAX_INVENTORY_SIZE]):
            if i < len(slot_rects):
                slot = slot_rects[i]
                
                if item == "Monster Energy":
                    if monster_img:
                        img = pygame.transform.scale(monster_img, (45, 55))
                        img_rect = img.get_rect(center=slot.center)
                        screen.blit(img, img_rect)
                    else:
                        pygame.draw.rect(screen, GREEN, 
                                       (slot.centerx - 20, slot.centery - 25, 40, 50))
                        
                elif item == "Bagel":
                    if bagel_img:
                        img = pygame.transform.scale(bagel_img, (45, 45))
                        img_rect = img.get_rect(center=slot.center)
                        screen.blit(img, img_rect)
                    else:
                        pygame.draw.circle(screen, ORANGE, (slot.centerx, slot.centery), 20)
        
        # Instructions
        draw_text("Press TAB to close", font_medium, WHITE, 
                 SCREEN_WIDTH // 2, inv_y + inv_height + 40)
                 
    def draw_game_over(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(220)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))
        
        if self.victory:
            draw_text("VICTORY!", font_large, GREEN, SCREEN_WIDTH // 2, 200)
            draw_text(f"You reached {GOAL_DISTANCE}m!", font_medium, WHITE, 
                     SCREEN_WIDTH // 2, 270)
            minutes = int((GAME_TIME - self.game_timer) // 60)
            seconds = int((GAME_TIME - self.game_timer) % 60)
            draw_text(f"Time: {minutes:02d}:{seconds:02d}", font_medium, WHITE,
                     SCREEN_WIDTH // 2, 320)
        else:
            draw_text("GAME OVER", font_large, RED, SCREEN_WIDTH // 2, 200)
            if self.game_timer <= 0:
                draw_text("Time ran out!", font_medium, WHITE, SCREEN_WIDTH // 2, 270)
            else:
                draw_text("You ran out of lives!", font_medium, WHITE, SCREEN_WIDTH // 2, 270)
            draw_text(f"Distance: {int(self.distance)}m / {GOAL_DISTANCE}m", font_medium, WHITE,
                     SCREEN_WIDTH // 2, 320)
            
        draw_text(f"Final Score: {self.score}", font_medium, WHITE, 
                 SCREEN_WIDTH // 2, 400)
        draw_text(f"Coins Collected: {self.coin_count}", font_medium, GOLD,
                 SCREEN_WIDTH // 2, 450)
        monster_count = self.inventory.count("Monster Energy")
        bagel_count = self.inventory.count("Bagel")
        draw_text(f"Items: M:{monster_count} B:{bagel_count}", font_medium, GREEN,
                 SCREEN_WIDTH // 2, 500)
        draw_text("Press R to restart or ESC for menu", font_medium, WHITE,
                 SCREEN_WIDTH // 2, 580)

# -------------------- INSTRUCTIONS SCREEN --------------------
def show_instructions():
    running = True
    while running:
        screen.fill(BLACK)
        draw_text("Instructions:", font_large, WHITE, SCREEN_WIDTH // 2, 50)
        draw_text("GOAL: Reach 1000 meters before time runs out!", font_medium, YELLOW,
                 SCREEN_WIDTH // 2, 120)
        draw_text("Use LEFT/RIGHT arrow keys to switch lanes", font_small, WHITE, 
                 SCREEN_WIDTH // 2, 180)
        draw_text("Avoid students - they take away hearts!", font_small, RED,
                 SCREEN_WIDTH // 2, 220)
        draw_text("Collect coins for points! (Common)", font_small, GOLD,
                 SCREEN_WIDTH // 2, 260)
        draw_text("Collect Monster Energy for speed boost! (Rare)", font_small, GREEN,
                 SCREEN_WIDTH // 2, 300)
        draw_text("Collect Bagels to restore +1 HP! (Very Rare)", font_small, ORANGE,
                 SCREEN_WIDTH // 2, 340)
        draw_text("Press SPACE to use Monster for speed boost!", font_small, ORANGE,
                 SCREEN_WIDTH // 2, 380)
        draw_text("Press TAB to view inventory (pauses game)", font_small, WHITE,
                 SCREEN_WIDTH // 2, 420)
        draw_text("Click items in inventory to use them!", font_small, ORANGE,
                 SCREEN_WIDTH // 2, 460)
        draw_text("Max 40 items in inventory!", font_small, WHITE,
                 SCREEN_WIDTH // 2, 500)
        draw_text("Game gets harder over time!", font_small, RED,
                 SCREEN_WIDTH // 2, 540)
        draw_text("You have 20 minutes - don't run out of time!", font_small, WHITE,
                 SCREEN_WIDTH // 2, 580)
        draw_text("Click anywhere to return", font_medium, WHITE, 
                 SCREEN_WIDTH // 2, 650)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                running = False

# -------------------- CREDITS SCREEN --------------------
def show_credit():
    running = True
    while running:
        screen.fill(BLACK)
        draw_text("Credits:", font_large, WHITE, SCREEN_WIDTH // 2, 200)
        draw_text("Lead Designer & Coder: Chethan Krishan Battini", font_medium, 
                 WHITE, SCREEN_WIDTH // 2, 300)
        draw_text("Lead Programmer & Storyboard: William Arney", font_medium, 
                 WHITE, SCREEN_WIDTH // 2, 350)
        draw_text("Click anywhere to return", font_medium, WHITE, 
                 SCREEN_WIDTH // 2, 500)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                running = False

# -------------------- TITLE SCREEN --------------------
def title_screen():
    running = True
    while running:
        screen.fill(BLACK)

        draw_text("The Adventures of Mr.Landa", font_large, WHITE, 
                 SCREEN_WIDTH // 2, 200)

        start_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, 350, 200, 50)
        instructions_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, 425, 200, 50)
        credits_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, 500, 200, 50)

        pygame.draw.rect(screen, WHITE, start_button_rect)
        draw_text("Start Game", font_medium, BLACK, SCREEN_WIDTH // 2, 375)

        pygame.draw.rect(screen, WHITE, instructions_rect)
        draw_text("Instructions", font_medium, BLACK, SCREEN_WIDTH // 2, 450)

        pygame.draw.rect(screen, WHITE, credits_rect)
        draw_text("Credits", font_medium, BLACK, SCREEN_WIDTH // 2, 525)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_button_rect.collidepoint(event.pos):
                    running = False
                elif instructions_rect.collidepoint(event.pos):
                    show_instructions()
                elif credits_rect.collidepoint(event.pos):
                    show_credit()

# -------------------- MAIN GAME LOOP --------------------
def main_game():
    game = Game()
    running = True
    
    while running:
        clock.tick(60)  # 60 FPS
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            elif event.type == pygame.KEYDOWN:
                if game.game_over:
                    if event.key == pygame.K_r:
                        game = Game()  # Restart
                    elif event.key == pygame.K_ESCAPE:
                        return  # Back to menu
                else:
                    if event.key == pygame.K_LEFT:
                        game.player.move_left()
                    elif event.key == pygame.K_RIGHT:
                        game.player.move_right()
                    elif event.key == pygame.K_SPACE:
                        game.use_boost()
                    elif event.key == pygame.K_TAB:
                        game.paused = not game.paused
                    elif event.key == pygame.K_ESCAPE:
                        return  # Back to menu
            
            elif event.type == pygame.MOUSEBUTTONDOWN and game.paused:
                slot_rects, inv_x, inv_y = game.get_inventory_slot_rects()
                mouse_pos = event.pos

                for i, slot in enumerate(slot_rects):
                    if i < len(game.inventory) and slot.collidepoint(mouse_pos):
                        item = game.inventory[i]
                        
                        if item == "Monster Energy" and game.boost_timer == 0:
                            game.inventory.pop(i)
                            game.boost_timer = BOOST_DURATION
                            game.current_speed = BOOST_SPEED
                            if drink_sound:
                                drink_sound.play()
                            game.paused = False
                            break
                        elif item == "Bagel" and game.lives < game.max_lives:
                            game.inventory.pop(i)
                            game.lives += 1
                            if eat_sound:
                                eat_sound.play()
                            break
                        
        game.update()
        game.draw()
        pygame.display.flip()

# -------------------- MAIN --------------------
def main():
    print("\n" + "="*50)
    print("THE ADVENTURES OF MR.LANDA")
    print("="*50)
    print("\nGame Configuration:")
    print(f"  Goal Distance: {GOAL_DISTANCE}m")
    print(f"  Time Limit: {GAME_TIME//60} minutes")
    print(f"  Max Inventory: {MAX_INVENTORY_SIZE} items")
    print(f"  Spawn Rates: Students {STUDENT_SPAWN_CHANCE*100}%, Coins {COIN_SPAWN_CHANCE*100}%")
    print(f"               Monsters {MONSTER_SPAWN_CHANCE*100}%, Bagels {BAGEL_SPAWN_CHANCE*100}%")
    print("="*50 + "\n")
    while True:
        title_screen()
        main_game()

if __name__ == "__main__":
    main()