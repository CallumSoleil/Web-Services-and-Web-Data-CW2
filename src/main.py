import sys
import json

from crawler import crawl
from indexer import build_index, save_index, load_index
from search import print_word, find_terms


START_URL = "https://quotes.toscrape.com/"
INDEX_FILE = "index.json"


def cmd_build(args):
    if len(args) != 1:
        print("Usage: build <max_pages>")
        return None

    max_pages = int(args[0])

    print(f"Crawling from fixed URL: {START_URL} (max {max_pages} pages)")
    pages = crawl(START_URL, max_pages)

    print(f"Indexed {len(pages)} pages. Building index...")
    index = build_index(pages)

    save_index(index, INDEX_FILE)
    print(f"Index saved to {INDEX_FILE}")

    return index


def cmd_load():
    try:
        print(f"Loading index from {INDEX_FILE}...")
        return load_index(INDEX_FILE)
    except FileNotFoundError:
        print("Error: index.json not found. Run 'build <max_pages>' first.")
        return None


def cmd_print(index, args):
    if index is None:
        print("No index loaded. Use 'load' or 'build' first.")
        return

    if len(args) != 1:
        print("Usage: print <word>")
        return

    word = args[0]
    entry = print_word(index, word)

    if entry is None:
        print(f"'{word}' not found in index")
    else:
        print(json.dumps(entry, indent=2))


def cmd_find(index, args):
    if index is None:
        print("No index loaded. Use 'load' or 'build' first.")
        return

    if len(args) == 0:
        print("Usage: find <term1> <term2> ...")
        return

    results = find_terms(index, args)

    if not results:
        print("No documents contain all terms")
    else:
        print("Documents containing all terms:")
        for url in results:
            print(" -", url)


def main():
    print("Simple Search Engine Shell")
    print("Type 'help' for commands. Type 'exit' to quit.\n")

    index = None

    while True:
        try:
            line = input("shell> ").strip()
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
            index = cmd_build(args)

        elif command == "load":
            index = cmd_load()

        elif command == "print":
            cmd_print(index, args)

        elif command == "find":
            cmd_find(index, args)

        else:
            print(f"Unknown command: {command}")


if __name__ == "__main__":
    main()