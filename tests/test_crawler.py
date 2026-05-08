import sys
import os
from unittest.mock import patch, Mock

# Ensure Python can import from src/
sys.path.append(os.path.abspath("src"))

from crawler import fetch_page, extract_links, extract_text, crawl


# -----------------------------
# FETCH PAGE TESTS
# -----------------------------

@patch("crawler.requests.get")
def test_fetch_page_success(mock_get):
    mock_response = Mock()
    mock_response.text = "<html><title>Test</title></html>"
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response

    html = fetch_page("http://example.com")

    assert html is not None
    assert "<title>Test</title>" in html


@patch("crawler.requests.get")
def test_fetch_page_failure(mock_get):
    mock_get.side_effect = Exception("Network error")

    html = fetch_page("http://bad-url.com")

    assert html is None


# -----------------------------
# EXTRACT LINKS TESTS
# -----------------------------

from urllib.parse import urljoin

def test_extract_links():
    html = """
    <html>
        <body>
            <a href="/page1">Page 1</a>
            <a href="https://example.com/page2">Page 2</a>
            <a href="https://other.com/page3">External</a>
        </body>
    </html>
    """

    base = "https://example.com/"
    links = extract_links(html, base)

    expected1 = urljoin(base, "/page1")
    expected2 = "https://example.com/page2"

    assert expected1 in links
    assert expected2 in links
    assert all("other.com" not in link for link in links)


# -----------------------------
# EXTRACT TEXT TESTS
# -----------------------------

def test_extract_text():
    html = "<html><body><h1>Hello</h1><p>World</p></body></html>"
    text = extract_text(html)

    assert "Hello" in text
    assert "World" in text


# -----------------------------
# CRAWL TESTS
# -----------------------------

@patch("crawler.fetch_page")
def test_crawl_unreachable_start_url(mock_fetch):
    mock_fetch.return_value = None

    pages = crawl("http://bad-url.com", max_pages=1)

    assert pages == {}  # Should stop immediately


@patch("crawler.fetch_page")
def test_crawl_collects_pages(mock_fetch):
    mock_fetch.return_value = "<html><body>Hello</body></html>"

    pages = crawl("http://example.com", max_pages=1)

    assert "http://example.com" in pages
    assert isinstance(pages["http://example.com"], str)
    assert len(pages) == 1
