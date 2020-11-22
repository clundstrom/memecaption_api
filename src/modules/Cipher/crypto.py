from collections import Counter
from .freqs import getFrequencyLetter, frequencies_english, alphabet_eng


def find_ngram(str, n):
    """
    Find all the n-grams and their distances
    :param str: string to match
    :param n: length of subsequence
    :return: list of distances between subsequences
    """
    distances = []
    for i in range(0, len(str) - 1):
        ngram = str[i:(i + n)]
        for j in range(i + 1, len(str) - 1):
            match = str[j:(j + n)]
            if (ngram == match):
                print(f"{match} - LOC: {i}, Match pos: {i + j}, Distance = {j}, Primes = {prime_factors(j)}")
                distances.append(j)
    return distances


def prime_factors(n):
    """
    Prime numbers of n
    """
    i = 2
    factors = []
    while i * i <= n:
        if n % i:
            i += 1
        else:
            n //= i
            factors.append(i)
    if n > 1:
        factors.append(n)
    return factors


def factorize(numlist):
    """
    Factorize distances of n-grams
    """
    primes = []
    for i in numlist:
        res = prime_factors(i)
        [primes.append(j) for j in res]
    return primes


def find_ngram_ofrange(str, length):
    """
    :param length: length of subsequence
    :return:
    """
    stats = []
    for i in range(2, length + 1):
        ngram = find_ngram(str, i)
        [stats.append(x) for x in ngram]

    return stats


def chi_square(ciphertext):
    """
    Calculates the CHI_SQUARE to determine the probability distributions of two Strings.
    If the two distributions are identical,
    the chi-squared statistic is 0,
    if the distributions are very different, some higher number will result.

    In cryptography this is used to compare strings against the English character distribution.

    :param ciphertext String to analyse.
    """

    result = 0
    ciphertext = ciphertext.upper()
    length = len(ciphertext)
    for i in frequencies_english:
        observed = ciphertext.count(i)
        expected = (getFrequencyLetter(i) / 100) * length
        result += ((observed - expected) ** 2) / expected
        ciphertext = ciphertext.replace(i, "")
    return round(result, 2)


def shift_char(char, shift):
    """
    Shifts char x steps. Based on English alphabet.
    :param char: char to shift.
    :param shift: amount to shift.
    :return: char.
    """
    char = char.upper()
    char = alphabet_eng[(alphabet_eng.index(char) + shift) % 26]
    return char


def caesar_shift(cipher, shift):
    """
    Caesar shift a string of characters.. Example: A,2 -> C
    :param cipher: ciphertext.
    :param shift: steps to shift.
    :return: new string.
    """
    new_cipher = []
    for i in cipher:
        new_cipher.append(shift_char(i, shift))
    return ''.join(new_cipher)


def chi_key_search(cipher):
    """
    Calculates CHI_SQUARE for all possible caesar shifts of a cipher and
    returns list of results.
    :param cipher: Ciphertext.
    :return: List of results.
    """
    results = []
    for i in range(0, 26):
        temp = caesar_shift(cipher, i)
        results.append((i, chi_square(temp), temp))
    return results


def print_results(result):
    print('{:<5}{:<10}{:<5}'.format("KEY", "CHI", "CIPHER"))

    for res in result:
        print('{:<5}{:<10}{:<5}'.format(res[0], res[1], res[2]))

    finding = min(result, key=lambda t: t[1])

    print("Findings..")
    print('{:<5}{:<10}{:<5}'.format(finding[0], finding[1], finding[2]))


if __name__ == '__main__':
    pass