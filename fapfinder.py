#!/usr/bin/env python3 

from bs4 import BeautifulSoup as bs
import requests
import json
import sys

SEARCH_KEYWORDS = 'фап fap afg'
PAGES_COUNT = 9  

keywords_list = SEARCH_KEYWORDS.split()

def parse(html):
    soup = bs(html, 'html.parser')
    text = soup.get_text()

    return text 

def get_threads_page(page_num):
    page_url = 'https://2ch.hk/b/%s.json' % page_num
    response = requests.get(page_url).json()

    return response['threads']
    
def search():
    results = []

    for page_num in range(1, PAGES_COUNT + 1):
        sys.stdout.flush()
        sys.stdout.write('\rСтраница %d из %d' % (page_num, PAGES_COUNT))
        
        threads_page = get_threads_page(page_num)
        
        for thread in threads_page:
            thread_info = thread['posts'][0]

            thread_comment= thread_info['comment'].lower() 
            thread_subject = thread_info['subject']
            thread_id = thread_info['num']
            thread_files_count = thread_info['files_count']
       
            for keyword in keywords_list:
                if keyword in thread_comment:
                    post = {
                        'id': thread_id,
                        'title': parse(thread_subject)
                    }

                    if post not in results:
                        results.append(post)

    sys.stdout.write('\n\n')

    return results



if __name__ == '__main__':
    print('\nПоиск...\n')

    results = search()

    if len(results) > 0:
        print('Найденные фап-треды:\n')

        for index, result in enumerate(results):
            url = 'https://2ch.hk/b/res/%s.html' % result['id']

            print('%s. %s\n%s\n' % (index + 1, result['title'], url))
    else:
        print('Фап-тред не найден :c')

