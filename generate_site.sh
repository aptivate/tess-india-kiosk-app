#!/bin/bash

# get the directory the script is in
# from http://stackoverflow.com/a/246128/3189
SCRIPT_DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

MARKDOWN_DIR=$SCRIPT_DIR/WebSource/markdown
HTML_DIR=$SCRIPT_DIR/WebSource/html
OUT_DIR=$SCRIPT_DIR/WebContent

# convert markdown files
for mkdfile in $MARKDOWN_DIR/*.mkd ; do
    outfile=$HTML_DIR/$(basename ${mkdfile%.mkd}).html
    cat $MARKDOWN_DIR/head.html > $outfile
    markdown $mkdfile >> $outfile
    cat $MARKDOWN_DIR/foot.html >> $outfile
done

# remove old output
rm -rf $OUT_DIR
mkdir $OUT_DIR
# the empty file is for git
touch $OUT_DIR/empty

# put new content in there
cp -r $HTML_DIR/* $OUT_DIR
