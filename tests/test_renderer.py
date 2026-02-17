"""Tests for mdview renderer."""

from mdview.renderer import render_markdown


def test_render_markdown():
    """Verify basic Markdown rendering."""

    html = render_markdown("# Hello")
    assert "<h1" in html
    assert "Hello" in html
