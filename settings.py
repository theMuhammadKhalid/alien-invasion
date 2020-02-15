class Settings():
    """Settings for Alien Invasion"""

    def __init__(self):
        #screen settings
        self.screen_width = 1000
        self.screen_height = 600
        self.bg_color = (230,230,230)
        #Ship settings    
        self.ship_limit = 3
        #Bullet Settings
        self.bullet_speed_factor = 2
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60,60,60)
        #Alien Settings
        self.alien_speed_factor = 0.6
        self.fleet_drop_speed = 10

        #Scoring
        self.alien_points = 50
        #How quickly the alien point value increase
        self.score_scale = 1.5

        self.speedup_scale = 1.1
        self.initialize_dynamic_settings()     


    def initialize_dynamic_settings(self):
        #Initialize settings that change throughout the game
        self.ship_speed_factor = 2
        self.bullet_speed_factor = 2
        self.alien_speed_factor = 0.6
        #1 for right,-1 for left
        self.fleet_direction = 1

    def increase_speed(self):
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.aliens_points = int(self.alien_points * self.score_scale)
        
        
    
