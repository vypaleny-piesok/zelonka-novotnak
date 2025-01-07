import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import datetime
import json
from PIL import Image, ImageTk

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


def nastavit_prijem():
    prijem_okno = tk.Toplevel(root)
    bg_image = Image.open("food.jpg")
    bg_photo = ImageTk.PhotoImage(bg_image)

    # Create background label with image
    bg_label = tk.Label(prijem_okno, image=bg_photo)
    bg_label.image = bg_photo  # Keep a reference to avoid garbage collection
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    prijem_okno.title("Nastavenie príjmu")
    prijem_okno.geometry("400x300")  # Set a fixed window size for better design control

    # Set transparent or styled label and slider
    label_slider = tk.Label(prijem_okno, text="Nastavte cieľový kalorický príjem:",
                            bg="#ffffff", fg="#333333", font=("Helvetica", 12, "bold"))
    label_slider.place(relx=0.5, rely=0.3, anchor='center')

    # Customize slider colors
    slider = tk.Scale(prijem_okno, from_=1000, to=8000, orient='horizontal', length=300,
                      bg="#ffffff", fg="#000000", troughcolor="#76c7c0", sliderlength=25,
                      highlightbackground="#ffffff", activebackground="#ffa07a")
    slider.set(3000)  # Prednastavená hodnota
    slider.place(relx=0.5, rely=0.5, anchor='center')


root = tk.Tk()
root.title("Počítanie kalórií")
root.geometry("400x600")
bg_image = Image.open("food.jpg")
bg_photo = ImageTk.PhotoImage(bg_image)

# Create background label with image
bg_label = tk.Label(root, image=bg_photo)
bg_label.image = bg_photo  # Keep a reference to avoid garbage collection
bg_label.place(x=0, y=0, relwidth=1, relheight=1)
jedlo_var = tk.StringVar()
jedlo_label = tk.Label(root, text="Vyberte si jedlo:", bg="#ffffff", fg="#333333", font=("Helvetica", 12, "bold"))
jedlo_label.pack(pady=10)
jedlo_menu = ttk.Combobox(root, textvariable=jedlo_var, values=list(jedalna_databaza.keys()), state="readonly")
jedlo_menu.pack(pady=5)

# Create a style for the buttons
style = ttk.Style()
style.configure("TButton",
                font=("Helvetica", 10, "bold"),
                background="#76c7c0",
                foreground="black",
                padding=10,
                borderwidth=0,
                focuscolor='none')

# Modern buttons with style and positioning
pridat_button = ttk.Button(root, text="Pridať jedlo", command=pridat_jedlo, style="TButton")
pridat_button.pack(pady=10)

zrusit_button = ttk.Button(root, text="Zrušiť posledné jedlo", command=zrusit_posledne_jedlo, style="TButton")
zrusit_button.pack(pady=10)

historia_button = ttk.Button(root, text="Zobraziť históriu", command=zobrazit_historiu, style="TButton")
historia_button.pack(pady=10)

prijem_button = ttk.Button(root, text="Nastaviť denný príjem", command=nastavit_prijem, style="TButton")
prijem_button.pack(pady=10)

ulozit_button = ttk.Button(root, text="Uložiť údaje", command=ulozit_logy, style="TButton")
ulozit_button.pack(pady=10)

# Display summary of calorie intake
suhrn_label = tk.Label(root, text="📊 Súhrn príjmu kalórií:", bg="#ffffff", fg="#333333", font=("Helvetica", 12, "bold"))
suhrn_label.pack(pady=10)
suhrn_text = tk.Text(root, height=15, width=50, state=tk.DISABLED, bg="#f5f5f5", fg="#333333", font=("Helvetica", 10))
suhrn_text.pack(pady=10)


root.mainloop()

ulozit_logy()
