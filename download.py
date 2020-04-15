import argparse
import os
from collections import namedtuple
from urllib.parse import urljoin

import pandas as pd
import requests
from tqdm.auto import tqdm

# add progress_apply to pd.DataFrame
tqdm.pandas()

# config urls
books_url = "https://resource-cms.springernature.com/springer-cms/rest/v1/content/17858272/data/v4"

base_pdf = "https://link.springer.com/content/pdf/10.1007/"

# struct
Book = namedtuple("Book", ["title", "isbn"])


# TODO: add epub downlaods
def pdf_url(isbn):
    return urljoin(base_pdf, f"{isbn}.pdf")


def get_books():
    fp = "books.xlsx"

    if os.path.isfile(fp):
        return pd.read_excel(fp)
    else:
        r = requests.get(books_url)

        with open(fp, "wb") as f:
            f.write(r.content)

        return pd.read_excel(r.content)


def download(book):

    fp = f"books/{book.title}_{book.isbn}.pdf"

    if os.path.isfile(fp):
        return

    r = requests.get(pdf_url(book.isbn))

    with open(fp, "wb") as f:
        f.write(r.content)


def parse_args():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "-t",
        "--titles",
        nargs="+",
        help="list of book titles to download; matches will be exact (case-sensitive)",
    )
    group.add_argument(
        "-s",
        "--subject",
        help="download books of a given subject; matches will be exact (case-in-sensitive)",
    )
    group.add_argument(
        "--contains",
        help="download via substring matches on book title (case-in-sensitive)",
    )
    group.add_argument(
        "--regex", help="download via regex pattern matches on book title"
    )
    return parser.parse_args()


def main():
    args = parse_args()

    df = get_books()

    # columns to access
    title_col = "Book Title"
    subject_col = "Subject Classification"
    isbn_col = "Electronic ISBN"

    # apply filters
    if args.titles:
        df = df[df[title_col].isin(args.titles)]

    if args.subject:
        df = df[df[subject_col].str.contains(args.subject, case=False, regex=False)]

    if args.contains:
        df = df[df[title_col].str.contains(args.contains, case=False, regex=False)]

    if args.regex:
        df = df[df[title_col].str.contains(args.regex, regex=True)]

    # skip download if no matches
    if df.empty:
        print("No book matched query args; nothing to downlaod")
        return

    # download progress
    df.progress_apply(
        lambda x: download(Book(title=x[title_col], isbn=x[isbn_col])), axis=1
    )

    print(f"Successfully downloaded {df.shape[0]} books!")


if __name__ == "__main__":
    main()
