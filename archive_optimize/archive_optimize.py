#!/usr/bin/env python

import os
import sys
from distutils import dir_util

from bs4 import BeautifulSoup
import magic


BASE_DIR = os.path.abspath(os.path.dirname(__file__))
MOBILE_CSS_FILE = os.path.join(BASE_DIR, 'mobile.css')
MEDIA_DIR = os.path.join(BASE_DIR, 'media')

with open(MOBILE_CSS_FILE, 'r') as f:
    MOBILE_CSS = u"%s" % f.read()


def add_mobile_css(soup):
    mobile_style = soup.new_tag("style")
    mobile_style.append(MOBILE_CSS)
    soup.head.append(mobile_style)


def remove_inline_styles(soup):
    for inlined in soup.select('[style]'):
        del inlined['style']


def find_related_video_link(obj):
    link = obj.find_next("a", text="video")
    return link.attrs.get('href') if link else None


def build_video_element(soup, obj, link):
    video = soup.new_tag("video",
                         src=link,
                         preload='metadata',
                         controls=True)

    copy_attrs = ('height', 'width')
    for attr in copy_attrs:
        if obj.attrs.get(attr):
            video.attrs[attr] = obj.attrs[attr]

    return video


def replace_youtube_videos(soup):
    for obj in soup.find_all("object"):
        video_link = find_related_video_link(obj)
        if video_link:  # Replace with HTML5 video player
            video = build_video_element(soup, obj, video_link)
            obj.replace_with(video)
        else:  # Just remove it
            # Removes YouTube links (all flash objects really)
            obj.extract()


def process_page(content):
    soup = BeautifulSoup(content)

    add_mobile_css(soup)
    remove_inline_styles(soup)
    replace_youtube_videos(soup)

    return soup.prettify()


def process_file(filename):
    content = ''
    with open(filename, 'r') as f:
        orig_content = f.read()
        content = process_page(orig_content)

    with open(filename, 'w') as f:
        f.write(content.encode('utf8'))


def is_webpage(filename):
    webpage = False
    base, ext = os.path.splitext(filename)
    if ext:
        if ext == '.html':
            webpage = True
    elif magic.from_file(filename, mime=True) == "text/html":
        webpage = True
    return webpage


def main(orig_dir, copy_dir):
    if os.path.exists(copy_dir):
        print 'Destination directory already exists. Exiting!'
        sys.exit(1)
    dir_util.copy_tree(MEDIA_DIR, copy_dir)
    dir_util.copy_tree(orig_dir, copy_dir)
    for root, dirs, files in os.walk(copy_dir):
        if len(files):
            for name in files:
                f = os.path.join(root, name)
                if is_webpage(f):
                    print 'Processing: ', f
                    process_file(f)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print 'Not enough parameters.\n\nUsage: tess_optimize <content_dir> <output_dir>'
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])
