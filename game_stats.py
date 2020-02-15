class GameStats():
    """Track statistics for Alien Invasion"""

    def __init__(self,ai_settings):
        self.ai_settings = ai_settings
        self.game_active = False
        #High score should never be reset
        self.high_score = 0
        self.reset_stats()

    def reset_stats(self):
        self.ship_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1 
