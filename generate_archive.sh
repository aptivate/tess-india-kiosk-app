#!/bin/bash

# get the directory the script is in
# from http://stackoverflow.com/a/246128/3189
SCRIPT_DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

GENERATED_DIR=$SCRIPT_DIR/SiteArchive/generated_content
TESS_URLS_FILE=$GENERATED_DIR/tess_urls_file
TESS_OER_URLS=$GENERATED_DIR/tess_oer_urls.txt

ARCHIVE_URLS=$SCRIPT_DIR/SiteArchive/generated_content/urls

if [ ! -d "$GENERATED_DIR" ]; then
   mkdir $GENERATED_DIR
fi

$SCRIPT_DIR/extract_urls/extract_urls.py

# using the argument "small" means that only one web page will be downloaded (plus it's videos, CSS etc)
if [ $# -eq 1 ] && [ $1 = 'small' ]; then
    cp $ARCHIVE_URLS/tess_india_video_resources/planning_lessons_urls $TESS_OER_URLS
else
    find $ARCHIVE_URLS -type f -exec ls -1 {} \; 2> /dev/null > $TESS_URLS_FILE
    cat $TESS_URLS_FILE | xargs -i cat {} > $TESS_OER_URLS
fi

wget --timestamping \
    --no-remove-listing \
    --adjust-extension \
    --page-requisites \
    --convert-links \
    --no-parent \
    --user-agent=Mozilla \
    --input-file=$TESS_OER_URLS \
    --directory-prefix=$GENERATED_DIR
