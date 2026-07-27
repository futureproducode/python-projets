# Compresseur d'images

Réduit le poids de fichiers image par lot, avec un curseur de qualité réglable de 1 à 100. Disponible en application de bureau (Python) et en version navigateur (HTML/JS).

## Fonctionnalités

- Formats pris en charge : `.jpg`, `.jpeg`, `.png`, `.bmp`, `.webp`, `.tiff`
- Glisser-déposer des fichiers, ou sélection d'un dossier entier
- Curseur de qualité avec estimation en direct (compression maximale → haute qualité)
- Traitement par lot avec barre de progression
- Résultat affiché : nombre de fichiers traités, taille avant/après, pourcentage de réduction
- Les images compressées sont enregistrées dans un sous-dossier `compressees/`, les originaux ne sont jamais modifiés

## Version Python

Fichier : [`compresseur_image_interface.py`](compresseur_image_interface.py) — interface Tkinter.

**Dépendances :**
```bash
pip install Pillow tkinterdnd2
```
- `Pillow` est obligatoire (fait la compression).
- `tkinterdnd2` est optionnel : sans lui, le glisser-déposer est désactivé mais le bouton "choisir un fichier/dossier" reste fonctionnel.

**Lancer :**
```bash
python compresseur_image_interface.py
```

## Version HTML

Fichier : [`compresseur_dragdrop_image.html`](compresseur_dragdrop_image.html) — même interface, dans le navigateur.

Aucune installation nécessaire : ouvrir le fichier directement dans un navigateur. La compression se fait localement via `canvas`, aucun fichier n'est envoyé sur un serveur.
