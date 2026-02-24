### mdview - Markdown viewer with GitHub-style rendering

#### Usage
    mdview [--light | --dark] [-h] [-v] [-V] [--print-config] [--print-url]
           [--completion [SHELL]]
           [file]
    
Display Markdown files with GitHub-style formatting

#### Positional Arguments
    file                Path to the Markdown file to display (default: stdin).

#### Options
    --light             Use light mode theme.
    --dark              Use dark mode theme (default).

#### General options
    -h, --help          Show this help message and exit.
    -v, --verbose       `-v` for detailed output and `-vv` for more detailed.
    -V, --version       Print version number and exit.
    --print-config      Print effective config and exit.
    --print-url         Print project url and exit.
    --completion [SHELL]
                        Print completion scripts for `SHELL` and exit
                        (default: `bash`).
