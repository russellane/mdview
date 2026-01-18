#!/usr/bin/env python3
"""

Markdown viewer with GitHub-style rendering.

"""

import argparse
import sys
from pathlib import Path

import markdown
import webview

GITHUB_CSS = """
body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans", Helvetica, Arial, sans-serif;
    font-size: 16px;
    line-height: 1.5;
    word-wrap: break-word;
    max-width: 980px;
    margin: 0 auto;
    padding: 45px;
    color: #1f2328;
    background-color: #ffffff;
}

a {
    color: #0969da;
    text-decoration: none;
}

a:hover {
    text-decoration: underline;
}

h1, h2, h3, h4, h5, h6 {
    margin-top: 24px;
    margin-bottom: 16px;
    font-weight: 600;
    line-height: 1.25;
}

h1 {
    font-size: 2em;
    padding-bottom: 0.3em;
    border-bottom: 1px solid #d1d9e0;
}

h2 {
    font-size: 1.5em;
    padding-bottom: 0.3em;
    border-bottom: 1px solid #d1d9e0;
}

h3 { font-size: 1.25em; }
h4 { font-size: 1em; }
h5 { font-size: 0.875em; }
h6 { font-size: 0.85em; color: #656d76; }

p, blockquote, ul, ol, dl, table, pre {
    margin-top: 0;
    margin-bottom: 16px;
}

blockquote {
    padding: 0 1em;
    color: #656d76;
    border-left: 0.25em solid #d1d9e0;
}

ul, ol {
    padding-left: 2em;
}

li + li {
    margin-top: 0.25em;
}

code {
    padding: 0.2em 0.4em;
    margin: 0;
    font-size: 85%;
    white-space: break-spaces;
    background-color: #eff1f3;
    border-radius: 6px;
    font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, "Liberation Mono", monospace;
}

pre {
    padding: 16px;
    overflow: auto;
    font-size: 85%;
    line-height: 1.45;
    color: #1f2328;
    background-color: #f6f8fa;
    border-radius: 6px;
}

pre code {
    padding: 0;
    margin: 0;
    font-size: 100%;
    background-color: transparent;
    border: 0;
    display: inline;
    line-height: inherit;
    word-wrap: normal;
    white-space: pre;
}

table {
    border-spacing: 0;
    border-collapse: collapse;
    width: max-content;
    max-width: 100%;
    overflow: auto;
}

table th, table td {
    padding: 6px 13px;
    border: 1px solid #d1d9e0;
}

table th {
    font-weight: 600;
    background-color: #f6f8fa;
}

table tr {
    background-color: #ffffff;
    border-top: 1px solid #d1d9e0;
}

table tr:nth-child(2n) {
    background-color: #f6f8fa;
}

img {
    max-width: 100%;
    box-sizing: border-box;
}

hr {
    height: 0.25em;
    padding: 0;
    margin: 24px 0;
    background-color: #d1d9e0;
    border: 0;
}

.task-list-item {
    list-style-type: none;
}

.task-list-item input {
    margin: 0 0.2em 0.25em -1.4em;
    vertical-align: middle;
}

/* Syntax highlighting (Pygments friendly) */
.codehilite { background: #f6f8fa; padding: 16px; border-radius: 6px; overflow: auto; }
.codehilite .hll { background-color: #ffffcc }
.codehilite .c { color: #6a737d } /* Comment */
.codehilite .k { color: #d73a49 } /* Keyword */
.codehilite .o { color: #d73a49 } /* Operator */
.codehilite .cm { color: #6a737d } /* Comment.Multiline */
.codehilite .cp { color: #d73a49 } /* Comment.Preproc */
.codehilite .c1 { color: #6a737d } /* Comment.Single */
.codehilite .cs { color: #6a737d } /* Comment.Special */
.codehilite .gd { color: #b31d28; background-color: #ffeef0 } /* Generic.Deleted */
.codehilite .gi { color: #22863a; background-color: #f0fff4 } /* Generic.Inserted */
.codehilite .gs { font-weight: bold } /* Generic.Strong */
.codehilite .gu { color: #6f42c1; font-weight: bold } /* Generic.Subheading */
.codehilite .kc { color: #005cc5 } /* Keyword.Constant */
.codehilite .kd { color: #d73a49 } /* Keyword.Declaration */
.codehilite .kn { color: #d73a49 } /* Keyword.Namespace */
.codehilite .kp { color: #d73a49 } /* Keyword.Pseudo */
.codehilite .kr { color: #d73a49 } /* Keyword.Reserved */
.codehilite .kt { color: #d73a49 } /* Keyword.Type */
.codehilite .m { color: #005cc5 } /* Literal.Number */
.codehilite .s { color: #032f62 } /* Literal.String */
.codehilite .na { color: #005cc5 } /* Name.Attribute */
.codehilite .nb { color: #005cc5 } /* Name.Builtin */
.codehilite .nc { color: #6f42c1 } /* Name.Class */
.codehilite .no { color: #005cc5 } /* Name.Constant */
.codehilite .nd { color: #6f42c1 } /* Name.Decorator */
.codehilite .ni { color: #24292e } /* Name.Entity */
.codehilite .nf { color: #6f42c1 } /* Name.Function */
.codehilite .nl { color: #005cc5 } /* Name.Label */
.codehilite .nn { color: #6f42c1 } /* Name.Namespace */
.codehilite .nt { color: #22863a } /* Name.Tag */
.codehilite .nv { color: #e36209 } /* Name.Variable */
.codehilite .ow { color: #d73a49 } /* Operator.Word */
.codehilite .w { color: #bbbbbb } /* Text.Whitespace */
.codehilite .mf { color: #005cc5 } /* Literal.Number.Float */
.codehilite .mh { color: #005cc5 } /* Literal.Number.Hex */
.codehilite .mi { color: #005cc5 } /* Literal.Number.Integer */
.codehilite .mo { color: #005cc5 } /* Literal.Number.Oct */
.codehilite .sb { color: #032f62 } /* Literal.String.Backtick */
.codehilite .sc { color: #032f62 } /* Literal.String.Char */
.codehilite .sd { color: #032f62 } /* Literal.String.Doc */
.codehilite .s2 { color: #032f62 } /* Literal.String.Double */
.codehilite .se { color: #032f62 } /* Literal.String.Escape */
.codehilite .sh { color: #032f62 } /* Literal.String.Heredoc */
.codehilite .si { color: #005cc5 } /* Literal.String.Interpol */
.codehilite .sx { color: #032f62 } /* Literal.String.Other */
.codehilite .sr { color: #032f62 } /* Literal.String.Regex */
.codehilite .s1 { color: #032f62 } /* Literal.String.Single */
.codehilite .ss { color: #005cc5 } /* Literal.String.Symbol */
.codehilite .bp { color: #005cc5 } /* Name.Builtin.Pseudo */
.codehilite .vc { color: #e36209 } /* Name.Variable.Class */
.codehilite .vg { color: #e36209 } /* Name.Variable.Global */
.codehilite .vi { color: #e36209 } /* Name.Variable.Instance */
.codehilite .il { color: #005cc5 } /* Literal.Number.Integer.Long */
"""

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>{css}</style>
</head>
<body>
{content}
</body>
</html>
"""


def render_markdown(md_content: str) -> str:
    """

    Convert Markdown content to HTML using GitHub-flavored extensions.

    """
    md = markdown.Markdown(
        extensions=[
            "fenced_code",
            "codehilite",
            "tables",
            "toc",
            "nl2br",
            "sane_lists",
            "smarty",
            "md_in_html",
        ],
        extension_configs={
            "codehilite": {
                "css_class": "codehilite",
                "guess_lang": True,
            },
        },
    )
    return md.convert(md_content)


def create_html_document(md_content: str, title: str) -> str:
    """

    Create a complete HTML document with GitHub styling.

    """
    html_content = render_markdown(md_content)
    return HTML_TEMPLATE.format(title=title, css=GITHUB_CSS, content=html_content)


def main() -> int:
    """

    Main entry point for the Markdown viewer.

    """
    parser = argparse.ArgumentParser(
        description="Display Markdown files with GitHub-style formatting"
    )
    parser.add_argument(
        "file",
        type=Path,
        nargs="?",
        help="Path to the Markdown file to display",
    )
    args = parser.parse_args()

    if args.file:
        md_path = args.file
    else:
        # Open file dialog if no file specified
        file_types = ("Markdown Files (*.md;*.markdown)", "All Files (*.*)")
        result = webview.windows.create_file_dialog(
            webview.OPEN_DIALOG, file_types=file_types
        )
        if not result:
            print("No file selected.", file=sys.stderr)
            return 1
        md_path = Path(result[0])

    if not md_path.exists():
        print(f"Error: File not found: {md_path}", file=sys.stderr)
        return 1

    md_content = md_path.read_text(encoding="utf-8")
    html_document = create_html_document(md_content, title=md_path.name)

    window = webview.create_window(
        title=f"Markdown Viewer - {md_path.name}",
        html=html_document,
        width=1000,
        height=800,
    )
    webview.start()

    return 0


if __name__ == "__main__":
    sys.exit(main())
