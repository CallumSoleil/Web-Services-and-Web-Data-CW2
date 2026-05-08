import json
import os
import re
from typing import Dict, List, Any

TOKEN_PATTERN = re.compile(r"[a-zA-Z0-9]+")


def tokenize(text: str) -> List[str]:
    """Convert text into lowercase alphanumeric tokens."""
    return TOKEN_PATTERN.findall(text.lower())


def build_index(pages: Dict[str, str]) -> Dict[str, List[dict]]:
    """
    Build an inverted index using sorted posting lists.

    New structure:
    {
        "word": [
            {"url": str, "freq": int, "positions": [int, ...]},
            ...
        ],
        ...
    }

    Posting lists are sorted by URL to support efficient intersection.
    """
    index: Dict[str, Dict[str, dict]] = {}

    # First pass: build temporary dict-of-dicts (easy for counting)
    for url, text in pages.items():
        words = tokenize(text)

        for pos, word in enumerate(words):
            if word not in index:
                index[word] = {}

            if url not in index[word]:
                index[word][url] = {"freq": 0, "positions": []}

            index[word][url]["freq"] += 1
            index[word][url]["positions"].append(pos)

    # Second pass: convert each word's postings into a sorted list
    final_index: Dict[str, List[dict]] = {}

    for word, posting_dict in index.items():
        postings_list = [
            {"url": url, "freq": data["freq"], "positions": data["positions"]}
            for url, data in posting_dict.items()
        ]

        # Sort postings by URL for deterministic ordering + efficient intersection
        postings_list.sort(key=lambda p: p["url"])

        final_index[word] = postings_list

    return final_index


def save_index(index: Dict[str, Any], path: str) -> None:
    """Save the inverted index to a JSON file."""
    os.makedirs(os.path.dirname(path), exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(index, f, indent=2)


def load_index(path: str) -> Dict[str, Any]:
    """Load an inverted index from a JSON file."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"Index file not found at {path}")

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
