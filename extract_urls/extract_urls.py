#!/usr/bin/env python

from bs4 import BeautifulSoup
import os
import requests
import re
import shutil


start_page = 'http://www.open.edu/openlearnworks/course/view.php?id=1911'
content_identifier = 'oucontent'
subpage_identifier = 'subpage'
link_list_item_regex = '(subpage|oucontent)'
current_directory = os.path.dirname(__file__)
generated_urls_parent_directory = os.path.join(
    current_directory,
    '..',
    'SiteArchive',
    'generated_content'
)
generated_urls_main_directory = os.path.join(
    generated_urls_parent_directory,
    'urls'
)


def clean_file_name(file_name):
    file_name = re.sub('[^A-Za-z0-9 ]+', '', file_name)
    file_name = file_name.replace(' ', '_')
    return file_name + '.links'


def save_urls(directory, file_name, urls):
    if not isinstance(urls, list):
        print "The urls to be saved should be passed in as a list."
        exit()

    if not os.path.exists(directory):
        os.mkdir(directory)

    file_path = os.path.join(directory, clean_file_name(file_name))

    with open(file_path, 'a') as file:
        urls_to_save = "\n".join(urls)
        file.write(urls_to_save)


def convert_page_to_soup(url):
    sub_page = requests.get(url)
    soup = BeautifulSoup(sub_page.text)
    return soup


def print_menu_links(soup):
    menu_section = soup.find('li', class_='type_activity depth_4 item_with_icon current_branch')
    if menu_section:
        for link in menu_section.findAll('a', href=True):
            print link.attrs['href']


def mid_level_page_parser(url):
    soup = convert_page_to_soup(url)
    page = soup.findAll('li', class_=re.compile(link_list_item_regex))

    for list_item in page:
        link = list_item.find('a', href=True)

        if link:
            if content_identifier in link.attrs['href']:
                thin_soup = convert_page_to_soup(link.attrs['href'])
                print_menu_links(thin_soup)
            elif subpage_identifier in link.attrs['href']:
                    mid_level_page_parser(link.attrs['href'])
                    print link.attrs['href']
            else:
                print link.attrs['href']


def top_level_page_parser(url):
    web_page = requests.get(url)
    the_soup = BeautifulSoup(web_page.text)

    page = the_soup.findAll('li', class_=re.compile(link_list_item_regex))

    links = []

    for list_item in page:
        link = list_item.find('a', href=True)
        if link:
            mid_level_page_parser(link.attrs['href'])
            links.append(link.attrs['href'])

    save_urls(generated_urls_main_directory, 'main', links)


def setup_directories():
    if os.path.exists(generated_urls_main_directory):
        shutil.rmtree(generated_urls_main_directory)

    os.mkdir(generated_urls_main_directory)


def main():
    setup_directories()

    top_level_page_parser(start_page)


if __name__ == '__main__':
    main()
