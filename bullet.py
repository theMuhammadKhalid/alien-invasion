import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """A class to manage bullets fired from the ship"""

    def __init__(self,ai_settings,screen,real_ship):
        super().__init__()
        self.screen = screen
        #create a bullet rect at (0,0) and set the current position
        self.rect = pygame.Rect(0,0,ai_settings.bullet_width,ai_settings.bullet_height)
        self.rect.centerx = real_ship.rect.centerx
        self.rect.top = real_ship.rect.top

        #store the bullets positon as a decimal value
        self.y = float(self.rect.y)
        self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor


    def update(self):
        """Move the bullet up the screen"""
        #update the decimal position of bullet
        self.y -= self.speed_factor 
        #update the rect position
        self.rect.y = self.y

    def draw_bullets(self):
        """Draw the bullet to the screen"""
        pygame.draw.rect(self.screen,self.color,self.rect)
        
