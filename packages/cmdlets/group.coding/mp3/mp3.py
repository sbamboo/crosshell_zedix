import os
try:
    from pydub import AudioSegment
    from pydub.playback import play
except:
    os.system("python3 -m pip install pydub")
    from pydub import AudioSegment
    from pydub.playback import play

sound = AudioSegment.from_file(f"{CSScriptRoot}{os.sep}file.mp3", format="mp3")
#play(sound)
