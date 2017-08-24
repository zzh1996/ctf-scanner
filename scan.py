#!/usr/bin/env python3

import requests
from termcolor import colored
import sys

timeout = 5
extensions = ['html', 'htm', 'php', 'asp', 'aspx']
backups = ['%s', '%s.bak', '%s~', '.%s.swp']


def scan(url):
    if url.endswith('/'):
        url = url[:-1]
    with open('sensitive_files.txt') as f:
        for line in f:
            line = line.strip()
            if line.startswith('#'):  # comment
                continue
            if not line:  # empty line
                continue
            if '*' in line:
                base = url + line[:line.rindex('/') + 1]
                filename = line[line.rindex('/') + 1:]
                for ext in extensions:
                    for fmt in backups:
                        test_url(base + fmt % filename.replace('*', ext))

            else:
                test_url(url + line)


def test_url(url):
    try:
        r = requests.head(url, timeout=timeout)
    except requests.exceptions.Timeout:
        print(colored('Timeout ' + url, 'blue'))
        return
    if r.status_code != 404:
        color = 'red'
    else:
        color = 'white'
    print(colored(str(r.status_code) + ' ' + url, color))


if __name__ == '__main__':
    try:
        scan(sys.argv[1])
    except IndexError:
        print('Usage: ' + sys.argv[0] + ' [url]')
