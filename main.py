import tkinter as tk
from tkinter import messagebox
import datetime
import json

# Databáza jedal(nedokoncene)
jedalna_databaza = {
    'jablko': 52,
    'banán': 96,
    'kuracie prsia': 165,
    'ryža': 130,
    'vajce': 68,
    'chlieb': 265,
    'brokolica': 55,
    'zemiaky': 77,
    'paradajka': 18,
    'losos': 208,
}

try:
    with open('ulozene_jedla.json', 'r') as subor:
        denny_log = json.load(subor)
except FileNotFoundError:
    denny_log = {}

celkove_kalorie = 0
jedalny_zaznam = []


def ulozit_logy():
    dnes = datetime.date.today().isoformat()
    if dnes not in denny_log:
        denny_log[dnes] = []
    denny_log[dnes].extend(jedalny_zaznam)
    with open('ulozene_jedla.json', 'w') as subor:
        json.dump(denny_log, subor, indent=4)

def pridat_jedlo():
    global celkove_kalorie
    jedlo = jedlo_var.get()
    if jedlo in jedalna_databaza:
        kalorie = jedalna_databaza[jedlo]
        celkove_kalorie += kalorie
        jedalny_zaznam.append((jedlo, kalorie))
        aktualizovat_suhrn()
    else:
        messagebox.showerror("Chyba", "Jedlo nie je v databáze. Skúste znova.")
def zrusit_posledne_jedlo():
    global celkove_kalorie
    if jedalny_zaznam:
        posledne_jedlo, posledne_kalorie = jedalny_zaznam.pop()
        celkove_kalorie -= posledne_kalorie
        aktualizovat_suhrn()
    else:
        messagebox.showinfo("Informácia", "Nie sú žiadne jedlá na zrušenie.")

def aktualizovat_suhrn():
    suhrn_text.config(state=tk.NORMAL)
    suhrn_text.delete(1.0, tk.END)
    for polozka, kal in jedalny_zaznam:
        suhrn_text.insert(tk.END, f"- {polozka}: {kal} kcal\n")
    suhrn_text.insert(tk.END, f"\n🔥 Celkový počet kalórií: {celkove_kalorie} kcal")
    suhrn_text.config(state=tk.DISABLED)


def zobrazit_historiu():
    historia_okno = tk.Toplevel(root)
    historia_okno.title("História jedál")
    historia_text = tk.Text(historia_okno, height=20, width=50)
    historia_text.pack()
    historia_text.config(state=tk.NORMAL)
    for datum, zaznamy in denny_log.items():
        historia_text.insert(tk.END, f"📅 {datum}\n")
        for jedlo, kalorie in zaznamy:
            historia_text.insert(tk.END, f"  - {jedlo}: {kalorie} kcal\n")
        historia_text.insert(tk.END, "\n")
    historia_text.config(state=tk.DISABLED)
    
root = tk.Tk()
root.title("Počítanie kalórií")
root.geometry("400x600")

jedlo_var = tk.StringVar()
jedlo_label = tk.Label(root, text="Vyberte si jedlo:")
jedlo_label.pack()
jedlo_menu = tk.OptionMenu(root, jedlo_var, *jedalna_databaza.keys())
jedlo_menu.pack()

# Button na pridanie jedla
pridat_button = tk.Button(root, text="Pridať jedlo", command=pridat_jedlo)
pridat_button.pack()

# Button na zrusenie posledneho jedla
zrusit_button = tk.Button(root, text="Zrušiť posledné jedlo", command=zrusit_posledne_jedlo)
zrusit_button.pack()

# Button na zobrazenie historie
historia_button = tk.Button(root, text="Zobraziť históriu", command=zobrazit_historiu)
historia_button.pack()

# Button na ulozenie historie
ulozit_button = tk.Button(root, text="Uložiť údaje", command=ulozit_logy)
ulozit_button.pack()

# Zobrazenie prijmu kalorii
suhrn_label = tk.Label(root, text="📊 Súhrn príjmu kalórií:")
suhrn_label.pack()
suhrn_text = tk.Text(root, height=15, width=50, state=tk.DISABLED)
suhrn_text.pack()

root.mainloop()

ulozit_logy()
