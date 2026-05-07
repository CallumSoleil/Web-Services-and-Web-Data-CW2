import sys
import os

# Ensure Python can import from src/
sys.path.append(os.path.abspath("src"))

from search import print_word, find_terms


def test_print_word_found():
    index = {
        "hello": {
            "url1": {"freq": 2, "positions": [0, 3]}
        }
    }

    result = print_word(index, "hello")
    assert result is not None
    assert "url1" in result
    assert result["url1"]["freq"] == 2


def test_print_word_not_found():
    index = {"hello": {}}
    result = print_word(index, "missingword")
    assert result is None


def test_find_terms_single_word():
    index = {
        "good": {
            "url1": {"freq": 1, "positions": [0]},
            "url2": {"freq": 2, "positions": [1, 4]},
        }
    }

    result = find_terms(index, ["good"])
    assert result == {"url1", "url2"}


def test_find_terms_multi_word_and():
    index = {
        "good": {"url1": {}, "url2": {}},
        "friends": {"url1": {}},
    }

    result = find_terms(index, ["good", "friends"])
    assert result == {"url1"}


def test_find_terms_missing_word():
    index = {
        "good": {"url1": {}}
    }

    result = find_terms(index, ["good", "nonexistent"])
    assert result == set()
