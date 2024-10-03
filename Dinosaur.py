import pygame
import Logique
import asyncio

# Dimensions de la fenêtre
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Initialisation de Pygame
pygame.init()

# Configuration de la fenêtre
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Dino Runner')

# Chargement du tileset (remplacez 'tileset.png' par le chemin de votre fichier tileset)
tileset = pygame.image.load('assets/dinosaur-tileset2.png').convert_alpha()

# Classe Dino
class Dino(pygame.sprite.Sprite):
    def __init__(self, logic):
        super().__init__()
        self.logic = logic
        self.tile_size = self.logic.size["width"]
        self.offset = 1855

        self.images = [tileset.subsurface((i * self.tile_size + self.offset , 0, self.tile_size, self.tile_size)) for i in range(0, 2)]
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.x = self.logic.getX()
        self.rect.y = self.logic.getY()
        self.animation_index = 0
        self.animation_time = 0

    def update(self, **kwargs):

        self.animation_time += 1
        if self.animation_time % 10 == 0:
            self.animation_index = (self.animation_index + 1) % len(self.images)
            self.image = self.images[self.animation_index]

        self.rect.x = self.logic.getX()
        self.rect.y = self.logic.getY()

    def setX(self, x):
        self.rect.x = x 

    def setY(self,y):
        self.rect.y = y

# Classe Obstacle
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, logic):
        super().__init__()
        self.logic = logic

        self.tile_size_x = self.logic.size[self.logic.obstacle_id]["width"]
        self.tile_size_y = self.logic.size[self.logic.obstacle_id]["height"]
        self.offset_x = self.logic.size[self.logic.obstacle_id]["offset_x"]
        self.offset_y = self.logic.size[self.logic.obstacle_id]["offset_y"]

        if self.logic.obstacle_id == 4:
            self.images = [tileset.subsurface((self.offset_x + i * self.tile_size_x, self.offset_y, self.tile_size_x, self.tile_size_y)) for i in range(0, 2)]
            self.image = self.images[0]
        else:
            self.image = tileset.subsurface((self.offset_x, self.offset_y, self.tile_size_x, self.tile_size_y))

        self.rect = self.image.get_rect()
        self.rect.x = self.logic.getX()
        self.rect.y = self.logic.getY()

        self.animation_index = 0
        self.animation_tick = 0

    def update(self, **kwargs):

        self.animation_tick += 1
        if self.animation_tick % 10 == 0 and self.logic.obstacle_id == 4:
            self.animation_index = (self.animation_index + 1) % len(self.images)
            self.image = self.images[self.animation_index]

        self.rect.x = self.logic.getX()
        self.rect.y = self.logic.getY()

    def setX(self, x):
        self.rect.x = x 

    def setY(self,y):
        self.rect.y = y

