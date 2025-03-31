# BlindTest Generator
 Just a small software that generates Blind Test with your local tracks, ideal to train !


Still in development, not working atm !!!
=======
# Blind Test Musical

Une application de blind test musical avec une interface moderne et intuitive.

## Installation

### Version exécutable (recommandée)

1. Téléchargez la dernière version de l'application depuis la section "Releases"
2. Extrayez le contenu du fichier zip
3. Double-cliquez sur `BlindTest.exe` pour lancer l'application

### Version source

1. Clonez ce dépôt
2. Installez les dépendances :
```bash
pip install -r requirements.txt
```
3. Lancez l'application :
```bash
python main.py
```

## Utilisation

1. Cliquez sur "Choisir le dossier" pour sélectionner le dossier contenant vos musiques
2. Sélectionnez un genre musical si vous souhaitez filtrer les chansons
3. Choisissez la durée de l'extrait (en secondes)
4. Cliquez sur le bouton Play (▶) pour commencer
5. Devinez le titre et l'artiste
6. Cliquez sur l'œil (👁) pour voir la réponse
7. Écoutez la suite de la chanson avec le bouton ♫ ou passez à la suivante avec ⏭

## Fonctionnalités

- Interface moderne style Spotify
- Support des formats MP3, WAV, OGG et FLAC
- Filtrage par genre musical
- Durée d'extrait personnalisable
- Affichage des pochettes d'albums
- Contrôle du volume
- Cache des métadonnées pour un chargement rapide

## Configuration

L'application crée deux fichiers de configuration :
- `config.json` : stocke le dernier dossier de musique utilisé
- `music_cache.json` : stocke les métadonnées des chansons pour un chargement plus rapide

## Développement

Pour créer une nouvelle version exécutable :
```bash
python build.py
```

L'exécutable sera créé dans le dossier `dist/`.