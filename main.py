import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import datetime
import json
from PIL import Image, ImageTk

# Databáza jedál
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


# Funkcia na načítanie dnešných jedál
def nacitat_denne_jedla():
    """Načíta jedlá za dnešný deň zo súboru a aktualizuje súhrn."""
    global celkove_kalorie, jedalny_zaznam
    dnes = datetime.date.today().isoformat()
    if dnes in denny_log:
        jedalny_zaznam = denny_log[dnes]  # Načítaj existujúce záznamy
        celkove_kalorie = sum(kalorie for _, kalorie in jedalny_zaznam)
        aktualizovat_suhrn()



def ulozit_logy():
    dnes = datetime.date.today().isoformat()
    denny_log[dnes] = jedalny_zaznam  # Prepíš dnešný záznam aktuálnymi údajmi
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
    global celkove_kalorie, jedalny_zaznam, denny_log
    if jedalny_zaznam:
        posledne_jedlo, posledne_kalorie = jedalny_zaznam.pop()  # Odstráni len posledné jedlo
        celkove_kalorie -= posledne_kalorie

        # Aktualizácia denného logu
        dnes = datetime.date.today().isoformat()
        if dnes in denny_log and denny_log[dnes]:
            # Odstráni len posledný záznam v logu pre dnešný deň
            denny_log[dnes] = denny_log[dnes][:-1]  # Skôr odstráni posledný záznam, nie celú položku

            # Uloženie zmeneného logu do súboru
            ulozit_logy()

        aktualizovat_suhrn()  # Aktualizuje zobrazenie
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


def nastavit_prijem():
    prijem_okno = tk.Toplevel(root)
    bg_image = Image.open("")
    bg_photo = ImageTk.PhotoImage(bg_image)

    bg_label = tk.Label(prijem_okno, image=bg_photo)
    bg_label.image = bg_photo
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    prijem_okno.title("Nastavenie príjmu")
    prijem_okno.geometry("400x300")

    label_slider = tk.Label(prijem_okno, text="Nastavte cieľový kalorický príjem:",
                            bg="#ffffff", fg="#333333", font=("Helvetica", 12, "bold"))
    label_slider.place(relx=0.5, rely=0.3, anchor='center')

    slider = tk.Scale(prijem_okno, from_=1000, to=8000, orient='horizontal', length=300,
                      bg="#ffffff", fg="#000000", troughcolor="#76c7c0", sliderlength=25,
                      highlightbackground="#ffffff", activebackground="#ffa07a")
    slider.set(3000)
    slider.place(relx=0.5, rely=0.5, anchor='center')


# Funkcia na vymazanie dnešných jedal
def vymazat_denne_jedla():
    """Vymaže všetky jedlá za dnešný deň."""
    global celkove_kalorie, jedalny_zaznam
    dnes = datetime.date.today().isoformat()
    if dnes in denny_log:
        del denny_log[dnes]
    jedalny_zaznam = []
    celkove_kalorie = 0
    aktualizovat_suhrn()
    ulozit_logy()
    messagebox.showinfo("Vymazané", "Všetky jedlá za dnešný deň boli vymazané.")


# Hlavné GUI
root = tk.Tk()
root.title("Počítanie kalórií")
root.geometry("400x600")
bg_image = Image.open("")
bg_photo = ImageTk.PhotoImage(bg_image)

bg_label = tk.Label(root, image=bg_photo)
bg_label.image = bg_photo
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

jedlo_var = tk.StringVar()
jedlo_label = tk.Label(root, text="Vyberte si jedlo:", bg="#ffffff", fg="#333333", font=("Helvetica", 12, "bold"))
jedlo_label.pack(pady=10)

jedlo_menu = ttk.Combobox(root, textvariable=jedlo_var, values=list(jedalna_databaza.keys()), state="readonly")
jedlo_menu.pack(pady=5)

pridat_button = ttk.Button(root, text="Pridať jedlo", command=pridat_jedlo)
pridat_button.pack(pady=10)

zrusit_button = ttk.Button(root, text="Zrušiť posledné jedlo", command=zrusit_posledne_jedlo)
zrusit_button.pack(pady=10)

historia_button = ttk.Button(root, text="Zobraziť históriu", command=zobrazit_historiu)
historia_button.pack(pady=10)

prijem_button = ttk.Button(root, text="Nastaviť denný príjem", command=nastavit_prijem)
prijem_button.pack(pady=10)

vymazat_button = ttk.Button(root, text="Vymazať dnešné jedlá", command=vymazat_denne_jedla)
vymazat_button.pack(pady=10)

suhrn_text = tk.Text(root, height=15, width=50, state=tk.DISABLED)
suhrn_text.pack(pady=10)

nacitat_denne_jedla()
root.mainloop()

ulozit_logy()
