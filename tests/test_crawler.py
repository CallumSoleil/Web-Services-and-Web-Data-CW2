import pytest
import sys
import os

# Ensure Python can import from src/
sys.path.append(os.path.abspath("src"))

from crawler import fetch_page, extract_links, extract_text, crawl




TEST_URL = "https://quotes.toscrape.com/"


def test_fetch_page_success():
    html = fetch_page(TEST_URL)
    assert html is not None
    assert "<title>Quotes to Scrape</title>" in html


def test_fetch_page_failure():
    html = fetch_page("https://nonexistent.invalid.domain")
    assert html is None

from urllib.parse import urljoin
def test_extract_links():
    html = """
    <html>
        <body>
            <a href="/page1">Page 1</a>
            <a href="https://quotes.toscrape.com/page2">Page 2</a>
            <a href="https://other.com/page3">External</a>
        </body>
    </html>
    """
    links = extract_links(html, TEST_URL)

    expected_page1 = urljoin(TEST_URL, "/page1")
    expected_page2 = "https://quotes.toscrape.com/page2"

    assert expected_page1 in links
    assert expected_page2 in links
    assert all("other.com" not in link for link in links)


def test_extract_text():
    html = "<html><body><h1>Hello</h1><p>World</p></body></html>"
    text = extract_text(html)
    assert "Hello" in text
    assert "World" in text


def test_crawl_unreachable_start_url():
    pages = crawl("https://nonexistent.invalid.domain", max_pages=1)
    assert pages == {}  # Should stop immediately


def test_crawl_collects_pages():
    pages = crawl(TEST_URL, max_pages=1)
    assert TEST_URL in pages
    assert isinstance(pages[TEST_URL], str)
    assert len(pages) == 1
