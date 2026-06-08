import os
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pypdf import PdfReader, PdfWriter

try:
    from tkinterdnd2 import TkinterDnD, DND_FILES
    DND_DISPONIBLE = True
except ImportError:
    DND_DISPONIBLE = False

# ─────────────────────────────────────────────
#  COMPRESSEUR DE PDFs - Interface kawaii
#  by Kenz 💜
# ─────────────────────────────────────────────

C = {
    "fond":       "#1a0a1e",
    "panneau":    "#2d1040",
    "card":       "#3d1a55",
    "rose":       "#ff6eb4",
    "rose_clair": "#ff9dd4",
    "violet":     "#c084fc",
    "violet_dim": "#7c3aed",
    "texte":      "#fdf4ff",
    "texte_dim":  "#c4b5d4",
    "bordure":    "#7c3aed",
    "succes":     "#34d399",
}

FONT_TITRE = ("Segoe UI", 22, "bold")
FONT_LABEL = ("Segoe UI", 10, "bold")
FONT_PETIT = ("Segoe UI", 9)
FONT_MONO  = ("Consolas", 9)


def taille_lisible(o):
    if o < 1024: return f"{o} o"
    elif o < 1024**2: return f"{o/1024:.1f} Ko"
    else: return f"{o/1024**2:.1f} Mo"


def compresser_pdf(chemin_in, chemin_out, niveau):
    reader = PdfReader(chemin_in)
    writer = PdfWriter()
    for page in reader.pages:
        if niveau >= 2:
            page.compress_content_streams()
        writer.add_page(page)
    if niveau >= 1:
        for page in writer.pages:
            for img in page.images:
                img.replace(img.image, quality=max(10, 85 - (niveau - 1) * 25))
    writer.compress_identical_objects(remove_identicals=True, remove_orphans=True)
    with open(chemin_out, "wb") as f:
        writer.write(f)


