# Générateur de mot de passe

Génère des mots de passe aléatoires cryptographiquement sûrs, avec choix de la longueur et des types de caractères, et une estimation de la force du résultat. Disponible en outil en ligne de commande (Python) et en version navigateur (HTML/JS).

## Fonctionnalités

- Longueur configurable (8 à 20 caractères)
- Choix des types de caractères inclus : minuscules, majuscules, chiffres, symboles
- Génération via le module `secrets` (cryptographiquement sûr, contrairement à `random`)
- Chaque type de caractère activé est garanti présent dans le résultat
- Estimation de la force du mot de passe (score /100 + label : faible, modéré, fort, très fort)

## Version Python

Fichier : [`generateur_mot_de_passe.py`](generateur_mot_de_passe.py) — outil en ligne de commande.

**Dépendances :** aucune. Le programme n'utilise que la bibliothèque standard de Python (`secrets` et `string`).

**Lancer :**
```bash
python generateur_mot_de_passe.py
```

## Version HTML

Fichier : [`generateur_mot_de_passe.html`](generateur_mot_de_passe.html) — même logique, dans le navigateur.

Aucune installation nécessaire : ouvrir le fichier directement dans un navigateur. La génération se fait localement, rien n'est envoyé sur un serveur.
