import os
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image

try:
    from tkinterdnd2 import TkinterDnD, DND_FILES
    DND_DISPONIBLE = True
except ImportError:
    DND_DISPONIBLE = False

# ─────────────────────────────────────────────
#  COMPRESSEUR D'IMAGES - Interface Kawaii Moderne
#  by Kenz 💜
# ─────────────────────────────────────────────

# Palette kawaii
C = {
    "fond":         "#1a0a1e",
    "panneau":      "#2d1040",
    "card":         "#3d1a55",
    "rose":         "#ff6eb4",
    "rose_clair":   "#ff9dd4",
    "violet":       "#c084fc",
    "violet_dim":   "#7c3aed",
    "texte":        "#fdf4ff",
    "texte_dim":    "#c4b5d4",
    "bordure":      "#7c3aed",
    "succes":       "#34d399",
    "drop_bg":      "#2d1040",
    "drop_border":  "#ff6eb4",
}

FORMATS = (".jpg", ".jpeg", ".png", ".bmp", ".webp", ".tiff")

# Police kawaii: on utilise les polices système les plus douces disponibles
FONT_TITRE  = ("Segoe UI", 18, "bold")
FONT_SOUS   = ("Segoe UI", 10)
FONT_LABEL  = ("Segoe UI", 10, "bold")
FONT_PETIT  = ("Segoe UI", 9)
FONT_BTN    = ("Segoe UI", 12, "bold")
FONT_MONO   = ("Consolas", 9)


def taille_lisible(o):
    if o < 1024: return f"{o} o"
    elif o < 1024**2: return f"{o/1024:.1f} Ko"
    else: return f"{o/1024**2:.1f} Mo"


class RoundedFrame(tk.Canvas):
    """Canvas simulant un cadre arrondi."""
    def __init__(self, parent, bg_outer, bg_inner, radius=18, border_color=None, border_width=2, **kwargs):
        width  = kwargs.pop("width", 200)
        height = kwargs.pop("height", 100)
        super().__init__(parent, width=width, height=height,
                         bg=bg_outer, highlightthickness=0, **kwargs)
        self.radius = radius
        self.bg_inner = bg_inner
        self.border_color = border_color
        self.border_width = border_width
        self._draw(width, height)

    def _draw(self, w, h):
        r = self.radius
        if self.border_color:
            self.create_rounded_rect(2, 2, w-2, h-2, r, fill=self.border_color)
            bw = self.border_width
            self.create_rounded_rect(bw+1, bw+1, w-bw-1, h-bw-1, r-bw, fill=self.bg_inner)
        else:
            self.create_rounded_rect(0, 0, w, h, r, fill=self.bg_inner)

    def create_rounded_rect(self, x1, y1, x2, y2, r, **kwargs):
        self.create_arc(x1, y1, x1+2*r, y1+2*r, start=90,  extent=90,  style="pieslice", outline="", **kwargs)
        self.create_arc(x2-2*r, y1, x2, y1+2*r, start=0,   extent=90,  style="pieslice", outline="", **kwargs)
        self.create_arc(x1, y2-2*r, x1+2*r, y2, start=180, extent=90,  style="pieslice", outline="", **kwargs)
        self.create_arc(x2-2*r, y2-2*r, x2, y2, start=270, extent=90,  style="pieslice", outline="", **kwargs)
        self.create_rectangle(x1+r, y1, x2-r, y2, outline="", **kwargs)
        self.create_rectangle(x1, y1+r, x2, y2-r, outline="", **kwargs)


