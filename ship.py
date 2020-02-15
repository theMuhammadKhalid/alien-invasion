import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    def __init__(self,ai_settings,screen):
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        
        #load the image and get its rectangle
        self.image = pygame.image.load("images\ship.bmp")
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        #start each new ship at the bottom center of the screen
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        #Movement Flag
        self.moving_right = False
        self.moving_left = False

        #store a decimal vlaue for the ship's center
        self.center = float(self.rect.centerx)

    def blitme(self):
        """Draw the ship at its current location"""
        self.screen.blit(self.image,self.rect)

    def update(self):
        """Update the ship's center value not the rect"""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            
            self.center += self.ai_settings.ship_speed_factor
            
        elif self.moving_left and self.rect.left > 0:
            
            self.center -= self.ai_settings.ship_speed_factor

        #update rect object from self.center
        self.rect.centerx = self.center

    def center_ship(self):
        self.center = self.screen_rect.centerx
        
