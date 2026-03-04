import pygame 
import random
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 100, 255)
YELLOW = (255, 255, 0)
PURPLE = (200, 0, 200)

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((40, 50))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 7
        self.health = 100
        self.max_health = 100
        
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.rect.y += self.speed
        
        # Keep player on screen
        self.rect.x = max(0, min(self.rect.x, SCREEN_WIDTH - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, SCREEN_HEIGHT - self.rect.height))
    
    def draw_detailed(self, screen):
        # Draw player as a spaceship
        pygame.draw.polygon(screen, GREEN, [
            (self.rect.centerx, self.rect.top),
            (self.rect.left, self.rect.bottom),
            (self.rect.centerx - 5, self.rect.centery),
            (self.rect.right, self.rect.bottom)
        ])
        # Draw cockpit
        pygame.draw.circle(screen, BLUE, (self.rect.centerx, self.rect.centery), 5)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((35, 35))
        self.image.fill(RED)
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = random.randint(2, 5)
        self.health = 30
        self.max_health = 30
        self.direction = random.choice([-1, 1])
        
    def update(self):
        self.rect.x += self.direction * self.speed
        
        # Bounce off walls
        if self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
            self.direction *= -1
        
        # Random vertical movement
        self.rect.y += random.randint(-1, 1)
        self.rect.y = max(0, min(self.rect.y, SCREEN_HEIGHT - self.rect.height))
    
    def draw_detailed(self, screen):
        # Draw enemy as a spaceship
        pygame.draw.polygon(screen, RED, [
            (self.rect.centerx, self.rect.top),
            (self.rect.left, self.rect.centery),
            (self.rect.centerx, self.rect.bottom),
            (self.rect.right, self.rect.centery)
        ])

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 15))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 10
        
    def update(self):
        self.rect.y -= self.speed
        
        if self.rect.bottom < 0:
            self.kill()

class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 15))
        self.image.fill(PURPLE)
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 6
        
    def update(self):
        self.rect.y += self.speed
        
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

