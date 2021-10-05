"""Kindle Clipping TXT file to HTML document formatter.

This module provides a set of functions to convert Kindle Clippings from their
native TXT file format to a styled HTML document.

Example:
    $ python3 kindle_clipping_html_formatter.py

"""

import re
import os
from datetime import datetime
import argparse

from kindle_clipping_html_templates import PAGE, HIGHLIGHT

HIGHLIGHT_SEPARATOR = "=========="

########################################################################################################################
class Book:
    """Represents a Book and its attributes.

    Attributes:
        book_titles (set): stores a set of all known book titles
        title (str): the book title
        author (str): the book author
        highlights (list of str): the books highlights

    """
    book_titles = set() # maintain a set of book titles

    ####################################################################################################################
    def __init__(self, title, author):
        """Initialises a new book.

        Attributes:
            title (str): the new books title
            author (str): the new books author

        """
        self.title = Book.tidy_title(title)
        Book.book_titles.add(self.title) # add book to list of known books
        self.author = author
        self.highlights = []

    ####################################################################################################################
    def add_highlight(self, highlight):
        """Adds a highlight to the book.

        Attributes:
            highlight (highlight): the new highlight for the book

        """
        if highlight:
            self.highlights.append(highlight)

    ####################################################################################################################
    def highlights_to_html(self):
        """Creates the HTML for all highlights

        Returns:
            str: HTML content for all highlights

        """
        # iterate over all highlights creating HTML for each
        for highlight in self.highlights:
            yield HIGHLIGHT.safe_substitute({
                'text': highlight.content,
                'location': highlight.main_loc,
                'datetime': highlight.date
            })

    ####################################################################################################################
    def write_book_to_html(self):
        """Writes all book attributes to a HTML file."""
        # get filename from book title and output file extension
        filename = "{}.html".format(self.title)

        # get all the highlights as HTML
        highlights_html = self.highlights_to_html()

        # get current datetime in our format
        datetime_now = datetime.now().strftime('%d/%m/%y %H:%M:%S')

        # write the book to HTML
        with open(filename, 'w') as book_file:
            book_file.write(PAGE.safe_substitute({
                'book_title': self.title,
                'book_author': self.author,
                'file_datetime': datetime_now,
                'book_highlights': '\n'.join(list(highlights_html))
            }))
            # give status prompt to user
            print(f"HTML file produced for: {self.title}")

    ####################################################################################################################
    @staticmethod
    def tidy_title(raw_title):
        """Removed unwanted characters from the highlight title.

        Attributes:
            raw_title (str): the unprocessed title string

        Returns:
            str: our processed title string

        """
        # remove chars tht are not alphanumeric or ; , _ - . ( ) : ' "
        title = re.sub(r"[^a-zA-Z\d\s;,_\-\.():'\"]+", "", str(raw_title))
        # Trim off anything that isn't a word at the start & end
        title = re.sub(r"^\W+|\W+$", "", title)
        return title

    ####################################################################################################################
    def __str__(self):
        """Prints the book's data members.

        Returns:
            str: a string containing the book's data members

        """
        return f'Book - Title: {self.title} \t Author: {self.author} \t' \
            f'Highlights: {self.highlights}.'

########################################################################################################################
class Highlight:
    """Represents a Highlight within a Book and its attributes.

    Attributes:
        title (str): the book title
        author (str): the book author
        main_loc (str): the main location of the highlight
        date (str): the date the highlight was made
        content (str): the content of the highlight

    """

    ####################################################################################################################
    def __init__(self, raw_highlight_str):
        """Initialises a new book.

        Attributes:
            raw_highlight_str (str): the unprocessed highlight data

        """
        self.title, self.author, self.main_loc, self.date, self.content = \
            Highlight.parse_highlight(raw_highlight_str)

    ####################################################################################################################
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

    ####################################################################################################################
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
            title = Book.tidy_title(book_details[:book_details_split.start()])
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

    ####################################################################################################################
    def __str__(self):
        """Prints the highlight's data members.

        Returns:
            str: a string containing the highlight's data members

        """
        return f'Highlight - Title: {self.title} \t Author: {self.author} \t' \
            + f'Highlight Main Loc: {self.main_loc} \t' \
            + f'Highlight Date: {self.date} \t' \
            + f'Highlight Content: {self.content}.'

########################################################################################################################
def process(clippings_file_path, output_dir_path):
    processed_books = []
    library = []

    # move to the cwd
    cwd = os.getcwd()
    os.chdir(cwd)
    # create output folder if not exists
    if not os.path.exists(output_dir_path):
        os.mkdir(output_dir_path)

    # reset knowledge of book titles
    Book.book_titles = set()

    # read in the clippings
    with open(clippings_file_path, "r") as clippings_file:
        file_contents = clippings_file.read()

    # move to the output directory
    os.chdir(output_dir_path)

    # split all the highlights up into a list
    highlights = file_contents.split(HIGHLIGHT_SEPARATOR)

    # process each highlight
    for raw_str in highlights:
        h = Highlight(raw_str)
        # if haven't seen the book title before create a new book, then add the highlight
        if (not h.title is None) and (h.title not in Book.book_titles):
            b = Book(h.title, h.author)
            b.add_highlight(h) # add highlight to book
            library.append(b) # add the new book to our library
        else:
            # check all other books we know about to add highlight to its own book
            for b in library:
                if b.title == h.title:
                    b.add_highlight(h)

    # process each book in our library
    for book in library:
        if book.title:
            # if we haven't processed the book, process now
            if book.title.strip() not in processed_books:
                book.write_book_to_html() # send to output
                processed_books.append(book.title.strip()) # add the book as processed
            else:
                print(f"HTML file already produced for: {book.title}")

########################################################################################################################
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--clippings_file_path", help="The path to the Kindle clippings text file.", \
                        default="./My Clippings.txt")
    parser.add_argument("-o", "--output_dir_path", help="The path for the output directory.", \
                        default="./output/")
    args = parser.parse_args()

    process(args.clippings_file_path, args.output_dir_path)
