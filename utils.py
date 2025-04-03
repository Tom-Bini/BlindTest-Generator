import os
import tkinter as tk
from tkinter import font
from PIL import Image, ImageTk
import io
from mutagen import File
from mutagen.id3 import ID3

def load_font():
    # Chemin vers le dossier des polices dans Windows
    font_path = os.path.join(os.environ['WINDIR'], 'Fonts')
    roboto_fonts = {
        'regular': 'Roboto-Regular.ttf',
        'bold': 'Roboto-Bold.ttf',
        'medium': 'Roboto-Medium.ttf'
    }
    
    # Vérifier si Roboto est déjà installé
    available_fonts = [f.lower() for f in font.families()]
    if 'roboto' in available_fonts:
        return 'Roboto'
        
    return 'Helvetica'  # Police de fallback si Roboto n'est pas disponible

def load_title_font():
    # Vérifier si Luckiest Guy est déjà installé
    available_fonts = [f.lower() for f in font.families()]
    if 'luckiest guy' in available_fonts:
        return 'Luckiest Guy'
    else:
        print("La police Luckiest Guy n'est pas installée sur votre système.")
        print("Veuillez l'installer depuis Google Fonts : https://fonts.google.com/specimen/Luckiest+Guy")
        
    return 'Arial'  # Police de fallback si Luckiest Guy n'est pas disponible

def get_metadata(file_path):
    try:
        # Récupération des métadonnées
        title = None
        artist = None
        genre = None
        photo = None
        
        # Essayer d'abord avec ID3 pour les MP3
        try:
            audio = ID3(file_path)
            if audio:
                # Récupération du titre, artiste et genre
                title = str(audio.get('TIT2', ''))
                artist = str(audio.get('TPE1', ''))
                genre = str(audio.get('TCON', ''))
                
                # Récupération de la pochette
                for tag in audio.values():
                    if tag.FrameID == 'APIC':
                        image_data = tag.data
                        image = Image.open(io.BytesIO(image_data))
                        # Redimensionner l'image à 300x300 en conservant les proportions
                        image.thumbnail((300, 300), Image.Resampling.LANCZOS)
                        # Créer une nouvelle image carrée avec fond gris
                        background = Image.new('RGB', (300, 300), '#282828')
                        # Centrer l'image sur le fond
                        offset = ((300 - image.size[0]) // 2, (300 - image.size[1]) // 2)
                        background.paste(image, offset)
                        photo = ImageTk.PhotoImage(background)
                        break
        except:
            # Si ce n'est pas un MP3 avec ID3, essayer avec File
            audio = File(file_path)
            if audio is not None and hasattr(audio, 'tags'):
                # Pour les fichiers FLAC
                title = audio.tags.get('TITLE', [None])[0]
                artist = audio.tags.get('ARTIST', [None])[0]
                genre = audio.tags.get('GENRE', [None])[0]
                
                # Pour les fichiers FLAC, chercher dans les métadonnées Vorbis
                if 'METADATA_BLOCK_PICTURE' in audio.tags:
                    cover = audio.tags['METADATA_BLOCK_PICTURE'][0].data
                    image = Image.open(io.BytesIO(cover))
                    # Redimensionner l'image à 300x300 en conservant les proportions
                    image.thumbnail((300, 300), Image.Resampling.LANCZOS)
                    # Créer une nouvelle image carrée avec fond gris
                    background = Image.new('RGB', (300, 300), '#282828')
                    # Centrer l'image sur le fond
                    offset = ((300 - image.size[0]) // 2, (300 - image.size[1]) // 2)
                    background.paste(image, offset)
                    photo = ImageTk.PhotoImage(background)
        
        return title, artist, genre, photo
    except Exception as e:
        print(f"Erreur lors de la lecture des métadonnées: {str(e)}")
        return None, None, None, None

def get_file_info(file_path):
    try:
        stat = os.stat(file_path)
        return {
            'size': stat.st_size,
            'mtime': stat.st_mtime,
            'ctime': stat.st_ctime
        }
    except:
        return None 