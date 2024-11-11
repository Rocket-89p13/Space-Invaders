import pygame.draw

class Bullet:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.white = (255, 255, 255)
        self.green = (0, 255, 0)
        self.red = (255, 0, 0)
        self.color = self.white
        self.vel_y = -12

    def update(self):
        self.y += self.vel_y

    def draw(self, screen):
        if 0 <= self.y <= 100:
            self.color = self.red
        elif 100 < self.y <= 700:
            self.color = self.white
        else:
            self.color = self.green
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
    
    def collision_rect(self):
        return (self.x, self.y, self.width, self.height)