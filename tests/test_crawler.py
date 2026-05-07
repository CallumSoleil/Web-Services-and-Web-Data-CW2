import sys
import os

# Make sure Python can find the src/ folder
sys.path.append(os.path.abspath("src"))

from crawler import extract_text, extract_links


def test_extract_text_basic_html():
    html = "<html><body><h1>Title</h1><p>Hello world</p></body></html>"
    text = extract_text(html)
    assert "Title" in text
    assert "Hello world" in text


def test_extract_links_same_domain():
    html = """
    <html><body>
        <a href="/page1">Page 1</a>
        <a href="https://example.com/page2">Page 2</a>
        <a href="https://other.com/page3">Other</a>
    </body></html>
    """
    links = extract_links(html, "https://example.com")

    assert "https://example.com/page1" in links
    assert "https://example.com/page2" in links
    assert all("other.com" not in link for link in links)
