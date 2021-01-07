import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from consts import bdd
from fonctions import *


class Application(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        accueil = tk.Button(self, text='Accueil', command=lambda: self.show_frame(Menu))
        quitter = tk.Button(self, text='Quitter', command=self.destroy)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        accueil.pack(side=tk.LEFT, fill="both", expand=True)
        quitter.pack(side=tk.RIGHT, fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (Menu, Page1, Page2, Page3, Page4, Page5, Playing, Page6):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(Menu)

    def destroy(self):
        self.frames[Playing].stop_thread = True
        super(Application, self).destroy()

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def play(self, frequences, pauses):
        self.show_frame(Playing)
        self.frames[Playing].play(frequences, pauses)


class Liste(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.titres = titres_partitions(bdd)
        tk.Frame.__init__(self, parent)
        self.liste = tk.Listbox(self)
        for i, titre in enumerate(self.titres):
            self.liste.insert(i, titre[3:-1])
        self.liste.pack(side="top", fill="both", expand=True)


class Menu(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        bouton1 = tk.Button(self, text='Jouer une parition',
                            command=lambda: controller.show_frame(Page5))
        bouton2 = tk.Button(self, text='Ajouter une partition',
                            command=lambda: controller.show_frame(Page2))
        bouton3 = tk.Button(self, text='Lecteur ( animation )',
                            command=lambda: controller.show_frame(Playing))
        bouton1.pack(side="top", fill="x")
        bouton2.pack(side="top", fill="x")
        bouton3.pack(side="top", fill="x")


class Page1(Liste):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        play = tk.Button(self, text='Jouer la partition',
                         command=lambda: controller.play(
                             *read_sheet(read_line_file(bdd, (self.liste.curselection()[0] + 1) * 2))))
        play.pack(side="top", fill="x")


class Page2(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text='Ajouter une partition')
        bouton1 = tk.Button(self, text='depuis un fichier',
                            command=lambda: self.add_from_file())
        bouton2 = tk.Button(self, text='par inversion une partition existante',
                            command=lambda: controller.show_frame(Page3))
        bouton3 = tk.Button(self, text='par transposition une partition existante',
                            command=lambda: controller.show_frame(Page4))
        bouton4 = tk.Button(self, text='en créant une partition depuis celles déjà existante',
                            command=lambda: controller.show_frame(Page6))
        label.pack(side="top", fill="x")
        bouton1.pack(side="top", fill="x")
        bouton2.pack(side="top", fill="x")
        bouton3.pack(side="top", fill="x")
        bouton4.pack(side="top", fill="x")

    def add_from_file(self):
        filename = filedialog.askopenfilename(initialdir="/",
                                              title="Selectionner une partition",
                                              filetypes=(("txt files", "*.txt"),))
        append_partition(read_line_file(filename, 1))


class Page3(Liste):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        bouton = tk.Button(self, text="inverser", command=lambda: self.inversion())
        bouton.pack(side="top", fill="x")

    def inversion(self):
        line = read_line_file(bdd, (self.liste.curselection()[0] + 1) * 2)
        notes = list(read_sheet_frequences(line))
        notes = frequency_to_notes(notes)
        inversion(notes)
        partition = partition_to_line(notes, read_pauses(line))
        append_partition(partition)


class Page4(Liste):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        bouton = tk.Button(self, text="transposer", command=lambda: self.transposition())
        bouton.pack(side="top", fill="x")

    def transposition(self):
        line = read_line_file(bdd, (self.liste.curselection()[0] + 1) * 2)
        notes = list(read_sheet_frequences(line))
        notes = frequency_to_notes(notes)
        transposition(notes, simpledialog.askinteger(title="Transposition par k", prompt='Rentrer un entier k'))
        partition = partition_to_line(notes, read_pauses(line))
        append_partition(partition)


class Page5(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text='Jouer une partition ')
        bouton1 = tk.Button(self, text='depuis la base de données',
                            command=lambda: controller.show_frame(Page1))
        bouton2 = tk.Button(self, text='depuis un fichier',
                            command=lambda: self.open_file(controller))

        label.pack(side="top", fill="x")
        bouton1.pack(side="top", fill="x")
        bouton2.pack(side="top", fill="x")

    def open_file(self, controller):
        filename = filedialog.askopenfilename(initialdir="/",
                                              title="Selectionner une partition",
                                              filetypes=(("txt files", "*.txt"),))
        controller.thread = controller.play(*read_sheet(read_line_file(filename, 1)))


class Page6(Liste):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        bouton = tk.Button(self, text="appliquer markov", command=lambda: self.markov())
        bouton.pack(side="top", fill="x")

    def markov(self):
        line = read_line_file(bdd, (self.liste.curselection()[0] + 1) * 2)
        notes = list(read_sheet_frequences(line))
        notes = frequency_to_notes(notes)
        markov(notes, simpledialog.askinteger(title="Markov", prompt="Markov mode 1 ou 2 ?"))
        partition = partition_to_line(notes, read_pauses(line))
        append_partition(partition)


class Playing(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        length = self.winfo_width()
        self.canvas = tk.Canvas(self, )
        self.progress = ttk.Progressbar(self, orient=tk.HORIZONTAL, length=length, mode='indeterminate')
        self.bouton = tk.Button(self, text='pause', command=self.pause)
        self.bouton.pack(side="bottom", fill="x")
        self.progress.pack(side="bottom", fill="x")
        self.thread_play = None
        self.stop_thread = False
        self.pause_state = False

    def pause(self):
        if self.bouton['text'] == 'pause':
            self.bouton.configure(text='relancer')
        else:
            self.bouton.configure(text='pause')
        self.pause_state = not self.pause_state

    def play(self, frequences, pauses):
        """
        Fonction intermédiaire qui sert a lancer la fonction playsheet en background
        """
        self.progress["value"] = 0
        if self.thread_play:
            self.stop_thread = not self.stop_thread
            while self.thread_play.is_alive():
                sleep(0.1)
            self.stop_thread = not self.stop_thread

        if self.pause_state:
            self.pause()
        self.thread_play = threading.Thread(target=self.play_sheet, name="Player", args=(frequences, pauses))
        self.thread_play.start()

    def play_sheet(self, frequences, pauses):
        """
        Fonction qui à partir d’une séquence de fréquences et de durées, appelle
        les fonctions sound et sleep pour lire la partition musicale.
        :param frequences: liste de fréquences
        :param pauses: liste de durées
        """
        temps = 0
        for temp in pauses:
            temps += temp
        for i in range(len(frequences)):
            if not self.pause_state:
                if not self.stop_thread:
                    sound(frequences[i], pauses[i])
                    self.progress["value"] += pauses[i] * (100 / temps)
                    # bah c'est mieux sans pause enfait
                    # sleep(pauses[i])
            else:
                while self.pause_state and not self.stop_thread:
                    sleep(0.1)
