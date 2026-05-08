import sys
import os

# Ensure Python can import from src/
sys.path.append(os.path.abspath("src"))

from search import print_word, find_terms


# -----------------------------
# PRINT WORD TESTS
# -----------------------------

def test_print_word_found():
    index = {
        "hello": [
            {"url": "url1", "freq": 2, "positions": [0, 3]}
        ]
    }

    result = print_word(index, "hello")

    assert result is not None
    assert isinstance(result, list)
    assert result[0]["url"] == "url1"
    assert result[0]["freq"] == 2
    assert result[0]["positions"] == [0, 3]


def test_print_word_case_insensitive():
    index = {
        "hello": [
            {"url": "url1", "freq": 1, "positions": [0]}
        ]
    }

    result = print_word(index, "HeLLo")

    assert result is not None
    assert result[0]["url"] == "url1"


def test_print_word_not_found():
    index = {"hello": []}
    result = print_word(index, "missingword")
    assert result is None


# -----------------------------
# FIND TERMS TESTS
# -----------------------------

def test_find_terms_single_word():
    index = {
        "good": [
            {"url": "url1", "freq": 1, "positions": [0]},
            {"url": "url2", "freq": 2, "positions": [1, 4]},
        ]
    }

    result = find_terms(index, ["good"])

    assert set(result) == {"url1", "url2"}


def test_find_terms_multi_word_and():
    index = {
        "good": [
            {"url": "url1", "freq": 1, "positions": []},
            {"url": "url2", "freq": 1, "positions": []},
        ],
        "friends": [
            {"url": "url1", "freq": 1, "positions": []}
        ]
    }

    result = find_terms(index, ["good", "friends"])

    assert result == ["url1"]


def test_find_terms_missing_word():
    index = {
        "good": [
            {"url": "url1", "freq": 1, "positions": []}
        ]
    }

    result = find_terms(index, ["good", "nonexistent"])

    assert result == []


def test_find_terms_case_insensitive():
    index = {
        "hello": [
            {"url": "url1", "freq": 1, "positions": []}
        ],
        "world": [
            {"url": "url1", "freq": 1, "positions": []},
            {"url": "url2", "freq": 1, "positions": []}
        ]
    }

    result = find_terms(index, ["HeLLo", "WORLD"])

    assert result == ["url1"]
