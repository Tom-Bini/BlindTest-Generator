import os
import shutil
import subprocess

def build_exe():
    # Créer le dossier dist s'il n'existe pas
    if not os.path.exists('dist'):
        os.makedirs('dist')
    
    # Copier le logo dans le dossier dist
    if os.path.exists('logo.ico'):
        shutil.copy('logo.ico', 'dist/logo.ico')
    
    # Créer l'exécutable avec PyInstaller
    subprocess.run([
        'pyinstaller',
        '--noconfirm',
        '--onefile',
        '--windowed',
        '--icon=logo.ico',
        '--add-data=logo.ico;.',
        '--name=BlindTest',
        'main.py'
    ])
    
    # Copier les fichiers de configuration dans le dossier dist
    if os.path.exists('config.json'):
        shutil.copy('config.json', 'dist/config.json')
    if os.path.exists('music_cache.json'):
        shutil.copy('music_cache.json', 'dist/music_cache.json')
    
    print("L'exécutable a été créé avec succès dans le dossier dist/")

if __name__ == "__main__":
    build_exe() 