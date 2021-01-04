import tkinter as tk
from consts import bdd
from utils import *
from fonctions import *


def main():
    fenetre = tk.Tk()
    titres = titres_partitions(bdd)
    print(titres)
    liste = tk.Listbox(fenetre)
    play = tk.Button(fenetre, text=liste.curselection(), command=fenetre.quit)
    for i, titre in enumerate(titres):
        liste.insert(i, titre[3:-1])
    play.pack()
    liste.pack()
    fenetre.mainloop()


# on lance le programmme seulement si il est execute dans ce .py
if __name__ == '__main__':
    main()
