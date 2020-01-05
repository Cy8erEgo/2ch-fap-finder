#!/usr/bin/env python3

import requests
from user_agent import generate_user_agent


class TwoChannel:
    def __init__(self):
        self.base_url = "https://2ch.hk/b/"
        self.session = requests.session()
        self.session.headers = {"user-agent": generate_user_agent()}

    def _query(self, url):
        return self.session.get(url).json()

    def get_all_threads(self):
        url = self.base_url + "threads.json"
        return self._query(url)["threads"]

    def get_fap_threads(self):
        keywords_list = "фап fap afg".split()
        all_threads = self.get_all_threads()
        fap_threads = []

        for thread in all_threads:
            # TODO: поиск регуляркой
            subject = thread["subject"].lower()

            for k in keywords_list:
                if k in subject and thread not in fap_threads:
                    fap_threads.append(thread)

        return sorted(
            fap_threads, key=lambda x: x["posts_count"], reverse=True
        )

    def get_thread(self, thread_id):
        url = self.base_url + "res/%s.json" % thread_id
        return self._query(url)

    def get_thread_posts(self, thread_id):
        thread = self.get_thread(thread_id)
        return thread["threads"][0]["posts"]

    def get_media_count(self, thread_id):
        posts = self.get_thread_posts(thread_id)

        webm_cnt = 0
        imgs_cnt = 0

        for post in posts:
            if post["files"]:
                for f in post["files"]:
                    if f["type"] in (6, 10):
                        webm_cnt += 1
                    elif f["type"] in (1, 2, 4):
                        imgs_cnt += 1
                    else:
                        print(f["type"], f["path"])

        return (webm_cnt, imgs_cnt)


if __name__ == "__main__":
    from pprint import pprint
    ch = TwoChannel()
    pprint(ch.get_fap_threads())
