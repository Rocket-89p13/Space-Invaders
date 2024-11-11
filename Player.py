class Player:
    def __init__(self, image, x, y):
        self.image = image
        self.x = x
        self.y = y
        self.width = image.get_width()
        self.height = image.get_height()
        self.vel_x = 0
        self.score = 0
        self.lives = 3
    
    def increase_score(self, points):
        self.score += points

    def update(self):
        self.x += self.vel_x

        if(self.x <= 0):
            self.x = 0
        if(self.x > 900 - self.width):
            self.x = 900 - self.width
    
    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
    
    def collision_rect(self):
        return (self.x, self.y, self.width, self.height)