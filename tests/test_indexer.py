import sys
import os
import json

# Ensure Python can import from src/
sys.path.append(os.path.abspath("src"))

from indexer import tokenize, build_index, save_index, load_index


# -----------------------------
# TOKENIZE TESTS
# -----------------------------

def test_tokenize_basic():
    text = "Hello, WORLD! 123"
    tokens = tokenize(text)
    assert tokens == ["hello", "world", "123"]


def test_tokenize_punctuation_and_case():
    text = "Good-good...GOOD!!"
    tokens = tokenize(text)
    assert tokens == ["good", "good", "good"]


def test_tokenize_empty_string():
    assert tokenize("") == []


def test_tokenize_numbers_and_letters():
    text = "abc123 456def"
    tokens = tokenize(text)
    assert tokens == ["abc123", "456def"]


# -----------------------------
# BUILD INDEX TESTS
# -----------------------------

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

    # Posting lists should be lists
    assert isinstance(index["good"], list)

    # Extract URLs from posting list
    urls = [p["url"] for p in index["good"]]
    assert "url1" in urls
    assert "url2" in urls

    # Frequency should be correct
    p_url1 = next(p for p in index["good"] if p["url"] == "url1")
    p_url2 = next(p for p in index["good"] if p["url"] == "url2")

    assert p_url1["freq"] == 2
    assert p_url2["freq"] == 1

    # Positions should be lists
    assert isinstance(p_url1["positions"], list)


def test_build_index_positions():
    pages = {"url": "a b a c a"}
    index = build_index(pages)

    postings_a = index["a"][0]
    postings_b = index["b"][0]
    postings_c = index["c"][0]

    assert postings_a["positions"] == [0, 2, 4]
    assert postings_b["positions"] == [1]
    assert postings_c["positions"] == [3]


def test_build_index_case_insensitive():
    pages = {"url": "Hello hELLo HELLO"}
    index = build_index(pages)

    assert "hello" in index
    postings = index["hello"][0]
    assert postings["freq"] == 3


def test_build_index_empty_pages():
    pages = {}
    index = build_index(pages)
    assert index == {}


def test_build_index_single_word():
    pages = {"url": "test"}
    index = build_index(pages)

    assert "test" in index
    postings = index["test"][0]
    assert postings["url"] == "url"
    assert postings["freq"] == 1
    assert postings["positions"] == [0]


# -----------------------------
# SAVE / LOAD TESTS
# -----------------------------

def test_save_and_load_index(tmp_path):
    pages = {"url1": "hello world hello"}
    index = build_index(pages)

    path = tmp_path / "index.json"
    save_index(index, str(path))

    assert os.path.exists(path)

    loaded = load_index(str(path))

    # JSON round-trip should preserve structure exactly
    assert loaded == json.loads(json.dumps(index))


def test_save_index_creates_directory(tmp_path):
    # Save into a nested directory that doesn't exist yet
    nested_dir = tmp_path / "nested" / "deep"
    path = nested_dir / "index.json"

    index = {
        "hello": [
            {"url": "url", "freq": 1, "positions": [0]}
        ]
    }

    save_index(index, str(path))

    assert os.path.exists(path)
    assert load_index(str(path)) == index
