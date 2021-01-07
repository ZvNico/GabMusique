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
            fichier.writelines(line + "\n")


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
        else:
            notes.append(frequence)
    return notes


def partition_to_line(notes, pauses):
    """
    :param notes: liste de notes musicales
    :param pauses: liste de pauses déjà en caractère
    :return: ligne de partitions
    """
    ligne = ""
    p = 0
    minimum = minpositif(notes)
    for i in range(len(pauses)):
        if pauses[i] != 'p':
            if notes[i - p] == -1:
                ligne += 'Z'
            else:
                ligne += consts.notes[notes[i - p] - minimum]
        else:
            p += 1
        ligne += pauses[i]
        ligne += " "

    return ligne[:-1]


def minpositif(liste):
    minimum = liste[0]
    for i in range(1, len(liste)):
        if 0 < liste[i] < minimum:
            minimum = liste[i]
    return minimum


def transposition(liste, k):
    """
    Opération de transposition sur une partition musicales
    :param liste: liste de notes musicales
    :param k: entier
    """
    L = [minpositif(liste), max(liste)]
    for i in range(len(liste)):
        if liste[i] != -1:
            # pour chaque note on ajouter k
            liste[i] += k
            # on met au modulo L car on veut que la note reste dans l'intervalle de l'liste originel
            liste[i] %= (L[1] + 1)
            if liste[i] == 0:
                liste[i] += L[0]


def inversion(liste):
    """
    Opération d'inversion sur un ensemble de notes musicales
    :param liste: liste de notes musicales
    """
    L = [minpositif(liste), max(liste)]
    for i in range(len(liste)):
        if liste[i] != -1:
            # on inverse chaque note
            liste[i] = (L[1] + 1) - liste[i]
            # on met au modulo L car on veut que la note reste dans l'intervalle de l'liste originel
            liste[i] %= (L[1] + 1)
            if liste[i] == 0:
                liste[i] += L[0]


def markov(liste, mode=1):
    """
    :param liste: liste de notes musicales
    :param mode: mode  1 ou 2
    """
