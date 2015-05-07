#!/bin/bash

# get the directory the script is in
# from http://stackoverflow.com/a/246128/3189
SCRIPT_DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

MARKDOWN_DIR=$SCRIPT_DIR/WebSource/markdown
HTML_DIR=$SCRIPT_DIR/WebSource/html
OUT_DIR=$SCRIPT_DIR/WebContent
TESSCONTENT=tess
TESS_DIR=$OUT_DIR/$TESSCONTENT

# TODO: reintroduce but don't delete zip file if skipzip
# maybe wait until unite with fab script
# remove old output
#rm -rf $OUT_DIR
mkdir -p $OUT_DIR

# copy HTML, images, CSS etc
cp -r $HTML_DIR/* $OUT_DIR

# convert markdown files
for mkdfile in $MARKDOWN_DIR/*.mkd ; do
    outfile=$OUT_DIR/$(basename ${mkdfile%.mkd}).html
    cat $MARKDOWN_DIR/head.html > $outfile
    markdown $mkdfile >> $outfile
    cat $MARKDOWN_DIR/foot.html >> $outfile
done

# include the optimised mirror of the TESS archive
if [ -e $TESS_DIR ]; then rm $TESS_DIR; fi
ln -s $SCRIPT_DIR/SiteArchive/generated_content/optimized $TESS_DIR


skipzip="noskip"
if [ $# -eq 1 ] && [ $1 = 'skipzip' ]; then
    skipzip="skip"
fi

if [ $skipzip = "noskip" ]; then
    # create zip file (and dir)
    cd $OUT_DIR
    zip -r tess.zip $TESSCONTENT
fi
