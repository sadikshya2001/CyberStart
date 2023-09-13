# config.py

class Config:
    def __init__(self):

        self._config = {}
        self.avatar_image_path = None
        self.username = None
        self.screen_width = 800  # Default screen width
        self.screen_height = 600  # Default screen height
        self.game_state = "PLAY_GAME"
        # Add any other attributes you need here

    def __getitem__(self, key):
        return self._config[key]

    def __setitem__(self, key, value):
        self._config[key] = value

    def __contains__(self, key):
        return key in self._config

    def get(self, key, default=None):
        return self._config.get(key, default)

    # Add a method to set the username
    def set_username(self, username):
        self.username = username

    # Add a method to get the username
    def get_username(self):
        return self.username

    # Method to set screen size
    def set_screen_size(self, width, height):
        self.screen_width = width
        self.screen_height = height

    # Method to get screen size
    def get_screen_size(self):
        return self.screen_width, self.screen_height