class AppCompresseurPDF:
    def __init__(self, root):
        self.root = root
        self.root.title("Compresseur de PDFs ✦ by Kenz")
        self.root.configure(bg=C["fond"])
        self.root.resizable(False, False)
        self.fichiers = []
        self.en_cours = False
        self._build()
        self._centrer(720, 660)

    def _centrer(self, w, h):
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() - w) // 2
        y = (self.root.winfo_screenheight() - h) // 2
        self.root.geometry(f"{w}x{h}+{x}+{y}")

    def _lbl(self, parent, text, font=None, fg=None, bg=None, **kw):
        return tk.Label(parent, text=text,
                        font=font or FONT_PETIT,
                        fg=fg or C["texte"],
                        bg=bg or C["fond"], **kw)

    def _build(self):
        # Header
        header = tk.Frame(self.root, bg=C["panneau"], pady=18)
        header.pack(fill="x")
        self._lbl(header, "✦  ✦  ✦", fg=C["rose"], bg=C["panneau"], font=("Segoe UI", 10)).pack()
        self._lbl(header, "Compresseur de PDFs", fg=C["texte"], bg=C["panneau"], font=FONT_TITRE).pack()
        self._lbl(header, "by Kenz  💜", fg=C["violet"], bg=C["panneau"], font=("Segoe UI", 11)).pack()
        self._lbl(header, "✨  kawaii & moderne  ✨", fg=C["rose_clair"], bg=C["panneau"], font=("Segoe UI", 9)).pack(pady=(2,0))

        body = tk.Frame(self.root, bg=C["fond"])
        body.pack(fill="both", expand=True, padx=30, pady=16)

        # Zone drop
        self._lbl(body, "  📄  PDFs à compresser", fg=C["rose_clair"], font=FONT_LABEL).pack(anchor="w", pady=(0,6))

        self.zone_drop = tk.Frame(body, bg=C["card"],
                                  highlightbackground=C["rose"],
                                  highlightthickness=2, cursor="hand2")
        self.zone_drop.pack(fill="x", ipady=20)
        self.zone_drop.bind("<Button-1>", lambda e: self._parcourir())

        self.label_drop = tk.Label(self.zone_drop,
            text="📄   Glisse tes PDFs ici\nou clique pour choisir",
            bg=C["card"], fg=C["texte_dim"],
            font=("Segoe UI", 12), justify="center")
        self.label_drop.pack(pady=10)
        self.label_drop.bind("<Button-1>", lambda e: self._parcourir())

        if DND_DISPONIBLE:
            self.zone_drop.drop_target_register(DND_FILES)
            self.zone_drop.dnd_bind("<<Drop>>", self._on_drop)

        tk.Button(body, text="📁  Choisir un dossier entier",
                  bg=C["fond"], fg=C["violet"],
                  font=("Segoe UI", 9, "underline"),
                  relief="flat", cursor="hand2", bd=0,
                  activebackground=C["fond"], activeforeground=C["rose"],
                  command=self._parcourir_dossier).pack(anchor="e", pady=(4,10))

        # Liste
        cadre_liste = tk.Frame(body, bg=C["card"],
                               highlightbackground=C["bordure"],
                               highlightthickness=1)
        cadre_liste.pack(fill="x", pady=(0,10))

        entete = tk.Frame(cadre_liste, bg=C["card"])
        entete.pack(fill="x", padx=10, pady=(8,4))
        self._lbl(entete, "🎀  Fichiers sélectionnés", fg=C["rose_clair"], bg=C["card"], font=FONT_LABEL).pack(side="left")
        tk.Button(entete, text="✕ vider", bg=C["card"], fg=C["texte_dim"],
                  font=("Segoe UI", 8), relief="flat", cursor="hand2", bd=0,
                  activebackground=C["card"], activeforeground=C["rose"],
                  command=self._vider).pack(side="right")

        self.liste = tk.Listbox(cadre_liste, height=5,
                                bg=C["card"], fg=C["texte"],
                                font=FONT_MONO,
                                selectbackground=C["violet_dim"],
                                relief="flat", highlightthickness=0, bd=0,
                                activestyle="none")
        self.liste.pack(fill="x", padx=10, pady=(0,8))

        # Niveau de compression
        cadre_niv = tk.Frame(body, bg=C["card"],
                             highlightbackground=C["bordure"],
                             highlightthickness=1)
        cadre_niv.pack(fill="x", pady=(0,10))
        tk.Frame(cadre_niv, bg=C["card"]).pack(pady=6)
        self._lbl(cadre_niv, "  💫  Niveau de compression", fg=C["rose_clair"], bg=C["card"], font=FONT_LABEL).pack(anchor="w", padx=10)

        self.niveau_var = tk.IntVar(value=2)
        niveaux = [("1 — Léger  (qualité maximale)", 1),
                   ("2 — Moyen  (équilibré)", 2),
                   ("3 — Maximum  (taille minimale)", 3)]

        for txt, val in niveaux:
            tk.Radiobutton(cadre_niv, text=txt,
                           variable=self.niveau_var, value=val,
                           bg=C["card"], fg=C["texte"],
                           selectcolor=C["violet_dim"],
                           activebackground=C["card"],
                           activeforeground=C["rose_clair"],
                           font=("Segoe UI", 10),
                           cursor="hand2").pack(anchor="w", padx=20, pady=2)
        tk.Frame(cadre_niv, bg=C["card"]).pack(pady=4)

        # Progression
        cadre_prog = tk.Frame(body, bg=C["fond"])
        cadre_prog.pack(fill="x", pady=(0,6))

        style = ttk.Style()
        style.theme_use("default")
        style.configure("PDF.Horizontal.TProgressbar",
                        troughcolor=C["panneau"],
                        background=C["rose"], thickness=8)
        self.progress = ttk.Progressbar(cadre_prog, mode="determinate",
                                         style="PDF.Horizontal.TProgressbar")
        self.progress.pack(fill="x")
        self.label_statut = self._lbl(cadre_prog, "", fg=C["texte_dim"], font=FONT_PETIT)
        self.label_statut.pack(anchor="w", pady=(4,0))

        # Bouton
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

        self.label_resultat = self._lbl(body, "", fg=C["succes"], font=("Segoe UI", 10, "bold"))
        self.label_resultat.pack(pady=(4,0))

        self._lbl(self.root, "✦  made with love by kenz  ✦",
                  fg=C["violet_dim"], font=("Segoe UI", 8)).pack(pady=(0,10))

    def _on_drop(self, event):
        for chemin in self.root.tk.splitlist(event.data):
            chemin = chemin.strip("{}")
            if os.path.isdir(chemin): self._ajouter_dossier(chemin)
            elif chemin.lower().endswith(".pdf"): self._ajouter(chemin)

    def _parcourir(self):
        for f in filedialog.askopenfilenames(
            title="Choisir des PDFs",
            filetypes=[("PDF", "*.pdf")]
        ): self._ajouter(f)

    def _parcourir_dossier(self):
        d = filedialog.askdirectory(title="Choisir un dossier")
        if d: self._ajouter_dossier(d)

    def _ajouter_dossier(self, d):
        for f in os.listdir(d):
            if f.lower().endswith(".pdf"):
                self._ajouter(os.path.join(d, f))

    def _ajouter(self, chemin):
        if chemin not in self.fichiers:
            self.fichiers.append(chemin)
            self.liste.insert("end", f"  {os.path.basename(chemin)}")
        self.label_drop.config(text=f"📄   {len(self.fichiers)} PDF(s) sélectionné(s)")

    def _vider(self):
        self.fichiers.clear()
        self.liste.delete(0, "end")
        self.label_drop.config(text="📄   Glisse tes PDFs ici\nou clique pour choisir")
        self.label_resultat.config(text="")
        self.progress["value"] = 0
        self.label_statut.config(text="")

    def _lancer(self):
        if self.en_cours: return
        if not self.fichiers:
            messagebox.showwarning("Oups !", "Ajoute d'abord des PDFs 📄"); return
        self.en_cours = True
        self.btn.config(state="disabled", text="⏳   Compression en cours...")
        threading.Thread(target=self._compresser, daemon=True).start()

    def _compresser(self):
        niveau = self.niveau_var.get()
        total  = len(self.fichiers)
        av_tot = ap_tot = succes = 0
        self.progress.config(maximum=total, value=0)

        for i, chemin in enumerate(self.fichiers):
            nom    = os.path.basename(chemin)
            sortie = os.path.join(os.path.dirname(chemin), "compresses")
            os.makedirs(sortie, exist_ok=True)
            dest   = os.path.join(sortie, os.path.splitext(nom)[0] + "_compressed.pdf")
            self.label_statut.config(text=f"  ⏳  {nom}")
            try:
                av = os.path.getsize(chemin)
                compresser_pdf(chemin, dest, niveau)
                ap = os.path.getsize(dest)
                av_tot += av; ap_tot += ap; succes += 1
            except Exception: pass
            self.progress["value"] = i + 1
            self.root.update_idletasks()

        red = (1 - ap_tot / av_tot) * 100 if av_tot else 0
        self.label_statut.config(text="  ✓  PDFs sauvegardés dans le dossier 'compresses'")
        self.label_resultat.config(
            text=f"💜  {succes}/{total} PDFs  ·  {taille_lisible(av_tot)} → {taille_lisible(ap_tot)}  ·  -{red:.0f}% !"
        )
        self.btn.config(state="normal", text="✨   Compresser   ✨")
        self.en_cours = False


if __name__ == "__main__":
    root = TkinterDnD.Tk() if DND_DISPONIBLE else tk.Tk()
    AppCompresseurPDF(root)
    root.mainloop()
