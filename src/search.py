from typing import Dict, List, Optional, Set, Optional


def print_word(index: Dict[str, List[dict]], word: str) -> Optional[List[dict]]:
    """
    Return the posting list for a word (case-insensitive).
    """
    word = word.lower()
    return index.get(word)



def find_terms(index: Dict[str, List[dict]], terms: List[str]) -> List[str]:
    """
    Return a sorted list of URLs that contain ALL of the given terms.
    Works with posting-list index structure:
        index[word] = [
            {"url": str, "freq": int, "positions": [...]},
            ...
        ]
    """
    # Normalise terms
    terms = [t.lower() for t in terms]

    # If any term missing, no results
    for term in terms:
        if term not in index:
            return []

    # Convert first term's postings into a list of URLs
    result_urls = [p["url"] for p in index[terms[0]]]

    # Intersect with remaining posting lists
    for term in terms[1:]:
        term_urls = [p["url"] for p in index[term]]

        # Both lists are sorted → linear-time intersection
        i = j = 0
        intersection = []

        while i < len(result_urls) and j < len(term_urls):
            if result_urls[i] == term_urls[j]:
                intersection.append(result_urls[i])
                i += 1
                j += 1
            elif result_urls[i] < term_urls[j]:
                i += 1
            else:
                j += 1

        result_urls = intersection

        if not result_urls:
            return []

    return result_urls
