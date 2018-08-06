import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
import smtplib
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


"""
OPOMBA K PROGRAMU:

Ko boste pregledovali program, uporabite račun
ime: lojzekpintar@gmail.com
geslo: lojzekpintar123
saj je sicer treba spremeniti nastavitve v google računu, česar ne pričakujem, ne želim pa se zameriti googlu s tem,
da bi poizkušal zaobiti njihove varnostne ukrepe (gotovo mi tudi ne bi uspelo). Ta račun pa je namenjen izključno
eksperimentiranju.

Če računa ne želite uporabljati, v tekstovno datoteko imena_gesla.txt navedite "ime, geslo" in tako se boste lahko
prijavili s tem imenom in geslom. Sporočil v tem primeru ne boste mogli pošiljati, lahko pa jih boste vseeno shranili.
"""


DATOTEKA_UPORABNIKOV = "imena_gesla.txt"
DATOTEKA_SPOROČIL = "poslana_sporocila.txt"
UPORABNIKI = list()
UPORABNIK = list()
try:
    with open(DATOTEKA_UPORABNIKOV, "x") as dat:
        for vrstica in dat:
            UPORABNIKI.append(tuple(vrstica.split(", ")))
except:
    with open(DATOTEKA_UPORABNIKOV, "r") as dat:
        for vrstica in dat:
            UPORABNIKI.append(tuple(vrstica.split(", ")))


# povezava razredov

class Mail(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, "Mail")

        vsebina = tk.Frame(self)
        vsebina.pack(expand=True)
        vsebina.grid_rowconfigure(100, weight=1)
        vsebina.grid_columnconfigure(100, weight=1)

        self.frames = dict()

        for i in [Prijava, Registracija, Posiljanje]:
            frame = i(vsebina, self)
            self.frames[i] = frame
            frame.grid(row=100, column=100, sticky="nsew")

        self.show_frame(Prijava)

    def show_frame(self, vsebina):
        frame = self.frames[vsebina]
        frame.tkraise()


# prijavni okvir

class Prijava(tk.Frame):
    def __init__(self, stars, nadzor):
        self.nadzor = nadzor

        tk.Frame.__init__(self, stars)

        self.uporabnikEntry = tk.Entry(self)
        self.gesloEntry = tk.Entry(self, show="*")
        self.opozorilo = tk.Label(self, text="Uporabniško ime ali geslo ni pravo. Ali si se registriral?",
                                  font=("Times", "10"))

        ttk.Label(self, text='Pozdravljen v mailu. Tukaj lahko pošlješ eno ali "spam" sporočil.', font=("Times", "20"))\
            .grid(row=1, columnspan=100, pady=(10, 20), padx=10, sticky="nsew")

        ttk.Label(self, text="POZOR! Pred prvo prijavo se moraš registrirati!", font=("Times", "13"))\
            .grid(row=2, columnspan=4, pady=(30, 30), padx=10, sticky="nsew")
        ttk.Button(self, text="registracija", command=lambda: nadzor.show_frame(Registracija))\
            .grid(row=2, column=4, pady=(30, 30))

        ttk.Label(self, text="Ko si registriran, se lahko tukaj prijaviš:", font=("Times", "13")) \
            .grid(row=3, columnspan=4, pady=(30, 15), padx=10, sticky="nsew")

        tk.Label(self, text="Uporabniško ime: ", font=("Times", "11"))\
            .grid(row=4, column=1, pady=(5, 10), sticky="e")

        self.uporabnikEntry.grid(row=4, column=2, pady=(5, 10), sticky="nsew")

        tk.Label(self, text="@gmail.com", font=("Times", "11")) \
            .grid(row=4, column=3, pady=(5, 10), sticky="w")

        tk.Label(self, text="Geslo: ", font=("Times", "11"))\
            .grid(row=5, column=1, pady=(5, 10), sticky="e")

        self.gesloEntry.grid(row=5, column=2, pady=(5, 10), sticky="nsew")

        ttk.Button(self, text="prijava", command=self.verificiraj)\
            .grid(row=6, column=2, pady=5, sticky="nsew")
        ttk.Button(self, text="izhod", command=quit)\
            .grid(row=7, column=2, pady=5, sticky="nsew")

    def verificiraj(self):
        up_ime = str(self.uporabnikEntry.get())
        geslo = str(self.gesloEntry.get()) + "\n"

        if (up_ime, geslo) in UPORABNIKI:
            UPORABNIK.append((up_ime, geslo[:-1]))
            self.opozorilo.grid_forget()
            return self.nadzor.show_frame(Posiljanje)
        else:
            self.opozorilo.grid(row=8, columnspan=100, pady=0, padx=10, sticky="w")
            return self.nadzor.show_frame(Prijava)


