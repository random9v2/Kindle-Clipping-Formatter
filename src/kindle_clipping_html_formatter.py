import re
import os
from datetime import datetime

from kindle_clipping_html_templates import PAGE, HIGHLIGHT

CLIPPINGS_FILENAME = "My Clippings.txt"
HTML_FILE_EXTENSION = ".html"
OUTPUT_DIRECTORY_NAME = 'output'
HIGHLIGHT_SEPARATOR = "=========="

class Highlight:
    """Represents a Highlight within a Book and its attributes.

    Attributes:
        title (str): the book title
        author (str): the book author
        main_loc (str): the main location of the highlight
        date (str): the date the highlight was made
        content (str): the content of the highlight

    """

    def __init__(self, raw_highlight_str):
        """Initialises a new book.

        Attributes:
            raw_highlight_str (str): the unprocessed highlight data

        """
        self.title, self.author, self.main_loc, self.date, self.content = \
            Highlight.parse_highlight(raw_highlight_str)

    @staticmethod
    def tidy_date(raw_date):
        """Tidies a clipping date into our desired format.

        Attributes:
            raw_date (str): the unprocessed date as a string

        Returns:
            str: our processed date as a string

        """
        # remove unwanted preface
        date_str = raw_date.replace('Added on ', '')
        # define our input datetime string format
        # expected date_str: Tuesday, 4 December 12 22:52:19
        date_str_in_format = '%A, %d %B %Y %H:%M:%S'
        # read in our datetime using our expected format string
        datetime_object = datetime.strptime(date_str, date_str_in_format)
        # define an output datetime string format
        date_str_out_format = '%d/%m/%y %H:%M'
        # return the datetime in our desired format
        return datetime_object.strftime(date_str_out_format)

    @staticmethod
    def parse_highlight(raw_highlight_str):
        """Parses a raw highlight string into a Highlight object.

        Attributes:
            raw_highlight_str (str): the unprocessed highlight as a string

        Returns:
            (str, str, str, str, str): title, author, main location, highlight
            date, highlight content

        """
        # split the highlight up by line
        split_str = raw_highlight_str.split('\n')
        # ensure has enough lines
        if len(split_str) < 5:
            return (None, None, None, None, None)

        # determine if we are not on the first clipping in the file
        if split_str[0] == '':
            # remove the first split as it was a separator originally
            split_str = split_str[1:]

        # get book title and author
        book_details = split_str[0]
        # get last content in round brackets
        book_details_split = re.search(r"\(([^)]*)\)[^(]*$", book_details)
        if book_details_split:
            # get the title and author from the split result
            title = book_details[:book_details_split.start()]
            author = book_details_split.group(1)
        else:
            return (None, None, None, None, None)

        # get highlight details
        highlight_details = split_str[1]
        highlight_details_split = highlight_details.split(" | ")
        if highlight_details_split:
            # get the main location and highlight date from the split result
            main_loc = highlight_details_split[0]
            if len(highlight_details_split) == 2:
                date = highlight_details_split[1]
            else:
                # add the second location attribute
                main_loc = main_loc + ', ' + highlight_details_split[1]
                date = highlight_details_split[2]
        else:
            return (None, None, None, None, None)

        # tidy our date up into our desired format
        date = Highlight.tidy_date(date)

        # get the highlight content
        content = '\n'.join(split_str[3:-1])

        return (title, author, main_loc, date, content)

    def __str__(self):
        """Prints the highlight's data members.

        Returns:
            str: a string containing the highlight's data members

        """
        return f'Highlight - Title: {self.title} \t Author: {self.author} \t' \
            + f'Highlight Main Loc: {self.main_loc} \t' \
            + f'Highlight Date: {self.date} \t' \
            + f'Highlight Content: {self.content}.'

