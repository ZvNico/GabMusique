import tkinter as tk
from tkinter import filedialog
from consts import bdd
from utils import *
from fonctions import *


class Application(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.threads = []
        accueil = tk.Button(self, text='Accueil', command=lambda: self.show_frame(Menu))
        quitter = tk.Button(self, text='Quitter', command=self.destroy)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        accueil.pack(side=tk.LEFT, fill="both", expand=True)
        quitter.pack(side=tk.RIGHT, fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (Menu, Page1, Page2):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(Menu)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class Menu(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        bouton1 = tk.Button(self, text='Jouer une parition depuis la base de données',
                            command=lambda: controller.show_frame(Page1))
        bouton2 = tk.Button(self, text='Jouer une partition depuis un fichier',
                            command=lambda: self.open_file(controller))
        bouton3 = tk.Button(self, text='Ajouter une partition',
                            command=lambda: controller.show_frame(Page2))
        bouton1.pack(side="top", fill="x")
        bouton2.pack(side="top", fill="x")
        bouton3.pack(side="top", fill="x")

    def open_file(self, controller):
        filename = filedialog.askopenfilename(initialdir="/",
                                              title="Selectionner une partition",
                                              filetypes=(("txt files", "*.txt"),))
        controller.threads.append(play_sheet(*read_sheet(read_line_file(filename, 2))))


class Page1(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        titres = titres_partitions(bdd)
        liste = tk.Listbox(self)
        play = tk.Button(self, text='Jouer la partition',
                         command=lambda: play_sheet(
                             *read_sheet(read_line_file(bdd, (liste.curselection()[0] + 1) * 2))))
        for i, titre in enumerate(titres):
            liste.insert(i, titre[3:-1])
        liste.pack(side="top", fill="both", expand=True)
        play.pack(side="top", fill="x")


class Page2(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text='Ajouter une partition')
        bouton1 = tk.Button(self, text='depuis un fichier',
                            command=lambda: controller.show_frame(Page1))
        bouton2 = tk.Button(self, text='par inversion une partition existante',
                            command=lambda: controller.show_frame(Page1))
        bouton3 = tk.Button(self, text='par transposition une partition existante',
                            command=lambda: controller.show_frame(Page1))
        bouton4 = tk.Button(self, text='en créant une partition depuis celles déjà existante',
                            command=lambda: controller.show_frame(Page1))
        label.pack(side="top", fill="x")
        bouton1.pack(side="top", fill="x")
        bouton2.pack(side="top", fill="x")
        bouton3.pack(side="top", fill="x")
        bouton4.pack(side="top", fill="x")
