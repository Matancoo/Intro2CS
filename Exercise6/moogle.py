##############################################################################
# FILE: moogle.py
# EXERCISE: Intro2cs ex6 2022-2023
# WRITER: matan cohen
# DESCRIPTION: Ex6 main file
# additional files: ...
##############################################################################

##############################################################################
#                                   Imports                                  #
##############################################################################
import copy
from typing import List, Union
import urllib.parse
import sys
import pickle
from typing import Optional
import requests  # to extracdt HTML files
from bs4 import BeautifulSoup
# Collections
# argparse TODO: check what are these library
##############################################################################
#                                   Typing                                   #
##############################################################################
traffic_dict: dict[str, dict[str, int]]
word_dict: dict[str, dict[str, int]]


##############################################################################
#                                 CONSTANTS                                  #
##############################################################################
BASE_URL = 'https://www.cs.huji.ac.il/w~intro2cs1/ex6/wiki/'
INDEX_URL = '/Users/matancohen/Desktop/Ics/ex6/small_index.txt'
RESULT_URL = "/Users/matancohen/Desktop/Ics/ex6/results.txt"
##############################################################################
#                              Helper Functions                              #
##############################################################################


def is_int(s):
    '''Checks if a string can be casted to an integer'''
    try:
        int(s)
        return True
    except ValueError:
        return False


def combine_url(base_url: str, relative_url: str):
    """
    Combines base and relative url adresses
    return full url
    """
    full_url = urllib.parse.urljoin(base_url, relative_url)
    return full_url


def get_partial_url(full_url):
    """
    returns the partial part of the url
    """
    url_list = full_url.split('/')
    partial_url = url_list[-1].strip()
    return partial_url


def save_object_in_file(object: Optional[dict], target_filepath: str, mode='wb'):
    """
    helper function that saves object (dict or any type) unto targetfile
    """
    with open(target_filepath, mode) as target_file:
        pickle.dump(object, target_file, protocol=pickle.HIGHEST_PROTOCOL)
    target_file.close()


def open_file(file_path: str, method='rb'):
    """
    helper function to open file
    return file
    """
    with open(file_path, method) as target_file:
        file = pickle.load(target_file)
    return file


def get_HTML(file_path: str) -> str:
    """
    Helper function to gets file and convert it to HTML file.
    file_path : full URL path
    return html
    """
    response = requests.get(file_path)
    html = response.text
    return html


def is_url_absolute(url) -> bool:
    """
    Helper function to check if url is absolute
    """
    return bool(urllib.parse.urlparse(url).netloc)


def init_traffic_dict(html_files: list[str], full_urls: list[str], partial_urls: list[str]) -> dict:
    """
      Helper function that initiate traffic dict based on connection btw base and target HTML files
      INPLACE
      ASsume all inputs are of same order
      """
    traffic_dict: dict[str, dict] = dict()
    for i in range(len(html_files)):
        page_file = html_files[i]
        page_name = partial_urls[i]
        soup = BeautifulSoup(page_file, 'html.parser')
        for paragraph in soup.find_all("p"):
            # run on all links_to_other_pages in page
            for link in paragraph.find_all("a"):
                linked_page_name = link.get("href")
                if linked_page_name == "":
                    continue
                if is_url_absolute(linked_page_name):
                    linked_page_name = get_partial_url(linked_page_name)
                if linked_page_name not in partial_urls:
                    continue
                if page_name not in traffic_dict.keys():
                    traffic_dict[page_name] = dict()

                if linked_page_name not in traffic_dict[page_name].keys():
                    traffic_dict[page_name][linked_page_name] = 0
                traffic_dict[page_name][linked_page_name] += 1

    return traffic_dict


def init_word_dict(html_files: list[str], partial_urls: list[str]) -> dict:
    """
      Helper function that initiate traffic dict based on connection btw base and target HTML files
      INPLACE
      ASsume all inputs are of same order
      """
    word_dict: dict[str, dict] = dict()
    for i in range(len(html_files)):
        page_file = html_files[i]
        page_name = partial_urls[i]
        soup = BeautifulSoup(page_file, 'html.parser')

        # run on each line in conetent
        for p in soup.find_all("p"):
            current_line = (p.text).split()

            for i in range(len(current_line)):
                # TODO: see if thus loop necessary
                current_word = current_line[i].rstrip()  # NEED REMOVE ALSO \n

                if current_word not in word_dict.keys():
                    word_dict[current_word] = dict()

                if page_name not in word_dict[current_word].keys():
                    word_dict[current_word][page_name] = 0
                word_dict[current_word][page_name] += 1

    return word_dict


def preprocess_traffic(index_file: str, base_url=BASE_URL) -> dict:
    """
    index_file: assume contains full URL
    Function that initiate dict of connections between HTML files. their partial URL appearing in index_file. Their base url appear in base_url
    Below files are ordered similary
    """
    html_files: list[str]
    full_urls: list[str]
    partial_urls: list[str]
    traffic_dict: dict[str, dict[str, int]]

    # remove \n from names
    partial_urls = list(open(index_file, 'r'))
    for i in range(len(partial_urls)):
        partial_urls[i] = partial_urls[i].rstrip()

    # create list of full URL path
    full_urls = []
    for partial_url in partial_urls:
        full_url = combine_url(base_url, partial_url)
        full_urls.append(full_url)

    # create list of HTML_files
    html_files = [get_HTML(url) for url in full_urls]

    return html_files, full_urls, partial_urls


