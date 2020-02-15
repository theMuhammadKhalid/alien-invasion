import pygame
import game_functions as gfn
from settings import Settings
from ship import Ship
from alien import Alien
from pygame.sprite import Group
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard

def run_game():
    #intialize game and create a screen object
    pygame.init()
    ai_settings = Settings()    
    screen = pygame.display.set_mode((ai_settings.screen_width,ai_settings.screen_height))
    real_ship = Ship(ai_settings, screen)
    pygame.display.set_caption("Alien Invasion")
    stats = GameStats(ai_settings)
    #Make a group to store bullets
    bullets = Group()
    #Make group of aliens
    aliens = Group()
    #Create a fleet of aliens
    gfn.create_fleet(ai_settings,screen,real_ship,aliens)
    #Make the play button
    play_button = Button(ai_settings,screen,"Play")
    #Create an instance to store game statistics and create a scoreboard
    sb = Scoreboard(ai_settings,screen,stats)

    #start the main loop for the game
    while True:
        #watch for events
        gfn.check_events(real_ship,ai_settings,screen,bullets,stats,sb,play_button,aliens)
        if stats.game_active:
            real_ship.update()
            gfn.update_bullets(ai_settings,screen,stats,sb,real_ship, aliens, bullets)
            gfn.update_aliens(ai_settings,stats,screen,real_ship,aliens,bullets,sb)
                
        #make the most recently drawn screen visible
        gfn.update_screen(ai_settings,screen,stats,sb,real_ship,aliens,bullets,play_button)
       

run_game()
