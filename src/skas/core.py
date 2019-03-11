#!/usr/bin/python
import re

import spacy

"""
Syllabification
"""
nlp = spacy.load('es')
accents_re = re.compile("[áéíóú]", re.I | re.U)
paroxytone_re = re.compile("([aeiou]|n|[aeiou]s)$", re.I | re.U)  # checks if a str ends in unaccented vowel/N/S

letter_clusters_re = re.compile(r"""
    ([iuü]h[iuü])|                                            # 1: vowels
    ([aáeéíoóú]h[iuü])|                                       # 2: open vowels
    ([iuü]h[aáeéíoóú])|                                       # 3: closed vowels
    ([a-záéíóúñ][bcdfghjklmnñpqrstvxyz][hlr][aáeéiíoóuúü])|   # 4: liquid and mute consonants
    ([bcdfghjklmnñpqrstvxyz][hlr][aáeéiíoóuúü])|              # 5: any char followed by liquid and mute consonant
    ([a-záéíóúñ][bcdfghjklmnñpqrstvxyz][aáeéiíoóuúü])|        # 6: non-liquid consonant
    ([aáeéíoóú][aáeéíoóú])|                                   # 7: vowel group
    ([a-záéíóúñ])                                             # 8: any char
""", re.I | re.U | re.VERBOSE)  # re.VERBOSE is needed to be able to catch the regex group for parse()

"""
Metrical Analysis
"""
LIASON_FIRST_PART = set(u"aeiouáéíóúAEIOUÁÉÍÓÚy")
LIASON_SECOND_PART = set(u"aeiouáéíóúAEIOUÁÉÍÓÚhy")
STRESSED_UNACCENTED_MONOSYLLABLES = set(["yo", "vio", "dio", "fe", "sol", "ti", "un"])
UNSTRESSED_UNACCENTED_MONOSYLLABLES = set(["me", "nos", "te", "os", "lo", "la", "los", "las", "le", "les", "se", "tan"])
"""
Metrical Analysis functions
"""


def have_prosodic_liason(first_syllable, second_syllable):
    """
    Checkfor prosodic liason between two syllables
    :param first_syllable: dic with key syllable (str) and is_stressed (bool) representing the first syllable
    :param second_syllable: dic with key syllable (str) and is_stressed (bool) representing the second syllable
    :return: True if there is prosodic liason and False otherwise
    :rtype: bool
    """
    return (first_syllable['syllable'][-1] in LIASON_FIRST_PART
            and second_syllable['syllable'][0] in LIASON_SECOND_PART)


"""
Syllabifier functions
"""


def hyphenate(word):
    """
    Hyphenates a word.
    :param word: The word to be hyphenated.
    :return: Hyphenation.
    :rtype: list
    """
    output = ""
    while len(word) > 0:
        output += word[0]
        # Returns first matching pattern.
        m = letter_clusters_re.search(word)
        if m is not None:
            # Adds hyphen to syllables if regex pattern is 4, 6, or 7
            output += "-" if m.lastindex in set([4, 6, 7]) else ""
        word = word[1:]
    return output.split("-")


def get_orthographic_accent(syllable_list):
    """
    Given a list of str representing syllables,
    return position in the list of a syllable bearing
    orthographic stress (with the acute accent mark in Spanish)
    :param syllable_list: list of syllables as str or unicode each
    :return: Position or None if no orthographic stress
    :rtype: int
    """
    word = "|".join(syllable_list)
    match = accents_re.search(word)
    position = None
    if match is not None:
        last_index = match.span()[0]
        position = word[:last_index].count("|")
    return position


def is_paroxytone(syllable_list):
    """
    Given a list of str representing syllables from a single word, check is it is paroxytonic (llana) or not
    :param syllable_list: List of syllables as str
    :return: True if paroxytone, False if not
    :rtype: bool
    """
    if not get_orthographic_accent("".join(syllable_list)):
        return paroxytone_re.search(syllable_list[len(syllable_list) - 1]) is not None
    return False


def spacy_tag_to_dict(tag):
    """
    Creater a dict from spacy pos tags
    :param tag: Extended spacy pos tag ("Definite=Ind|Gender=Masc|Number=Sing|PronType=Art")
    :return: A dictionary in the form of "{'Definite': 'Ind', 'Gender': 'Masc', 'Number': 'Sing', 'PronType': 'Art'}"
    :rtype: dict
    """
    if tag and '=' in tag:
        return dict([t.split('=') for t in tag.split('|')])
    else:
        return {}


def get_word_stress(word, pos, tag):
    """
    Gets a list of syllables from a word and creates a list with syllabified word and stressed syllable index
    :param word: List of str representing syllables
    :param pos: PoS tag from spacy ("DET")
    :param tag: Extended PoS tag info from spacy ("Definite=Ind|Gender=Masc|Number=Sing|PronType=Art")
    :return: Dictionary with [original syllab. word, stressed syllab. word, negative index position of stressed syllable]
    :rtype: dict
    """

    syllable_list = hyphenate(word)
    if len(syllable_list) == 1:
        if ((syllable_list[0] not in UNSTRESSED_UNACCENTED_MONOSYLLABLES)
                and ((syllable_list[0] in STRESSED_UNACCENTED_MONOSYLLABLES)
                     or (pos not in ("DET", "PRON"))
                     or (pos == "PRON" and tag.get("Case") == "Nom")
                     or (pos == "DET" and tag.get("Definite") == "Ind"))):
            stressed_position = -1
        else:
            stressed_position = 0  # unstressed monosyllable
    else:
        tilde = get_orthographic_accent(syllable_list)
        # If an orthographic accent exists, that syllable negative index is saved.
        if tilde is not None:
            stressed_position = -(len(syllable_list) - tilde)
        # Else if the word is paroxytone (llana) we save the penultimate syllable.
        elif is_paroxytone(syllable_list):
            stressed_position = -2
        # If the word does not meet the above criteria that means that it's an oxytone word (aguda).
        else:
            stressed_position = -1
    return {
        "syllables": [{"syllable": syllable, "is_stressed": len(syllable_list) - index == -stressed_position}
                      for index, syllable in enumerate(syllable_list)],
        "stress_position": stressed_position,
    }


def get_syllables(word_list):
    """
    Gets a list of syllables from a word and creates a list with syllabified word and stressed syllabe index
    :param word_list: List of spacy objects representing a word or sentence
    :return: List with [original syllab. word, stressed syllab. word, negative index position of stressed syllable]
    :rtype: list
    """
    out = []
    for word in word_list:
        if word.is_alpha:
            pos, tag = word.tag_.split("__")
            tags = spacy_tag_to_dict(tag)
            stressed_word = get_word_stress(word.text, pos, tags)
            out.append(stressed_word)
        else:
            out.append({"symbol": word.text})
    return out


def get_scansion(text):
    """
    Generates a list of dictionaries for each line
    :param text: Full text to be analized
    :return: list of dictionaries per line
    :rtype: list
    """
    tokens = nlp(text)
    seen_tokens = []
    lines = []
    for token in tokens:
        if token.pos_ == "SPACE" and '\n' in token.orth_ and len(seen_tokens) > 0:
            lines.append({"tokens": get_syllables(seen_tokens)})
            seen_tokens = []
        else:
            seen_tokens.append(token)
    if len(seen_tokens) > 0:
        lines.append({"tokens": get_syllables(seen_tokens)})
    return lines
