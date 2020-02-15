from bullet import Bullet
from alien import Alien
from time import sleep
import sys, pygame

def check_KEYDOWN_events(event,ai_settings,screen,real_ship,bullets):
    if event.key == pygame.K_RIGHT:
        real_ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        real_ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings,screen,real_ship,bullets)
    elif event.key == pygame.K_q:
        sys.exit()
        
def check_KEYUP_events(event,real_ship):
    if event.key == pygame.K_RIGHT:
        real_ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        real_ship.moving_left = False

def check_events(real_ship,ai_settings,screen,bullets,stats,sb,play_button,aliens):
    """Respond to keypresses and mouse events"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()            
        elif event.type == pygame.KEYDOWN:
            check_KEYDOWN_events(event,ai_settings,screen,real_ship,bullets)     
        elif event.type == pygame.KEYUP:
            check_KEYUP_events(event,real_ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings,screen,stats,sb,play_button,real_ship,aliens,bullets,mouse_x,mouse_y)

def check_play_button(ai_settings,screen,stats,sb,play_button,real_ship,aliens,bullets,mouse_x,mouse_y):
    button_clicked = play_button.rect.collidepoint(mouse_x,mouse_y)
    if button_clicked and not stats.game_active:
        ai_settings.initialize_dynamic_settings()
        stats.game_active = True
        #Reset the scoreboard images
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ship()
        
        stats.reset_stats()
        aliens.empty()
        bullets.empty()
        create_fleet(ai_settings,screen,real_ship,aliens)
        real_ship.center_ship()
        pygame.mouse.set_visible(False)
                
def update_screen(ai_settings,screen,stats,sb,real_ship,aliens,bullets,play_button):
     screen.fill(ai_settings.bg_color)
     sb.show_score()
     #Redraw all bullets behind the ship and aliens
     for bullet in bullets.sprites():
         bullet.draw_bullets()
     real_ship.blitme()
     aliens.draw(screen)
     #Draw the play button if the game is inactive
     if not stats.game_active:
         play_button.draw_button()
         
     pygame.display.flip()
    

def update_bullets(ai_settings,screen,stats,sb,real_ship, aliens, bullets):
    """Update the position of bullets and get rid of old bullets"""
    bullets.update()
    for bullet in  bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_alien_collisions(ai_settings,screen,stats,sb,real_ship,aliens,bullets)

    

def check_bullet_alien_collisions(ai_settings,screen,stats,sb, real_ship,aliens,bullets):
    """Check for any bullets that have hit aliens.
       If so, get rid of the bullet and the alien"""
    collisions = pygame.sprite.groupcollide(bullets,aliens,True,True)
    if collisions:
        for aliens in collisions.values():
            stats.score += (ai_settings.alien_points*len(aliens))
            sb.prep_score()
        check_high_score(stats, sb)
    
    if len(aliens) == 0:
        #Destroy existing bullets,speed up and create new fleet
        bullets.empty()
        ai_settings.increase_speed()
        create_fleet(ai_settings,screen,real_ship,aliens)
        #If the entire fleet is destroyed start a new level
        stats.level += 1
        sb.prep_level()
    

def fire_bullet(ai_settings,screen,real_ship,bullets):
    #create a new bullet and add it to the bullets group
    new_bullet = Bullet(ai_settings,screen,real_ship)
    bullets.add(new_bullet)

def create_fleet(ai_settings,screen,real_ship,aliens):
    """Create a full fleet of aliens"""
    alien = Alien(ai_settings,screen) #this alien is not part of fleet
    
    number_aliens_x = get_number_aliens_x(ai_settings,alien.rect.width)
    number_rows = get_number_rows(ai_settings,real_ship.rect.height,alien.rect.height)

    #Create a fleet of aliens
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings,screen,aliens,alien_number,row_number)
    
def get_number_aliens_x(ai_settings,alien_width):
    available_space_x = ai_settings.screen_width-2*alien_width
    number_aliens_x = int(available_space_x/(2*alien_width))
    return number_aliens_x

def get_number_rows(ai_settings,ship_height,alien_height):
    available_space_y = (ai_settings.screen_height-(7*alien_height)-2*ship_height)
    number_rows = int(available_space_y/(2*alien_height))
    return number_rows

def create_alien(ai_settings,screen,aliens,alien_number,row_number):
    alien = Alien(ai_settings,screen) 
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.y = (alien.rect.height+2*alien.rect.height*row_number)+70
    alien.rect.x = alien.x
    aliens.add(alien)

def update_aliens(ai_settings,stats,screen,real_ship,aliens,bullets,sb):
    #update the position of all aliens in the fleet
    check_fleet_edges(ai_settings,aliens)
    aliens.update()
    check_aliens_bottom(ai_settings,stats,screen,real_ship,aliens,bullets,sb)
    if pygame.sprite.spritecollideany(real_ship,aliens):
        ship_hit(ai_settings,stats,screen,real_ship,aliens,bullets,sb)

def check_fleet_edges(ai_settings, aliens):
    """Respond appropriately if any
       aliens have reached an edge"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings,aliens)
            break

def change_fleet_direction(ai_settings,aliens):
    """Drop the entire fleet an change fleet direction"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def ship_hit(ai_settings,stats,screen,real_ship,aliens,bullets,sb):
    """Respond to ship hit by alien"""
    if stats.ship_left > 0:
        #Decrement ship left
        stats.ship_left -= 1
        #Empty the list of aliens and bullets
        aliens.empty()
        bullets.empty()
        #Create a new fleet and center the ship
        create_fleet(ai_settings,screen,real_ship,aliens)
        real_ship.center_ship()
        #Update scoreboard
        sb.prep_ship()
        #Pause
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)
        
    

def check_aliens_bottom(ai_settings,stats,screen,real_ship,aliens,bullets,sb):
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_settings,stats,screen,real_ship,aliens,bullets,sb)
            break

def check_high_score(stats, sb):
    """Check to see if there's a new high score"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()
    
    

    
