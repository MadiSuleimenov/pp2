import pygame
import os

class MusicPlayer:
    def __init__(self):
        pygame.mixer.init()

        self.folder = os.path.join(os.path.dirname(__file__), "music")
        self.playlist = []
        self.index = 0
        self.status = "Stopped"

        self.load_music()

    def load_music(self):
        if not os.path.exists(self.folder):
            print("music folder not found")
            return

        for file in os.listdir(self.folder):
            if file.lower().endswith((".mp3", ".wav")):
                self.playlist.append(os.path.join(self.folder, file))

    def play(self):
        if not self.playlist:
            return

        pygame.mixer.music.load(self.playlist[self.index])
        pygame.mixer.music.play()
        self.status = "Playing"

    def stop(self):
        pygame.mixer.music.stop()
        self.status = "Stopped"

    def next(self):
        self.index = (self.index + 1) % len(self.playlist)
        self.play()

    def prev(self):
        self.index = (self.index - 1) % len(self.playlist)
        self.play()

    def current(self):
        if not self.playlist:
            return "No music"
        return os.path.basename(self.playlist[self.index])

    def get_progress(self):
        pos = pygame.mixer.music.get_pos() / 1000  # секунды
        return min(pos / 180, 1)  # условно 3 мин трек