__author__ = 'anoop'

import os
import sys
import urllib2
from urllib import urlretrieve


class Constants:
    pattern_to_match = '<a\s*href=[\'|"](.*?)[\'"].*?>'


class Queue:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def enqueue(self, item):
        self.items.insert(0, item)

    def dequeue(self):
        return self.items.pop()

    def size(self):
        return len(self.items)


def download(url, destination=os.curdir, filename='download.file', silent=False):
    def get_size():
        meta = urllib2.urlopen(url).info()
        meta_func = meta.getheaders if hasattr(
            meta, 'getheaders') else meta.get_all
        meta_length = meta_func('Content-Length')
        try:
            return int(meta_length[0])
        except:
            return 0

    def get_response():
        response = urllib2.urlopen(url)
        return response.read()

    def kb_to_mb(kb):
        return kb / 1024.0 / 1024.0

    def callback(blocks, block_size, total_size):
        current = blocks * block_size
        percent = 100.0 * current / total_size
        line = '[{0}{1}]'.format(
            '=' * int(percent / 2), ' ' * (50 - int(percent / 2)))
        status = '\r{0:3.0f}%{1} {2:3.1f}/{3:3.1f} MB'
        sys.stdout.write(
            status.format(
                percent, line, kb_to_mb(current), kb_to_mb(total_size)))

    path = os.path.join(destination, filename)
    try:
        (path, headers) = urlretrieve(url, path, None if silent else callback)
    except Exception as e:
        os.remove(path)
        raise Exception("Can't download {0}".format(path))
    return get_response()
