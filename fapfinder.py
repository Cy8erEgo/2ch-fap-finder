#!/usr/bin/env python3

from models import TwoChannel
from prettytable import PrettyTable


def main():
    ch = TwoChannel()
    fap_threads = ch.get_fap_threads()

    tbl = PrettyTable(
        ["Тема", "Комментарии", "Webm", "Картинки", "Рейтинг", "URL"],
        border=False
    )

    for i, t in enumerate(fap_threads, 1):
        subject = t["subject"] if len(t["subject"]) <= 35 else t["subject"][:32] + "..."
        score = round(float(t["score"]), 2)
        webm_count, imgs_count = ch.get_media_count(t["num"])
        url = "https://2ch.hk/b/res/%s.html" % t["num"]

        tbl.add_row(
            [subject, t["posts_count"], webm_count, imgs_count, score, url]
        )

    print(tbl)


if __name__ == "__main__":
    main()
