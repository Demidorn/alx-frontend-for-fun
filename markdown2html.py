#!/usr/bin/python3
import sys
from os.path import exists

"""
A markdown to HTML file converter

Args:
    Arg 1: Markdown file
    Arg 2: Output file name (HTML)
"""

markdownHeader = {
    '#': '<h1> </h1>', '##': '<h2> </h2>', '###': '<h3> </h3>',
    '####': '<h4> </h4>', '#####': '<h5> </h5>', '######': '<h6> </h6>'
}

markdownList = {'-': '<li> </li>', '*': '<li> </li>'}

if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.stderr.write("Usage: ./markdown2html.py README.md README.html\n")
        exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    if not input_file.endswith(".md"):
        sys.stderr.write("First argument must be a markdown file\n")
        exit(1)

    if not exists(input_file):
        sys.stderr.write(f"Missing {input_file}\n")
        exit(1)

    ulCount = 0
    with open(input_file, 'r') as markdown, open(output_file, 'w') as htmlFile:
        for line in markdown:
            line = line.rstrip()
            if line.startswith('#'):
                hash = line.split(' ')[0]
                htmlFile.write('{}{}{}\n'.format(
                    markdownHeader[hash].split(' ')[0], line[len(hash)+1:], markdownHeader[hash].split(' ')[1]))
            elif line.startswith('-'):
                if ulCount == 0:
                    htmlFile.write('<ul>\n')
                htmlFile.write('\t{}{}{}\n'.format(
                    markdownList['-'].split(' ')[0], line[2:], markdownList['-'].split(' ')[1]))
                ulCount += 1
            else:
                if ulCount > 0:
                    htmlFile.write('</ul>\n')
                    ulCount = 0
                htmlFile.write(line + '\n')

        if ulCount > 0:
            htmlFile.write('</ul>\n')

    exit(0)
