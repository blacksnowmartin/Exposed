import pygame
import random
import sys
import time
from collections import deque

# Initialize Pygame
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("� Emoji Galaxy Rush")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 48)
big_font = pygame.font.SysFont("Arial", 72)

# Unique emojis from emojidb.org style + standard ones
EMOJIS = [
    "🖤⃝🦋", "🫶🏻", "💗⃝🌕", "𓆝 𓆟 𓆞", "🧿⃤", "✨", "🌟", "🔥", "🦋", "🦅",
    "🐦‍🔥", "🪼", "🌊", "🪐", "💎", "🗡️", "🛡️", "🍄", "🌈", "⚡", "❤️‍🔥",
    "🧿", "🪶", "🎀", "🫧", "🌙", "☄️", "🦚", "🐉", "🧚", "🔮"
]

# Game constants
PLAYER_SIZE = 40
ENEMY_SIZE = 35
COLLECT_SIZE = 30
FPS = 60

class Player:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT - 100
        self.speed = 5
        self.emoji = "🧙"  # Mage emoji
        self.health = 100
        self.score = 0
        self.level = 1

    def move(self, keys):
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.x += self.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.y -= self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.y += self.speed
        self.x = max(0, min(WIDTH - PLAYER_SIZE, self.x))
        self.y = max(0, min(HEIGHT - PLAYER_SIZE, self.y))

    def draw(self):
        text = font.render(self.emoji, True, (255, 255, 255))
        screen.blit(text, (self.x, self.y))

class Collectible:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.emoji = random.choice(EMOJIS)
        self.value = random.randint(10, 30)

    def draw(self):
        text = font.render(self.emoji, True, (0, 255, 255))
        screen.blit(text, (self.x, self.y))

class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = random.uniform(1.5, 3.5)
        self.emoji = random.choice(["💀", "👹", "🕷️", "🐍", "☠️"])
        self.direction = random.choice([-1, 1])

    def update(self):
        self.x += self.speed * self.direction
        if self.x <= 0 or self.x >= WIDTH - ENEMY_SIZE:
            self.direction *= -1

    def draw(self):
        text = font.render(self.emoji, True, (255, 50, 50))
        screen.blit(text, (self.x, self.y))

def draw_text(text, size, color, y_offset=0):
    f = big_font if size > 30 else font
    txt = f.render(text, True, color)
    rect = txt.get_rect(center=(WIDTH//2, HEIGHT//2 + y_offset))
    screen.blit(txt, rect)

def main():
    player = Player()
    collectibles = [Collectible(random.randint(50, WIDTH-50), random.randint(50, HEIGHT//2)) for _ in range(8)]
    enemies = [Enemy(random.randint(50, WIDTH-50), random.randint(50, 200)) for _ in range(4)]
    
    score_multiplier = 1
    game_over = False
    paused = False
    start_time = time.time()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = not paused
                if event.key == pygame.K_r and game_over:
                    main()  # Restart

        if game_over or paused:
            screen.fill((10, 10, 30))
            if game_over:
                draw_text("💥 GAME OVER 💥", 48, (255, 50, 50))
                draw_text(f"Final Score: {player.score}", 36, (255, 255, 100), 60)
            else:
                draw_text("⏸️ PAUSED", 48, (255, 255, 100))
            pygame.display.flip()
            clock.tick(10)
            continue

        keys = pygame.key.get_pressed()
        player.move(keys)

        # Spawn new collectibles
        if random.random() < 0.02 and len(collectibles) < 12:
            collectibles.append(Collectible(random.randint(50, WIDTH-50), random.randint(50, HEIGHT-100)))

        # Update enemies
        for enemy in enemies[:]:
            enemy.update()
            # Collision with player
            if (abs(enemy.x - player.x) < 30 and abs(enemy.y - player.y) < 30):
                player.health -= 20
                enemies.remove(enemy)
                if player.health <= 0:
                    game_over = True

        # Collectibles
        for coll in collectibles[:]:
            if abs(coll.x - player.x) < 35 and abs(coll.y - player.y) < 35:
                player.score += coll.value * score_multiplier
                collectibles.remove(coll)
                # Level up every 500 points
                if player.score > player.level * 500:
                    player.level += 1
                    score_multiplier += 0.5
                    # Add more enemies
                    if len(enemies) < 8:
                        enemies.append(Enemy(random.randint(50, WIDTH-50), random.randint(50, 150)))

        # Background
        screen.fill((15, 15, 40))
        
        # Stars / particles effect
        for _ in range(3):
            pygame.draw.circle(screen, (200, 200, 255), 
                             (random.randint(0, WIDTH), random.randint(0, HEIGHT)), 1)

        # Draw everything
        for coll in collectibles:
            coll.draw()
        for enemy in enemies:
            enemy.draw()
        player.draw()

        # HUD
        hud = font.render(f"❤️ {player.health}   Score: {player.score}   Level: {player.level}   ⏱️ {int(time.time()-start_time)}s", True, (255, 255, 100))
        screen.blit(hud, (10, 10))

        if player.health <= 0:
            game_over = True

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    print("🌟 Starting Emoji Quest...")
    print("Controls: WASD or Arrow keys to move")
    print("P to pause | Collect unique emojis!")
    main()