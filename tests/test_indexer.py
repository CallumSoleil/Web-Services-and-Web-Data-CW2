import sys
import os

# Ensure Python can import from src/
sys.path.append(os.path.abspath("src"))

from indexer import tokenize, build_index, save_index, load_index
import json


def test_tokenize_basic():
    text = "Hello, WORLD! 123"
    tokens = tokenize(text)
    assert tokens == ["hello", "world", "123"]


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


def test_save_and_load_index(tmp_path):
    pages = {"url1": "hello world"}
    index = build_index(pages)

    path = tmp_path / "index.json"
    save_index(index, str(path))

    assert os.path.exists(path)

    loaded = load_index(str(path))

    # JSON round-trip should preserve structure
    assert loaded == json.loads(json.dumps(index))
