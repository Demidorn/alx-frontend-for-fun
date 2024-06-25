#!/usr/bin/python3
import sys
import hashlib
from os.path import exists

def md5_hash(text):
    return hashlib.md5(text.encode()).hexdigest()

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

    ul_count = 0
    ol_count = 0
    with open(input_file, 'r') as markdown, open(output_file, 'w') as htmlFile:
        for line in markdown:
            line = line.rstrip()
            if line.startswith('#'):
                hash_count = line.count('#')
                line_content = line[hash_count:].strip()
                htmlFile.write(f'<h{hash_count}>{line_content}</h{hash_count}>\n')
            elif line.startswith('-'):
                if ul_count == 0:
                    htmlFile.write('<ul>\n')
                htmlFile.write(f'  <li>{line[2:].strip()}</li>\n')
                ul_count += 1
            elif line.startswith('*'):
                if ol_count == 0:
                    htmlFile.write('<ol>\n')
                htmlFile.write(f'  <li>{line[2:].strip()}</li>\n')
                ol_count += 1
            elif line == '':
                if ul_count > 0:
                    htmlFile.write('</ul>\n')
                    ul_count = 0
                if ol_count > 0:
                    htmlFile.write('</ol>\n')
                    ol_count = 0
            else:
                if ul_count > 0:
                    htmlFile.write('</ul>\n')
                    ul_count = 0
                if ol_count > 0:
                    htmlFile.write('</ol>\n')
                    ol_count = 0

                # Handle paragraph text
                paragraphs = line.split('\n\n')
                for paragraph in paragraphs:
                    paragraph = paragraph.strip()
                    if paragraph:
                        paragraph = paragraph.replace("**", "<b>").replace("__", "<em>").replace("**", "</b>").replace("__", "</em>")
                        paragraph = paragraph.replace("<br>", "<br/>")
                        
                        while '[[' in paragraph and ']]' in paragraph:
                            start = paragraph.index('[[')
                            end = paragraph.index(']]') + 2
                            content = paragraph[start+2:end-2]
                            md5_content = md5_hash(content)
                            paragraph = paragraph.replace(paragraph[start:end], md5_content)

                        while '((' in paragraph and '))' in paragraph:
                            start = paragraph.index('((')
                            end = paragraph.index('))') + 2
                            content = paragraph[start+2:end-2]
                            modified_content = content.replace('c', '').replace('C', '')
                            paragraph = paragraph.replace(paragraph[start:end], modified_content)

                        htmlFile.write(f'<p>\n    {paragraph}\n</p>\n')

        # Ensure any remaining lists are closed
        if ul_count > 0:
            htmlFile.write('</ul>\n')
        if ol_count > 0:
            htmlFile.write('</ol>\n')

    exit(0)