class AppCompresseur:
    def __init__(self, root):
        self.root = root
        self.root.title("Compresseur d'images ✦ by Kenz")
        self.root.configure(bg=C["fond"])
        self.root.resizable(False, False)
        self.fichiers = []
        self.en_cours = False
        self._construire_interface()
        self._centrer(720, 680)

    def _centrer(self, w, h):
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() - w) // 2
        y = (self.root.winfo_screenheight() - h) // 2
        self.root.geometry(f"{w}x{h}+{x}+{y}")

    def _label(self, parent, text, font=None, fg=None, bg=None, **kw):
        return tk.Label(parent,
                        text=text,
                        font=font or FONT_PETIT,
                        fg=fg or C["texte"],
                        bg=bg or C["fond"],
                        **kw)

    def _construire_interface(self):
        # ── En-tête ────────────────────────────────────────────
        header = tk.Frame(self.root, bg=C["panneau"], pady=18)
        header.pack(fill="x")

        self._label(header, "✦  ✦  ✦", fg=C["rose"], bg=C["panneau"],
                    font=("Segoe UI", 10)).pack()
        self._label(header, "Compresseur d'images", fg=C["texte"], bg=C["panneau"],
                    font=("Segoe UI", 22, "bold")).pack()
        self._label(header, "by Kenz  💜", fg=C["violet"], bg=C["panneau"],
                    font=("Segoe UI", 11)).pack()
        self._label(header, "✨  kawaii & moderne  ✨", fg=C["rose_clair"], bg=C["panneau"],
                    font=("Segoe UI", 9)).pack(pady=(2, 0))

        # ── Corps ──────────────────────────────────────────────
        body = tk.Frame(self.root, bg=C["fond"])
        body.pack(fill="both", expand=True, padx=30, pady=16)

        # Zone drop
        self._label(body, "  🌸  Images à compresser", fg=C["rose_clair"],
                    font=FONT_LABEL).pack(anchor="w", pady=(0, 6))

        self.zone_drop = tk.Frame(body, bg=C["drop_bg"],
                                  highlightbackground=C["drop_border"],
                                  highlightthickness=2,
                                  cursor="hand2")
        self.zone_drop.pack(fill="x", ipady=20)
        self.zone_drop.bind("<Button-1>", lambda e: self._parcourir_fichiers())

        self.label_drop = tk.Label(
            self.zone_drop,
            text="🌸   Glisse tes images ici\nou clique pour choisir",
            bg=C["drop_bg"], fg=C["texte_dim"],
            font=("Segoe UI", 12), justify="center"
        )
        self.label_drop.pack(pady=10)
        self.label_drop.bind("<Button-1>", lambda e: self._parcourir_fichiers())

        if DND_DISPONIBLE:
            self.zone_drop.drop_target_register(DND_FILES)
            self.zone_drop.dnd_bind("<<Drop>>", self._on_drop)

        # Bouton dossier
        tk.Button(body, text="📁  Choisir un dossier entier",
                  bg=C["fond"], fg=C["violet"],
                  font=("Segoe UI", 9, "underline"),
                  relief="flat", cursor="hand2", bd=0,
                  activebackground=C["fond"], activeforeground=C["rose"],
                  command=self._parcourir_dossier).pack(anchor="e", pady=(4, 10))

        # Liste fichiers
        cadre_liste = tk.Frame(body, bg=C["card"],
                               highlightbackground=C["bordure"],
                               highlightthickness=1)
        cadre_liste.pack(fill="x", pady=(0, 10))

        entete_liste = tk.Frame(cadre_liste, bg=C["card"])
        entete_liste.pack(fill="x", padx=10, pady=(8, 4))
        self._label(entete_liste, "🎀  Fichiers sélectionnés",
                    fg=C["rose_clair"], bg=C["card"], font=FONT_LABEL).pack(side="left")
        tk.Button(entete_liste, text="✕ vider",
                  bg=C["card"], fg=C["texte_dim"],
                  font=("Segoe UI", 8), relief="flat", cursor="hand2", bd=0,
                  activebackground=C["card"], activeforeground=C["rose"],
                  command=self._vider_liste).pack(side="right")

        self.liste = tk.Listbox(
            cadre_liste, height=5,
            bg=C["card"], fg=C["texte"],
            font=FONT_MONO,
            selectbackground=C["violet_dim"], selectforeground="white",
            relief="flat", highlightthickness=0, bd=0,
            activestyle="none"
        )
        self.liste.pack(fill="x", padx=10, pady=(0, 8))

        # Qualité
        cadre_q = tk.Frame(body, bg=C["card"],
                           highlightbackground=C["bordure"],
                           highlightthickness=1)
        cadre_q.pack(fill="x", pady=(0, 10))

        tk.Frame(cadre_q, bg=C["card"]).pack(pady=6)
        self._label(cadre_q, "  💫  Niveau de qualité", fg=C["rose_clair"],
                    bg=C["card"], font=FONT_LABEL).pack(anchor="w", padx=10)

        slider_row = tk.Frame(cadre_q, bg=C["card"])
        slider_row.pack(fill="x", padx=10, pady=6)

        self._label(slider_row, "1", fg=C["texte_dim"], bg=C["card"],
                    font=FONT_PETIT).pack(side="left")

        self.qualite_var = tk.IntVar(value=75)
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Kawaii.Horizontal.TScale",
                        background=C["card"],
                        troughcolor=C["panneau"],
                        sliderlength=22)
        self.slider = ttk.Scale(slider_row, from_=1, to=100,
                                variable=self.qualite_var,
                                orient="horizontal",
                                style="Kawaii.Horizontal.TScale",
                                command=self._maj_qualite)
        self.slider.pack(side="left", fill="x", expand=True, padx=8)
        self._label(slider_row, "100", fg=C["texte_dim"], bg=C["card"],
                    font=FONT_PETIT).pack(side="left")

        self.label_qualite = self._label(cadre_q, "Qualité : 75/100  —  Qualité équilibrée",
                                          fg=C["rose"], bg=C["card"],
                                          font=("Segoe UI", 10, "bold"))
        self.label_qualite.pack(anchor="w", padx=10, pady=(0, 8))

        # Progression
        cadre_prog = tk.Frame(body, bg=C["fond"])
        cadre_prog.pack(fill="x", pady=(0, 6))

        style.configure("Kawaii.Horizontal.TProgressbar",
                        troughcolor=C["panneau"],
                        background=C["rose"],
                        thickness=8)
        self.progress = ttk.Progressbar(cadre_prog, mode="determinate",
                                         style="Kawaii.Horizontal.TProgressbar")
        self.progress.pack(fill="x")

        self.label_statut = self._label(cadre_prog, "",
                                         fg=C["texte_dim"], font=FONT_PETIT)
        self.label_statut.pack(anchor="w", pady=(4, 0))

        # Bouton principal
        self.btn = tk.Button(body,
                             text="✨   Compresser   ✨",
                             bg=C["rose"], fg="white",
                             font=("Segoe UI", 13, "bold"),
                             relief="flat", cursor="hand2",
                             padx=20, pady=10,
                             activebackground=C["rose_clair"],
                             activeforeground=C["fond"],
                             command=self._lancer)
        self.btn.pack(fill="x", pady=6)

        self.label_resultat = self._label(body, "",
                                           fg=C["succes"],
                                           font=("Segoe UI", 10, "bold"))
        self.label_resultat.pack(pady=(4, 0))

        # Pied de page
        self._label(self.root, "✦  made with love by kenz  ✦",
                    fg=C["violet_dim"], font=("Segoe UI", 8)).pack(pady=(0, 10))

    def _maj_qualite(self, val=None):
        q = int(self.qualite_var.get())
        if q < 30:   desc = "Compression maximale"
        elif q < 60: desc = "Bonne compression"
        elif q < 80: desc = "Qualité équilibrée"
        else:        desc = "Haute qualité"
        self.label_qualite.config(text=f"Qualité : {q}/100  —  {desc}")

    def _on_drop(self, event):
        for chemin in self.root.tk.splitlist(event.data):
            chemin = chemin.strip("{}")
            if os.path.isdir(chemin):   self._ajouter_dossier(chemin)
            elif chemin.lower().endswith(FORMATS): self._ajouter_fichier(chemin)

    def _parcourir_fichiers(self):
        for f in filedialog.askopenfilenames(
            title="Choisir des images",
            filetypes=[("Images", "*.jpg *.jpeg *.png *.bmp *.webp *.tiff")]
        ): self._ajouter_fichier(f)

    def _parcourir_dossier(self):
        d = filedialog.askdirectory(title="Choisir un dossier")
        if d: self._ajouter_dossier(d)

    def _ajouter_dossier(self, d):
        for f in os.listdir(d):
            if f.lower().endswith(FORMATS):
                self._ajouter_fichier(os.path.join(d, f))

    def _ajouter_fichier(self, chemin):
        if chemin not in self.fichiers:
            self.fichiers.append(chemin)
            self.liste.insert("end", f"  {os.path.basename(chemin)}")
        self.label_drop.config(text=f"🌸   {len(self.fichiers)} image(s) sélectionnée(s)")

    def _vider_liste(self):
        self.fichiers.clear()
        self.liste.delete(0, "end")
        self.label_drop.config(text="🌸   Glisse tes images ici\nou clique pour choisir")
        self.label_resultat.config(text="")
        self.progress["value"] = 0
        self.label_statut.config(text="")

    def _lancer(self):
        if self.en_cours: return
        if not self.fichiers:
            messagebox.showwarning("Oups !", "Ajoute d'abord des images 🌸"); return
        self.en_cours = True
        self.btn.config(state="disabled", text="⏳   Compression en cours...")
        threading.Thread(target=self._compresser, daemon=True).start()

    def _compresser(self):
        qualite = int(self.qualite_var.get())
        total   = len(self.fichiers)
        av_tot  = ap_tot = succes = 0
        self.progress.config(maximum=total, value=0)

        for i, chemin in enumerate(self.fichiers):
            nom     = os.path.basename(chemin)
            sortie  = os.path.join(os.path.dirname(chemin), "compressees")
            os.makedirs(sortie, exist_ok=True)
            dest    = os.path.join(sortie, os.path.splitext(nom)[0] + "_compressed.jpg")
            self.label_statut.config(text=f"  ⏳  {nom}")
            try:
                av = os.path.getsize(chemin)
                img = Image.open(chemin)
                if img.mode in ("RGBA", "P"): img = img.convert("RGB")
                img.save(dest, "JPEG", quality=qualite, optimize=True)
                ap = os.path.getsize(dest)
                av_tot += av; ap_tot += ap; succes += 1
            except Exception: pass
            self.progress["value"] = i + 1
            self.root.update_idletasks()

        red = (1 - ap_tot / av_tot) * 100 if av_tot else 0
        self.label_statut.config(text="  ✓  Images sauvegardées dans le dossier 'compressees'")
        self.label_resultat.config(
            text=f"💜  {succes}/{total} images  ·  {taille_lisible(av_tot)} → {taille_lisible(ap_tot)}  ·  -{red:.0f}% !"
        )
        self.btn.config(state="normal", text="✨   Compresser   ✨")
        self.en_cours = False


if __name__ == "__main__":
    root = TkinterDnD.Tk() if DND_DISPONIBLE else tk.Tk()
    AppCompresseur(root)
    root.mainloop()
