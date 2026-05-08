from typing import Dict, List, Set, Optional


def print_word(index: Dict[str, Dict[str, dict]], word: str) -> Optional[Dict[str, dict]]:
    """
    Return the index entry for a single word (case-insensitive).
    If the word does not exist, return None.
    """
    word = word.lower()
    return index.get(word)


def find_terms(index: Dict[str, Dict[str, dict]], terms: List[str]) -> List[str]:
    """
    Return a sorted list of URLs that contain ALL of the given terms (case-insensitive).
    If any term is missing from the index, return an empty list.
    """
    # Normalise terms
    terms = [t.lower() for t in terms]

    # If any term is missing, no results
    if any(term not in index for term in terms):
        return []

    # Start with URLs for the first term
    result: Set[str] = set(index[terms[0]].keys())

    # Intersect with URLs for remaining terms
    for term in terms[1:]:
        result &= set(index[term].keys())

    # Return sorted list for deterministic output
    return sorted(result)
