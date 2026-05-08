import json
from typing import Dict, List, Optional

from crawler import crawl
from indexer import build_index, save_index, load_index
from search import print_word, find_terms


START_URL = "https://quotes.toscrape.com/"
INDEX_FILE = "data/index.json"


def cmd_build(args: List[str]) -> None:
    if len(args) != 1:
        print(
            "[ERROR] Invalid command usage.\n"
            "  Usage: build <max_pages>"
        )
        return

    max_pages = int(args[0])

    print(f"Crawling from fixed URL: {START_URL} (max {max_pages} pages)")
    pages = crawl(START_URL, max_pages)

    if not pages:
        print(
            "[ERROR] No pages were crawled.\n"
            "  - The website may be offline or unreachable.\n"
            "  - Index was NOT created."
        )
        return

    print(f"Indexed {len(pages)} pages. Building index...")
    index = build_index(pages)

    save_index(index, INDEX_FILE)
    print(f"Index saved to {INDEX_FILE}")
    print("Run 'load' to load the index into memory.")


def cmd_load() -> Optional[Dict[str, Dict[str, dict]]]:
    try:
        print(f"Loading index from {INDEX_FILE}...")
        return load_index(INDEX_FILE)
    except FileNotFoundError:
        print(
            "[ERROR] Index file not found.\n"
            f"  - Path: {INDEX_FILE}\n"
            "  - Run 'build <max_pages>' before loading the index."
        )
        return None


def cmd_print(index: Optional[Dict[str, Dict[str, dict]]], args: List[str]) -> None:
    if index is None:
        print(
            "[ERROR] No index loaded.\n"
            "  Use 'load' before running this command."
        )
        return

    if len(args) != 1:
        print(
            "[ERROR] Invalid command usage.\n"
            "  Usage: print <word>"
        )
        return

    word = args[0]
    entry = print_word(index, word)

    if entry is None:
        print(
            "[ERROR] Word not found in index.\n"
            f"  - Word: {word}"
        )
    else:
        print(json.dumps(entry, indent=2))


def cmd_find(index: Optional[Dict[str, Dict[str, dict]]], args: List[str]) -> None:
    if index is None:
        print(
            "[ERROR] No index loaded.\n"
            "  Use 'load' before running this command."
        )
        return

    if len(args) == 0:
        print(
            "[ERROR] Invalid command usage.\n"
            "  Usage: find <term1> <term2> ..."
        )
        return

    results = find_terms(index, args)

    if not results:
        print(
            "[ERROR] No documents contain all terms.\n"
            f"  - Terms: {', '.join(args)}"
        )
    else:
        print("Documents containing all terms:")
        for url in results:
            print(f"  - {url}")


def main() -> None:
    print("Simple Search Engine Shell")
    print("Type 'help' for commands. Type 'exit' to quit.\n")

    index: Optional[Dict[str, Dict[str, dict]]] = None

    while True:
        try:
            line = input("\nsearch> ").strip()
        except EOFError:
            break

        if not line:
            continue

        parts = line.split()
        command = parts[0]
        args = parts[1:]

        if command == "exit":
            print("Goodbye.")
            break

        elif command == "help":
            print("Commands:")
            print("  build <max_pages>")
            print("  load")
            print("  print <word>")
            print("  find <term1> <term2> ...")
            print("  exit")
            continue

        elif command == "build":
            cmd_build(args)

        elif command == "load":
            index = cmd_load()

        elif command == "print":
            cmd_print(index, args)

        elif command == "find":
            cmd_find(index, args)

        else:
            print(
                "[ERROR] Unknown command.\n"
                f"  - Received: {command}\n"
                "  - Type 'help' for a list of commands."
            )


if __name__ == "__main__":
    main()
