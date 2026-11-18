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
            self._md_path: Path | None = None
            self._md_content = sys.stdin.read()
            title = "stdin"
        else:
            self._md_path = Path(self.options.file)
            if not self._md_path.exists():
                print(f"Error: File not found: {self._md_path}", file=sys.stderr)
                sys.exit(1)
            self._md_content = self._md_path.read_text(encoding="utf-8")
            title = self._md_path.name

        self._title = title
        self._css = GITHUB_CSS_LIGHT if self.options.light else GITHUB_CSS_DARK
        html_document = create_html_document(self._md_content, title=title, css=self._css)

        webview.create_window(
            f"Markdown Viewer - {title}",
            html=html_document,
            width=1000,
            height=800,
            js_api=_Api(self),
        )
        webview.start()

    def reload(self, scroll_y: int = 0) -> str:
        """Re-read the Markdown file (if not stdin) and return the new HTML document."""

        if self._md_path is not None:
            try:
                self._md_content = self._md_path.read_text(encoding="utf-8")
            except OSError as err:
                print(f"Error: {err}", file=sys.stderr)
        return create_html_document(
            self._md_content, title=self._title, css=self._css, scroll_y=scroll_y
        )


class _Api:
    """Methods exposed to javascript as `window.pywebview.api`."""

    def __init__(self, cli: MdviewCLI) -> None:
        # Private attribute; pywebview does not expose (or recurse into) `_` names.
        self._cli = cli

    def reload(self, scroll_y: int = 0) -> str:
        """Return the reloaded document; javascript swaps it in."""

        return self._cli.reload(scroll_y)


def main(args: list[str] | None = None) -> None:
    """Command line interface entry point (function)."""

    MdviewCLI(args).main()