# registracijski okvir

class Registracija(tk.Frame):
    def __init__(self, stars, nadzor):
        self.nadzor = nadzor

        tk.Frame.__init__(self, stars)

        self.nov_uporabnikEntry = tk.Entry(self)
        self.novo_gesloEntry = tk.Entry(self, show="*")
        self.opozorilo = tk.Label(self, text="Neveljaven račun, ali pa je uporabnik že registriran! "
                                             "Morda pa moraš preveriti nastavitve na gmail računu.",
                                  font=("Times", "10"))
        self.uspeh = tk.Label(self, text="Uspešno ste se registrirali! Lahko se vrnete na stran za prijavo.",
                              font=("Times", "10"))

        ttk.Label(self, text="Tukaj se lahko registriraš. ", font=("Times", "20"))\
            .grid(row=1, columnspan=100, pady=(10, 20), padx=10, sticky="nsew")

        ttk.Label(self, text="Če si že registriran, se lahko vrneš na stran za prijavo.", font=("Times", "13")) \
            .grid(row=2, columnspan=5, pady=(30, 30), padx=10, sticky="nsew")
        ttk.Button(self, text="na prijavo", command=lambda: nadzor.show_frame(Prijava)) \
            .grid(row=2, column=5, pady=(30, 30))

        ttk.Label(self, text="Vpiši svoj gmail in geslo:", font=("Times", "13")) \
            .grid(row=3, columnspan=4, pady=(30, 15), padx=10, sticky="nsew")

        tk.Label(self, text="Gmail: ", font=("Times", "11"))\
            .grid(row=4, column=1, pady=(5, 10), sticky="e")

        self.nov_uporabnikEntry.grid(row=4, column=2, pady=(5, 10), sticky="nsew")

        tk.Label(self, text="@gmail.com", font=("Times", "11"))\
            .grid(row=4, column=3, pady=(5, 10), sticky="w")

        tk.Label(self, text="Geslo: ", font=("Times", "11"))\
            .grid(row=5, column=1, pady=(5, 10), sticky="e")

        self.novo_gesloEntry.grid(row=5, column=2, pady=(5, 10), sticky="nsew")

        ttk.Button(self, text="registriraj me", command=self.registracija)\
            .grid(row=6, column=2, pady=5, sticky="nsew")
        ttk.Button(self, text="izhod", command=quit)\
            .grid(row=7, column=2, pady=5, sticky="nsew")

    def registracija(self):
        ime = str(self.nov_uporabnikEntry.get())
        geslo = str(self.novo_gesloEntry.get()) + "\n"
        imena = [oseba[0] for oseba in UPORABNIKI]
        server = smtplib.SMTP("smtp.gmail.com", 587)
        if str(ime) in imena:
            self.uspeh.grid_forget()
            self.opozorilo.grid(row=8, columnspan=10, pady=0, padx=10, sticky="w")
        else:
            try:
                server.starttls()
                server.login(ime + "@gmail.com", geslo)
                with open(DATOTEKA_UPORABNIKOV, "a") as dat:
                    dat.write(ime + ", " + geslo)
                    UPORABNIKI.append((ime, geslo))
                self.opozorilo.grid_forget()
                self.uspeh.grid(row=8, columnspan=100, pady=0, padx=10, sticky="w")
            except:
                self.uspeh.grid_forget()
                self.opozorilo.grid(row=8, columnspan=100, pady=0, padx=10, sticky="w")
        return self.nadzor.show_frame(Registracija)


# Za pošiljanje

