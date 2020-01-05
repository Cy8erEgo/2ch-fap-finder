#!/usr/bin/env python3

from models import TwoChannel
from bs4 import BeautifulSoup as BS
from prettytable import PrettyTable
from argparse import ArgumentParser


# set up argparse
aparser = ArgumentParser()
aparser.add_argument("thread_id", help="Thread ID")
args = aparser.parse_args()

# get posts
ch = TwoChannel()
posts = ch.get_thread_posts(args.thread_id)

# make a rating
rating = {}

for post in posts:
    comment_soup = BS(post["comment"], "html.parser")
    comment_link = comment_soup.find("a")

    if comment_link:
        parent_id = comment_link.get("data-num")
    else:
        continue

    if parent_id:
        parent_url = ch.base_url + f"res/{args.thread_id}.html#{parent_id}"

        if parent_url not in rating:
            rating[parent_url] = 1
        else:
            rating[parent_url] += 1

# output the rating
tbl = PrettyTable(["Id", "Ответы"], border=True, sortby="Ответы")

for r in rating.items():
    tbl.add_row([r[0], r[1]])

print(tbl)
