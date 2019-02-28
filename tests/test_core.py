from skas.core import get_orthographic_accent
from skas.core import get_syllables
from skas.core import get_word_stress
from skas.core import have_prosodic_liason
from skas.core import hyphenate
from skas.core import is_paroxytone


def test_have_prosodic_liason():
    first_syllable = {'syllable': 'ca', 'is_stressed': True}
    second_syllable = {'syllable': 'en', 'is_stressed': False}
    assert have_prosodic_liason(first_syllable, second_syllable) is True


def test_hyphenate():
    word = "platanero"
    output = ['pla', 'ta', 'ne', 'ro']
    assert hyphenate(word) == output


def test_get_orthographic_accent():
    syllable_list = ['plá', 'ta', 'no']
    output = 0
    assert get_orthographic_accent(syllable_list) == output


def test_get_orthographic_accent_with_no_tilde():
    syllable_list = ['pla', 'ta', 'ne', 'ro']
    assert get_orthographic_accent(syllable_list) is None


def test_is_paroxytone():
    syllable_list = ['pla', 'ta', 'ne', 'ro']
    assert is_paroxytone(syllable_list) is True


def test_is_paroxytone_with_tilde():
    syllable_list = ['cés', 'ped']
    assert is_paroxytone(syllable_list) is False


def test_is_paroxytone_with_proparoxytone():
    syllable_list = ['es', 'drú', 'ju', 'la']
    assert is_paroxytone(syllable_list) is False


def test_is_paroxytone_with_oxytone_with_tilde():
    syllable_list = ['a', 'com', 'pa', 'ñó']
    assert is_paroxytone(syllable_list) is False


def test_is_paroxytone_with_oxytone_no_tilde():
    syllable_list = ['tam', 'bor']
    assert is_paroxytone(syllable_list) is False


def test_get_word_stress():
    word = "plátano"
    output = {'syllables': [{'syllable': 'plá', 'is_stressed': True},
                            {'syllable': 'ta', 'is_stressed': False},
                            {'syllable': 'no', 'is_stressed': False}],
              'stress_position': -3}
    assert get_word_stress(word) == output


def test_get_word_stress_stressed_monosyllables_without_tilde():
    word = "yo"
    output = {'syllables': [{'syllable': 'yo', 'is_stressed': True}],
              'stress_position': -1}
    assert get_word_stress(word) == output


def test_get_word_stress_unstressed_monosyllables_without_tilde():
    word = "mi"
    output = {'syllables': [{'syllable': 'mi', 'is_stressed': False}],
              'stress_position': 0}
    assert get_word_stress(word) == output


def test_get_word_stress_no_tilde():
    word = "campo"
    output = {'syllables': [{'syllable': 'cam', 'is_stressed': True},
                            {'syllable': 'po', 'is_stressed': False}],
              'stress_position': -2}
    assert get_word_stress(word) == output


def test_get_word_stress_oxytone():
    word = "tambor"
    output = {'syllables': [{'syllable': 'tam', 'is_stressed': False},
                            {'syllable': 'bor', 'is_stressed': True}],
              'stress_position': -1}
    assert get_word_stress(word) == output


def test_test_get_syllables():
    word = "físico-químico"
    output = [{'syllables': [{'syllable': 'fí', 'is_stressed': True},
                             {'syllable': 'si', 'is_stressed': False},
                             {'syllable': 'co', 'is_stressed': False}],
               'stress_position': -3},
              {'syllables': [{'syllable': 'quí', 'is_stressed': True},
                             {'syllable': 'mi', 'is_stressed': False},
                             {'syllable': 'co', 'is_stressed': False}],
               'stress_position': -3}]
    assert get_syllables(word) == output
