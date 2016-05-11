__author__ = 'anoop'
import os
import re
import sys
import urlparse

import utilities

'''
python crawler.py <url endpoint> <maximum no of urls to visit>

'''

if __name__ == "__main__":
    url_to_start = None
    MAX_URLS_TO_PARSE = -1
    try:
        # max urls parse should be a positive integer
        url_to_start = sys.argv[1]
        MAX_URLS_TO_PARSE = int(sys.argv[2])
    except Exception, e:
        print("Please enter the proper format: python crawler.py <url endpoint> <maximum no of urls to visit>")
    try:
        visited_links = set()
        unvisited_nodes = utilities.Queue()
        queue_set = set()
        linkregex = re.compile(utilities.Constants.pattern_to_match)
        unvisited_nodes.enqueue(url_to_start)
        while unvisited_nodes.size() != 0 and len(visited_links) < MAX_URLS_TO_PARSE:
            current_url = unvisited_nodes.dequeue()
            scheme, netloc, url, params, query, fragment = urlparse.urlparse(current_url)
            url_sample = netloc + url
            if url != '' and url[-1] == '/':
                url = url[:-1]
            if url == '':
                current_url_path_list = url.split("/")
                current_url_filename = 'default.file'
                current_url_path_temp = '/'.join(current_url_path_list)
                actual_destination_path = netloc + "/" + current_url_path_temp
            else:
                current_url_path_list = url.split("/")
                current_url_filename = current_url_path_list.pop(-1)
                if not "." in current_url_filename:
                    current_url_path_list.append(current_url_filename)
                current_url_path_temp = '/'.join(current_url_path_list)
                actual_destination_path = netloc + current_url_path_temp

            if (not os.path.exists(actual_destination_path)):
                os.makedirs(actual_destination_path)
            file_response = utilities.download(current_url, actual_destination_path, current_url_filename, silent=True)
            links = linkregex.findall(file_response)
            visited_links.add(current_url)
            for link in (links.pop(0) for _ in xrange(len(links))):
                if link.startswith('/'):
                    link = '{0}://'.format(scheme) + netloc + link
                    if link not in queue_set:
                        print "Enqueing ", link
                        unvisited_nodes.enqueue(link)
                        queue_set.add(link)
                    else:
                        print "Visited {0}".format(link)
                elif link.startswith('http') or link.startswith('https'):
                    if link not in queue_set:
                        unvisited_nodes.enqueue(link)
                        queue_set.add(link)
                    else:
                        print "Visited {0}".format(link)
    except Exception as e:
        print(e.message)