class Ground(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.tile_size_x = 2390
        self.tile_size_y = 30
        self.image = tileset.subsurface((0, 100, self.tile_size_x, self.tile_size_y))
        self.rect = self.image.get_rect()
        self.rect.x = self.tile_size_x * position
        self.rect.y = SCREEN_HEIGHT - self.tile_size_y

    def update(self, **kwargs):
        self.rect.x -= 10 * kwargs.get("game_speed", 1)
        if self.rect.x <= -self.tile_size_x:
            self.rect.x = self.tile_size_x

class SunMoon(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.tile_x = 954
        self.tile_y = 0
        self.tile_size_x = 40
        self.tile_size_y = 82
        self.images = [tileset.subsurface((self.tile_x + i * self.tile_size_x, self.tile_y, self.tile_size_x, self.tile_size_y)) for i in range(0, 8)]
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.x = x - self.tile_size_x
        self.rect.y = y - self.tile_size_y

        self.animation_index = 0
        self.animation_tick = 0

    def update(self, **kwargs):

        # Animation du soleil ou de la lune
        self.animation_tick += 1
        if self.animation_tick % 120 == 0:
            self.animation_index = (self.animation_index + 1) % len(self.images)
            self.image = self.images[self.animation_index]

        # Recentrer l'image
        self.rect.x = self.x if 0 <= self.animation_index <= 3 else self.x + self.tile_size_x

# Classe Game
class Game:
    def __init__(self, machine_learning):
        self.machine_learning = machine_learning
        self.logic_game = self.machine_learning.get_game()

        self.all_sprites = pygame.sprite.Group()

        self.obstacles = []

        self.dino = Dino(self.logic_game.dino)
        self.all_sprites.add(self.dino)

        self.grounds_sprites = pygame.sprite.Group( [Ground(0), Ground(1)] )
        self.all_sprites.add(self.grounds_sprites)

        self.sunMoon = SunMoon(SCREEN_WIDTH - 100, 100)
        self.all_sprites.add(self.sunMoon)

        self.font = pygame.font.Font(None, 36)
        self.generation_text = self.font.render(f'Generation: {self.machine_learning.generations_count}', True, BLACK)

    def sync_obstacles(self):
        current_obstacles = {obstacle.logic.id: obstacle for obstacle in filter(lambda x: isinstance(x, Obstacle), self.all_sprites)}
        new_obstacles = {obstacle.id: obstacle for obstacle in self.logic_game.get_obstacles()}

        # Remove old obstacles
        for obstacle_id in list(current_obstacles.keys()):
            if obstacle_id not in new_obstacles:
                obstacle = current_obstacles[obstacle_id]
                self.all_sprites.remove(obstacle)
                self.obstacles.remove(obstacle)

        # Add new obstacles
        for obstacle_id in new_obstacles:
            if obstacle_id not in current_obstacles:
                logic_obstacle = new_obstacles[obstacle_id]
                obstacle = Obstacle(logic_obstacle)
                self.all_sprites.add(obstacle)
                self.obstacles.append(obstacle)

    async def run(self):
        last_update = pygame.time.get_ticks()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()

            # Mise à jour de la logique du machine learning le plus rapidement possible
            self.machine_learning.update()

            # Mise à jour de la logique du jeu 60 fois par seconde
            if pygame.time.get_ticks() - last_update > 1000 / 60:
                last_update = pygame.time.get_ticks()
                if not self.logic_game.update():
                    self.restart()
                    running = False

                self.sync_obstacles()

                self.all_sprites.update(game_speed=self.logic_game.game_speed)

                screen.fill(WHITE)

                self.logic_game.machine_learning.neron_draw(pygame, screen, (SCREEN_WIDTH, SCREEN_HEIGHT))

                self.all_sprites.draw(screen)

                score_text = self.font.render(f'Score: {self.logic_game.score}', True, BLACK)
                ml_score_text = self.font.render(f'Score ML: {self.logic_game.ml_score}', True, BLACK)

                screen.blit(score_text, (10, 10))
                screen.blit(ml_score_text, (10, 25))
                screen.blit(self.generation_text, (10, 40))

                pygame.display.flip()
                await asyncio.sleep(0)  # Very important, and keep it 0


    def restart(self):
        self.all_sprites.empty()
        self.logic_game = self.machine_learning.get_game()
        self.dino = Dino(self.logic_game.dino)
        self.grounds_sprites = pygame.sprite.Group( [Ground(0), Ground(1)] )
        self.sunMoon = SunMoon(SCREEN_WIDTH - 100, 100)
        self.all_sprites.add(self.dino)
        self.all_sprites.add(self.grounds_sprites)
        self.all_sprites.add(self.sunMoon)

        self.generation_text = self.font.render(f'Generation: {self.machine_learning.generations_count}', True, BLACK)

        self.run()

if __name__ == '__main__':
    machine_learning = Logique.LogicSimulation(100,200)
    game = asyncio.run(Game(machine_learning))
    game.run()
    
