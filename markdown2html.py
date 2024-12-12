#!/usr/bin/python3
"""
Write a script markdown2html.py that takes two arguments:
First argument is the name of the Markdown file
Second argument is the output file name
"""

import re
import hashlib
import sys
import os

if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.stderr.write("Usage: ./markdown2html.py README.md README.html\n")
        sys.exit(1)
    if not os.path.exists(sys.argv[1]):
        sys.stderr.write(f"Missing {sys.argv[1]}\n")
        sys.exit(1)

    with open(sys.argv[1], 'r') as r, open(sys.argv[2], 'w') as w:
        change_status = False
        ordered_status = False
        paragraph = False

        for line in r:
            line = line.replace('**', '<b>', 1).replace('**', '</b>', 1)
            line = line.replace('__', '<em>', 1).replace('__', '</em>', 1)

            md5_matches = re.findall(r'\[\[.+?\]\]', line)
            if md5_matches:
                md5_content = re.findall(r'\[\[(.+?)\]\]', line)[0]
                line = line.replace(md5_matches[0], hashlib.md5(md5_content.encode()).hexdigest())

            delete_c_matches = re.findall(r'\(\(.+?\)\)', line)
            if delete_c_matches:
                delete_c_content = re.findall(r'\(\((.+?)\)\)', line)[0]
                cleaned_content = ''.join(c for c in delete_c_content if c not in 'Cc')
                line = line.replace(delete_c_matches[0], cleaned_content)

            length = len(line)
            headings = line.lstrip('#')
            heading_count = length - len(headings)
            unordered = line.lstrip('-')
            unordered_count = length - len(unordered)
            ordered = line.lstrip('*')
            ordered_count = length - len(ordered)

            if 1 <= heading_count <= 6:
                line = f'<h{heading_count}>{headings.strip()}</h{heading_count}>\n'

            if unordered_count:
                if not change_status:
                    w.write('<ul>\n')
                    change_status = True
                line = f'<li>{unordered.strip()}</li>\n'
            if change_status and not unordered_count:
                w.write('</ul>\n')
                change_status = False

            if ordered_count:
                if not ordered_status:
                    w.write('<ol>\n')
                    ordered_status = True
                line = f'<li>{ordered.strip()}</li>\n'
            if ordered_status and not ordered_count:
                w.write('</ol>\n')
                ordered_status = False

            if not (heading_count or change_status or ordered_status):
                if not paragraph and length > 1:
                    w.write('<p>\n')
                    paragraph = True
                elif length > 1:
                    w.write('<br/>\n')
                elif paragraph:
                    w.write('</p>\n')
                    paragraph = False

            if length > 1:
                w.write(line)

        if ordered_status:
            w.write('</ol>\n')
        if paragraph:
            w.write('</p>\n')

    sys.exit(0)
