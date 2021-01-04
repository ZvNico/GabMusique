from utils import *


def titres_partitions(bdd=consts.bdd):
    """
    :param bdd: base de donnée
    :return: liste de titre de partitions
    """
    titres = []
    with open(bdd, 'r') as fichier:
        line = fichier.readline()
        while line != '\n' and line:
            titres.append(line)
            fichier.readline()
            line = fichier.readline()
    return titres


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


def frequency_to_notes(frequences):
    """
    Fonction qui prend en paramêtre une liste de fréquences pour retourner son équivalent en note codé numériquement
    :param fréquences: liste fréquences
    :return: liste de notes
    """
    notes = []
    for frequence in frequences:
        notes.append(consts.f_notes.index(frequence) + 1)
    return notes


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
