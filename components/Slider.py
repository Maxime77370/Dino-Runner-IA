import pygame

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

class Slider:
    def __init__(self, screen, x, y, width, height, min_val, max_val, initial_val, type=int):
        self.screen = screen
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.min_val = min_val
        self.max_val = max_val
        self.value = initial_val
        self.type = type
        self.slider_width = width - 20
        self.slider_x = self.x + 10 + (self.slider_width * (self.value - self.min_val) / (self.max_val - self.min_val))

    def draw(self):
        pygame.draw.rect(self.screen, BLACK, (self.x, self.y, self.width, self.height), 2)
        pygame.draw.rect(self.screen, RED, (self.slider_x, self.y, 20, self.height))

    def update(self, mouse_pos):
        if self.x <= mouse_pos[0] <= self.x + self.width and self.y <= mouse_pos[1] <= self.y + self.height:
            self.slider_x = mouse_pos[0] - 10
            if self.slider_x < self.x + 10:
                self.slider_x = self.x + 10
            elif self.slider_x > self.x + self.width - 10:
                self.slider_x = self.x + self.width - 10
            self.value = self.min_val + (self.slider_x - (self.x + 10)) * (self.max_val - self.min_val) / self.slider_width
        
        return self.type(self.value)
    
    def setPosition(self, x,y, origin = "top-left"):
        if origin == "top-left":
            self.x = x
            self.y = y
        elif origin == "top-right":
            self.x = x - self.width
            self.y = y
        elif origin == "bottom-left":
            self.x = x
            self.y = y - self.height
        elif origin == "bottom-right":
            self.x = x - self.width
            self.y = y - self.height
        elif origin == "center":
            self.x = x - self.width // 2
            self.y = y - self.height // 2

        self.slider_x = self.x + 10 + (self.slider_width * (self.value - self.min_val) / (self.max_val - self.min_val))

    def getRect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)