class Particle(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__()
        self.image = pygame.Surface((5, 5))
        self.image.fill(color)
        self.rect = self.image.get_rect(center=(x, y))
        self.vx = random.randint(-5, 5)
        self.vy = random.randint(-5, 5)
        self.lifetime = 30
        
    def update(self):
        self.rect.x += self.vx
        self.rect.y += self.vy
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.kill()

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Space Invaders 2D")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        self.reset_game()
        
    def reset_game(self):
        self.player_group = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()
        self.bullet_group = pygame.sprite.Group()
        self.enemy_bullet_group = pygame.sprite.Group()
        self.particle_group = pygame.sprite.Group()
        
        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 60)
        self.player_group.add(self.player)
        
        self.score = 0
        self.wave = 1
        self.enemies_spawned = 0
        self.spawn_timer = 0
        self.enemy_shot_timer = 0
        self.game_over = False
        self.paused = False
        
        self.spawn_enemies(self.wave + 2)
        
    def spawn_enemies(self, count):
        for _ in range(count):
            x = random.randint(50, SCREEN_WIDTH - 50)
            y = random.randint(30, 150)
            enemy = Enemy(x, y)
            self.enemy_group.add(enemy)
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullet = Bullet(self.player.rect.centerx, self.player.rect.top)
                    self.bullet_group.add(bullet)
                if event.key == pygame.K_p:
                    self.paused = not self.paused
                if event.key == pygame.K_r and self.game_over:
                    self.reset_game()
        return True
    
    def update(self):
        if self.paused or self.game_over:
            return
        
        self.player_group.update()
        self.enemy_group.update()
        self.bullet_group.update()
        self.enemy_bullet_group.update()
        self.particle_group.update()
        
        # Enemy shooting
        self.enemy_shot_timer += 1
        if self.enemy_shot_timer > 30 and self.enemy_group:
            enemy = random.choice(self.enemy_group.sprites())
            bullet = EnemyBullet(enemy.rect.centerx, enemy.rect.bottom)
            self.enemy_bullet_group.add(bullet)
            self.enemy_shot_timer = 0
        
        # Bullet-Enemy collisions
        for bullet in self.bullet_group:
            hit_enemies = pygame.sprite.spritecollide(bullet, self.enemy_group, False)
            for enemy in hit_enemies:
                enemy.health -= 25
                # Create particles
                for _ in range(10):
                    particle = Particle(bullet.rect.centerx, bullet.rect.centery, RED)
                    self.particle_group.add(particle)
                bullet.kill()
                
                if enemy.health <= 0:
                    enemy.kill()
                    self.score += 10
                    # More particles on death
                    for _ in range(20):
                        particle = Particle(enemy.rect.centerx, enemy.rect.centery, YELLOW)
                        self.particle_group.add(particle)
        
        # Enemy Bullet-Player collision
        for bullet in self.enemy_bullet_group:
            if pygame.sprite.spritecollide(self.player, self.enemy_bullet_group, True):
                self.player.health -= 10
                for _ in range(15):
                    particle = Particle(self.player.rect.centerx, self.player.rect.centery, BLUE)
                    self.particle_group.add(particle)
        
        # Enemy-Player collision
        if pygame.sprite.spritecollide(self.player, self.enemy_group, False):
            self.player.health -= 0.5
        
        # Check if all enemies defeated
        if len(self.enemy_group) == 0:
            self.wave += 1
            self.spawn_enemies(self.wave + 2)
        
        # Check game over
        if self.player.health <= 0:
            self.game_over = True
    
    def draw(self):
        self.screen.fill(BLACK)
        
        # Draw starfield background
        for _ in range(50):
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(0, SCREEN_HEIGHT)
            pygame.draw.circle(self.screen, WHITE, (x, y), 1)
        
        # Draw sprites with detailed graphics
        for sprite in self.player_group:
            sprite.draw_detailed(self.screen)
        
        for sprite in self.enemy_group:
            sprite.draw_detailed(self.screen)
            # Draw health bar
            bar_width = 30
            bar_height = 4
            bar_x = sprite.rect.centerx - bar_width // 2
            bar_y = sprite.rect.top - 10
            pygame.draw.rect(self.screen, RED, (bar_x, bar_y, bar_width, bar_height))
            health_width = int(bar_width * (sprite.health / sprite.max_health))
            pygame.draw.rect(self.screen, GREEN, (bar_x, bar_y, health_width, bar_height))
        
        self.bullet_group.draw(self.screen)
        self.enemy_bullet_group.draw(self.screen)
        self.particle_group.draw(self.screen)
        
        # Draw player health bar
        bar_width = 200
        bar_height = 20
        bar_x = 20
        bar_y = SCREEN_HEIGHT - 40
        pygame.draw.rect(self.screen, RED, (bar_x, bar_y, bar_width, bar_height))
        health_width = int(bar_width * (self.player.health / self.player.max_health))
        pygame.draw.rect(self.screen, GREEN, (bar_x, bar_y, health_width, bar_height))
        pygame.draw.rect(self.screen, WHITE, (bar_x, bar_y, bar_width, bar_height), 2)
        
        # Draw UI
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        wave_text = self.font.render(f"Wave: {self.wave}", True, WHITE)
        health_text = self.small_font.render(f"Health: {int(self.player.health)}/100", True, WHITE)
        
        self.screen.blit(score_text, (20, 20))
        self.screen.blit(wave_text, (20, 60))
        self.screen.blit(health_text, (bar_x, SCREEN_HEIGHT - 100))
        
        # Draw controls
        controls = self.small_font.render("WASD/Arrows: Move | SPACE: Shoot | P: Pause", True, BLUE)
        self.screen.blit(controls, (SCREEN_WIDTH - 450, 20))
        
        # Draw paused message
        if self.paused:
            paused_text = self.font.render("PAUSED", True, YELLOW)
            self.screen.blit(paused_text, (SCREEN_WIDTH // 2 - 70, SCREEN_HEIGHT // 2))
        
        # Draw game over message
        if self.game_over:
            gameover_text = self.font.render("GAME OVER", True, RED)
            final_score = self.font.render(f"Final Score: {self.score}", True, WHITE)
            restart_text = self.small_font.render("Press R to Restart", True, YELLOW)
            
            self.screen.blit(gameover_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 50))
            self.screen.blit(final_score, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2))
            self.screen.blit(restart_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 50))
        
        pygame.display.flip()
    
    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()