def init_ranking_dict(traffic_dict, iteration_num):
    """
    Helper function that creates a grading dictionary. Used to grade sites acc to their reference in other sites

    """
    r = {page_name: 1.0 for page_name in traffic_dict.keys()}
    count = iteration_num
    while count:  # I work directly on that
        count -= 1
        new_r = {page_name: 0.0 for page_name in traffic_dict.keys()}

        for page_name in traffic_dict:
            page_traffic_dict = traffic_dict[page_name]
            total_traffic_in_page = sum(page_traffic_dict.values())
            for linked_page in page_traffic_dict.keys():
                val = page_traffic_dict[linked_page]
                # assert is_int(val)
                relative_val = val/total_traffic_in_page
                # assert linked_page in new_r.keys()
                new_r[linked_page] += r[page_name] * relative_val
            # NOTE: Is deep copy necessary here? shallow copy is enough I gather
        r = copy.deepcopy(new_r)
    return r


def _is_quary_in_page(quary: list, word_dict: dict[str, dict[str, int]]):
    """PART D
    Helper function that returns dict 
    Keys : pages that contain all words in quary 
    val: dict - quary words as keys, number of appearance in page as val (int)

    Note if exist word in quary that is not in word_dict--> return empty list
    """
    valid_pages: dict[str, dict[str, int]] = dict()

    if not quary:
        return []

    for word in quary:
        if word not in word_dict.keys():
            return []  # for bool val
        for potential_page in word_dict[word].keys():
            if potential_page not in valid_pages.keys():
                valid_pages[potential_page] = dict()
            page_dict = valid_pages[potential_page]
            if word not in page_dict.keys():
                page_dict[word] = 0
            page_dict[word] += word_dict[word][potential_page]

    # extract valid_pages
    # if a val is zero --> page not valid as it doesnt contain all words in quary
    for page in valid_pages.keys():
        page_dict = valid_pages[page]
        for val in page_dict.values():
            if val == 0:
                # delete page from valid pages if word doesnt exist
                del valid_pages[page]

    return valid_pages


def _rank_valid_pages(valid_pages, ranking_dict, max_results):
    """PART D
    Helper fucntion
    We will create two list: sorted_pages1: given valid_pages, ranks them according to score in ranking dict.
                             sorted_pages2 : sort pages according to the prevalence of the words from the quary, that appear in them
    After ranking we will chose a max_result number of valid pages
    """
    # TODO: try to do the following using zip

    valid_pages_list = sorted(ranking_dict, key=ranking_dict.get, reverse=True)

    # TODO: I odnt get why when I add condition(if page in valid_pages.keys()) in the creation of page rank, I do not get the same results.
    lst = []
    for page in valid_pages_list:
        if page in valid_pages.keys():
            lst.append(page)

    lst = lst[:max_results]
    # valid_pages_list = valid_pages_list[:max_results]
    pages_rank = {page: min(valid_pages[page].values())
                  for page in lst}  # no need this if condition

    final_pages_rank = {page: pages_rank[page] * ranking_dict[page]
                        for page in pages_rank.keys() if page in ranking_dict.keys()}  # no need this if condition

    # assume returns list of tupples
    final_pages: list[tuple] = list(final_pages_rank.items())
    sorted_pages = sorted(
        final_pages, key=lambda tup: tup[1], reverse=True)

    # get at most max_results posible pages
    # sorted_pages = sorted_pages[:max_results] TODO: did this in beginning as instructed
    return sorted_pages


##############################################################################
#                              Exercise                               #
##############################################################################

if __name__ == '__main__':

    # NOTE: I have problem in presubmit with crawl. I tried everything including three lab supports session.
    if sys.argv[1] == 'crawl':

        base_url = sys.argv[2]
        index_file = sys.argv[3]
        output_file = sys.argv[4]
        html_files, full_urls, partial_urls = preprocess_traffic(
            index_file, base_url)

        traffic_dict = init_traffic_dict(html_files, full_urls, partial_urls)

        save_object_in_file(traffic_dict, output_file)

    if sys.argv[1] == 'page_rank':
        iteration_num = int(sys.argv[2])
        traffic_dict = open_file(sys.argv[3])
        output_file_path = sys.argv[4]  # TODO: assume legal input
        r = init_ranking_dict(traffic_dict, iteration_num)
        save_object_in_file(r, output_file_path)

    if sys.argv[1] == 'words_dict':

        base_url = sys.argv[2]
        index_file = sys.argv[3]
        output_file = sys.argv[4]

        html_files, full_urls, partial_urls = preprocess_traffic(
            index_file, base_url)

    # init dictionary
        word_dict = init_word_dict(html_files, partial_urls)
        save_object_in_file(word_dict, output_file)

    if sys.argv[1] == 'search':
        quary = (sys.argv[2]).split(" ")  # TODO: check if need reslpit
        ranking_dict: dict = open_file(sys.argv[3])
        word_dict: str = open_file(sys.argv[4])
        max_results: int = int(sys.argv[5])
        valid_pages = _is_quary_in_page(quary, word_dict)

        if valid_pages:
            sorted_pages: list[tuple] = _rank_valid_pages(
                valid_pages, ranking_dict, max_results)

            for page in sorted_pages:
                string = page[0] + " " + str(page[1])
                print(string)

    # create text file
    # NOTE: after reading the forum I understood that I can create the text file by hand.
        # thus the below code is not used
