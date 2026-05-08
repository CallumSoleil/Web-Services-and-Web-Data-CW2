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
        return

    max_pages = int(args[0])

    print(f"Crawling from fixed URL: {START_URL} (max {max_pages} pages)")
    pages = crawl(START_URL, max_pages)

    print(f"Indexed {len(pages)} pages. Building index...")
    index = build_index(pages)

    save_index(index, INDEX_FILE)
    print(f"Index saved to {INDEX_FILE}")


def cmd_print(index, args):
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
    if len(sys.argv) < 2:
        print("Commands: build, print, find")
        return

    command = sys.argv[1]
    args = sys.argv[2:]

    # BUILD
    if command == "build":
        cmd_build(args)
        return


    try:
        index = load_index(INDEX_FILE)
    except FileNotFoundError:
        print("Error: index.json not found. Run 'build <max_pages>' first.")
        return

    if command == "print":
        cmd_print(index, args)
    elif command == "find":
        cmd_find(index, args)
    else:
        print("Unknown command:", command)


if __name__ == "__main__":
    main()