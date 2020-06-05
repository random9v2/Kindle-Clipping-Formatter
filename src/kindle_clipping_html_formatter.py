import re
import os
from datetime import datetime

from kindle_clipping_html_templates import PAGE, HIGHLIGHT

CLIPPINGS_FILENAME = "My Clippings.txt"
HTML_FILE_EXTENSION = ".html"
OUTPUT_DIRECTORY_NAME = 'output'
HIGHLIGHT_SEPARATOR = "=========="

class Highlight:

    def __init__(self, raw_highlight_str):
        self.title, self.author, self.main_loc, self.date, self.content = \
            Highlight.parse_highlight(raw_highlight_str)

    @staticmethod
    def parse_highlight(raw_highlight_str):
        # split the highlight up by line
        split_str = raw_highlight_str.split('\n')
        

    def __str__(self):
        return f'Highlight - Title: {self.title} \t Author: {self.author} \t' \
            + f'Highlight Main Loc: {self.main_loc} \t' \
            + f'Highlight Date: {self.date} \t' \
            + f'Highlight Content: {self.content}.'

