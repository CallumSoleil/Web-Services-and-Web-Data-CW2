import json
import os
import re
from typing import Dict, List


# Simple alphanumeric token pattern
TOKEN_PATTERN = re.compile(r"[a-zA-Z0-9]+")


def tokenize(text: str) -> List[str]:
    """
    Convert text into lowercase alphanumeric tokens.
    Case-insensitive by design.
    """
    return TOKEN_PATTERN.findall(text.lower())


def build_index(pages: Dict[str, str]) -> Dict[str, Dict[str, dict]]:
    """
    Build an inverted index with frequency and positional statistics.

    Structure:
    {
        "word": {
            "url1": {"freq": int, "positions": [int, ...]},
            "url2": {"freq": int, "positions": [int, ...]}
        },
        ...
    }
    """
    index: Dict[str, Dict[str, dict]] = {}

    for url, text in pages.items():
        words = tokenize(text)

        for pos, word in enumerate(words):
            if word not in index:
                index[word] = {}

            if url not in index[word]:
                index[word][url] = {"freq": 0, "positions": []}

            index[word][url]["freq"] += 1
            index[word][url]["positions"].append(pos)

    return index


def save_index(index: dict, path: str) -> None:
    """
    Save the inverted index to a JSON file.
    """
    directory = os.path.dirname(path)
    if directory == "":
        path = os.path.join("data", path)

    with open(path, "w") as f:
        json.dump(index, f, indent=2)


def load_index(path: str) -> dict:
    """
    Load an inverted index from a JSON file.
    """
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
