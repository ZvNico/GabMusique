import tkinter as tk
from consts import bdd
from utils import *
from fonctions import *


def main():
    fenetre = tk.Tk()
    titres = titres_partitions(bdd)
    print(titres)
    liste = tk.Listbox(fenetre)
    play = tk.Button(fenetre, text='Jouer partition',
                     command=lambda: play_sheet(*read_sheet(read_line_file(bdd, (liste.curselection()[0] + 1) * 2))))
    for i, titre in enumerate(titres):
        liste.insert(i, titre[3:-1])
    liste.pack()
    play.pack()
    fenetre.mainloop()


# on lance le programmme seulement si il est execute dans ce .py
if __name__ == '__main__':
    main()
