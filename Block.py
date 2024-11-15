import pygame.draw

class Block:
    def __init__(self, x, y, width = 1, height = 1):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
    
    def draw(self, screen):
        pygame.draw.rect(screen, (0, 255, 0), (self.x, self.y, self.width, self.height))
    
    def collision_rect(self):
        return (self.x, self.y, self.width, self.height)