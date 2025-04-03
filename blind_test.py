import os
import random
import pygame
from mutagen import File
from mutagen.id3 import ID3
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk, messagebox, font, filedialog
import io
import threading
import time
import json
from datetime import datetime
import math
import ctypes

from buttons import CircleButton, RoundedButton
from utils import load_font, load_title_font, get_metadata, get_file_info
from config import Config

class BlindTest:
    def __init__(self, root):
        self.root = root
        self.config = Config()
        
        # Définir l'ID de l'application pour Windows
        try:
            icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logo.ico")
            # Définir l'ID unique de l'application
            myappid = "com.blindtest.app"
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
            # Charger et appliquer l'icône
            self.root.iconbitmap(default=icon_path)
            # Forcer l'icône pour la barre des tâches
            self.root.tk.call('wm', 'iconphoto', self.root._w, tk.PhotoImage(file=icon_path.replace('.ico', '.png')))
        except Exception as e:
            print(f"Erreur lors de la définition de l'icône: {str(e)}")
            
        self.root.title("Blind Test Musical")
        self.root.geometry("994x700")
        self.root.configure(bg='#121212')
        self.root.resizable(False, False)
        
        # Charger et appliquer le logo personnalisé
        try:
            icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logo.ico")
            self.root.iconbitmap(icon_path)
        except Exception as e:
            print(f"Erreur lors du chargement du logo: {str(e)}")
        
        # Charger la police
        self.font_family = load_font()
        self.title_font = load_title_font()
        
        # Initialisation de pygame mixer
        pygame.mixer.init()
        
        # Variables pour le volume
        self.volume = 0.7
        self.volume_var = tk.DoubleVar(value=70)
        # Initialiser le volume au démarrage
        pygame.mixer.music.set_volume(self.volume)
        
        # Variables pour la progression
        self.progress_var = tk.DoubleVar(value=0)
        self.duration = 0
        self.progress_thread = None
        
        # Liste des fichiers musicaux et des genres
        self.music_files = []
        self.genres = set()
        self.current_song = None
        self.is_playing = False
        self.current_thread = None
        self.selected_genre = tk.StringVar(value="Tous les genres")
        
        # Variables pour la durée de l'extrait
        self.selected_duration = tk.IntVar(value=4)  # Index par défaut (5 secondes)
        
        # Variables pour la lecture complète
        self.is_full_song = False
        self.extract_thread = None
        self.full_song_thread = None
        
        # Charger la configuration
        self.config.load_config()
        
        # Style
        self.style = ttk.Style()
        
        # Configuration du style pour le Scale
        self.style.configure('Spotify.Horizontal.TScale',
                           background='#121212',
                           troughcolor='#535353',
                           sliderthickness=20)

        # Option pour le style des menus déroulants
        self.root.option_add('*TCombobox*Listbox.background', '#282828')
        self.root.option_add('*TCombobox*Listbox.foreground', 'white')
        self.root.option_add('*TCombobox*Listbox.selectBackground', '#404040')
        self.root.option_add('*TCombobox*Listbox.selectForeground', 'white')
        self.root.option_add('*TCombobox*Listbox.font', (self.font_family, 14))
        
        # Création de l'interface
        self.create_interface()
        
        # Chargement des fichiers musicaux
        self.load_music_files()

    def choose_music_directory(self):
        """Ouvre une boîte de dialogue pour choisir le dossier de musique"""
        directory = filedialog.askdirectory(
            title="Choisir le dossier contenant les musiques",
            initialdir=self.config.music_dir
        )
        if directory:
            self.config.music_dir = directory
            self.config.save_config()
            self.load_music_files()

    def toggle_play_pause(self):
        """Démarre la lecture de la musique"""
        if not self.is_playing:
            self.play_song()

    def create_interface(self):
        # Frame principale
        main_frame = tk.Frame(self.root, bg='#121212')
        main_frame.pack(fill='both', expand=True)
        
        # Frame pour le contenu principal
        self.content_main_frame = tk.Frame(main_frame, bg='#121212')
        self.content_main_frame.pack(fill='both', expand=True)
        self.content_main_frame.grid_rowconfigure(0, weight=1)
        
        # Barre latérale gauche avec coins arrondis à droite
        sidebar = tk.Frame(self.content_main_frame, bg='#000000', width=300)
        sidebar.grid(row=0, column=0, sticky='nsew')
        sidebar.grid_propagate(False)
        
        # Frame pour le logo et le titre
        logo_frame = tk.Frame(sidebar, bg='#000000')
        logo_frame.pack(pady=30)
        
        # Charger et afficher le logo
        try:
            logo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logo.png")
            logo_image = Image.open(logo_path)
            # Redimensionner le logo à une taille appropriée (par exemple 40x40)
            logo_image = logo_image.resize((40, 40), Image.Resampling.LANCZOS)
            logo_photo = ImageTk.PhotoImage(logo_image)
            logo_label = tk.Label(logo_frame,
                                image=logo_photo,
                                bg='#000000')
            logo_label.image = logo_photo  # Garder une référence
            logo_label.pack(side='left', padx=(0, 10))
        except Exception as e:
            print(f"Erreur lors du chargement du logo: {str(e)}")
            # En cas d'erreur, afficher un symbole de musique
            logo_label = tk.Label(logo_frame,
                                text="♪",
                                font=(self.font_family, 36),
                                fg='#1DB954',
                                bg='#000000')
            logo_label.pack(side='left', padx=(0, 10))
        
        # Titre
        title_label = tk.Label(logo_frame,
                             text="BLIND TEST",
                             font=(self.title_font, 36, 'bold'),
                             fg='#1DB954',
                             bg='#000000')
        title_label.pack(side='left')
        
        # Séparateur horizontal
        separator = tk.Frame(sidebar, bg='#404040', height=1, width=200)
        separator.pack(pady=10)
        
        # Menu des genres
        genre_frame = tk.Frame(sidebar, bg='#000000')
        genre_frame.pack(fill='x', padx=40, pady=30)
        
        # Bouton pour choisir le dossier de musique
        folder_button = RoundedButton(genre_frame,
                                    text="Choisir le dossier",
                                    command=self.choose_music_directory,
                                    width=200,
                                    height=40,
                                    corner_radius=20,
                                    color='#404040',
                                    hover_color='#505050',
                                    fg='white',
                                    font=(self.font_family, 12))
        folder_button.pack(pady=(0, 15))
        
        # Afficher le chemin actuel
        self.path_label = tk.Label(genre_frame,
                                 text=f"Dossier : {os.path.basename(self.config.music_dir)}",
                                 font=(self.font_family, 12),
                                 fg='#B3B3B3',
                                 bg='#000000',
                                 wraplength=200)
        self.path_label.pack(pady=(0, 15))
        
        # Séparateur horizontal
        separator2 = tk.Frame(genre_frame, bg='#404040', height=1, width=200)
        separator2.pack(pady=15)
        
        genre_label = tk.Label(genre_frame,
                             text="Genre musical",
                             font=(self.font_family, 16, 'bold'),
                             fg='white',
                             bg='#000000')
        genre_label.pack(anchor='center', pady=15)
        
        self.genre_menu = ttk.Combobox(genre_frame,
                                     textvariable=self.selected_genre,
                                     state='readonly',
                                     width=25,
                                     font=(self.font_family, 14))
        self.genre_menu.pack(pady=15)
        
        # Créer le bouton Appliquer avec des coins arrondis
        apply_button = RoundedButton(genre_frame,
                                   text="Appliquer",
                                   command=self.apply_genre_filter,
                                   width=200,
                                   height=50,
                                   corner_radius=25,
                                   color='#1DB954',
                                   hover_color='#1ed760',
                                   fg='white',
                                   font=(self.font_family, 14))
        apply_button.pack(pady=15)
        
        # Séparateur horizontal
        separator3 = tk.Frame(genre_frame, bg='#404040', height=1, width=200)
        separator3.pack(pady=15)
        
        # Ajout du menu pour la durée de l'extrait
        duration_label = tk.Label(genre_frame,
                                text="Durée de l'extrait (secondes)",
                                font=(self.font_family, 16, 'bold'),
                                fg='white',
                                bg='#000000')
        duration_label.pack(anchor='center', pady=(15, 0))
        
        # Frame pour le slider de durée
        duration_slider_frame = tk.Frame(genre_frame, bg='#000000')
        duration_slider_frame.pack(fill='x', pady=15)
        
        # Valeurs possibles pour la durée
        self.duration_values = [0.1, 0.5, 1, 2, 5, 10, 15, 20, 30]
        
        # Créer le slider de durée
        self.duration_slider = ttk.Scale(duration_slider_frame,
                                       from_=0,
                                       to=8,  # 9 valeurs (0 à 8)
                                       orient='horizontal',
                                       variable=self.selected_duration,
                                       command=self.update_duration,
                                       style='Spotify.Horizontal.TScale',
                                       length=200)
        self.duration_slider.pack(fill='x')
        
        # Label pour afficher la valeur actuelle
        self.duration_value_label = tk.Label(duration_slider_frame,
                                           text="5 s",
                                           font=(self.font_family, 12),
                                           fg='#B3B3B3',
                                           bg='#000000')
        self.duration_value_label.pack(pady=(5, 0))
        
        # Définir la valeur par défaut (5 secondes = index 4)
        self.duration_slider.set(4)
        self.selected_duration.set(4)
        
        # Zone principale
        content_frame = tk.Frame(self.content_main_frame, bg='#121212')
        content_frame.grid(row=0, column=1, sticky='nsew')
        content_frame.grid_rowconfigure(1, weight=1)
        content_frame.grid_columnconfigure(0, weight=1)
        
        # Zone de la pochette
        self.cover_frame = tk.Frame(content_frame, bg='#121212', width=400, height=400)
        self.cover_frame.grid(row=1, column=0, pady=40)
        self.cover_frame.grid_propagate(False)
        
        # Créer une pochette par défaut
        self.default_cover = tk.Frame(self.cover_frame, bg='#282828', width=300, height=300)
        self.default_cover.place(relx=0.5, rely=0.5, anchor='center')
        
        # Icône de musique par défaut
        self.music_icon = tk.Label(self.default_cover,
                                 text="♪",
                                 font=(self.font_family, 48),
                                 fg='#404040',
                                 bg='#282828')
        self.music_icon.place(relx=0.5, rely=0.5, anchor='center')
        
        # Label pour le décompte (initialement caché)
        self.countdown_label = tk.Label(self.cover_frame,
                                      text="",
                                      font=(self.title_font, 120, 'bold'),
                                      fg='#1DB954',
                                      bg='#282828',
                                      width=1,
                                      height=1)
        
        # Frame pour contenir le décompte avec la même taille que la pochette
        self.countdown_container = tk.Frame(self.cover_frame,
                                         bg='#282828',
                                         width=300,
                                         height=300)
        
        # Label pour le décompte dans le container
        self.countdown_label = tk.Label(self.countdown_container,
                                      text="",
                                      font=(self.title_font, 120, 'bold'),
                                      fg='#1DB954',
                                      bg='#282828')
        self.countdown_label.place(relx=0.5, rely=0.5, anchor='center')
        
        self.album_cover_label = tk.Label(self.cover_frame,
                                        bg='#282828')
        self.album_cover_label.place(relx=0.5, rely=0.5, anchor='center')
        
        # Zone de réponse avec hauteur fixe
        answer_frame = tk.Frame(content_frame, 
                              bg='#121212',
                              width=600,
                              height=60)
        answer_frame.grid(row=2, column=0, pady=10)
        answer_frame.grid_propagate(False)
        answer_frame.grid_columnconfigure(0, weight=1)
        
        self.answer_label = tk.Label(answer_frame,
                                   text="Cliquez sur Play pour commencer !",
                                   font=(self.font_family, 16),
                                   fg='#B3B3B3',
                                   bg='#121212',
                                   justify='center',
                                   wraplength=580)
        self.answer_label.grid(row=0, column=0)
        
        # Frame pour les contrôles
        control_frame = tk.Frame(content_frame, bg='#121212')
        control_frame.grid(row=3, column=0, sticky='ew', padx=40, pady=(10, 5))  # Réduire le padding en bas
        
        # Centrer les contrôles
        control_frame.grid_columnconfigure(0, weight=1)
        control_frame.grid_columnconfigure(2, weight=1)
        
        # Frame pour les boutons principaux (au centre)
        buttons_frame = tk.Frame(control_frame, bg='#121212')
        buttons_frame.grid(row=0, column=1)
        
        # Style des boutons de contrôle
        button_params = {
            'width': 70,  # Augmenté de 60 à 70
            'height': 70,  # Augmenté de 60 à 70
            'padding': 4,  # Réduit pour avoir plus d'espace pour le bouton
            'color': '#282828',
            'hover_color': '#383838',
            'fg': 'white',
            'font': (self.font_family, 18)  # Augmenté de 14 à 18
        }
        
        # Créer les boutons
        self.play_button = CircleButton(buttons_frame,
                                      text="▶",
                                      command=self.toggle_play_pause,
                                      **button_params)
        self.play_button.pack(side='left', padx=8)
        
        self.show_answer_button = CircleButton(buttons_frame,
                                             text="👁",
                                             command=self.show_answer,
                                             **button_params)
        self.show_answer_button.pack(side='left', padx=8)
        
        self.next_button = CircleButton(buttons_frame,
                                      text="⏭",
                                      command=self.next_song,
                                      **button_params)
        self.next_button.pack(side='left', padx=8)
        
        self.listen_more_button = CircleButton(buttons_frame,
                                             text="♫",
                                             command=self.listen_full_song,
                                             **button_params)
        self.listen_more_button.pack(side='left', padx=8)
        # Désactiver le bouton next par défaut
        self.next_button.config(state='disabled')
        
        # Frame pour le volume (à droite)
        volume_frame = tk.Frame(control_frame, bg='#121212')
        volume_frame.grid(row=0, column=2, sticky='e', padx=20)
        
        volume_label = tk.Label(volume_frame,
                              text="🔊",
                              font=(self.font_family, 14),
                              fg='white',
                              bg='#121212')
        volume_label.pack(side='left', padx=(0, 5))
        
        self.volume_slider = ttk.Scale(volume_frame,
                                     from_=0,
                                     to=100,
                                     orient='horizontal',
                                     variable=self.volume_var,
                                     command=self.update_volume,
                                     style='Spotify.Horizontal.TScale',
                                     length=120)
        self.volume_slider.pack(side='left')
        
        # Frame pour les statistiques
        stats_frame = tk.Frame(content_frame, bg='#121212')
        stats_frame.grid(row=4, column=0, sticky='ew', padx=40, pady=5)
        
        self.songs_left_label = tk.Label(stats_frame,
                                       text="",
                                       font=(self.font_family, 12),
                                       fg='#B3B3B3',
                                       bg='#121212')
        self.songs_left_label.pack()

    def play_song(self):
        # Si on est en mode "?" (l'extrait a déjà été joué), on rejoue l'extrait
        if self.countdown_label.cget('text') == "?":
            self.replay_extract()
            return
            
        if not self.music_files:
            messagebox.showinfo("Information", "Plus de chansons disponibles")
            return
            
        if self.is_playing:
            return
            
        self.current_song = self.music_files.pop(0)
        self.is_playing = True
        self.is_full_song = False
        
        # Effacer la réponse précédente
        self.answer_label.config(text="")
        
        # Cacher la pochette et afficher le décompte
        self.album_cover_label.place_forget()
        self.default_cover.place_forget()
        self.music_icon.place_forget()
        self.countdown_container.place(relx=0.5, rely=0.5, anchor='center')
        self.countdown_label.config(text=str(self.duration_values[self.selected_duration.get()]))
        
        # Désactiver les boutons pendant la lecture
        self.listen_more_button.config(state='disabled')
        self.next_button.config(state='disabled')
        self.play_button.config(state='disabled')
        self.show_answer_button.config(state='disabled')  # Griser le bouton œil
        
        # Mettre à jour le nombre de chansons restantes
        self.update_songs_left()
        
        # Réinitialiser la barre de progression
        self.progress_var.set(0)
        
        # Récupérer la durée de la chanson
        try:
            audio = File(self.current_song)
            self.duration = audio.info.length
            
            # Calculer la position de départ aléatoire
            extract_duration = self.duration_values[self.selected_duration.get()]
            max_start_position = max(0, self.duration - extract_duration - 5)
            if max_start_position > 0:
                self.current_start_position = random.uniform(0, max_start_position)
            else:
                self.current_start_position = 0
            
            # Lecture de la musique
            pygame.mixer.music.load(self.current_song)
            pygame.mixer.music.play(start=self.current_start_position)
            pygame.mixer.music.set_volume(self.volume)
            
        except Exception as e:
            print(f"Erreur lors du chargement de la musique: {str(e)}")
            self.duration = 0
            self.current_start_position = 0
            pygame.mixer.music.load(self.current_song)
            pygame.mixer.music.play()
        
        # Démarrer le thread pour le décompte
        self.countdown_thread = threading.Thread(target=self.update_countdown)
        self.countdown_thread.start()
        
        # Démarrer le thread pour arrêter après la durée sélectionnée
        self.extract_thread = threading.Thread(target=self.stop_after_delay)
        self.extract_thread.start()

    def replay_extract(self):
        if not self.current_song or self.is_playing:
            return
            
        self.is_playing = True
        self.is_full_song = False
        
        # Réinitialiser le décompte
        self.countdown_container.place(relx=0.5, rely=0.5, anchor='center')
        self.countdown_label.config(text=str(self.duration_values[self.selected_duration.get()]))
        
        # Désactiver les boutons pendant la lecture
        self.listen_more_button.config(state='disabled')
        self.next_button.config(state='disabled')
        self.play_button.config(state='disabled')
        self.show_answer_button.config(state='disabled')  # Griser le bouton œil
        
        # Réinitialiser la barre de progression
        self.progress_var.set(0)
        
        # Lecture de la musique depuis la même position
        pygame.mixer.music.load(self.current_song)
        pygame.mixer.music.play(start=self.current_start_position)
        pygame.mixer.music.set_volume(self.volume)
        
        # Démarrer le thread pour le décompte
        self.countdown_thread = threading.Thread(target=self.update_countdown)
        self.countdown_thread.start()
        
        # Démarrer le thread pour arrêter après la durée sélectionnée
        self.extract_thread = threading.Thread(target=self.stop_after_delay)
        self.extract_thread.start()

    def update_countdown(self):
        extract_duration = self.duration_values[self.selected_duration.get()]
        # Pour les durées inférieures à 1 seconde, pas besoin de décompte
        if extract_duration < 1:
            if self.is_playing:
                self.countdown_label.config(text="<1")
                self.root.update()
            return
            
        for i in range(int(extract_duration), 0, -1):
            if not self.is_playing:
                break
            self.countdown_label.config(text=str(i))
            self.root.update()  # Forcer la mise à jour de l'interface
            time.sleep(1)
            
    def stop_after_delay(self):
        extract_duration = self.duration_values[self.selected_duration.get()]
        time.sleep(extract_duration)
        if self.is_playing and not self.is_full_song:
            pygame.mixer.music.stop()
            self.is_playing = False
            time.sleep(0.5)
            
            # Afficher le "?" à la place du décompte
            self.countdown_label.config(text="?", font=(self.title_font, 80, 'bold'))
            
            # Réactiver le bouton play et le bouton œil
            self.play_button.config(state='normal')
            self.show_answer_button.config(state='normal')  # Réactiver le bouton œil
            
            # Si l'œil a été cliqué (bouton désactivé), activer les autres boutons
            if self.show_answer_button.cget('state') == 'disabled':
                self.listen_more_button.config(state='normal')
                self.next_button.config(state='normal')
            else:
                # Si l'œil n'a pas été cliqué, on désactive les boutons
                self.listen_more_button.config(state='disabled')
                self.next_button.config(state='disabled')

    def listen_full_song(self):
        if not self.current_song or self.is_playing:
            return
            
        self.is_full_song = True
        self.is_playing = True
        
        # Désactiver le bouton pendant la lecture
        self.listen_more_button.config(state='disabled')
        
        # Réinitialiser la barre de progression
        self.progress_var.set(0)
        
        # Lecture de la musique complète
        pygame.mixer.music.load(self.current_song)
        pygame.mixer.music.play()
        
        # Démarrer le thread pour surveiller la fin de la chanson
        self.full_song_thread = threading.Thread(target=self.check_song_end)
        self.full_song_thread.start()
        
    def check_song_end(self):
        while self.is_playing and pygame.mixer.music.get_busy():
            time.sleep(0.1)
            
        if self.is_playing:
            self.is_playing = False
            self.is_full_song = False
            # Réactiver le bouton "Écouter la suite"
            self.listen_more_button.config(state='normal')
            
    def stop_song(self):
        if self.is_playing:
            pygame.mixer.music.stop()
            self.is_playing = False
            self.is_full_song = False
            if self.extract_thread:
                self.extract_thread.join()
            if self.full_song_thread:
                self.full_song_thread.join()
            # Réinitialiser la barre de progression
            self.progress_var.set(0)
            # Désactiver les boutons
            self.listen_more_button.config(state='disabled')
            self.next_button.config(state='disabled')
            # Cacher le décompte et afficher la pochette par défaut
            self.countdown_container.place_forget()
            self.default_cover.place(relx=0.5, rely=0.5, anchor='center')
            self.music_icon.place(relx=0.5, rely=0.5, anchor='center')
        
    def next_song(self):
        # Stocker l'état actuel du bouton "Écouter la suite"
        listen_more_state = self.listen_more_button.cget('state')
        
        self.stop_song()
        self.answer_label.config(text="")
        # Cacher la pochette et réafficher la pochette par défaut
        self.album_cover_label.place_forget()
        self.default_cover.place(relx=0.5, rely=0.5, anchor='center')
        self.music_icon.place(relx=0.5, rely=0.5, anchor='center')
        
        # Réinitialiser l'état du bouton "Écouter la suite"
        self.listen_more_button.config(state=listen_more_state)
        
        # Réactiver le bouton œil
        self.show_answer_button.config(state='normal')
        
        # Passer à la musique suivante
        if self.music_files:
            self.current_song = self.music_files.pop(0)
            self.update_songs_left()
            self.play_song()
        else:
            messagebox.showinfo("Information", "Plus de chansons disponibles")

    def show_answer(self):
        if not self.current_song:
            return
            
        # Vérifier si l'extrait est terminé (mode "?")
        if self.countdown_label.cget('text') != "?":
            return  # Ne rien faire si l'extrait n'est pas terminé
            
        # Cacher le décompte et le "?"
        self.countdown_container.place_forget()
        
        title, artist, genre, photo = get_metadata(self.current_song)
        if title and artist:
            self.answer_label.config(text=f"Titre: {title}\nArtiste: {artist}")
            if photo:
                # Cacher la pochette par défaut
                self.default_cover.place_forget()
                self.music_icon.place_forget()
                # Afficher la pochette
                self.album_cover_label.config(image=photo)
                self.album_cover_label.image = photo  # Garder une référence
                self.album_cover_label.place(relx=0.5, rely=0.5, anchor='center')
        else:
            self.answer_label.config(text=f"Fichier: {os.path.basename(self.current_song)}")
            
        # Griser le bouton œil après avoir cliqué dessus
        self.show_answer_button.config(state='disabled')
        
        # Activer les boutons "Écouter la suite" et "Next"
        self.listen_more_button.config(state='normal')
        self.next_button.config(state='normal')

    def apply_genre_filter(self):
        selected_genre = self.selected_genre.get()
        if selected_genre == "Tous les genres":
            self.load_music_files()
        else:
            # Charger le cache
            cache = self.config.load_cache()
            
            # Filtrer les fichiers par genre en utilisant le cache
            filtered_files = []
            for file_path in os.listdir(self.config.music_dir):
                full_path = os.path.join(self.config.music_dir, file_path)
                if full_path in cache and cache[full_path]['genre'] == selected_genre:
                    filtered_files.append(full_path)
            
            if filtered_files:
                self.music_files = filtered_files
                random.shuffle(self.music_files)
                self.update_songs_left()
            else:
                messagebox.showinfo("Information", f"Aucune chanson trouvée pour le genre {selected_genre}")

    def update_volume(self, value):
        # Conversion de la valeur linéaire (0-100) en volume logarithmique (0-1)
        try:
            value = float(value)
            if value == 0:
                self.volume = 0
            else:
                # Formule logarithmique pour une meilleure perception du volume
                self.volume = math.exp(value * 0.0461) / 100
            pygame.mixer.music.set_volume(self.volume)
        except:
            pass

    def update_songs_left(self):
        self.songs_left_label.config(text=f"Chansons restantes: {len(self.music_files)}")
        
    def load_music_files(self):
        supported_formats = ('.mp3', '.wav', '.ogg', '.flac')
        self.music_files = []
        self.genres = set()
        
        # Charger le cache existant
        cache = self.config.load_cache()
        new_cache = {}
        
        try:
            # Parcourir uniquement les fichiers du dossier principal
            for file in os.listdir(self.config.music_dir):
                if file.lower().endswith(supported_formats):
                    file_path = os.path.join(self.config.music_dir, file)
                    file_info = get_file_info(file_path)
                    
                    if not file_info:
                        continue
                    
                    # Initialiser genre à None
                    genre = None
                    
                    # Vérifier si le fichier est dans le cache et n'a pas été modifié
                    if file_path in cache:
                        cached_info = cache[file_path]
                        if (cached_info['size'] == file_info['size'] and 
                            cached_info['mtime'] == file_info['mtime']):
                            # Utiliser les informations du cache
                            self.music_files.append(file_path)
                            genre = cached_info['genre']
                            if genre:
                                self.genres.add(genre)
                        else:
                            # Fichier modifié, récupérer les nouvelles métadonnées
                            _, _, genre, _ = get_metadata(file_path)
                            self.music_files.append(file_path)
                            if genre:
                                self.genres.add(genre)
                    else:
                        # Nouveau fichier, récupérer les métadonnées
                        _, _, genre, _ = get_metadata(file_path)
                        self.music_files.append(file_path)
                        if genre:
                            self.genres.add(genre)
                    
                    # Mettre à jour le cache
                    new_cache[file_path] = {
                        'size': file_info['size'],
                        'mtime': file_info['mtime'],
                        'ctime': file_info['ctime'],
                        'genre': genre
                    }
            
            # Supprimer les fichiers qui n'existent plus
            for file_path in cache:
                if not os.path.exists(file_path):
                    if cache[file_path]['genre']:
                        self.genres.discard(cache[file_path]['genre'])
            
            if not self.music_files:
                messagebox.showerror("Erreur", "Aucun fichier musical trouvé dans le dossier Music")
                return
            
            # Ajouter "Tous les genres" à la liste des genres
            self.genres.add("Tous les genres")
            
            # Mettre à jour le menu déroulant
            self.genre_menu['values'] = sorted(list(self.genres))
            self.genre_menu.set("Tous les genres")
            
            # Sauvegarder le nouveau cache
            self.config.save_cache(new_cache)
            
            # Mélanger les fichiers
            random.shuffle(self.music_files)
            
            # Mettre à jour le nombre de chansons restantes
            self.update_songs_left()
            
        except Exception as e:
            print(f"Erreur lors du chargement des fichiers : {str(e)}")

    def update_duration(self, value):
        try:
            index = int(float(value))
            if 0 <= index < len(self.duration_values):
                self.selected_duration.set(index)
                self.duration_value_label.config(text=f"{self.duration_values[index]} s")
        except:
            pass

if __name__ == "__main__":
    root = tk.Tk()
    app = BlindTest(root)
    root.mainloop() 