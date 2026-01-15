import sys
import random
import math
import pygame

pygame.init()

# -------------------- SCREEN SETUP --------------------
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("The Adventures of Mr.Landa")
clock = pygame.time.Clock()

# -------------------- LOAD IMAGES --------------------
def load_image(image_data, size=None):
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
except:
    background_img = None

# Load Level 2 room backgrounds
room_backgrounds = {}
room_positions = [
    (0, 0), (0, 1), (0, 2),
    (1, 0), (1, 1), (1, 2),
    (2, 0), (2, 1), (2, 2)
]

room_image_files = [
    "0.png", "1.png", "2.png",
    "3.png", "storage.png", "8.png",
    "7.png", "6.png", "5.png"
]

for i, (row, col) in enumerate(room_positions):
    try:
        room_img = pygame.image.load(room_image_files[i])
        room_img = pygame.transform.scale(room_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
        room_backgrounds[(row, col)] = room_img
    except:
        room_backgrounds[(row, col)] = background_img if background_img else None

# Load images
try:
    full_heart_img = pygame.image.load("Heart.png")
    full_heart_img = pygame.transform.scale(full_heart_img, (30, 30))
except:
    full_heart_img = None

try:
    broken_heart_img = pygame.image.load("Broken heart.png")
    broken_heart_img = pygame.transform.scale(broken_heart_img, (30, 30))
except:
    broken_heart_img = None

try:
    player_img = pygame.image.load("landa.png")
    player_img = pygame.transform.scale(player_img, (70, 90))
except:
    player_img = None

try:
    student_img = pygame.image.load("pngegg.png")
    student_img = pygame.transform.scale(student_img, (60, 80))
except:
    student_img = None

try:
    monster_img = pygame.image.load("monster.png")
    monster_img = pygame.transform.scale(monster_img, (40, 70))
except:
    monster_img = None

try:
    bagel_img = pygame.image.load("bagel.png")
    bagel_img = pygame.transform.scale(bagel_img, (50, 50))
except:
    bagel_img = None

try:
    coin_img = pygame.image.load("coin_icon.webp")
    coin_img = pygame.transform.scale(coin_img, (40, 40))
except:
    try:
        coin_img = pygame.image.load("coin_icon.png")
        coin_img = pygame.transform.scale(coin_img, (40, 40))
    except:
        coin_img = None

try:
    key_img = pygame.image.load("key.png")
    key_img = pygame.transform.scale(key_img, (20, 20))
except:
    key_img = None

minecraft_inv_img = None
inventory_files = ["minecraft_inventory.png", "minecraft_inventory.jpg", "inventory.jpg", "inventory.png"]
for filename in inventory_files:
    try:
        minecraft_inv_img = pygame.image.load(filename)
        minecraft_inv_img = pygame.transform.scale(minecraft_inv_img, (700, 600))
        break
    except:
        continue

try:
    blue_car_img = pygame.image.load("blue_car.png")
    blue_car_img = pygame.transform.scale(blue_car_img, (60, 120))
except:
    blue_car_img = None

try:
    red_car_img = pygame.image.load("red_car.png")
    red_car_img = pygame.transform.scale(red_car_img, (60, 120))
except:
    red_car_img = None

try:
    green_car_img = pygame.image.load("green_car.png")
    green_car_img = pygame.transform.scale(green_car_img, (60, 120))
except:
    green_car_img = None

try:
    police_car_img = pygame.image.load("police_car.png")
    police_car_img = pygame.transform.scale(police_car_img, (180, 360))
except:
    police_car_img = None

# -------------------- AUDIO SETUP --------------------
pygame.mixer.init()

try:
    pygame.mixer.music.load("background_music.mp3")
    pygame.mixer.music.set_volume(0.1)
    pygame.mixer.music.play(-1)
except:
    pass

drink_sound = None
try:
    drink_sound = pygame.mixer.Sound("drink.mp3")
    drink_sound.set_volume(0.4)
except:
    pass

eat_sound = None
try:
    eat_sound = pygame.mixer.Sound("eat.mp3")
    eat_sound.set_volume(0.4)
except:
    pass

pickup_sound = None
try:
    pickup_sound = pygame.mixer.Sound("pickup.mp3")
    pickup_sound.set_volume(0.3)
except:
    pass

coin_sound = None
try:
    coin_sound = pygame.mixer.Sound("coin.mp3")
    coin_sound.set_volume(0.3)
except:
    pass

# Load Level 3 highway background
try:
    highway_img = pygame.image.load("highway.png")
    highway_img = pygame.transform.scale(highway_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
except:
    highway_img = None
    pass

try:
    house_img = pygame.image.load("house.png")
    house_img = pygame.transform.scale(house_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
except:
    house_img = None
    pass

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

# -------------------- GAME CONSTANTS --------------------
LANE_WIDTH = SCREEN_WIDTH // 3
LANES = [LANE_WIDTH // 2, SCREEN_WIDTH // 2, SCREEN_WIDTH - LANE_WIDTH // 2]

LEVEL_1_TIME = 1200
LEVEL_1_DISTANCE = 1000

LEVEL_2_TIME = 900
LEVEL_2_DISTANCE = 1000 # NEED IT TO RUN THE GAME BUT NOT USED IN LEVEL 2 LOGIC
GRID_ROOMS = 3
ROOM_EDGE_THRESHOLD = 20

LEVEL_3_TIME = 1200
LEVEL_3_DISTANCE = 1000
MIN_SPEED_MPH = 20  # Changed from 25
MAX_SPEED_MPH = 25  # Changed from 30
SPEED_WARNING_TIME = 300  # 5 seconds

MAX_INVENTORY_SIZE = 40

BASE_SPEED = 5
BOOST_SPEED = 12
BOOST_DURATION = 180

INITIAL_SPAWN_RATE = 80
MIN_SPAWN_RATE = 25
SPAWN_RATE_DECREASE = 0.5

STUDENT_SPAWN_CHANCE = 0.55
COIN_SPAWN_CHANCE = 0.30
MONSTER_SPAWN_CHANCE = 0.10
BAGEL_SPAWN_CHANCE = 0.05

DODGE_POINTS = 10
MONSTER_POINTS = 50
BAGEL_POINTS = 75
COIN_VALUE = 1

MAX_LIVES = 3
INVINCIBILITY_FRAMES = 60

def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)

def draw_text_left(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

# -------------------- COLLISION BOX CLASS --------------------
class CollisionBox:
    def __init__(self, x, y, width, height, room_row, room_col):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.room_row = room_row
        self.room_col = room_col
        self.rect = pygame.Rect(x - width//2, y - height//2, width, height)
    
    def collides_with(self, player):
        px = player.x
        py = player.y
        pw = player.width
        ph = player.height
        
        return (abs(self.x - px) < (self.width + pw) // 2 and
                abs(self.y - py) < (self.height + ph) // 2)
    
    def draw_debug(self):
        pygame.draw.rect(screen, RED, self.rect, 2)

# -------------------- PLAYER CLASS --------------------
class Player:
    def __init__(self, level=1):
        self.level = level
        self.width = 70
        self.height = 90
        self.color = BLUE
        self.move_cooldown = 0
        self.image = player_img
        self.room_transition_cooldown = 0
        self.last_dir = "up"
        
        if level == 1:
            self.lane = 1
            self.x = LANES[self.lane]
            self.y = SCREEN_HEIGHT - 150
        elif level == 2:
            self.room_row = 1
            self.room_col = 1
            self.x = SCREEN_WIDTH // 2
            self.y = SCREEN_HEIGHT // 2
        else:  # Level 3
            self.lane = 1
            self.x = LANES[self.lane]
            self.y = SCREEN_HEIGHT - 150
            self.width = 60
            self.height = 120
            self.mph = 22.5  # Changed from 27.5
            self.image = blue_car_img  # Changed from green_car_img
        
    def move_left(self):
        if self.level == 1 or self.level == 3:
            if self.lane > 0 and self.move_cooldown == 0:
                self.lane -= 1
                self.move_cooldown = 10
                self.last_dir = "left"
        else:
            self.x -= 8
            self.last_dir = "left"
                
    def move_right(self):
        if self.level == 1 or self.level == 3:
            if self.lane < 2 and self.move_cooldown == 0:
                self.lane += 1
                self.move_cooldown = 10
                self.last_dir = "right"
        else:
            self.x += 8
            self.last_dir = "right"

    def move_up(self):
        if self.level == 2:
            self.y -= 8
            self.last_dir = "up"
        elif self.level == 3:
            self.mph += 1
            self.last_dir = "up"

    def move_down(self):
        if self.level == 2:
            self.y += 8
            self.last_dir = "down"
        elif self.level == 3:
            self.mph -= 1
            self.last_dir = "down"

            
    def update(self):
        if self.room_transition_cooldown > 0:
            self.room_transition_cooldown -= 1

        if self.level == 1 or self.level == 3:
            target_x = LANES[self.lane]
            if self.x < target_x:
                self.x = min(self.x + 15, target_x)
            elif self.x > target_x:
                self.x = max(self.x - 15, target_x)
            
        if self.move_cooldown > 0:
            self.move_cooldown -= 1
    
    def check_room_transition(self):
        if self.level != 2:
            return False

        if self.room_transition_cooldown > 0:
            return False

        transitioned = False

        if self.x >= SCREEN_WIDTH - ROOM_EDGE_THRESHOLD:
            self.room_col = (self.room_col + 1) % GRID_ROOMS
            self.x = ROOM_EDGE_THRESHOLD + 5
            transitioned = True
        elif self.x <= ROOM_EDGE_THRESHOLD:
            self.room_col = (self.room_col - 1) % GRID_ROOMS
            self.x = SCREEN_WIDTH - ROOM_EDGE_THRESHOLD - 5
            transitioned = True
        elif self.y >= SCREEN_HEIGHT - ROOM_EDGE_THRESHOLD:
            self.room_row = (self.room_row + 1) % GRID_ROOMS
            self.y = ROOM_EDGE_THRESHOLD + 5
            transitioned = True
        elif self.y <= ROOM_EDGE_THRESHOLD:
            self.room_row = (self.room_row - 1) % GRID_ROOMS
            self.y = SCREEN_HEIGHT - ROOM_EDGE_THRESHOLD - 5
            transitioned = True

        if transitioned:
            self.room_transition_cooldown = 10

        return transitioned
            
    def draw(self, boosted=False):
        if boosted:
            for i in range(3):
                pygame.draw.rect(screen, YELLOW, 
                    (self.x - self.width//2 - 10 + i*2, 
                    self.y - self.height//2 - 10 + i*2, 
                    self.width + 20 - i*4, 
                    self.height + 20 - i*4), 2)
        
        if self.image:
            # Rotate player car 180 degrees for Level 3
            if self.level == 3:
                rotated_img = pygame.transform.rotate(self.image, 180)
                img_rect = rotated_img.get_rect(center=(self.x, self.y))
                screen.blit(rotated_img, img_rect)
            else:
                img_rect = self.image.get_rect(center=(self.x, self.y))
                screen.blit(self.image, img_rect)
        else:
            pygame.draw.rect(screen, self.color, 
                            (self.x - self.width//2, self.y - self.height//2, 
                            self.width, self.height))

# -------------------- STUDENT CLASS --------------------
class Student:
    def __init__(self, lane, speed, level=1):
        self.lane = lane
        self.level = level
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
        if self.image:
            img_rect = self.image.get_rect(center=(self.x, self.y))
            screen.blit(self.image, img_rect)
        else:
            pygame.draw.rect(screen, self.color,
                            (self.x - self.width//2, self.y - self.height//2,
                             self.width, self.height))
        
    def is_off_screen(self):
        return self.y > SCREEN_HEIGHT + 100
        
    def collides_with(self, player):
        px = player.x
        py = player.y
        pw = player.width
        ph = player.height
        
        return (abs(self.x - px) < (self.width + pw) // 2 and
                abs(self.y - py) < (self.height + ph) // 2)

# -------------------- MONSTER CLASS --------------------
class Monster:
    def __init__(self, lane, speed, level=1):
        self.lane = lane
        self.level = level
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
        if self.image:
            img_rect = self.image.get_rect(center=(self.x, self.y))
            screen.blit(self.image, img_rect)
        else:
            pygame.draw.rect(screen, self.color,
                            (self.x - self.width//2, self.y - self.height//2,
                             self.width, self.height))
        
    def is_off_screen(self):
        return self.y > SCREEN_HEIGHT + 100
        
    def collides_with(self, player):
        px = player.x
        py = player.y
        pw = player.width
        ph = player.height
        
        return (abs(self.x - px) < (self.width + pw) // 2 and
                abs(self.y - py) < (self.height + ph) // 2)

# -------------------- BAGEL CLASS --------------------
class Bagel:
    def __init__(self, lane, speed, level=1):
        self.lane = lane
        self.level = level
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
        if self.image:
            img_rect = self.image.get_rect(center=(self.x, self.y))
            screen.blit(self.image, img_rect)
        else:
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), 25)
        
    def is_off_screen(self):
        return self.y > SCREEN_HEIGHT + 100
        
    def collides_with(self, player):
        px = player.x
        py = player.y
        pw = player.width
        ph = player.height
        
        return (abs(self.x - px) < (self.width + pw) // 2 and
                abs(self.y - py) < (self.height + ph) // 2)

# -------------------- COIN CLASS --------------------
class Coin:
    def __init__(self, lane, speed, level=1):
        self.lane = lane
        self.level = level
        self.x = LANES[lane]
        self.y = -100
        self.width = 40
        self.height = 40
        self.speed = speed
        self.color = GOLD
        self.image = coin_img
        self.rotation = 0
        
    def update(self):
        self.y += self.speed
        self.rotation = (self.rotation + 5) % 360
        
    def draw(self):
        if self.image:
            rotated_img = pygame.transform.rotate(self.image, self.rotation)
            img_rect = rotated_img.get_rect(center=(self.x, self.y))
            screen.blit(rotated_img, img_rect)
        else:
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), 20)
        
    def is_off_screen(self):
        return self.y > SCREEN_HEIGHT + 100
        
    def collides_with(self, player):
        px = player.x
        py = player.y
        pw = player.width
        ph = player.height
        
        return (abs(self.x - px) < (self.width + pw) // 2 and
                abs(self.y - py) < (self.height + ph) // 2)

# -------------------- TRAFFIC CAR CLASS (Level 3) --------------------
class TrafficCar:
    def __init__(self, lane, speed):
        self.lane = lane
        self.x = LANES[lane]
        self.y = -150
        self.width = 180
        self.height = 360
        self.hitbox_width = 90
        self.hitbox_height = 180
        self.speed = speed
        self.image = police_car_img
        self.color = BLUE
    
    def update(self):
        self.y += self.speed
    
    def draw(self):
        if self.image:
            # Rotate 180 degrees
            rotated_img = pygame.transform.rotate(self.image, 90)
            img_rect = rotated_img.get_rect(center=(self.x, self.y))
            screen.blit(rotated_img, img_rect)
        else:
            pygame.draw.rect(screen, self.color,
                           (self.x - self.width//2, self.y - self.height//2,
                            self.width, self.height))
    
    def is_off_screen(self):
        return self.y > SCREEN_HEIGHT + 150
    
    def collides_with(self, player):
        return (abs(self.x - player.x) < (self.hitbox_width + player.width) // 2 and
                abs(self.y - player.y) < (self.hitbox_height + player.height) // 2)
    
# -------------------- CAR CLASS --------------------
class Car:
    def __init__(self, x, y, color, car_type, room_row, room_col, reward_type, rotation=0):
        self.x = x
        self.y = y
        self.width = 60
        self.height = 120
        self.color = color
        self.car_type = car_type
        self.room_row = room_row
        self.room_col = room_col
        self.is_winning_car = False
        self.opened = False
        self.reward_type = reward_type
        self.rotation = rotation  # 0, 90, 180, or 270
        
        if car_type == "blue":
            self.image = blue_car_img
        elif car_type == "red":
            self.image = red_car_img
        elif car_type == "green":
            self.image = green_car_img
        else:
            self.image = None
    
    def draw(self):
        if self.image:
            if self.rotation != 0:
                rotated_img = pygame.transform.rotate(self.image, self.rotation)
                img_rect = rotated_img.get_rect(center=(self.x, self.y))
                screen.blit(rotated_img, img_rect)
            else:
                img_rect = self.image.get_rect(center=(self.x, self.y))
                screen.blit(self.image, img_rect)
        else:
            pygame.draw.rect(screen, self.color,
                           (self.x - self.width//2, self.y - self.height//2,
                            self.width, self.height))
    
    def collides_with(self, player):
        px = player.x
        py = player.y
        pw = player.width
        ph = player.height
        
        return (abs(self.x - px) < (self.width + pw) // 2 and
                abs(self.y - py) < (self.height + ph) // 2)
    
    def clicked(self, mouse_pos):
        mx, my = mouse_pos
        return (abs(self.x - mx) < self.width // 2 and
                abs(self.y - my) < self.height // 2)

# -------------------- POLICE CAR CLASS --------------------
class PoliceCar:
    def __init__(self, path_points, speed=3, room_row=0, room_col=0, start_wait=0):
        self.path_points = path_points
        self.current_point = 0
        self.x = path_points[0][0]
        self.y = path_points[0][1]
        self.room_row = room_row
        self.room_col = room_col
        self.width = 180
        self.height = 360
        self.hitbox_width = 90
        self.hitbox_height = 180
        self.speed = speed
        self.image = police_car_img
        self.wait_timer = start_wait
        self.is_waiting = False
        
    def update(self):
        if self.is_waiting:
            self.wait_timer -= 1
            if self.wait_timer <= 0:
                self.is_waiting = False
                self.current_point = 0
                self.x = self.path_points[0][0]
                self.y = self.path_points[0][1]
                self.room_row = self.path_points[0][2]
                self.room_col = self.path_points[0][3]
            return
        
        target_x, target_y, target_room_row, target_room_col, action = self.path_points[self.current_point]
        
        dx = target_x - self.x
        dy = target_y - self.y
        dist = math.sqrt(dx*dx + dy*dy)
        
        if dist < self.speed:
            self.current_point += 1
            
            if self.current_point >= len(self.path_points):
                self.is_waiting = True
                self.wait_timer = 120
            else:
                _, _, self.room_row, self.room_col, _ = self.path_points[self.current_point]
        else:
            self.x += (dx / dist) * self.speed
            self.y += (dy / dist) * self.speed
    
    def draw(self):
        if self.image:
            img_rect = self.image.get_rect(center=(int(self.x), int(self.y)))
            screen.blit(self.image, img_rect)
        else:
            pygame.draw.rect(screen, (0, 0, 255),
                           (int(self.x) - self.width//2, int(self.y) - self.height//2,
                            self.width, self.height))
    
    def collides_with(self, player):
        px = player.x
        py = player.y
        pw = player.width
        ph = player.height
        
        return (abs(self.x - px) < (self.hitbox_width + pw) // 2 and
                abs(self.y - py) < (self.hitbox_height + ph) // 2)
    
# -------------------- SHOP CLASS (Level 3) --------------------
class Shop3:
    def __init__(self, game):
        self.game = game
        self.running = True
        # Define items in the shop
        self.items = [
            {"name": "Monster Energy", "price": 10, "image": monster_img},
            {"name": "Bagel", "price": 5, "image": bagel_img},
            {"name": "Shield", "price": 15, "image": None},
        ]
        self.buttons = []
        self.font = pygame.font.SysFont(None, 36)
        self.create_buttons()

    def create_buttons(self):
        start_x = SCREEN_WIDTH // 2 - 150
        start_y = 250
        spacing_y = 120
        button_width = 300
        button_height = 80

        self.buttons.clear()
        for i, item in enumerate(self.items):
            rect = pygame.Rect(start_x, start_y + i * spacing_y, button_width, button_height)
            self.buttons.append((rect, item))

    def run(self):
        shop_clock = pygame.time.Clock()
        while self.running:
            shop_clock.tick(60)
            self.handle_events()
            self.draw()
            pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for rect, item in self.buttons:
                    if rect.collidepoint(event.pos):
                        self.buy_item(item)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_TAB or event.key == pygame.K_s:
                    self.running = False

    def buy_item(self, item):
        if self.game.coin_count >= item["price"]:
            if len(self.game.inventory) < MAX_INVENTORY_SIZE:
                self.game.coin_count -= item["price"]
                self.apply_item(item)
                if pickup_sound:
                    pickup_sound.play()
            else:
                print("Inventory full!")
        else:
            print("Not enough coins!")

    def apply_item(self, item):
        # Monster Energy goes to inventory
        if item["name"] == "Monster Energy":
            self.game.inventory.append("Monster Energy")
            print("Monster Energy added to inventory!")

        # Bagel restores health and adds to inventory
        elif item["name"] == "Bagel":
            if self.game.lives < self.game.max_lives:
                self.game.lives += 1
            self.game.inventory.append("Bagel")
            print("Bagel added to inventory!")

        # Shield gives blue aura around the player
        elif item["name"] == "Shield":
            self.game.shield_active = True
            self.game.shield_timer = 10 * 60  # lasts 10 seconds
            print("Shield activated!")

    def draw(self):
        screen.fill(DARK_GRAY)
        draw_text("Level 3 Shop", font_large, GOLD, SCREEN_WIDTH // 2, 100)
        draw_text(f"Coins: {self.game.coin_count}", font_medium, GOLD, SCREEN_WIDTH // 2, 180)
        draw_text("Press ESC, TAB, or S to close", font_small, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50)
        
        for rect, item in self.buttons:
            pygame.draw.rect(screen, WHITE, rect)
            pygame.draw.rect(screen, BLACK, rect, 3)
            
            # Draw item image
            if item["image"]:
                img = pygame.transform.scale(item["image"], (60, 60))
                img_rect = img.get_rect(center=(rect.x + 60, rect.centery))
                screen.blit(img, img_rect)

            # Draw item name and price
            draw_text(item["name"], self.font, BLACK, rect.centerx + 50, rect.centery - 15)
            draw_text(f"{item['price']} coins", self.font, BLACK, rect.centerx + 50, rect.centery + 20)

# -------------------- PLAYER DRAWING WITH SHIELD --------------------
# Inside your Game.draw() or Player.draw() function
def draw_player_with_shield(self):
    # Draw shield aura if active
    if getattr(self.game, "shield_active", False) and self.game.shield_timer > 0:
        pygame.draw.circle(screen, (0, 0, 255), (int(self.x), int(self.y)), max(self.width, self.height), 5)
        self.game.shield_timer -= 1
        if self.game.shield_timer <= 0:
            self.game.shield_active = False

    # Draw normal player
    self.draw(self.boost_timer > 0)

# -------------------- KEY CLASS --------------------
class Key:
    def __init__(self, x, y, room_row, room_col):
        self.x = x
        self.y = y
        self.width = 12
        self.height = 12
        self.room_row = room_row
        self.room_col = room_col
        self.collected = False
        self.image = key_img

    def draw(self):
        if not self.collected:
            if self.image:
                tiny_key = pygame.transform.scale(self.image, (12, 12))
                img_rect = tiny_key.get_rect(center=(self.x, self.y))
                screen.blit(tiny_key, img_rect)
            else:
                pygame.draw.circle(screen, GOLD, (int(self.x), int(self.y)), 5)

    def clicked(self, mouse_pos):
        if self.collected:
            return False
        mx, my = mouse_pos
        return math.sqrt((self.x - mx)**2 + (self.y - my)**2) < 15

# -------------------- GAME CLASS --------------------
class Game:
    def __init__(self, level=1, player_state=None):
        self.level = level
        self.player = Player(level)
        self.students = []
        self.monsters = []
        self.bagels = []
        self.coins = []
        
        # Load player state if provided, otherwise use defaults
        if player_state:
            self.lives = player_state.get('lives', MAX_LIVES)
            self.max_lives = player_state.get('max_lives', MAX_LIVES)
            self.inventory = player_state.get('inventory', []).copy()
            self.coin_count = player_state.get('coin_count', 0)
        else:
            self.lives = MAX_LIVES
            self.max_lives = MAX_LIVES
            self.inventory = []
            self.coin_count = 0

        self.score = 0
        self.spawn_timer = 0
        self.spawn_rate = INITIAL_SPAWN_RATE
        
        if level == 1:
            self.game_timer = LEVEL_1_TIME
            self.goal_distance = LEVEL_1_DISTANCE
        elif level == 2:
            self.game_timer = LEVEL_2_TIME
            self.goal_distance = LEVEL_2_DISTANCE
        else:  # Level 3
            self.game_timer = LEVEL_3_TIME
            self.goal_distance = LEVEL_3_DISTANCE
            
        self.start_ticks = pygame.time.get_ticks()
        self.paused = False
        self.invincible_timer = 0
        self.game_over = False
        self.victory = False
        self.distance = 0
        self.current_speed = BASE_SPEED
        self.boost_timer = 0
        self.scroll_offset = 0
        # Shield for Level 3
        self.shield_active = False
        self.shield_timer = 0
        
        # Difficulty progression
        self.difficulty_checkpoints = [250, 500, 750]
        self.difficulty_level = 0
        
        # Level 2 specific
        self.cars = []
        self.police_cars = []
        self.collision_boxes = []
        self.key = None
        self.has_key = False
        self.message = ""
        self.message_timer = 0
        
        # Level 3 specific
        self.traffic_cars = []
        self.speed_warning_timer = 0
        self.out_of_range = False
        
        if level == 2:
            self.setup_level2()
        
    def setup_level2(self):
        storage_boxes = [
            CollisionBox(350, 150, 400, 80, 1, 1),
            CollisionBox(350, 500, 400, 200, 1, 1),
            CollisionBox(100, 200, 80, 200, 1, 1),
            CollisionBox(750, 250, 150, 300, 1, 1),
        ]
        self.collision_boxes.extend(storage_boxes)
        
        # Create parked cars with rewards and rotations
        car_positions = [
            # Top row parking (room [0,1]) - horizontal (90 degrees)
            (250, 350, "blue", 0, 1, "monster", 0),
            (425, 350, "red", 0, 1, "bagel", 0),
            (575, 350, "green", 0, 1, "monster", 0),
            (750, 350, "blue", 0, 1, "bagel", 0),
            
            # Right side parking (room [1,2]) - vertical (0 degrees)
            (550, 190, "red", 1, 2, "bagel", 90),
            (550, 330, "green", 1, 2, "monster", 90),
            (550, 475, "blue", 1, 2, "bagel", 90),
            (550, 610, "green", 1, 2, "monster", 90),
            
            # Bottom parking (room [2,1]) - horizontal (0 degrees)
            (250, 450, "green", 2, 1, "monster", 0),
            (425, 450, "red", 2, 1, "bagel", 0),
            (600, 450, "blue", 2, 1, "monster", 0),
            (750, 450, "red", 2, 1, "bagel", 0),
            
            # Left side parking (room [1,0]) - vertical (90 degrees)
            (450, 200, "blue", 1, 0, "bagel", 90),
            (450, 335, "green", 1, 0, "monster", 90),
            (450, 475, "blue", 1, 0, "bagel", 90),
            (450, 625, "green", 1, 0, "monster", 90),

            # Room [0,0] - mixed orientations
            (400, 250, "blue", 0, 0, "bagel", 0),
            (575, 250, "green", 0, 0, "monster", 0),
            (735, 250, "blue", 0, 0, "bagel", 0),
            (275, 465, "green", 0, 0, "monster", 90),
            (275, 615, "blue", 0, 0, "bagel", 90),

            # Room [0,2] - mixed orientations
            (275, 225, "blue", 0, 2, "bagel", 0),
            (415, 225, "green", 0, 2, "monster", 0),
            (700, 325, "blue", 0, 2, "bagel", 90),
            (700, 465, "green", 0, 2, "monster", 90),
            (700, 600, "blue", 0, 2, "bagel", 270),

            # Room [2,0] - mixed orientations
            (350, 200, "blue", 2, 0, "bagel", 90),
            (350, 335, "green", 2, 0, "monster", 90),
            (350, 475, "blue", 2, 0, "bagel", 90),
            (600, 575, "green", 2, 0, "monster", 180),
            (750, 575, "blue", 2, 0, "bagel", 180),

            # Room [2,2] - mixed orientations
            (725, 200, "blue", 2, 2, "bagel", 90),
            (725, 325, "green", 2, 2, "monster", 90),
            (275, 550, "blue", 2, 2, "bagel", 0),
            (425, 550, "green", 2, 2, "monster", 0),
            (575, 550, "blue", 2, 2, "bagel", 0),
        ]
        
        for x, y, car_type, row, col, reward, rotation in car_positions:
            color_map = {"blue": BLUE, "red": RED, "green": GREEN}
            car = Car(x, y, color_map[car_type], car_type, row, col, reward, rotation)
            self.cars.append(car)
        
        # One random car is the winning car
        winning_car = random.choice(self.cars)
        winning_car.is_winning_car = True
        
        # Place key in center room (1,1)
        self.key = Key(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 1, 1)
        
        # Create police cars for each room with specific patrol patterns
        
        # Room [0,0] - Top-left
        police_00 = PoliceCar([
            (SCREEN_WIDTH + 100, 425, 0, 0, "right"),
            (SCREEN_WIDTH // 2, 425, 0, 0, "right"),
            (SCREEN_WIDTH // 2, SCREEN_HEIGHT + 100, 0, 0, "down"),
        ], speed=5, room_row=0, room_col=0, start_wait=0)
        self.police_cars.append(police_00)
        
        # Room [0,1] - Top-middle
        police_01 = PoliceCar([
            (SCREEN_WIDTH + 100, 525, 0, 1, "left"),
            (-100, 525, 0, 1, "left"),
        ], speed=6, room_row=0, room_col=1, start_wait=60)
        self.police_cars.append(police_01)
        
        # Room [0,2] - Top-right
        police_02 = PoliceCar([
            (450, SCREEN_HEIGHT - 10, 0, 2, "up"),
            (450, SCREEN_HEIGHT // 2, 0, 2, "up"),
            (-100, SCREEN_HEIGHT // 2, 0, 2, "left"),
        ], speed=5, room_row=0, room_col=2, start_wait=90)
        self.police_cars.append(police_02)
        
        # Room [1,0] - Middle-left
        police_10 = PoliceCar([
            (650, -100, 1, 0, "down"),
            (650, SCREEN_HEIGHT + 100, 1, 0, "down"),
        ], speed=6, room_row=1, room_col=0, start_wait=30)
        self.police_cars.append(police_10)
        
        # Room [1,2] - Middle-right
        police_12 = PoliceCar([
            (350, SCREEN_HEIGHT + 100, 1, 2, "up"),
            (350, -100, 1, 2, "up"),
        ], speed=6, room_row=1, room_col=2, start_wait=150)
        self.police_cars.append(police_12)
        
        # Room [2,0] - Bottom-left
        police_20 = PoliceCar([
            (550, -100, 2, 0, "up"),
            (550, SCREEN_HEIGHT // 2, 2, 0, "up"),
            (1100, SCREEN_HEIGHT // 2, 2, 0, "left"),
        ], speed=5, room_row=2, room_col=0, start_wait=180)
        self.police_cars.append(police_20)
        
        # Room [2,1] - Bottom-middle
        police_21 = PoliceCar([
            (-100, 300, 2, 1, "right"),
            (SCREEN_WIDTH + 100, 300, 2, 1, "right"),
        ], speed=6, room_row=2, room_col=1, start_wait=0)
        self.police_cars.append(police_21)
        
        # Room [2,2] - Bottom-right
        police_22 = PoliceCar([
            (-100, 375, 2, 2, "right"),
            (SCREEN_WIDTH // 2, 375, 2, 2, "right"),
            (SCREEN_WIDTH // 2, -100, 2, 2, "down"),
        ], speed=5, room_row=2, room_col=2, start_wait=210)
        self.police_cars.append(police_22)
    
    def show_message(self, text, duration=120):
        self.message = text
        self.message_timer = duration
    
    def use_boost(self):
        if self.boost_timer > 0:
            return  # Already boosting

        # Check if player has Monster Energy
        if "Monster Energy" not in self.inventory:
            self.show_message("No Monster Energy!", 60)
            return

        # Remove Monster Energy from inventory
        self.inventory.remove("Monster Energy")

        # Level 1 – lane speed boost
        if self.level == 1:
            self.boost_timer = BOOST_DURATION
            self.current_speed = BOOST_SPEED
            self.show_message("BOOST!", 60)
            if drink_sound:
                drink_sound.play()

        # Level 2 – dash forward
        elif self.level == 2:
            dash_dist = 200
            if self.player.last_dir == "up":
                self.player.y -= dash_dist
            elif self.player.last_dir == "down":
                self.player.y += dash_dist
            elif self.player.last_dir == "left":
                self.player.x -= dash_dist
            elif self.player.last_dir == "right":
                self.player.x += dash_dist

            self.show_message("DASH!", 45)
            if drink_sound:
                drink_sound.play()

        # Level 3 – lane boost
        elif self.level == 3:
            self.boost_timer = BOOST_DURATION
            self.current_speed = BOOST_SPEED
            self.show_message("BOOST!", 60)
            if drink_sound:
                drink_sound.play()
    
    def use_bagel(self):
        if "Bagel" not in self.inventory:
            print("No bagel to use")
            return

        if self.lives >= self.max_lives:
            self.show_message("Health already full!", 60)
            return

        # Use bagel
        self.inventory.remove("Bagel")
        self.lives += 1

        self.show_message("+1 Health!", 90)

        if pickup_sound:
            pickup_sound.play()
        if eat_sound:
            eat_sound.play()

        print(f"Bagel used — lives now {self.lives}")

            
    def spawn_obstacle(self):
        if self.level == 2:
            return

        lane = random.randint(0, 2)

        if self.level == 3:
            # Progress-based difficulty
            progress = min(self.distance / self.goal_distance, 1.0)

            # Dynamic spawn chances based on progress (0.0 → start, 1.0 → end)
            traffic_chance = 0.4 + 0.3 * progress   # 40% → 70%
            coin_chance    = 0.35 + 0.7 * progress  # 35% → 15%
            monster_chance = 0.15 + 0.3 * progress  # 15% → 25%
            bagel_chance   = 0.1  + 0.5 * progress # 10% → 5%

            rand = random.random()
            if rand < traffic_chance:
                self.traffic_cars.append(TrafficCar(lane, self.current_speed))
            elif rand < traffic_chance + coin_chance:
                self.coins.append(Coin(lane, self.current_speed, self.level))
            elif rand < traffic_chance + coin_chance + monster_chance:
                self.monsters.append(Monster(lane, self.current_speed, self.level))
            else:
                self.bagels.append(Bagel(lane, self.current_speed, self.level))
            return
        else:
            # Level 1: Original spawning
            rand = random.random()
            if rand < STUDENT_SPAWN_CHANCE:
                self.students.append(Student(lane, self.current_speed, self.level))
            elif rand < STUDENT_SPAWN_CHANCE + COIN_SPAWN_CHANCE:
                self.coins.append(Coin(lane, self.current_speed, self.level))
            elif rand < STUDENT_SPAWN_CHANCE + COIN_SPAWN_CHANCE + MONSTER_SPAWN_CHANCE:
                self.monsters.append(Monster(lane, self.current_speed, self.level))
            else:
                self.bagels.append(Bagel(lane, self.current_speed, self.level))
                
    def update(self):
        if self.paused or self.game_over:
            return
            
        elapsed = (pygame.time.get_ticks() - self.start_ticks) / 1000
        if self.level == 1:
            self.game_timer = max(0, LEVEL_1_TIME - elapsed)
        elif self.level == 2:
            self.game_timer = max(0, LEVEL_2_TIME - elapsed)
        else:
            self.game_timer = max(0, LEVEL_3_TIME - elapsed)
                
        if self.game_timer <= 0:
            self.game_over = True
            self.victory = False
            return
        
        # Level 3 speed monitoring
        if self.level == 3:
            # Speed can go as high as player wants
            self.player.mph -= 0.01  # slowly decreases over time
            # don't clamp to MAX_SPEED_MPH
            
            # Check if MPH is outside target range 20-25
            if self.player.mph < 20 or self.player.mph > 25:
                if not self.out_of_range:
                    self.out_of_range = True
                    self.speed_warning_timer = 5 * 60  # 5 seconds in frames
                else:
                    self.speed_warning_timer -= 1
                    if self.speed_warning_timer <= 0:
                        self.lives -= 1
                        self.invincible_timer = INVINCIBILITY_FRAMES
                        self.out_of_range = False
                        self.speed_warning_timer = 0
                        self.show_message("Speed violation! Lost a life!", 90)
                        if self.lives <= 0:
                            self.game_over = True
                            self.victory = False
            else:
                self.out_of_range = False
                self.speed_warning_timer = 0
        
        if self.level == 3 and self.boost_timer > 0:
            self.boost_timer -= 1
            if self.boost_timer == 0:
                # Clamp back to safe range
                self.player.mph = max(20, min(25, self.player.mph))


        # Update difficulty (replaces ration degrees)
        if self.level == 1 and self.difficulty_level < len(self.difficulty_checkpoints):
            if self.distance >= self.difficulty_checkpoints[self.difficulty_level]:
                self.difficulty_level += 1
                if self.spawn_rate > MIN_SPAWN_RATE:
                    self.spawn_rate = max(MIN_SPAWN_RATE, self.spawn_rate - 10)
                self.current_speed = min(self.current_speed + 1, BOOST_SPEED - 2)
            
        if self.boost_timer > 0:
            self.boost_timer -= 1
            if self.boost_timer == 0:
                self.current_speed = BASE_SPEED
                
        distance_gain = self.current_speed / 60.0
        self.distance += distance_gain
        
        if self.level == 1 or self.level == 3:
            self.scroll_offset += self.current_speed
            if self.scroll_offset >= 100:
                self.scroll_offset = 0
        
        if self.distance >= self.goal_distance:
            self.victory = True
            self.game_over = True
            return
            
        self.player.update()
        
        if self.level == 2:
            if self.player.check_room_transition():
                pass
            
            # Check collision with obstacles
            for box in self.collision_boxes:
                if box.room_row == self.player.room_row and box.room_col == self.player.room_col:
                    if box.collides_with(self.player):
                        # Push player back
                        if self.player.x < box.x:
                            self.player.x = box.x - (box.width + self.player.width) // 2 - 2
                        else:
                            self.player.x = box.x + (box.width + self.player.width) // 2 + 2
                        
                        if self.player.y < box.y:
                            self.player.y = box.y - (box.height + self.player.height) // 2 - 2
                        else:
                            self.player.y = box.y + (box.height + self.player.height) // 2 + 2
            
        if self.level == 2:
            for police in self.police_cars:
                if police.room_row == self.player.room_row and police.room_col == self.player.room_col:
                    police.update()  # Move the police car along its patrol
                    if police.collides_with(self.player) and self.invincible_timer == 0:
                        self.lives -= 1
                        self.invincible_timer = INVINCIBILITY_FRAMES
                        self.show_message("Hit by police car!", 90)
                        if self.lives <= 0:
                            self.game_over = True
                            self.victory = False

        # Update Level 3 traffic cars
        if self.level == 3:
            for traffic_car in self.traffic_cars[:]:
                traffic_car.update()
                if traffic_car.is_off_screen():
                    self.traffic_cars.remove(traffic_car)
                elif traffic_car.collides_with(self.player) and self.invincible_timer == 0:
                    self.traffic_cars.remove(traffic_car)
                    self.lives -= 1
                    self.invincible_timer = INVINCIBILITY_FRAMES
                    self.show_message("Hit by police car!", 90)
                    if self.lives <= 0:
                        self.game_over = True
                        self.victory = False
            
            # Check car collisions
            for car in self.cars:
                if car.room_row == self.player.room_row and car.room_col == self.player.room_col:
                    if car.collides_with(self.player):
                        # Push player back
                        if self.player.x < car.x:
                            self.player.x = car.x - (car.width + self.player.width) // 2 - 2
                        else:
                            self.player.x = car.x + (car.width + self.player.width) // 2 + 2
                        
                        if self.player.y < car.y:
                            self.player.y = car.y - (car.height + self.player.height) // 2 - 2
                        else:
                            self.player.y = car.y + (car.height + self.player.height) // 2 + 2
        
        if self.invincible_timer > 0:
            self.invincible_timer -= 1
        
        if self.message_timer > 0:
            self.message_timer -= 1
        
        if self.level == 1 or self.level == 3:
            self.spawn_timer += 1
            if self.spawn_timer >= self.spawn_rate:
                self.spawn_obstacle()
                self.spawn_timer = 0
                if self.spawn_rate > MIN_SPAWN_RATE:
                    self.spawn_rate = max(MIN_SPAWN_RATE, self.spawn_rate - SPAWN_RATE_DECREASE)
                
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
                    
            for monster in self.monsters[:]:
                monster.speed = self.current_speed
                monster.update()
                if monster.is_off_screen():
                    self.monsters.remove(monster)
                elif monster.collides_with(self.player):
                    self.monsters.remove(monster)
                    if len(self.inventory) < MAX_INVENTORY_SIZE:
                        self.inventory.append("Monster Energy")
                    self.score += MONSTER_POINTS
                    if pickup_sound:
                        pickup_sound.play()
                
            for bagel in self.bagels[:]:
                bagel.speed = self.current_speed
                bagel.update()
                if bagel.is_off_screen():
                    self.bagels.remove(bagel)
                elif bagel.collides_with(self.player):
                    self.bagels.remove(bagel)
                    if len(self.inventory) < MAX_INVENTORY_SIZE:
                        self.inventory.append("Bagel")
                    self.score += BAGEL_POINTS
                    if pickup_sound:
                        pickup_sound.play()
        
            for coin in self.coins[:]:
                coin.speed = self.current_speed
                coin.update()
                if coin.is_off_screen():
                    self.coins.remove(coin)
                elif coin.collides_with(self.player):
                    self.coins.remove(coin)
                    self.coin_count += COIN_VALUE
                    self.score += COIN_VALUE * 5
                    if coin_sound:
                        coin_sound.play()
                
    def draw(self):
        if background_img and self.level == 1:
            y_offset = self.scroll_offset % SCREEN_HEIGHT
            screen.blit(background_img, (0, y_offset))
            screen.blit(background_img, (0, y_offset - SCREEN_HEIGHT))
        elif self.level == 3 and highway_img:
            y_offset = self.scroll_offset % SCREEN_HEIGHT
            screen.blit(highway_img, (0, y_offset))
            screen.blit(highway_img, (0, y_offset - SCREEN_HEIGHT))
        elif self.level == 2:
            current_room = (self.player.room_row, self.player.room_col)
            room_bg = room_backgrounds.get(current_room)
            
            if room_bg:
                screen.blit(room_bg, (0, 0))
            else:
                screen.fill(DARK_GRAY)
        else:
            screen.fill(BLACK)
            
            if self.level == 1:
                for i in range(4):
                    x = i * LANE_WIDTH
                    pygame.draw.line(screen, GRAY, (x, 0), (x, SCREEN_HEIGHT), 2)
                    
                for y in range(-20, SCREEN_HEIGHT + 100, 100):
                    for i in range(1, 3):
                        x = i * LANE_WIDTH
                        marker_y = (y + self.scroll_offset) % SCREEN_HEIGHT
                        pygame.draw.rect(screen, WHITE, (x - 5, marker_y, 10, 40))
        
        if self.level == 2:
            minimap_size = 120
            minimap_x = SCREEN_WIDTH - minimap_size - 20
            minimap_y = 120
            cell_size = minimap_size // GRID_ROOMS
            
            room_labels = [
                ["[0,0]", "[0,1]", "[0,2]"],
                ["[1,0]", "[1,1]", "[1,2]"],
                ["[2,0]", "[2,1]", "[2,2]"]
            ]
            
            for row in range(GRID_ROOMS):
                for col in range(GRID_ROOMS):
                    x = minimap_x + col * cell_size
                    y = minimap_y + row * cell_size
                    if row == self.player.room_row and col == self.player.room_col:
                        pygame.draw.rect(screen, GREEN, (x, y, cell_size, cell_size))
                    else:
                        pygame.draw.rect(screen, GRAY, (x, y, cell_size, cell_size))
                    pygame.draw.rect(screen, WHITE, (x, y, cell_size, cell_size), 1)
                    
                    label_font = pygame.font.SysFont(None, 18)
                    label = room_labels[row][col]
                    draw_text(label, label_font, BLACK if row == self.player.room_row and col == self.player.room_col else WHITE, 
                             x + cell_size // 2, y + cell_size // 2)
            
            for car in self.cars:
                if car.room_row == self.player.room_row and car.room_col == self.player.room_col:
                    car.draw()
            
            for police in self.police_cars:
                if police.room_row == self.player.room_row and police.room_col == self.player.room_col:
                    police.draw()
            
            if self.key and self.key.room_row == self.player.room_row and self.key.room_col == self.player.room_col:
                self.key.draw()
        
        if self.level == 1:
            for student in self.students:
                student.draw()
                
            for monster in self.monsters:
                monster.draw()
                
            for bagel in self.bagels:
                bagel.draw()
            
            for coin in self.coins:
                coin.draw()
    
        # Level 3 drawing
        if self.level == 3:
            for traffic_car in self.traffic_cars:
                traffic_car.draw()
                
            for monster in self.monsters:
                monster.draw()
                
            for bagel in self.bagels:
                bagel.draw()
            
            for coin in self.coins:
                coin.draw()

            
        if self.invincible_timer == 0 or (self.invincible_timer // 5) % 2 == 0:
            self.player.draw(self.boost_timer > 0)
            
        self.draw_hud()
        
        if self.message_timer > 0:
            overlay = pygame.Surface((600, 100))
            overlay.set_alpha(200)
            overlay.fill(BLACK)
            screen.blit(overlay, (SCREEN_WIDTH // 2 - 300, SCREEN_HEIGHT // 2 - 50))
            draw_text(self.message, font_medium, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        
        if self.paused:
            self.draw_inventory()
            
        if self.game_over:
            self.draw_game_over()
            
    def draw_hud(self):
        hud_surface = pygame.Surface((SCREEN_WIDTH, 100))
        hud_surface.set_alpha(180)
        hud_surface.fill(BLACK)
        screen.blit(hud_surface, (0, 0))
        
        level_text = f"LEVEL {self.level}"
        if self.level == 1:
            level_color = GREEN
        elif self.level == 3:
            level_color = BLUE
        else:
            level_color = ORANGE
        draw_text_left(level_text, font_medium, level_color, 20, 10)
        
        heart_x = 180
        for i in range(self.max_lives):
            if i < self.lives:
                if full_heart_img:
                    screen.blit(full_heart_img, (heart_x + i * 40, 20))
                else:
                    pygame.draw.circle(screen, RED, (heart_x + i * 35, 30), 12)
            else:
                if broken_heart_img:
                    screen.blit(broken_heart_img, (heart_x + i * 40, 20))
                else:
                    pygame.draw.circle(screen, GRAY, (heart_x + i * 35, 30), 12, 2)
        
        minutes = int(self.game_timer // 60)
        seconds = int(self.game_timer % 60)
        timer_text = f"Time: {minutes:02d}:{seconds:02d}"
        timer_color = RED if self.game_timer < 60 else WHITE
        draw_text_left(timer_text, font_small, timer_color, SCREEN_WIDTH - 200, 25)
        
        coin_x = 20
        coin_y = 70
        if coin_img:
            small_coin = pygame.transform.scale(coin_img, (30, 30))
            screen.blit(small_coin, (coin_x, coin_y - 5))
            draw_text_left(f"x {self.coin_count}", font_small, GOLD, coin_x + 35, coin_y)
        else:
            draw_text_left(f"Coins: {self.coin_count}", font_small, GOLD, coin_x, coin_y)
        
        # Progress bar for Level 1 and 3
        if self.level == 1 or self.level == 3:
            bar_width = 400
            bar_height = 25
            bar_x = SCREEN_WIDTH // 2 - bar_width // 2
            bar_y = 25
            
            progress = min(self.distance / self.goal_distance, 1.0)
            fill_width = int(bar_width * progress)
            
            pygame.draw.rect(screen, DARK_GRAY, (bar_x, bar_y, bar_width, bar_height))
            pygame.draw.rect(screen, GREEN, (bar_x, bar_y, fill_width, bar_height))
            pygame.draw.rect(screen, WHITE, (bar_x, bar_y, bar_width, bar_height), 2)
            
            progress_text = f"{int(self.distance)}/{self.goal_distance}m"
            draw_text(progress_text, font_small, WHITE, SCREEN_WIDTH // 2, bar_y + bar_height // 2)
        
        monster_count = self.inventory.count("Monster Energy")
        bagel_count = self.inventory.count("Bagel")
        
        if self.level == 2:
            key_status = "KEY: ✓" if self.has_key else "KEY: ✗"
            draw_text_left(f"{key_status} | M:{monster_count} B:{bagel_count}", font_small, GREEN, 200, 70)

        if self.level == 3:
            # Show speed
            speed_color = WHITE
            if self.out_of_range:
                # Flashing red/yellow
                speed_color = RED if (pygame.time.get_ticks() // 250) % 2 == 0 else YELLOW

            speed_text = f"MPH: {self.player.mph:.1f} MPH"
            draw_text_left(speed_text, font_small, speed_color, 200, 70)

            if self.out_of_range:
                # Show countdown timer for correction
                warning_seconds = max(self.speed_warning_timer // 60, 0)
                warning_text = f"OUT OF RANGE! Correct in {warning_seconds}s"
                draw_text(warning_text, font_medium, RED, SCREEN_WIDTH // 2, 150)
            else:
                range_text = f"Target: 20-25 MPH"
                draw_text_left(range_text, font_small, LIGHT_GRAY, 300, 100)

        if self.boost_timer > 0:
            boost_text = f"BOOST! {self.boost_timer // 60 + 1}s"
            draw_text(boost_text, font_medium, ORANGE, SCREEN_WIDTH // 2, 70)
        else:
            if self.level == 1:
                draw_text_left("SPACE: Boost | TAB: Inventory | B: Use Bagel", font_small, LIGHT_GRAY, 400, 70)
            elif self.level == 2:
                draw_text_left("ARROWS: Move | Click: Key/Car | B: Use Bagel", font_small, LIGHT_GRAY, 400, 70)
            elif self.level == 3:
                    draw_text_left("LEFT/RIGHT: Lane | UP/DOWN: Speed | S: Shop | B: Bagel", font_small, LIGHT_GRAY, 400, 70)
        
    def get_inventory_slot_rects(self):
        inv_width = 700
        inv_height = 600
        inv_x = (SCREEN_WIDTH - inv_width) // 2
        inv_y = (SCREEN_HEIGHT - inv_height) // 2
        
        slot_rects = []
        slot_size = 64
        spacing = 8
        
        main_grid_x = inv_x + 52
        main_grid_y = inv_y + 320
        
        for row in range(3):
            for col in range(9):
                x = main_grid_x + col * (slot_size + spacing)
                y = main_grid_y + row * (slot_size + spacing)
                slot_rects.append(pygame.Rect(x, y, slot_size, slot_size))
        
        hotbar_y = inv_y + 525
        for col in range(9):
            x = main_grid_x + col * (slot_size + spacing)
            y = hotbar_y
            slot_rects.append(pygame.Rect(x, y, slot_size, slot_size))
        
        extra_slot_x = inv_x + 52
        extra_slot_y = inv_y + 80
        for col in range(4):
            x = extra_slot_x + col * (slot_size + spacing)
            y = extra_slot_y
            slot_rects.append(pygame.Rect(x, y, slot_size, slot_size))
        
        return slot_rects, inv_x, inv_y
    
    def draw_inventory(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))
        
        inv_width = 700
        inv_height = 600
        inv_x = (SCREEN_WIDTH - inv_width) // 2
        inv_y = (SCREEN_HEIGHT - inv_height) // 2
        
        if minecraft_inv_img:
            screen.blit(minecraft_inv_img, (inv_x, inv_y))
        else:
            pygame.draw.rect(screen, (139, 87, 66), (inv_x, inv_y, inv_width, inv_height))
            pygame.draw.rect(screen, (50, 50, 50), (inv_x, inv_y, inv_width, inv_height), 5)
            draw_text("Inventory", font_large, WHITE, SCREEN_WIDTH // 2, inv_y + 30)
        
        slot_rects, _, _ = self.get_inventory_slot_rects()
        
        if not minecraft_inv_img:
            for slot in slot_rects:
                pygame.draw.rect(screen, DARK_GRAY, slot)
                pygame.draw.rect(screen, (150, 150, 150), slot, 2)
        
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
        
        draw_text("Press TAB to close", font_medium, WHITE, 
                 SCREEN_WIDTH // 2, inv_y + inv_height + 40)
                 
    def draw_game_over(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(220)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))
        
        if self.victory:
            draw_text("VICTORY!", font_large, GREEN, SCREEN_WIDTH // 2, 200)
            if self.level == 1:
                draw_text(f"You reached the parking lot!", font_medium, WHITE, SCREEN_WIDTH // 2, 270)
            elif self.level == 2:
                draw_text(f"You escaped the parking lot!", font_medium, WHITE, SCREEN_WIDTH // 2, 270)
            elif self.level == 3:
                draw_text(f"YOU FINISHED THE GAME!", font_medium, WHITE, SCREEN_WIDTH // 2, 270)
            time_limit = LEVEL_1_TIME if self.level == 1 else (LEVEL_2_TIME if self.level == 2 else LEVEL_3_TIME)
            minutes = int((time_limit - self.game_timer) // 60)
            seconds = int((time_limit - self.game_timer) % 60)
            draw_text(f"Time: {minutes:02d}:{seconds:02d}", font_medium, WHITE,SCREEN_WIDTH //  2, 320)

            if self.level == 1:
                draw_text("Next level is Level 2 (Parking Lot!)", font_medium, ORANGE, SCREEN_WIDTH // 2, 370)
            elif self.level == 2:
                draw_text("Next level is Level 3 (Highway!)", font_medium, BLUE, SCREEN_WIDTH // 2, 370)
            elif self.level == 3:
                draw_text("All Levels Complete!", font_medium, GOLD, SCREEN_WIDTH // 2, 370)
        else:
            draw_text("GAME OVER", font_large, RED, SCREEN_WIDTH // 2, 200)
            if self.level == 1:
                if self.game_timer <= 0:
                    draw_text("You have been fired!", font_medium, WHITE, SCREEN_WIDTH // 2, 270)
                else:
                    draw_text("The students parents sued you!", font_medium, WHITE, SCREEN_WIDTH // 2, 270)
            elif self.level == 2:
                    if self.game_timer <= 0:
                        draw_text("You have been fired!", font_medium, WHITE, SCREEN_WIDTH // 2, 270)
                    else:
                        draw_text("The cars sent you to the hospital and you are in debt!", font_medium, WHITE, SCREEN_WIDTH // 2, 270)
            elif self.level == 3:
                    if self.game_timer <= 0:
                        draw_text("You have been fired!", font_medium, WHITE, SCREEN_WIDTH // 2, 270)
                    else:
                        draw_text("You are were in a car crash! (Say your final words)", font_medium, WHITE, SCREEN_WIDTH // 2, 270)
            
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


# -------------------- LEVEL COUNTDOWN --------------------
def level_countdown(next_level):
    countdown = 3
    last_tick = pygame.time.get_ticks()
    
    while countdown > 0:
        screen.fill(BLACK)
        draw_text(f"Going to Level {next_level} in {countdown}", font_large, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        now = pygame.time.get_ticks()
        if now - last_tick >= 1000:  # 1 second per number
            countdown -= 1
            last_tick = now

# -------------------- LEVEL INSTRUCTIONS --------------------
def show_level_instructions(level):
    running = True
    while running:
        screen.fill(BLACK)
        if level == 1:
            draw_text("LEVEL 1: Lane Mode", font_large, GREEN, SCREEN_WIDTH // 2, 100)
            draw_text("GOAL: Survive and reach the end!", font_medium, WHITE, SCREEN_WIDTH // 2, 150)
            draw_text("Use LEFT / RIGHT arrow keys to switch lanes", font_small, WHITE, SCREEN_WIDTH // 2, 200)
            draw_text("Press SPACE for Monster boost | B to use Bagel", font_small, YELLOW, SCREEN_WIDTH // 2, 230)
        elif level == 2:
            draw_text("LEVEL 2: Parking Lot Escape", font_large, ORANGE, SCREEN_WIDTH // 2, 100)
            draw_text("GOAL: Find the key and unlock the correct car!", font_medium, WHITE, SCREEN_WIDTH // 2, 150)
            draw_text("Use ARROW KEYS to move freely", font_small, WHITE, SCREEN_WIDTH // 2, 200)
            draw_text("Click the key to collect it | Click cars to open", font_small, YELLOW, SCREEN_WIDTH // 2, 230)
            draw_text("Avoid police cars or lose a heart!", font_small, RED, SCREEN_WIDTH // 2, 260)
        elif level == 3:
            draw_text("LEVEL 3: Ultimate Fight", font_large, GOLD, SCREEN_WIDTH // 2, 100)
            draw_text("GOAL: GET YOUR GLASSES", font_medium, WHITE, SCREEN_WIDTH // 2, 150)
            draw_text("Use UP/DOWN arrows to control MPH", font_small, WHITE, SCREEN_WIDTH // 2, 200)
            draw_text("Keep speed between 20–25 MPH", font_small, GREEN, SCREEN_WIDTH // 2, 230)
            draw_text("You have 5 seconds to correct out-of-range speed", font_small, RED, SCREEN_WIDTH // 2, 260)
            draw_text("Stay focused and survive the final challenge!", font_small, WHITE, SCREEN_WIDTH // 2, 290)
            draw_text("Win the fight and make it to school on time!", font_small, WHITE, SCREEN_WIDTH // 2, 320)
            draw_text("Press B to use Bagel | S to open Shop", font_small, YELLOW, SCREEN_WIDTH // 2, 350)

        draw_text("Click anywhere to start!", font_medium, WHITE, SCREEN_WIDTH // 2, 500)
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
        draw_text("Artwork & Lead Programmer: Chethan Krishan Battini", font_medium, WHITE, SCREEN_WIDTH // 2, 300)
        draw_text("Programmer & Lead Storyboard: William Arney", font_medium, WHITE, SCREEN_WIDTH // 2, 350)
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
                    show_level_instructions(level=1)
                elif credits_rect.collidepoint(event.pos):
                    show_credit()

# -------------------- MAIN GAME LOOP --------------------
def main_game(level=1, player_state=None):
    show_level_instructions(level)

    game = Game(level, player_state)
    auto_transition_timer = None  # For 2-second wait

    running = True
    while running:
        clock.tick(60)
        keys = pygame.key.get_pressed()

        if not game.game_over and not game.paused:
            if keys[pygame.K_LEFT]:
                game.player.move_left()
            if keys[pygame.K_RIGHT]:
                game.player.move_right()
            if keys[pygame.K_UP]:
                game.player.move_up()
            if keys[pygame.K_DOWN]:
                game.player.move_down()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
                    game.paused = not game.paused

                elif event.key == pygame.K_b:
                    game.use_bagel()

                elif event.key == pygame.K_SPACE:
                    game.use_boost()

                elif event.key == pygame.K_ESCAPE:
                    return 0, None  # go back to menu

                elif event.key == pygame.K_s and game.level == 3:
                    shop = Shop3(game)
                    shop.run()

                # Cheats / testing
                elif event.key == pygame.K_1:
                    game.distance = game.goal_distance
                    game.victory = True
                    game.game_over = True

                elif game.game_over:
                    if event.key == pygame.K_r:
                        # Restart same level - keep the state from BEFORE this attempt
                        game = Game(level, player_state)
                    elif event.key == pygame.K_ESCAPE:
                        return 0, None

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if game.level == 2 and game.key:
                    if (
                        game.key.room_row == game.player.room_row and
                        game.key.room_col == game.player.room_col and
                        game.key.clicked(event.pos)
                    ):
                        game.key.collected = True
                        game.has_key = True
                        game.show_message("You found the key!", 120)
                        if pickup_sound:
                            pickup_sound.play()

                if game.level == 2:
                    for car in game.cars:
                        if (
                            car.room_row == game.player.room_row and
                            car.room_col == game.player.room_col and
                            car.clicked(event.pos)
                        ):
                            if not game.has_key:
                                game.show_message("You need a key!", 90)
                                break

                            if car.opened:
                                break

                            car.opened = True

                            if car.is_winning_car:
                                game.show_message("Correct car! Escaping...", 120)
                                game.victory = True
                                game.game_over = True
                            else:
                                if car.reward_type == "monster":
                                    if len(game.inventory) < MAX_INVENTORY_SIZE:
                                        game.inventory.append("Monster Energy")
                                    game.show_message("Found Monster Energy!", 120)
                                    if pickup_sound:
                                        pickup_sound.play()
                                else:
                                    if len(game.inventory) < MAX_INVENTORY_SIZE:
                                        game.inventory.append("Bagel")
                                    game.show_message("Found a Bagel!", 120)
                                    if pickup_sound:
                                        pickup_sound.play()
                            break

        game.update()
        game.draw()
        pygame.display.flip()

        # -------------------- AUTO LEVEL TRANSITION --------------------
        if game.game_over and game.victory:
            if auto_transition_timer is None:
                auto_transition_timer = pygame.time.get_ticks()  # start 2-second timer
            elif pygame.time.get_ticks() - auto_transition_timer >= 2000:
                # Carry over player state
                player_state = {
                    'lives': game.lives,
                    'max_lives': game.max_lives,
                    'inventory': game.inventory.copy(),
                    'coin_count': game.coin_count
                }

                if level == 1:
                    level_countdown(2)
                    return 2, player_state
                elif level == 2:
                    level_countdown(3)
                    return 3, player_state
                elif level == 3:
                    return 0, None
        else:
            auto_transition_timer = None

    return level, player_state

# -------------------- MAIN FUNCTION --------------------
if __name__ == "__main__":
    title_screen()
    current_level = 1
    player_state = None  # Initialize player state
    
    while True:
        next_level, player_state = main_game(current_level, player_state)
        
        if next_level == 0:
            # Return to menu - reset everything
            title_screen()
            current_level = 1
            player_state = None
        else:
            # Continue to next level with carried state
            current_level = next_level