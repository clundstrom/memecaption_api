alphabet_eng = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
frequencies_english = {"A": 8.55,
                       "B": 1.60,
                       "C": 3.16,
                       "D": 3.87,
                       "E": 12.10,
                       "F": 2.18,
                       "G": 2.09,
                       "H": 4.96,
                       "I": 7.33,
                       "J": 0.22,
                       "K": 0.81,
                       "L": 4.21,
                       "M": 2.53,
                       "N": 7.17,
                       "O": 7.47,
                       "P": 2.07,
                       "Q": 0.10,
                       "R": 6.33,
                       "S": 6.73,
                       "T": 8.94,
                       "U": 2.68,
                       "V": 1.06,
                       "W": 1.83,
                       "X": 0.19,
                       "Y": 1.72,
                       "Z": 0.11}


def getFrequencyLetter(letter: str):
    if letter is None:
        raise ValueError("Invalid letter.")
    return frequencies_english.get(letter.upper(), 0)
