import json
import os
import re
from typing import Dict, List, Any

TOKEN_PATTERN = re.compile(r"[a-zA-Z0-9]+")


def tokenize(text: str) -> List[str]:
    """
    Convert text into lowercase alphanumeric tokens.
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


def save_index(index: Dict[str, Any], path: str) -> None:
    """
    Save the inverted index to a JSON file.
    Creates directories if needed.
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(index, f, indent=2)


def load_index(path: str) -> Dict[str, Any]:
    """
    Load an inverted index from a JSON file.
    Raises FileNotFoundError if the file does not exist.
    """
    if not os.path.exists(path):
        print(
            "[ERROR] Index file not found.\n"
            f"  - Path: {path}\n"
            "  - Run 'build <max_pages>' before loading the index."
        )
        raise FileNotFoundError(path)

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
