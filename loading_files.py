import os
from pydub import AudioSegment
from pydub.playback import play
import random
import tempfile
import pyglet


# Change le dossier temporaire utilisé par pydub
tempfile.tempdir = os.path.join(os.getcwd(), "temp")
os.makedirs(tempfile.tempdir, exist_ok=True)

path = "C:\\Users\\Tom\\Music"
music_paths = []
def loadingFiles(path):
    for dossier_actuel, sous_dossiers, fichiers in os.walk(path):

        for fichier in fichiers:

            if fichier.lower().endswith(".mp3"):
                full_path = os.path.join(dossier_actuel, fichier)
                music_paths.append(full_path)
loadingFiles(path)

audio_path = random.choice(music_paths)
print(audio_path)

son = pyglet.media.load(audio_path, streaming=False)
son.play()
pyglet.app.run()

print(audio)