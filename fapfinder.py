#!/usr/bin/python3 

from bs4 import BeautifulSoup
import requests
import json
import sys

searchKeywords = 'фап fap afg'
keywordsList = searchKeywords.split()
results = list()
pages = int(sys.argv[1])

def parse(html):
    soup = BeautifulSoup(html, 'html5lib')
    text = soup.get_text()

    return text 
    
def search():
    print('Поиск...\n')

    for pageNum in range(1, pages):
        pageP = 'https://2ch.hk/b/%s.json' % pageNum

        r = requests.get(pageP).json()
        
        for thread in r['threads']:
            threadInfo = thread['posts'][0]

            threadComment= threadInfo['comment'].lower() 
            threadSubject = threadInfo['subject']
            threadId = threadInfo['num']
            threadFilesCount = threadInfo['files_count']
       
            for keyword in keywordsList:
                if keyword in threadComment:
                    post = {
                        'id': threadId,
                        'title': parse(threadSubject)
                    }

                    results.append(post)


search()

if len(results) > 0:
    print('Фап-тред найден:\n')
    print('-' * 30)

    for result in results:
        
        url = 'https://2ch.hk/b/res/%s.html' % result['id']
        print(result['title'] + '\n' + url)

    print('-' * 30)
else:
    print('Фап-тред не найден :c')



