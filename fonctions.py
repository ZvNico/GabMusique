from utils import *
from tkinter import simpledialog


def append_partition(line, bdd=consts.bdd):
    with open(bdd, 'r+') as fichier:
        fichier.readline()
        temp = fichier.readline()
        i = 1
        while temp:
            if temp == line:
                simpledialog.messagebox.showerror(
                    message="Cette partition est déjà dans la base de donnée, il s'agit de la partition " + str(i))
                return
            fichier.readline()
            temp = fichier.readline()
            i += 1
        titre = simpledialog.askstring(title="Ajouter partition", prompt="Rentrer le titre de votre partition")
        if titre:
            fichier.writelines(f"#{i} {titre}\n")
            fichier.writelines(line)


def titres_partitions(bdd=consts.bdd):
    """
    :param bdd: base de donnée
    :return: liste de titre de partitions
    """
    titres = []
    with open(bdd, 'r') as fichier:
        line = fichier.readline()
        while line:
            titres.append(line)
            fichier.readline()
            line = fichier.readline()
    return titres


def frequency_to_notes(frequences):
    """
    Fonction qui prend en paramêtre une liste de fréquences pour retourner son équivalent en note codé numériquement
    :param fréquences: liste fréquences
    :return: liste de notes
    """
    notes = []
    for frequence in frequences:
        if frequence != -1:
            notes.append(consts.f_notes.index(frequence) + 1)
    return notes


def partition_to_line(notes, pauses):
    """
    :param notes: liste de notes musicales
    :return: ligne de partitions
    """
    ligne = ""
    print(notes, pauses)
    for note, pause in notes, pauses:
        print(note, pause)
        temp = consts.pauses.index(pause)
        if note == -1:
            ligne += 'Z'
        else:
            if temp != 'p':
                ligne += consts.notes.index(note)
        ligne += temp
        ligne += " "
    return ligne


def transposition(array, k):
    """
    Opération de transposition sur une partition musicales
    :param array: liste de notes musicales
    :param k: entier
    """
    # L est la taille de l'array
    L = len(array)
    for note in array:
        # pour chaque note on ajouter k
        note += k
        # on met au modulo L car on veut que la note reste dans l'intervalle de l'array originel
        note %= (L + 1)


def inversion(array):
    """
    Opération d'inversion sur un ensemble de notes musicales
    :param array: liste de notes musicales
    """
    L = len(array)

    for note in array:
        # on inverse chaque note
        note = (L + 1) - note
        # on met au modulo L car on veut que la note reste dans l'intervalle de l'array originel
        note %= (L + 1)


def markov(array, mode=1):
    """
    :param array: liste de notes musicales
    :param mode: mode  1 ou 2
    """
