class Enemy: #this should be abstract class but abc in python are stupid

    def __init__(self, image, image2, x, y, type, points):
        self.images = [image, image2]
        self.current_image = 0
        self.anim_speed = 0.02
        self.image = self.images[self.current_image]
        self.x = x
        self.y = y
        self.width = image.get_width()
        self.height = image.get_height()
        self.vel_x = 0.1
        self.type = type
        self.points = points
        
    def update(self):
        self.x += self.vel_x

        self.current_image += self.anim_speed
        if self.current_image >= len(self.images):
            self.current_image = 0
        self.image = self.images[int(self.current_image)]

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
    
    def collision_rect(self):
        return (self.x, self.y, self.width, self.height)