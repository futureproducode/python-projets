# Journal des modifications

Historique des versions de ce dépôt, de la plus récente à la plus ancienne.

---

## [1.1.0] — 27 juillet 2026

### Corrigé

- **Compresseur de PDF (navigateur) — les niveaux de compression ne faisaient pas ce qu'ils annonçaient.**
  L'interface proposait 5 niveaux, mais un seul réglage variait réellement dans le code : les niveaux 1 et 2 produisaient un fichier identique, tout comme les niveaux 3, 4 et 5. Choisir « Maximum » donnait exactement le même résultat que « Moyen », à l'octet près. Les descriptions promettaient par ailleurs des traitements absents du code (suppression des objets orphelins, compression des flux). Remplacés par **3 niveaux réellement distincts**, décrits fidèlement.

- **Compresseur de PDF (navigateur) — le fichier pouvait grossir.**
  Sur un PDF déjà optimisé, la réécriture produisait un fichier plus lourd que l'original : 11 Ko devenaient 21 Ko lors d'un test. Ajout d'un garde-fou qui renvoie le fichier d'origine si la compression n'apporte rien.

- **Générateur de mot de passe — le programme refusait de démarrer sans `pyperclip`.**
  L'import n'était pas protégé : en l'absence de la bibliothèque, le script s'arrêtait sur une erreur avant même d'afficher quoi que ce soit, alors que la documentation la présentait comme optionnelle.

### Ajouté

- **Recompression des images dans le compresseur de PDF (navigateur).**
  Les images intégrées sont désormais extraites, décodées, repassées en JPEG puis réinjectées dans le document. C'est ce qui manquait pour compresser réellement : jusqu'ici, seule la structure du fichier était réorganisée, ce qui ne pèse presque rien face aux images.
  Gain mesuré sur une présentation de 11 pages : **12,55 Mo → 1,02 Mo (−92 %) en 2 secondes.**
  Deux protections : une image n'est remplacée que si elle y gagne, et les formats non gérés (CMYK, palettes indexées) sont laissés intacts plutôt que dégradés.

- `README.md` — page d'accueil présentant les trois projets.
- `requirements.txt` — dépendances installables en une commande.
- `.gitignore` — empêche la publication des fichiers générés automatiquement (`__pycache__`) et des dossiers de sortie des compresseurs, qui peuvent contenir des fichiers personnels.
- Un README détaillé par projet.

### Modifié

- Les trois pages HTML n'appellent plus les polices Google et **fonctionnent hors connexion**, avec repli sur les polices du système.
- Le générateur de mot de passe n'a plus **aucune dépendance externe** : bibliothèque standard uniquement.

### Supprimé

- La copie automatique dans le presse-papiers du générateur de mot de passe, avec sa dépendance `pyperclip`. Le mot de passe reste affiché à l'écran.

---

## [1.0.0] — 8 juin 2026

### Ajouté

- **Compresseur d'images** — traitement par lot, curseur de qualité de 1 à 100, formats JPG, PNG, WEBP, BMP et TIFF.
- **Compresseur de PDF** — traitement par lot avec niveaux de compression.
- **Générateur de mot de passe** — génération via le module `secrets`, longueur et types de caractères configurables, estimation de la force du résultat.
- Une version navigateur autonome pour chacun des trois outils.

---

## À propos de ce fichier

Ce journal suit la convention [Keep a Changelog](https://keepachangelog.com/fr/) et la [gestion sémantique de version](https://semver.org/lang/fr/) : `MAJEUR.MINEUR.CORRECTIF`.
