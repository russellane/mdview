"""Command line interface."""

import sys
from pathlib import Path

import webview
from libcli import BaseCLI

from mdview.renderer import GITHUB_CSS_DARK, GITHUB_CSS_LIGHT, create_html_document

__all__ = ["MdviewCLI"]


class MdviewCLI(BaseCLI):
    """Command line interface."""

    config = {
        "dist-name": "rlane-mdview",
    }

    def init_parser(self) -> None:
        """Initialize argument parser."""

        self.parser = self.ArgumentParser(
            prog=__package__,
            description="Display Markdown files with GitHub-style formatting",
        )

    def add_arguments(self) -> None:
        """Add arguments to parser."""

        self.parser.add_argument(
            "file",
            nargs="?",
            default="-",
            help="Path to the Markdown file to display (default: stdin)",
        )
        theme_group = self.parser.add_mutually_exclusive_group()
        theme_group.add_argument(
            "--light",
            action="store_true",
            help="Use light mode theme",
        )
        theme_group.add_argument(
            "--dark",
            action="store_true",
            help="Use dark mode theme (default)",
        )

    def main(self) -> None:
        """Command line interface entry point (method)."""

        if self.options.file == "-":
            md_content = sys.stdin.read()
            title = "stdin"
        else:
            md_path = Path(self.options.file)
            if not md_path.exists():
                print(f"Error: File not found: {md_path}", file=sys.stderr)
                sys.exit(1)
            md_content = md_path.read_text(encoding="utf-8")
            title = md_path.name

        css = GITHUB_CSS_LIGHT if self.options.light else GITHUB_CSS_DARK
        html_document = create_html_document(md_content, title=title, css=css)

        webview.create_window(
            title=f"Markdown Viewer - {title}",
            html=html_document,
            width=1000,
            height=800,
        )
        webview.start()


def main(args: list[str] | None = None) -> None:
    """Command line interface entry point (function)."""

    MdviewCLI(args).main()
