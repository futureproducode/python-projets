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

Fichier : [`compresseur_pdf_dragdrop.html`](compresseur_pdf_dragdrop.html) — même principe, dans le navigateur.

Aucune installation nécessaire : ouvrir le fichier directement dans un navigateur. **Une connexion Internet est requise** : la page charge la bibliothèque `pdf-lib`, qui lit et réécrit les PDF.

Ses 3 niveaux :

1. **Léger** — métadonnées supprimées et structure du fichier compactée. Les images ne sont pas touchées, le document est strictement préservé. Gain de quelques pourcents.
2. **Moyen** — les images intégrées sont extraites, repassées en JPEG (qualité 75) et réinjectées ; les signets, données d'accessibilité, JavaScript et pièces jointes sont supprimés. C'est le niveau recommandé : **80 à 95 % de gain** sur des PDF de présentation ou de scans.
3. **Fort** — même chose avec des images en qualité 45, et sans les annotations ni les champs de formulaire. Les liens cliquables sont perdus et les images perdent en netteté.

Exemple mesuré sur une présentation de 11 pages : **12,55 Mo → 1,02 Mo** au niveau 3, en 2 secondes.

Deux garde-fous : une image n'est remplacée que si elle y gagne réellement, et le fichier final n'est jamais renvoyé s'il est plus lourd que l'original.
