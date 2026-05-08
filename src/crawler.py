import time
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

POLITENESS_SECONDS = 6


def fetch_page(url: str) -> str | None:
    """
    Fetch a single page and return its HTML as a string.
    Returns None if the request fails.
    Respects a politeness delay after each request.
    """
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()

        # Politeness window
        time.sleep(POLITENESS_SECONDS)

        return response.text

    except requests.exceptions.Timeout:
        print(
            "[ERROR] Timeout while fetching page.\n"
            f"  - URL: {url}\n"
            "  - Reason: Request timed out."
        )
        return None

    except requests.exceptions.ConnectionError:
        print(
            "[ERROR] Connection error while fetching page.\n"
            f"  - URL: {url}\n"
            "  - Reason: Unable to establish a connection."
        )
        return None

    except requests.exceptions.HTTPError as e:
        print(
            "[ERROR] HTTP error while fetching page.\n"
            f"  - URL: {url}\n"
            f"  - Reason: {e}"
        )
        return None

    except requests.exceptions.RequestException as e:
        print(
            "[ERROR] Request failed while fetching page.\n"
            f"  - URL: {url}\n"
            f"  - Reason: {e}"
        )
        return None

    except Exception as e:
        print(
            "[ERROR] Unexpected error while fetching page.\n"
            f"  - URL: {url}\n"
            f"  - Reason: {e}"
        )
        return None


def extract_links(html: str, base_url: str) -> set[str]:
    """
    Extract all in-domain absolute links from the HTML.
    """
    soup = BeautifulSoup(html, "html.parser")
    links: set[str] = set()

    base_domain = urlparse(base_url).netloc

    for tag in soup.find_all("a", href=True):
        absolute = urljoin(base_url, tag["href"])
        if urlparse(absolute).netloc == base_domain:
            links.add(absolute)

    return links


def extract_text(html: str) -> str:
    """
    Extract visible text from HTML.
    """
    soup = BeautifulSoup(html, "html.parser")
    return soup.get_text(separator=" ", strip=True)


def crawl(start_url: str, max_pages: int = 20) -> dict[str, str]:
    """
    Crawl pages starting from start_url.
    Returns a mapping: url -> extracted text.
    """
    to_visit: list[str] = [start_url]
    visited: set[str] = set()
    pages: dict[str, str] = {}

    while to_visit and len(visited) < max_pages:
        url = to_visit.pop(0)
        if url in visited:
            continue

        html = fetch_page(url)
        if html is None:
            if url == start_url and not visited:
                print(
                    "[ERROR] Failed to fetch the starting URL.\n"
                    f"  - URL: {start_url}\n"
                    "  - The website may be offline or unreachable.\n"
                    "  - Crawling aborted."
                )
                return {}

            print(
                "[ERROR] Skipping unreachable page.\n"
                f"  - URL: {url}"
            )
            continue

        visited.add(url)
        pages[url] = extract_text(html)

        for link in extract_links(html, start_url):
            if link not in visited and link not in to_visit:
                to_visit.append(link)

    return pages
