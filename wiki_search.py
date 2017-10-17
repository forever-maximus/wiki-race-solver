from flask_socketio import emit
from bs4 import BeautifulSoup
from collections import deque
import requests
import json
import datetime

search_requests = deque()


class WikiPageNode():
    """ Represents a wikipedia page """

    def __init__(self, url):
        self.url = url
        self.parent_node = None


def add_search_request(new_request):
    search_requests.append(new_request)


def get_search_requests():
    list_of_searches = []
    for request in search_requests:
        list_of_searches.append(request)
    return list_of_searches
    

def find_shortest_path(start, end):
    start_node = WikiPageNode(start)
    wiki_node_queue = deque()
    wiki_node_queue.append(start_node)
    visited_nodes = set()

    while len(wiki_node_queue) != 0:
        print('<----------------->') # temp
        current_wiki_page = wiki_node_queue.popleft()
        visited_nodes.add(current_wiki_page.url)
        print('before GET request - ' + current_wiki_page.url + ' - ' + str(datetime.datetime.now())) # temp
        http_request = requests.get(current_wiki_page.url)
        html_content = BeautifulSoup(http_request.text, 'html.parser')
        linked_wiki_url_list = html_content.find_all('a')
        for link in linked_wiki_url_list:
            linked_wiki_url = link.get('href')
            print(visited_nodes)
            if isinstance(linked_wiki_url, str) and linked_wiki_url.startswith('/wiki/') \
                and ':' not in linked_wiki_url and 'https://en.wikipedia.org' + linked_wiki_url not in visited_nodes:
                linked_wiki_page = WikiPageNode('https://en.wikipedia.org' + linked_wiki_url)
                linked_wiki_page.parent_node = current_wiki_page
                wiki_node_queue.append(linked_wiki_page)
                #emit('search response', linked_wiki_url, broadcast=True)
                if ('https://en.wikipedia.org' + linked_wiki_url == end):
                    return linked_wiki_page
    #end


def get_formatted_shortest_path(goal_wiki_page):
    path_list = []
    path_list.append(goal_wiki_page.url.split('/wiki/')[1])
    while goal_wiki_page.parent_node != None:
        goal_wiki_page = goal_wiki_page.parent_node
        path_list.append(goal_wiki_page.url.split('/wiki/')[1])
    path_list.reverse()
    return path_list

