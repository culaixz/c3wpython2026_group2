import pygame

class AudioManager:
    def __init__(self):
        # Initialize mixer just in case it hasn't been already
        if not pygame.mixer.get_init():
            pygame.mixer.init()
            
        # Define paths to your .mp3 assets
        self.menu_track = "MENU MUSIC.mp3"
        self.game_track = "GAMEPLAYAUDIO.mp3"
        
        # Track the active song state to prevent restarting a track that is already playing
        self.current_track = None

    def play_menu_music(self):
        # Plays the menu theme. Loops indefinitely
        if self.current_track != "menu":
            try:
                pygame.mixer.music.load(self.menu_track)
                pygame.mixer.music.set_volume(0.5)  # Set volume to 50%
                pygame.mixer.music.play(-1)          # -1 to loop forever
                self.current_track = "menu"
            except pygame.error as e:
                print(f"Could not load menu music: {e}")

    def play_gameplay_music(self):
        # Fades out menu music and transitions into the arena theme
        if self.current_track != "gameplay":
            try:
                # Fade out old track over 1000 milliseconds (1 second) for a smooth mix
                pygame.mixer.music.fadeout(1000)
                pygame.mixer.music.load(self.game_track)
                pygame.mixer.music.set_volume(0.4)  # Battle music can be slightly quieter
                pygame.mixer.music.play(-1)
                self.current_track = "gameplay"
            except pygame.error as e:
                print(f"Could not load gameplay music: {e}")

    def stop_music(self):
        # Stops all background tracks immediately
        pygame.mixer.music.stop()
        self.current_track = None
