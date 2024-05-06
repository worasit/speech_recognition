import pygame
import random
import sys
import os

# Initialize pygame
pygame.init()

current_dir = os.path.dirname(os.path.abspath(__file__))
dino_file = os.path.join(current_dir, 'dino.png')
cactus_file = os.path.join(current_dir, 'cactus.png')
jump_sound_file = os.path.join(current_dir, 'jump.mp3')
game_over_sound_file = os.path.join(current_dir, 'game_over.wav')
background_music_file = os.path.join(current_dir, 'background.wav')
sun_file = os.path.join(current_dir, 'sun.png')

# Set up game parameters
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
GROUND_HEIGHT = SCREEN_HEIGHT - 50
SAND_COLOR = (216, 174, 106)  # Light brown color representing desert sand
ROAD_COLOR = (100, 100, 100)   # Color representing road
UNDER_ROAD_COLOR = (153, 101, 21)  # Darker brown color representing sand under the road
SKY_TOP_COLOR = (135, 206, 235)   # Light blue color representing sky at the top
SKY_BOTTOM_COLOR = (0, 191, 255)  # Dark blue color representing sky at the bottom
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FPS = 60
GRAVITY = 1.5
JUMP_HEIGHT = 27

# Set up the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dinosaur Run")

# Load images
dino_img = pygame.image.load(dino_file)
cactus_img = pygame.image.load(cactus_file)
sun_img = pygame.image.load(sun_file)

# Scale images
dino_img = pygame.transform.scale(dino_img, (50, 50))
cactus_img = pygame.transform.scale(cactus_img, (50, 50))
sun_img = pygame.transform.scale(sun_img, (80, 80))

# Load sounds
jump_sound = pygame.mixer.Sound(jump_sound_file)
game_over_sound = pygame.mixer.Sound(game_over_sound_file)

# Load background music
pygame.mixer.music.load(background_music_file)
pygame.mixer.music.play(-1)  # Loop the background music indefinitely

# Define Dinosaur class
class Dinosaur(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = dino_img
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = GROUND_HEIGHT - self.rect.height
        self.velocity_y = 0
        self.is_jumping = False

    def update(self):
        self.velocity_y += GRAVITY
        self.rect.y += self.velocity_y
        if self.rect.y >= GROUND_HEIGHT - self.rect.height:
            self.rect.y = GROUND_HEIGHT - self.rect.height
            self.velocity_y = 0
            self.is_jumping = False

    def jump(self):
        if not self.is_jumping:
            self.velocity_y = -JUMP_HEIGHT
            self.is_jumping = True
            jump_sound.play()


# Define Cactus class
class Cactus(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = cactus_img
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH
        self.rect.y = GROUND_HEIGHT - self.rect.height

    def update(self):
        self.rect.x -= 5
        if self.rect.right < 0:
            self.kill()  # Remove the cactus sprite when it goes off-screen


# Define Sun class
class Sun(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = sun_img
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH - self.rect.width - 20
        self.rect.y = 20


# Create sprite groups
all_sprites = pygame.sprite.Group()
cacti_group = pygame.sprite.Group()
all_sprites.add(Dinosaur())
sun = Sun()
all_sprites.add(sun)

# Main game loop
clock = pygame.time.Clock()
score = 0
running = True
game_over = False
next_cactus_time = 0
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over:
                all_sprites.sprites()[0].jump()
            elif event.key == pygame.K_SPACE and game_over:
                game_over = False
                all_sprites = pygame.sprite.Group()
                cacti_group = pygame.sprite.Group()
                all_sprites.add(Dinosaur())
                score = 0

    # Update
    if not game_over:
        all_sprites.update()

        # Spawn cactus
        if pygame.time.get_ticks() > next_cactus_time:
            cactus = Cactus()
            cacti_group.add(cactus)
            all_sprites.add(cactus)
            next_cactus_time = pygame.time.get_ticks() + random.randint(1500, 3000)  # Random delay between cacti

        # Check for collisions
        hits = pygame.sprite.spritecollide(all_sprites.sprites()[0], cacti_group, False)
        if hits:
            game_over = True
            game_over_sound.play()

    # Draw sky gradient
    sky_gradient = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    sky_gradient.fill(SKY_TOP_COLOR)
    pygame.draw.rect(sky_gradient, SKY_BOTTOM_COLOR, (0, SCREEN_HEIGHT // 2, SCREEN_WIDTH, SCREEN_HEIGHT // 2))
    screen.blit(sky_gradient, (0, 0))

    # Draw sand under the road
    pygame.draw.rect(screen, UNDER_ROAD_COLOR, (0, GROUND_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT - GROUND_HEIGHT))

    # Draw road
    pygame.draw.line(screen, ROAD_COLOR, (0, GROUND_HEIGHT), (SCREEN_WIDTH, GROUND_HEIGHT), 5)

    all_sprites.draw(screen)

    # Display score
    font = pygame.font.Font(None, 36)
    text = font.render("Score: " + str(score), True, BLACK)
    screen.blit(text, (10, 10))
    score += 1

    if game_over:
        game_over_font = pygame.font.Font(None, 100)
        game_over_text = game_over_font.render("Game Over", True, BLACK)
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(game_over_text, game_over_rect)

    pygame.display.flip()
    clock.tick(FPS)

# Wait for a moment before quitting
pygame.time.wait(2000)

pygame.quit()
sys.exit()
