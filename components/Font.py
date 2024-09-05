import pygame

class Font:

    def __init__(self, font, size, position):
        self.font = pygame.font.Font(font, size)
        self.position = position

    def render(self, text, antialias, color):
        return self.font.render(text, antialias, color)

    def get_size(self, text):
        return self.font.size(text)