class Posiljanje(tk.Frame):
    def __init__(self, stars, nadzor):
        self.nadzor = nadzor

        tk.Frame.__init__(self, stars)

        self.prejemnikiEntry = tk.Entry(self)
        self.zadevaEntry = tk.Entry(self)
        self.sporociloText = ScrolledText(self, height=15)
        self.kolicinaEntry = tk.Entry(self, width=3)
        self.uspeh = tk.Label(self, text="Sporočilo poslano!", font=("Times", "10"))
        self.napaka = tk.Label(self, text="Prišlo je do napake! Poskusi ponovno.", font=("Times", "10"))
        self.shranjeno = tk.Label(self, text="Uspešno shranjeno!", font=("Times", "10"))

        tk.Label(self, text="Po uspešni prijavi, lahko sedaj pošiljaš sporočila.", font=("Times", "20"))\
            .grid(row=1, columnspan=100, pady=(10, 20), padx=10, sticky="nsew")

        ttk.Button(self, text="odjava", command=self.odjava)\
            .grid(row=2, column=1, pady=(30, 30), sticky="nsew")
        tk.Label(self, text="Ko končaš se lahko odjaviš tukaj.", font=("Times", "13")) \
            .grid(row=2, column=2, pady=(30, 30), padx=10, sticky="nsew")

        tk.Label(self, text="Prejemniki: ", font=("Times", "11"))\
            .grid(row=3, column=1, pady=(5, 10), sticky="e")
        self.prejemnikiEntry.grid(row=3, column=2, columnspan=99, pady=(5, 10), sticky="nsew")

        tk.Label(self, text="Zadeva: ", font=("Times", "11")) \
            .grid(row=4, column=1, pady=(5, 10), sticky="e")
        self.zadevaEntry.grid(row=4, column=2, columnspan=99, pady=(5, 10), sticky="nsew")

        tk.Label(self, text="Sporocilo: ", font=("Times", "11"))\
            .grid(row=5, column=1, pady=(5, 10), sticky="e")
        self.sporociloText.grid(row=5, column=2, columnspan=99, rowspan=20, pady=(5, 10))

        tk.Label(self, text="Koliko sporočil želiš poslati vsakemu? ", font=("Times", "11"))\
            .grid(row=26, column=2, sticky="e")
        self.kolicinaEntry.grid(row=26, column=3, sticky="w")
        self.kolicinaEntry.delete("0", "end")
        self.kolicinaEntry.insert("0", "1")

        ttk.Button(self, text="pošlji", command=self.poslji)\
            .grid(row=26, column=100, sticky="e")
        ttk.Button(self, text="shrani sporočilo", command=self.shrani) \
            .grid(row=26, column=99, sticky="e")

    def odjava(self):
        UPORABNIK.pop()
        return self.nadzor.show_frame(Prijava)

    def poslji(self):
        try:
            posiljatelj = UPORABNIK[-1][0] + "@gmail.com"
            geslo = UPORABNIK[-1][1]
            prejemniki = str(self.prejemnikiEntry.get()).split(", ")
            zadeva = str(self.zadevaEntry.get())
            sporocilo = str(self.sporociloText.get(index1="1.0", index2="end"))
            kolicina = str(self.kolicinaEntry.get())
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(posiljatelj, geslo)

            for oseba in prejemniki:
                for i in range(1, int(kolicina) + 1):
                    msg = MIMEMultipart()
                    msg["From"] = posiljatelj
                    msg["To"] = oseba
                    msg["Subject"] = zadeva + str(i)
                    msg.attach(MIMEText(sporocilo, "plain"))
                    text = msg.as_string()
                    server.sendmail(posiljatelj, oseba, text)
                    if int(kolicina) > 1:
                        time.sleep(2)
            self.napaka.grid_forget()
            self.shranjeno.grid_forget()
            self.uspeh.grid(row=27, column=2, sticky="w")
        except:
            self.uspeh.grid_forget()
            self.shranjeno.grid_forget()
            self.napaka.grid(row=27, column=2, sticky="w")

    def shrani(self):
        posiljatelj = UPORABNIK[-1][0] + "@gmail.com"
        prejemniki = str(self.prejemnikiEntry.get()).split(", ")
        zadeva = str(self.zadevaEntry.get())
        sporocilo = str(self.sporociloText.get(index1="1.0", index2="end"))
        trenutni_cas = time.strftime("%d-%m-%Y %H:%M:%S", time.localtime())
        with open(DATOTEKA_SPOROČIL, "a", encoding="UTF-8") as dat:
            dat.write("Pošiljatelj: " + posiljatelj + "\n" * 2)
            dat.write("Prejemniki: " + ", ".join(prejemniki) + "\n" * 2)
            dat.write("Zadeva: " + zadeva + "\n" * 2)
            dat.write("Sporočilo: " + "\n" + sporocilo + "\n" * 2)
            dat.write("Shranjeno: " + str(trenutni_cas) + "\n")
            dat.write("=" * 100 + "\n")
        self.uspeh.grid_forget()
        self.napaka.grid_forget()
        self.shranjeno.grid(row=27, column=2, sticky="w")


Mail().mainloop()
