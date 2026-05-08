import sys
import os
import json

# Ensure Python can import from src/
sys.path.append(os.path.abspath("src"))

from indexer import tokenize, build_index, save_index, load_index


def test_tokenize_basic():
    text = "Hello, WORLD! 123"
    tokens = tokenize(text)
    assert tokens == ["hello", "world", "123"]


def test_tokenize_punctuation_and_case():
    text = "Good-good...GOOD!!"
    tokens = tokenize(text)
    assert tokens == ["good", "good", "good"]


def test_build_index_structure():
    pages = {
        "url1": "Good friends good",
        "url2": "Good enemies",
    }

    index = build_index(pages)

    # Words should exist
    assert "good" in index
    assert "friends" in index
    assert "enemies" in index

    # URL entries should exist
    assert "url1" in index["good"]
    assert "url2" in index["good"]

    # Frequency should be correct
    assert index["good"]["url1"]["freq"] == 2
    assert index["good"]["url2"]["freq"] == 1

    # Positions should be lists
    assert isinstance(index["good"]["url1"]["positions"], list)


def test_build_index_positions():
    pages = {"url": "a b a c a"}
    index = build_index(pages)

    assert index["a"]["url"]["positions"] == [0, 2, 4]
    assert index["b"]["url"]["positions"] == [1]
    assert index["c"]["url"]["positions"] == [3]


def test_build_index_case_insensitive():
    pages = {"url": "Hello hELLo HELLO"}
    index = build_index(pages)

    assert "hello" in index
    assert index["hello"]["url"]["freq"] == 3


def test_empty_pages_produces_empty_index():
    pages = {}
    index = build_index(pages)
    assert index == {}


def test_save_and_load_index(tmp_path):
    pages = {"url1": "hello world hello"}
    index = build_index(pages)

    path = tmp_path / "index.json"
    save_index(index, str(path))

    assert os.path.exists(path)

    loaded = load_index(str(path))

    # JSON round-trip should preserve structure exactly
    assert loaded == json.loads(json.dumps(index))
