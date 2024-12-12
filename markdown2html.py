#!/usr/bin/python3

import sys
import os

if __name__ == "__main__":
    # Check if the correct number of arguments is passed
    if len(sys.argv) < 3:
        print("Usage: ./markdown2html.py README.md README.html", file=sys.stderr)
        sys.exit(1)

    # Get the arguments (Markdown file and output file)
    markdown_file = sys.argv[1]
    output_file = sys.argv[2]

    # Check if the Markdown file exists
    if not os.path.exists(markdown_file):
        print(f"Missing {markdown_file}", file=sys.stderr)
        sys.exit(1)

    # If everything is fine, convert Markdown to HTML
    with open(markdown_file, 'r') as md_file:
        md_text = md_file.read()

    # Convert the Markdown text to HTML
    html_output = ""
    lines = md_text.splitlines()
    for line in lines:
        if line.startswith("# "):
            html_output += f"<h1>{line[2:]}</h1>\n"
        elif line.startswith("## "):
            html_output += f"<h2>{line[3:]}</h2>\n"
        elif line.startswith("### "):
            html_output += f"<h3>{line[4:]}</h3>\n"
        elif line.startswith("#### "):
            html_output += f"<h4>{line[5:]}</h4>\n"
        else:
            html_output += f"<p>{line}</p>\n"

    # Write the HTML output to the output file
    with open(output_file, 'w') as html_file:
        html_file.write(html_output)

    sys.exit(0)
