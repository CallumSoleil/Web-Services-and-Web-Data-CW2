from typing import Dict, List, Set


def print_word(index: Dict[str, dict], word: str) -> Dict[str, dict] | None:
    """
    Return the index entry for a single word (case-insensitive).
    If the word does not exist, return None.
    """
    word = word.lower()
    return index.get(word)


def find_terms(index: Dict[str, dict], terms: List[str]) -> Set[str]:
    """
    Perform an AND search across multiple terms.
    Returns a set of URLs that contain *all* the given terms.
    """
    if not terms:
        return set()

    # Normalize terms
    terms = [t.lower() for t in terms]

    # If any term is missing, no results
    for term in terms:
        if term not in index:
            return set()

    # Start with URLs for the first term
    result_urls = set(index[terms[0]].keys())

    # Intersect with URLs for the remaining terms
    for term in terms[1:]:
        result_urls &= set(index[term].keys())

        # Early exit if empty
        if not result_urls:
            return set()

    return result_urls
