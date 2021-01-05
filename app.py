import tkinter as tk
from consts import bdd
from utils import *
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

        for F in (Menu, Page1):
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
        bouton1 = tk.Button(self, text='Jouer une parition depuis la base de donnée',
                            command=lambda: controller.show_frame(Page1))
        bouton1.pack()


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
        liste.pack()
        play.pack()
