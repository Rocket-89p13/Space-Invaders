import pygame.mixer

class Sounds:
    def __init__(self):
        pygame.mixer.set_num_channels(8)
        self.main_theme_1 = None
        self.main_theme_2 = None
        self.main_theme_3 = None
        self.main_theme_4 = None
        self.main_theme = pygame.mixer.music.load('Resources/sounds/Space_Invaders_Music.ogg')
        self.player_shooting = pygame.mixer.Sound('Resources/sounds/shoot.wav')
        self.player_shooting.set_volume(0.50)
        self.player_dieing = pygame.mixer.Sound('Resources/sounds/player die.wav')
        self.player_dieing.set_volume(0.50)
        self.enemy_killed = pygame.mixer.Sound('Resources/sounds/invaderkilled.wav')
        self.enemy_killed.set_volume(0.50)
        self.ufo_channel = pygame.mixer.Channel(0)
        self.ufo_entered = pygame.mixer.Sound('Resources/sounds/ufo enter.wav')
        self.ufo_entered.set_volume(0.50)
        self.ufo_dieing = pygame.mixer.Sound('Resources/sounds/ufo down.wav')
        self.ufo_dieing.set_volume(0.50)

    def play_ufo_sound(self):
        self.ufo_channel.play(self.ufo_entered, loops=1)
    
    def ufo_sound_playing(self):
        return self.ufo_channel.get_busy()