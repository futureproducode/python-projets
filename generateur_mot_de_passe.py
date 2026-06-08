import secrets
import string
import pyperclip  # pip install pyperclip

# ─────────────────────────────────────────────
#  GÉNÉRATEUR DE MOT DE PASSE SÉCURISÉ
#  Utilise le module `secrets` (cryptographiquement sûr)
# ─────────────────────────────────────────────

# Couleurs ANSI pour le terminal
VERT      = "\033[92m"
VERT_DIM  = "\033[32m"
ORANGE    = "\033[93m"
ROUGE     = "\033[91m"
BLANC     = "\033[97m"
GRIS      = "\033[90m"
RESET     = "\033[0m"
GRAS      = "\033[1m"


def afficher_banniere():
    print(f"""
{VERT_DIM}╔══════════════════════════════════════════╗
║  {VERT}{GRAS}⚡  SECURE_PASS_GEN  v2.1{RESET}{VERT_DIM}               ║
╚══════════════════════════════════════════╝{RESET}
""")


def calculer_force(mot_de_passe: str) -> tuple[int, str, str]:
    """Retourne (score 0-100, label, couleur)."""
    score = 0
    longueur = len(mot_de_passe)

    score += min(40, int(longueur * 2.5))
    if any(c.islower() for c in mot_de_passe):
        score += 10
    if any(c.isupper() for c in mot_de_passe):
        score += 15
    if any(c.isdigit() for c in mot_de_passe):
        score += 15
    if any(c in string.punctuation for c in mot_de_passe):
        score += 20
    score += min(10, len(set(mot_de_passe)) // 2)
    score = min(100, score)

    if score < 35:
        return score, "FAIBLE", ROUGE
    elif score < 60:
        return score, "MODÉRÉ", ORANGE
    elif score < 80:
        return score, "FORT", VERT_DIM
    else:
        return score, "TRÈS FORT", VERT


def afficher_barre_force(score: int, couleur: str):
    """Affiche une barre de progression colorée."""
    total = 30
    rempli = int(score / 100 * total)
    barre = "█" * rempli + "░" * (total - rempli)
    print(f"  {couleur}{barre}{RESET}  {score}/100")


def choisir_longueur() -> int:
    while True:
        try:
            valeur = input(f"  {GRIS}Longueur (8-20) [{BLANC}12{GRIS}] :{RESET} ").strip()
            if valeur == "":
                return 12
            longueur = int(valeur)
            if 8 <= longueur <= 20:
                return longueur
            print(f"  {ROUGE}⚠  Entrez un nombre entre 8 et 20.{RESET}")
        except ValueError:
            print(f"  {ROUGE}⚠  Nombre invalide.{RESET}")


def choisir_options() -> dict:
    options = {
        "minuscules": True,
        "majuscules": True,
        "chiffres":   True,
        "symboles":   True,
    }
    labels = {
        "minuscules": "abc  minuscules",
        "majuscules": "ABC  majuscules",
        "chiffres":   "123  chiffres",
        "symboles":   "!@#  symboles / ponctuation",
    }

    print(f"\n  {GRIS}Types de caractères (O=oui / N=non) :{RESET}")
    for cle, label in labels.items():
        defaut = "O"
        reponse = input(f"    {VERT_DIM}[{defaut}]{RESET} {label} ? ").strip().upper()
        if reponse == "N":
            options[cle] = False

    if not any(options.values()):
        print(f"\n  {ROUGE}⚠  Aucun type sélectionné — minuscules activées par défaut.{RESET}")
        options["minuscules"] = True

    return options


def generer_mot_de_passe(longueur: int, options: dict) -> str:
    """Génère un mot de passe avec `secrets` (cryptographiquement sûr)."""
    pool = ""
    garantis = []

    if options["minuscules"]:
        pool += string.ascii_lowercase
        garantis.append(secrets.choice(string.ascii_lowercase))
    if options["majuscules"]:
        pool += string.ascii_uppercase
        garantis.append(secrets.choice(string.ascii_uppercase))
    if options["chiffres"]:
        pool += string.digits
        garantis.append(secrets.choice(string.digits))
    if options["symboles"]:
        pool += string.punctuation
        garantis.append(secrets.choice(string.punctuation))

    # Compléter jusqu'à la longueur voulue
    reste = [secrets.choice(pool) for _ in range(longueur - len(garantis))]
    tous = garantis + reste

    # Mélanger aléatoirement
    secrets.SystemRandom().shuffle(tous)
    return "".join(tous)


def copier_dans_presse_papiers(mot_de_passe: str):
    try:
        pyperclip.copy(mot_de_passe)
        print(f"  {VERT}✓  Copié dans le presse-papiers !{RESET}")
    except Exception:
        print(f"  {ORANGE}⚠  Impossible de copier (installez pyperclip : pip install pyperclip){RESET}")


def main():
    afficher_banniere()

    while True:
        # ── Longueur ──────────────────────────────
        print(f"{GRIS}┌─ Configuration ───────────────────────────{RESET}")
        longueur = choisir_longueur()

        # ── Options ───────────────────────────────
        options = choisir_options()

        # ── Génération ────────────────────────────
        mot_de_passe = generer_mot_de_passe(longueur, options)
        score, label, couleur = calculer_force(mot_de_passe)

        print(f"\n{GRIS}┌─ Résultat ─────────────────────────────────{RESET}")
        print(f"  {GRAS}{VERT}{mot_de_passe}{RESET}")
        print(f"\n{GRIS}┌─ Force du mot de passe ────────────────────{RESET}")
        afficher_barre_force(score, couleur)
        print(f"  {couleur}{GRAS}{label}{RESET}\n")

        # ── Copier ────────────────────────────────
        copier = input(f"  {GRIS}Copier dans le presse-papiers ? (O/n) :{RESET} ").strip().upper()
        if copier != "N":
            copier_dans_presse_papiers(mot_de_passe)

        # ── Continuer ? ───────────────────────────
        print()
        encore = input(f"  {GRIS}Générer un autre mot de passe ? (O/n) :{RESET} ").strip().upper()
        if encore == "N":
            print(f"\n  {VERT_DIM}Au revoir.{RESET}\n")
            break
        print()


if __name__ == "__main__":
    main()
