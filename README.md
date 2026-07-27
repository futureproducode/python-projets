# Projets Python — Kenza

Trois utilitaires de bureau développés en Python, chacun décliné en **application graphique** et en **version navigateur** autonome.

| Projet | Ce qu'il fait | Version bureau | Version navigateur |
|---|---|---|---|
| 🖼️ **Compresseur d'images** | Réduit le poids d'images par lot, qualité réglable | [`compresseur_image_interface.py`](compresseur_image_interface.py) | [`compresseur_dragdrop_image.html`](compresseur_dragdrop_image.html) |
| 📄 **Compresseur de PDF** | Allège des PDF en recompressant leurs images | [`compresseur_pdf_interface.py`](compresseur_pdf_interface.py) | [`compresseur_pdf_dragdrop.html`](compresseur_pdf_dragdrop.html) |
| 🔑 **Générateur de mot de passe** | Crée des mots de passe cryptographiquement sûrs | [`generateur_mot_de_passe.py`](generateur_mot_de_passe.py) | [`generateur_mot_de_passe.html`](generateur_mot_de_passe.html) |

Chaque projet a son propre README détaillé :
[images](README_compresseur_image.md) · [PDF](README_compresseur_pdf.md) · [mots de passe](README_generateur_mot_de_passe.md)

---

## Démarrage rapide

**Version navigateur** — aucune installation : ouvrez le fichier `.html` dans un navigateur.

**Version Python** :

```bash
pip install -r requirements.txt
python compresseur_image_interface.py
```

---

## Ce que contiennent ces projets

**Interfaces graphiques Tkinter** — fenêtres personnalisées, glisser-déposer, barres de progression, traitement en arrière-plan pour ne jamais figer l'interface.

**Traitement par lot** — les fichiers sont traités en série avec suivi de progression, et les originaux ne sont **jamais** modifiés : les résultats vont dans un sous-dossier dédié.

**Compression PDF réelle** — la version navigateur ne se contente pas de réorganiser le fichier : elle extrait les images intégrées, les repasse en JPEG et les réinjecte dans le document. Sur des PDF de présentation ou de scans, le gain observé va de **80 à 95 %** (exemple mesuré : 12,55 Mo → 1,02 Mo). Un garde-fou empêche de renvoyer un fichier plus lourd que l'original.

**Génération sécurisée** — le générateur utilise le module `secrets` de Python, conçu pour la cryptographie, et non `random` qui est prévisible et inadapté aux mots de passe.

---

## Dépendances

| Bibliothèque | Utilisée par | Requise ? |
|---|---|---|
| `Pillow` | Compresseur d'images | oui |
| `pypdf` | Compresseur de PDF | oui |
| `tkinterdnd2` | Les deux compresseurs | non — sans elle, le glisser-déposer est désactivé, la sélection par bouton reste disponible |

Le générateur de mot de passe n'a **aucune dépendance** : il n'utilise que la bibliothèque standard.

Les versions navigateur fonctionnent hors ligne, à une exception près : le compresseur de PDF charge la bibliothèque `pdf-lib` depuis Internet et nécessite donc une connexion.

---

## Technologies

Python 3 · Tkinter · Pillow · pypdf · HTML/CSS · JavaScript (Canvas, pdf-lib)
