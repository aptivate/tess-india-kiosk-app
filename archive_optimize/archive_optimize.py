#!/usr/bin/env python

import os
import sys
from distutils import dir_util
from shutil import copyfile

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


def remove_unwanted_blocks(soup):
    selectors = (
        '#page-openlearnworks-header',
        '#page-openlearnworks-rhs',
        '#enrolbutton ',
        '#region-pre .block.oucontent-printablelink',
        '.oucontent-linkwithtip',
        '.oucontent-linktip',
        '.left.side',
        '.right.side',
        '.page-footer-links',
        '#page-footer-copyright',
        '#footer1'
    )
    for selector in selectors:
        matches = soup.select(selector)
        for match in matches:
            match.extract()


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


def add_dfid_logo(soup, filename):
    prefix = "../.." if 'openlearnworks/course/' in filename else "../../.."
    dfid_logo = os.path.join(prefix, 'tessindia/UK-AID-small.jpg')
    style = '''
#footer3 {
    background: url("%s") no-repeat scroll 0px 0px transparent;
    width: 113px;
    height: 125px;
}
    ''' % dfid_logo

    dfid = soup.new_tag("style")
    dfid.append(style)
    soup.head.append(dfid)

    footer3 = soup.new_tag("div", id="footer3")
    footer_root = soup.find("div", id="page-footer-image")
    if footer_root:
        footer_root.append(footer3)


def add_home_link_to_logo(soup):
    title = soup.select('#page-header h1.header-title')
    if title:
        title = title[0]
        home_url = title.find("a")['href']
        logo_wrap = soup.find(True, id="page-cobrand-image")
        logo_wrap.img.wrap(
            soup.new_tag("a", href=home_url)
        )
        title.extract()


def fix_sidebar(soup):
    '''
    Remove sidebar if there is no interesting content in it.

    If there is (.depth_4.current_branch exists), then replace its content
    with that branch.
    '''
    sidebar = soup.find("div", id="region-pre")
    if sidebar:
        branch = sidebar.select(".depth_4.current_branch")
        sidebar_root = sidebar.select("ul.block_tree")
        if branch and sidebar_root:
            branch = branch[0]
            sidebar_root = sidebar_root[0]
            sidebar_root.clear()
            sidebar_root.append(branch)
        else:
            sidebar.extract()


def remove_illegal_chars_from_name(text):
    """
    The VFAT filesystem cannot have file names with the following characters:
        \ / : * ? " < > | ^

    We also need to remove the HTML encoded version

    And we'll remove & just to be sure.
    """
    return text.replace('?', 'Q').replace('%3F', 'Q') \
        .replace('|', 'P') \
        .replace('&', 'M').replace('%26', 'M')


def remove_illegal_chars_from_links(soup):
    """
    We can't have ? in filenames in VFAT, as used by SD cards

    So instead we replace ? by Q, and then do the same to filenames
    """
    for link in soup.find_all('a', href=True):
        link.attrs['href'] = remove_illegal_chars_from_name(link.attrs['href'])


def process_page(content, filename):
    soup = BeautifulSoup(content)

    add_mobile_css(soup)
    add_home_link_to_logo(soup)
    remove_inline_styles(soup)
    remove_unwanted_blocks(soup)
    remove_illegal_chars_from_links(soup)
    replace_youtube_videos(soup)
    add_dfid_logo(soup, filename)
    fix_sidebar(soup)

    return soup.prettify()


def process_file(filename):
    content = ''
    with open(filename, 'r') as f:
        orig_content = f.read()
        content = process_page(orig_content, filename)

    with open(filename, 'w') as f:
        f.write(content.encode('utf8'))


def remove_illegal_chars_from_filename(filename):
    new_filename = remove_illegal_chars_from_name(filename)
    if new_filename != filename:
        os.rename(filename, new_filename)


def copy_new_logo(copy_dir):
    new_logo_path = os.path.join(MEDIA_DIR,
                                 'tessindia/TESS-India-Banner.jpg')
    old_logo_path = os.path.join(
        copy_dir,
        'openlearnworks/pluginfile.php/134332/theme_openlearnworks/image/Labspace-TESS-India-Banner2.jpg')
    copyfile(new_logo_path, old_logo_path)


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
    print 'Making a copy of content...'
    dir_util.copy_tree(orig_dir, copy_dir)
    copy_new_logo(copy_dir)
    for root, dirs, files in os.walk(copy_dir):
        if len(files):
            for name in files:
                f = os.path.join(root, name)
                if is_webpage(f):
                    print 'Processing: ', f
                    process_file(f)
                remove_illegal_chars_from_filename(f)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print 'Not enough parameters.\n\nUsage: archive_optimize.py <content_dir> <output_dir>'
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])
