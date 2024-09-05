import pygame
from components.Slider import Slider
from components.Font import Font
from Dinosaur import Game
from Logique import LogicSimulation

# Dimensions de la fenêtre
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Initialisation de Pygame
pygame.init()

# Configuration de la fenêtre
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Dino Runner')

class Menu:

    """
    Classe Menu permettant de gérer le menu du jeu.
    - On peut choisir le nombre de neurones par couche.
    - On peut choisir le nombre de couche.
    - On peut choisir le nombre de génération.
    - On peut choisir le nombre d'enfant par génération.
    - On peut choisir le taux de mutation.
    """

    def __init__(self):
        self.size = (1000, 600)
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption("ML_GAME")
        pygame.display.set_allow_screensaver(True)
        self.clock = pygame.time.Clock()
        self.speed = 100

        self.font = pygame.font.SysFont(None, 40)
        self.menu_options = [
            {"id": 0, "text": "Nombre de neurones par couche", "min": 1, "max": 100, "value": 2, "type": int},
            {"id": 1, "text": "Nombre de couches", "min": 0, "max": 100, "value": 1, "type": int},
            {"id": 2, "text": "Nombre de générations", "min": 1, "max": 500, "value": 10, "type": int},
            {"id": 3, "text": "Nombre d'enfants par génération", "min": 1, "max": 500, "value": 50, "type": int},
            {"id": 4, "text": "Taux de mutation", "min": 0, "max": 1, "value": 0.5, "type": float},
            {"id": 5, "text": "Commencer le jeu", "action": self.start_game, "type": "function"}
        ]
        self.sliders = [
            {"id": i, "slider": Slider(self.screen, 0, 0, 300, 20, option["min"], option["max"], option["value"], option["type"])}
            if i < len(self.menu_options) - 1 else None
            for i, option in enumerate(self.menu_options)
        ]

        self.Loop()

    def Loop(self):
        """
        Boucle principale du menu.
        """
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    for slider in self.sliders:
                        if slider:
                            self.menu_options[slider["id"]]["value"] = slider["slider"].update(mouse_pos)

                    # Check if the "Commencer le jeu" button is clicked
                    if self.start_button_rect.collidepoint(mouse_pos):
                        self.menu_options[5]["action"]()

            self.Draw()
            self.clock.tick(self.speed)

        pygame.quit()

    def Draw(self):
        """
        Dessine le menu.
        """
        # Add a background color or image
        self.screen.fill((135, 206, 235))  # Sky blue background color

        # Add a title to the menu
        title_font = pygame.font.SysFont(None, 75)
        title_surface = title_font.render("Dino Runner - Menu", True, BLACK)
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 50))
        self.screen.blit(title_surface, title_rect)

        # Draw the menu options and sliders
        for i, option in enumerate(self.menu_options):
            if self.sliders[i]:
                color = BLACK
                text_surface = self.font.render(option["text"], True, color)
                text_rect = text_surface.get_rect(center=(0, SCREEN_HEIGHT // 2 - 100 + i * 50))
                text_rect.x = 10
                self.screen.blit(text_surface, text_rect)

                # Positionnement et affichage du slider
                self.sliders[i]["slider"].setPosition(SCREEN_WIDTH - self.sliders[i]["slider"].width // 2 - 10,
                                                    SCREEN_HEIGHT // 2 - 100 + i * 50, origin="center")
                self.sliders[i]["slider"].draw()

                # Récupération du rectangle du slider pour le positionnement de la valeur
                slider_rect = self.sliders[i]["slider"].getRect()

                # Positionnement et affichage de la valeur du slider à gauche du slider
                slider_value_surface = self.font.render(str(option["value"]), True, color)
                slider_value_rect = slider_value_surface.get_rect(center=(slider_rect.x - 50,  # 50 pixels à gauche du slider
                                                                        SCREEN_HEIGHT // 2 - 100 + i * 50))
                self.screen.blit(slider_value_surface, slider_value_rect)
            elif option["type"] == "function":
                self.start_button_rect = pygame.Rect(0, 0, 300, 50)
                self.start_button_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100)
                pygame.draw.rect(self.screen, RED, self.start_button_rect)
                start_button_surface = self.font.render(option["text"], True, BLACK)
                start_button_rect = start_button_surface.get_rect(center=self.start_button_rect.center)
                self.screen.blit(start_button_surface, start_button_rect)

        pygame.display.flip()

    def start_game(self):
        """
        Démarre le jeu avec les paramètres choisis par l'utilisateur.
        """
        print("Starting game with the following parameters:")
        print (f"Nombre de neurones par couche: {self.menu_options[0]['value']}")
        print (f"Nombre de couches: {self.menu_options[1]['value']}")
        print (f"Nombre de générations: {self.menu_options[2]['value']}")
        print (f"Nombre d'enfants par génération: {self.menu_options[3]['value']}")
        print (f"Taux de mutation: {self.menu_options[4]['value']}")
        machine_learning = LogicSimulation(self.menu_options[2]["value"], self.menu_options[3]["value"], [2] + [self.menu_options[0]["value"] for i in range(self.menu_options[1]["value"])] + [1], self.menu_options[4]["value"])
        game = Game(machine_learning)
        game.run()

if __name__ == "__main__":
    Menu()
