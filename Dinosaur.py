import pygame
import Logique

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
        self.rect.x = self.logic.rect["x"]
        self.rect.y = self.logic.rect["y"]
        self.animation_index = 0
        self.animation_time = 0

    def update(self, **kwargs):

        self.animation_time += 1
        if self.animation_time % 10 == 0:
            self.animation_index = (self.animation_index + 1) % len(self.images)
            self.image = self.images[self.animation_index]

    def setX(self, x):
        self.rect.x = x 

    def setY(self,y):
        self.rect.y = y

# Classe Obstacle
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, logic):
        super().__init__()
        self.logic = logic
        self.tile_size_x = self.logic.size[self.logic.obstacles_id]["width"]
        self.tile_size_y = self.logic.size[self.logic.obstacles_id]["height"]
        self.offset_x = self.logic.size[self.logic.obstacles_id]["offset_x"]
        self.offset_y = self.logic.size[self.logic.obstacles_id]["offset_y"]
        self.image = tileset.subsurface((self.offset_x, self.offset_y, self.tile_size_x, self.tile_size_y))
        self.rect = self.image.get_rect()
        self.rect.x = self.logic.getX()
        self.rect.y = self.logic.getY()

    def update(self, **kwargs):
        self.logic.update(game_speed=kwargs.get("game_speed", 1))
        self.rect.x = self.logic.get_x()

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

# Classe Game
class Game:
    def __init__(self, machine_learning):
        self.machine_learning = machine_learning
        self.logic_game = self.machine_learning.get_game()
        self.all_sprites = pygame.sprite.Group()
        self.obstacles_sprites = pygame.sprite.Group()
        self.obstacles = []
        self.dino = Dino(self.logic_game.dino)
        self.all_sprites.add(self.dino)
        self.grounds_sprites = pygame.sprite.Group( [Ground(0), Ground(1)] )
        self.all_sprites.add(self.grounds_sprites)
        self.font = pygame.font.Font(None, 36)

    def sync_obstacles(self):
        current_obstacles = {obstacle.logic.id: obstacle for obstacle in self.obstacles_sprites}
        new_obstacles = {obstacle.id: obstacle for obstacle in self.logic_game.get_obstacles()}


        # Remove old obstacles
        for obstacle_id in list(current_obstacles.keys()):
            if obstacle_id not in new_obstacles:
                obstacle = current_obstacles[obstacle_id]
                self.obstacles_sprites.remove(obstacle)
                self.all_sprites.remove(obstacle)
                self.obstacles.remove(obstacle)

        # Add new obstacles
        for obstacle_id in new_obstacles:
            if obstacle_id not in current_obstacles:
                logic_obstacle = new_obstacles[obstacle_id]
                obstacle = Obstacle(logic_obstacle)
                self.obstacles_sprites.add(obstacle)
                self.all_sprites.add(obstacle)
                self.obstacles.append(obstacle)

    def run(self):
        clock = pygame.time.Clock()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()

            self.machine_learning.update()
            if not self.logic_game.update():
                self.logic_game = self.machine_learning.get_game()
            self.sync_obstacles()

            self.dino.update()
            self.dino.setX(self.logic_game.dino.getX())
            self.dino.setY(self.logic_game.dino.getY())

            self.grounds_sprites.update(game_speed=self.logic_game.game_speed)

            for obstacle_index in range(len(self.logic_game.get_obstacles())):
                self.obstacles[obstacle_index].setX(self.logic_game.get_obstacles()[obstacle_index].getX())
                self.obstacles[obstacle_index].setY(self.logic_game.get_obstacles()[obstacle_index].getY())


            screen.fill(WHITE)
            self.logic_game.MachineLearning.neron_draw(pygame, screen, (SCREEN_WIDTH, SCREEN_HEIGHT))
            self.all_sprites.draw(screen)

            score_text = self.font.render(f'Score: {self.logic_game.score}', True, BLACK)
            screen.blit(score_text, (10, 10))


            pygame.display.flip()

            if self.logic_game.collide():
                running = False

            clock.tick(60)  # Garde les FPS constants à 30
        self.restart()

    def restart(self):
        self.all_sprites.empty()
        self.obstacles_sprites.empty()
        self.dino = Dino(self.logic_game.dino)
        self.all_sprites.add(self.dino)
        self.logic_game = self.machine_learning.get_game()

        self.run()



if __name__ == '__main__':
    machine_learning = Logique.LogicSimulation(100,200)
    game = Game(machine_learning)
    game.run()
