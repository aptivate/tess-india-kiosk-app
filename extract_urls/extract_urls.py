#!/usr/bin/env python

from bs4 import BeautifulSoup
import requests
import re


start_page = 'http://www.open.edu/openlearnworks/course/view.php?id=1911'
subpage_identifier = 'oucontent'


def convert_page_to_soup(url):
    sub_page = requests.get(url)
    soup = BeautifulSoup(sub_page.text)
    return soup


def print_menu_links(soup):
    menu_section = soup.find('li', class_='type_activity depth_4 item_with_icon current_branch')
    link_count = 0
    if menu_section:
        for link in menu_section.findAll('a', href=True):
            link_count += 1
            print link.attrs['href']
    return link_count


def mid_level_page_parser(url):
    soup = convert_page_to_soup(url)
    page = soup.findAll('li', class_=re.compile('(subpage|oucontent)'))
    link_count = 0
    for list_item in page:
        link = list_item.find('a', href=True)
        if link:
            link_count += 1
            if subpage_identifier in link.attrs['href']:
                thin_soup = convert_page_to_soup(link.attrs['href'])
                link_count += print_menu_links(thin_soup)
            elif 'subpage' in link.attrs['href']:
                    link_count += mid_level_page_parser(link.attrs['href'])
                    print link.attrs['href']
            else:
                print link.attrs['href']
    return link_count


def top_level_page_parser(url):
    web_page = requests.get(url)
    the_soup = BeautifulSoup(web_page.text)
    link_count = 0

    page = the_soup.findAll('li', class_=re.compile('(subpage|oucontent)'))

    for list_item in page:
        link = list_item.find('a', href=True)
        if link:
            link_count += 1
            link_count += mid_level_page_parser(link.attrs['href'])
            print link.attrs['href']

    return link_count


def main():
    link_count = top_level_page_parser(start_page)
    print link_count

if __name__ == '__main__':
    main()
