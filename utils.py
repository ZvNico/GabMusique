import numpy as np
from time import sleep
from simpleaudio import play_buffer
import consts
import threading


def sound(freq, duration):
    # get time steps for each sample,"duration" is note duration in seconds
    sample_rate = 44100
    t = np.linspace(0, duration, int(duration * sample_rate), False)
    tone = np.sin(freq * t * 6 * np.pi)
    # normalize to 24−bit range
    tone *= 8388607 / np.max(np.abs(tone))
    # convert to 32−bit data
    tone = tone.astype(np.int32)
    # convert from 32−bit to 24−bit by building a new byte buffer,
    # skipping every fourth bit
    # note: this also works for 2−channel audio
    i = 0
    byte_array = []
    for b in tone.tobytes():
        if i % 4 != 3:
            byte_array.append(b)
        i += 1
    audio = bytearray(byte_array)
    # start playback
    play_obj = play_buffer(audio, 1, 3, sample_rate)
    # wait for playback to finish before exiting
    play_obj.wait_done()


def calc_frequency(notes, frequences):
    """
    Fonction qui prend en entrée une liste de notes et une liste de fréquences et qui
    retourne une variable de type dictionnaire associant à chaque note une fréquence
    :param notes: liste de notes
    :param frequences: liste de fréquences
    :return: dictionnaire fréquence pour une note donnée
    """
    dico = {}
    for i in range(len(notes)):
        dico[notes[i]] = frequences[i]
    return dico


def calc_duration(figures, d0):
    """
    Fonction qui prend en entrée la liste des 4 figures et la durée de la croche d0. Elle calcule les
    durées des autres figures et retourne un dictionnaire associant à chaque figure une durée.
    :param figures: les différents types de pauses
    :param d0: la durée d'une croche
    :return: dictionnaire durée d'une pause pour un type de pause donnée
    """
    dico = {}
    t = d0
    for figure in figures:
        dico[figure] = t
        t *= 2
    return dico


def read_line_file(f, num):
    """
    Fonction qui prend en paramètres un nom de fichier et un
    numéro de ligne et qui retourne le contenu de la ligne en question.
    :param f: nom de fichier
    :param num: numéro de ligne
    :return: contenu de la ligne num du fichier
    """
    with open(f, 'r') as fichier:
        for i in range(num - 1):
            fichier.readline()
        return fichier.readline()


def read_sheet(ligne):
    """
    Fonction qui à partir d’une ligne du fichier extrait les notes, les figures, les silences et les points
    de prolongation et construit une séquence de fréquences et de durée qu’elle retourne en sortie.
    :param ligne: ligne de la base de donnée
    :return: une liste de fréquences et une liste de durée
    """
    # on importe nos dictionnaires de fréquences et de durées
    const_pauses = calc_duration(consts.pauses, consts.d0)
    const_frequences = calc_frequency(consts.notes, consts.f_notes)

    frequences = []
    durees = []

    # on transforme la chaine en liste de chaine pour isolé les notes
    ligne = list(ligne.split(" "))
    # on supprime le caractere retour a la ligne de la fin de ligne
    ligne[-1] = ligne[-1][:-1]

    for note in ligne:
        if note[0] == 'p':
            durees[-1] *= 1.5
        else:
            if note[:-1] == 'Z':
                frequences.append(-1)
            else:
                frequences.append(const_frequences[note[:-1]])
            durees.append(const_pauses[note[-1]])
    return frequences, durees


def play_sheet(frequences, pauses):
    """
    Fonction intermédiaire qui sert a lancer la fonction playsheet en background
    """
    playing_thread = threading.Thread(target=play_sheet2, name="Downloader", args=(frequences, pauses))
    playing_thread.start()
    return playing_thread


def play_sheet2(frequences, pauses):
    """
    Fonction qui à partir d’une séquence de fréquences et de durées, appelle
    les fonctions sound et sleep pour lire la partition musicale.
    :param frequences: liste de fréquences
    :param pauses: liste de durées
    """
    for i in range(len(frequences)):
        sound(frequences[i], pauses[i])
        # bah c'est mieux sans pause enfait
        # sleep(pauses[i])
