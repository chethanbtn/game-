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
    background_img = pygame.image.load("hallway.jpg")
    background_img = pygame.transform.scale(background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
    print("Loaded hallway.jpg")
except:
    print("Could not load hallway.jpg")
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

# Load Minecraft inventory image - try multiple filenames
minecraft_inv_img = None
inventory_files = ["minecraft_inventory.jpg", "minecraft_inventory.png", "minecraft inventory.jpg", "inventory.jpg"]
for filename in inventory_files:
    try:
        minecraft_inv_img = pygame.image.load(filename)
        minecraft_inv_img = pygame.transform.scale(minecraft_inv_img, (700, 600))
        print(f"Loaded {filename}")
        break
    except:
        continue

if not minecraft_inv_img:
    print("Could not load Minecraft inventory - using fallback graphics")
    print("   Tried files:", inventory_files)

# -------------------- AUDIO SETUP --------------------
pygame.mixer.init()
try:
    pygame.mixer.music.load("background_music.mp3")
    pygame.mixer.music.set_volume(0.1)
    pygame.mixer.music.play(-1)
    print("Loaded background_music.mp3")
except:
    print("Background music not found")

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

# -------------------- FONTS --------------------
font_large = pygame.font.SysFont(None, 60)
font_medium = pygame.font.SysFont(None, 40)
font_small = pygame.font.SysFont(None, 30)

# -------------------- GAME CONSTANTS --------------------
LANE_WIDTH = SCREEN_WIDTH // 3
LANES = [LANE_WIDTH // 2, SCREEN_WIDTH // 2, SCREEN_WIDTH - LANE_WIDTH // 2]
GAME_TIME = 1200  # 20 minutes in seconds
GOAL_DISTANCE = 1000  # 1000 meters to win
BASE_SPEED = 5
BOOST_SPEED = 12
BOOST_DURATION = 180  # 3 seconds at 60 FPS

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

# -------------------- GAME CLASS --------------------
class Game:
    def __init__(self):
        self.player = Player()
        self.students = []
        self.monsters = []
        self.lives = 3
        self.max_lives = 3
        self.inventory = []
        self.score = 0
        self.spawn_timer = 0
        self.spawn_rate = 60  # Frames between spawns
        self.game_timer = GAME_TIME
        self.start_ticks = pygame.time.get_ticks()
        self.paused = False
        self.invincible_timer = 0
        self.game_over = False
        self.victory = False
        self.distance = 0  # Distance in meters
        self.current_speed = BASE_SPEED
        self.boost_timer = 0
        self.bg_scroll = 0
        
    def use_boost(self):
        """Use a monster from inventory to activate speed boost"""
        if len(self.inventory) > 0 and self.boost_timer == 0:
            self.inventory.pop()
            self.boost_timer = BOOST_DURATION
            self.current_speed = BOOST_SPEED
            
    def spawn_obstacle(self):
        lane = random.randint(0, 2)
        if random.random() < 0.7:  # 70% chance for student
            self.students.append(Student(lane, self.current_speed))
        else:  # 30% chance for monster
            self.monsters.append(Monster(lane, self.current_speed))
            
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
        distance_gain = self.current_speed / 60.0  # Convert to meters per frame
        self.distance += distance_gain
        
        # Update background scroll
        self.bg_scroll += self.current_speed
        if self.bg_scroll >= SCREEN_HEIGHT:
            self.bg_scroll = 0
        
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
        
        # Spawn obstacles
        self.spawn_timer += 1
        if self.spawn_timer >= self.spawn_rate:
            self.spawn_obstacle()
            self.spawn_timer = 0
            # Increase difficulty over time
            if self.spawn_rate > 30:
                self.spawn_rate -= 1
                
        # Update students
        for student in self.students[:]:
            student.speed = self.current_speed
            student.update()
            if student.is_off_screen():
                self.students.remove(student)
                self.score += 10  # Points for dodging
            elif student.collides_with(self.player) and self.invincible_timer == 0:
                self.students.remove(student)
                self.lives -= 1
                self.invincible_timer = 60  # 1 second of invincibility
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
                self.inventory.append("Monster Energy")
                self.score += 50
                
    def draw(self):
        # Draw scrolling background
        if background_img:
            # Draw two copies for seamless scrolling
            y_offset = self.bg_scroll % SCREEN_HEIGHT
            screen.blit(background_img, (0, y_offset - SCREEN_HEIGHT))
            screen.blit(background_img, (0, y_offset))
        else:
            screen.fill(BLACK)
            # Draw lanes
            for i in range(4):
                x = i * LANE_WIDTH
                pygame.draw.line(screen, GRAY, (x, 0), (x, SCREEN_HEIGHT), 2)
                
            # Draw lane markers
            marker_speed = 10 if self.boost_timer > 0 else 5
            for y in range(-20, SCREEN_HEIGHT, 100):
                adjusted_y = (y + (pygame.time.get_ticks() // marker_speed) % 100) % SCREEN_HEIGHT
                for i in range(1, 3):
                    x = i * LANE_WIDTH
                    pygame.draw.rect(screen, WHITE, (x - 5, adjusted_y, 10, 40))
                
        # Draw obstacles
        for student in self.students:
            student.draw()
            
        for monster in self.monsters:
            monster.draw()
            
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
        
        # Draw hearts using images or fallback
        heart_x = 20
        for i in range(self.max_lives):
            if i < self.lives:
                if full_heart_img:
                    screen.blit(full_heart_img, (heart_x + i * 50, 15))
                else:
                    pygame.draw.circle(screen, RED, (heart_x + i * 40, 30), 15)
                    pygame.draw.circle(screen, RED, (heart_x + i * 40 + 20, 30), 15)
                    pygame.draw.polygon(screen, RED, [
                        (heart_x + i * 40 - 15, 30),
                        (heart_x + i * 40 + 10, 50),
                        (heart_x + i * 40 + 35, 30)
                    ])
            else:
                if broken_heart_img:
                    screen.blit(broken_heart_img, (heart_x + i * 50, 15))
                else:
                    pygame.draw.circle(screen, GRAY, (heart_x + i * 40, 30), 15, 2)
                    pygame.draw.circle(screen, GRAY, (heart_x + i * 40 + 20, 30), 15, 2)
                
        # Draw distance (main progress bar)
        distance_percent = min(self.distance / GOAL_DISTANCE, 1.0)
        bar_width = 400
        bar_height = 30
        bar_x = SCREEN_WIDTH // 2 - bar_width // 2
        bar_y = 20
        
        # Background bar
        pygame.draw.rect(screen, GRAY, (bar_x, bar_y, bar_width, bar_height))
        # Progress bar
        progress_color = YELLOW if self.boost_timer > 0 else GREEN
        pygame.draw.rect(screen, progress_color, 
                        (bar_x, bar_y, int(bar_width * distance_percent), bar_height))
        # Border
        pygame.draw.rect(screen, WHITE, (bar_x, bar_y, bar_width, bar_height), 3)
        
        # Distance text
        distance_text = f"{int(self.distance)}m / {GOAL_DISTANCE}m"
        draw_text(distance_text, font_small, WHITE, SCREEN_WIDTH // 2, bar_y + bar_height // 2)
        
        # Draw timer
        minutes = int(self.game_timer // 60)
        seconds = int(self.game_timer % 60)
        timer_text = f"Time: {minutes:02d}:{seconds:02d}"
        timer_color = RED if self.game_timer < 60 else WHITE
        draw_text_left(timer_text, font_small, timer_color, SCREEN_WIDTH - 200, 25)
        
        # Draw inventory count
        draw_text_left(f"Monsters: {len(self.inventory)}", font_small, GREEN, 20, 70)
        
        # Draw boost status
        if self.boost_timer > 0:
            boost_text = f"BOOST! {self.boost_timer // 60 + 1}s"
            draw_text(boost_text, font_medium, ORANGE, SCREEN_WIDTH // 2, 70)
        else:
            draw_text_left("SPACE: Quick Boost | TAB: Inventory", font_small, LIGHT_GRAY, 250, 70)
        
    def get_inventory_slot_rects(self):
        """Get the rectangles for each inventory slot for click detection"""
        inv_width = 700
        inv_height = 600
        inv_x = (SCREEN_WIDTH - inv_width) // 2
        inv_y = (SCREEN_HEIGHT - inv_height) // 2
        
        # Main inventory grid (3 rows x 9 columns) - bottom section
        slot_rects = []
        slot_size = 64
        grid_start_x = inv_x + 52
        grid_start_y = inv_y + 430
        
        for row in range(3):
            for col in range(9):
                x = grid_start_x + col * 72
                y = grid_start_y + row * 72
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
        
        # Draw Minecraft inventory background
        if minecraft_inv_img:
            screen.blit(minecraft_inv_img, (inv_x, inv_y))
        else:
            # Fallback inventory with Minecraft-style design
            # Main background
            pygame.draw.rect(screen, (139, 87, 66), (inv_x, inv_y, inv_width, inv_height))
            pygame.draw.rect(screen, (50, 50, 50), (inv_x, inv_y, inv_width, inv_height), 5)
            
            # Draw title bar
            pygame.draw.rect(screen, (100, 70, 50), (inv_x, inv_y, inv_width, 60))
            draw_text("Inventory", font_large, WHITE, SCREEN_WIDTH // 2, inv_y + 30)
            
            # Draw grid slots
            slot_size = 64
            grid_start_x = inv_x + 52
            grid_start_y = inv_y + 430
            
            for row in range(3):
                for col in range(9):
                    x = grid_start_x + col * 72
                    y = grid_start_y + row * 72
                    # Slot background
                    pygame.draw.rect(screen, DARK_GRAY, (x, y, slot_size, slot_size))
                    # Slot border
                    pygame.draw.rect(screen, (150, 150, 150), (x, y, slot_size, slot_size), 2)
        
        # Draw title at top
        if not minecraft_inv_img:
            draw_text("Monster Energy Inventory", font_medium, WHITE, SCREEN_WIDTH // 2, inv_y + 100)
        
        # Get slot rectangles
        slot_rects, _, _ = self.get_inventory_slot_rects()
        
        # Draw monsters in inventory slots (bottom 3 rows)
        for i, item in enumerate(self.inventory[:27]):  # Max 27 slots (3x9 grid)
            if i < len(slot_rects):
                slot = slot_rects[i]
                # Draw monster can in slot
                if monster_img:
                    img = pygame.transform.scale(monster_img, (50, 60))
                    img_rect = img.get_rect(center=slot.center)
                    screen.blit(img, img_rect)
                else:
                    pygame.draw.rect(screen, GREEN, 
                                   (slot.centerx - 25, slot.centery - 30, 50, 60))
                    draw_text("M", font_small, BLACK, slot.centerx, slot.centery)
        
        # Draw instructions
        draw_text("Click on Monster to use boost!", font_small, YELLOW, 
                 SCREEN_WIDTH // 2, inv_y + inv_height + 20)
        draw_text("Press TAB to close", font_small, WHITE, 
                 SCREEN_WIDTH // 2, inv_y + inv_height + 50)
                 
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
        draw_text(f"Monsters Collected: {len(self.inventory)}", font_medium, GREEN,
                 SCREEN_WIDTH // 2, 450)
        draw_text("Press R to restart or ESC for menu", font_medium, WHITE,
                 SCREEN_WIDTH // 2, 550)

# -------------------- INSTRUCTIONS SCREEN --------------------
def show_instructions():
    running = True
    while running:
        screen.fill(BLACK)
        draw_text("Instructions:", font_large, WHITE, SCREEN_WIDTH // 2, 80)
        draw_text("GOAL: Reach 1000 meters before time runs out!", font_medium, YELLOW,
                 SCREEN_WIDTH // 2, 160)
        draw_text("Use LEFT/RIGHT arrow keys to switch lanes", font_small, WHITE, 
                 SCREEN_WIDTH // 2, 230)
        draw_text("Avoid students - they take away hearts!", font_small, RED,
                 SCREEN_WIDTH // 2, 280)
        draw_text("Collect Monster Energy drinks!", font_small, GREEN,
                 SCREEN_WIDTH // 2, 330)
        draw_text("Press SPACE to use Monster for speed boost!", font_small, ORANGE,
                 SCREEN_WIDTH // 2, 380)
        draw_text("Press TAB to view inventory (pauses game)", font_small, WHITE,
                 SCREEN_WIDTH // 2, 430)
        draw_text("Click on Monster in inventory to use it!", font_small, ORANGE,
                 SCREEN_WIDTH // 2, 480)
        draw_text("You have 20 minutes - don't run out of time!", font_small, WHITE,
                 SCREEN_WIDTH // 2, 530)
        draw_text("Click anywhere to return", font_medium, WHITE, 
                 SCREEN_WIDTH // 2, 620)

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
                        if game.boost_timer == 0:   # 🔧 THIS LINE FIXES THE BUG
                            game.inventory.pop(i)
                            game.boost_timer = BOOST_DURATION
                            game.current_speed = BOOST_SPEED
                            game.paused = False
                        break

                        
        game.update()
        game.draw()
        pygame.display.flip()

# -------------------- MAIN --------------------
def main():
    print("\n" + "="*50)
    print("THE ADVENTURES OF MR.LANDA")
    print("="*50)
    while True:
        title_screen()
        main_game()

if __name__ == "__main__":
    main()