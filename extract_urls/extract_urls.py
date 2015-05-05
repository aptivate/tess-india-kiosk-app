#!/usr/bin/env python

from bs4 import BeautifulSoup
import requests
import re


start_page = 'http://www.open.edu/openlearnworks/course/view.php?id=1911'
content_identifier = 'oucontent'
subpage_identifier = 'subpage'
link_list_item_regex = '(subpage|oucontent)'


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

    for list_item in page:
        link = list_item.find('a', href=True)
        if link:
            mid_level_page_parser(link.attrs['href'])
            print link.attrs['href']


def main():
    top_level_page_parser(start_page)

if __name__ == '__main__':
    main()
