"""This manages audio playback"""

import multiprocessing
from pathlib import Path
from .settings import settings


MUSIC_PATH = Path(__file__).parents[1] / 'assets' / 'music'


def audio_fn(song, play_audio, volume):
    """plays a song in loop
    ARGS:
        song: path to file
        play_audio: bool whether or not audio actually should be played
        volume: the sound volume as an int 0-100"""
    if not play_audio:
        return

    import playsound


    while True:
        playsound.playsound(str(MUSIC_PATH / song), volume)


class Audio:
    """Audio controler class"""

    def __init__(self):
        self.curr = None
        self.use_audio = True

    def start(self, song):
        """Starts playing a song
        ARGS:
            song: The song played"""
        self.curr = multiprocessing.Process(
            target=audio_fn,
            args=(
                song, settings("audio").val and self.use_audio,
                settings("volume").val
            )
        )
        self.curr.start()

    def switch(self, song):
        """Switched the played song
        ARGS:
            song: The song played"""
        self.kill()
        self.start(song)

    def kill(self):
        """Kills the running music"""
        self.curr.terminate()

audio = Audio()
