# Compresseur de PDFs

Réduit le poids de fichiers PDF par lot, avec 3 niveaux de compression. Disponible en application de bureau (Python) et en version navigateur (HTML/JS).

## Fonctionnalités

- Glisser-déposer des fichiers PDF, ou sélection d'un dossier entier
- 3 niveaux de compression :
  1. Léger — qualité maximale
  2. Moyen — équilibré
  3. Maximum — taille minimale (recompresse les images intégrées plus agressivement et allège les flux de contenu)
- Traitement par lot avec barre de progression
- Résultat affiché : nombre de fichiers traités, taille avant/après, pourcentage de réduction
- Les PDFs compressés sont enregistrés dans un sous-dossier `compresses/`, les originaux ne sont jamais modifiés

## Version Python

Fichier : [`compresseur_pdf_interface.py`](compresseur_pdf_interface.py) — interface Tkinter.

**Dépendances :**
```bash
pip install pypdf tkinterdnd2
```
- `pypdf` est obligatoire (fait la compression).
- `tkinterdnd2` est optionnel : sans lui, le glisser-déposer est désactivé mais le bouton "choisir un fichier/dossier" reste fonctionnel.

**Lancer :**
```bash
python compresseur_pdf_interface.py
```

## Version HTML

Fichier : [`compresseur_pdf_dragdrop.html`](compresseur_pdf_dragdrop.html) — même interface, dans le navigateur.

Aucune installation nécessaire : ouvrir le fichier directement dans un navigateur.
