#!/bin/sh

find ./urls -type f -exec ls -1 {} \; 2> /dev/null > generated_content/tess_urls_file
cat generated_content/tess_urls_file | xargs -i cat {} > generated_content/tess_oer_urls.txt
wget -N --no-remove-listing --adjust-extension --page-requisites --convert-links -np --user-agent=Mozilla -i tess_oer_urls.txt -P generated_content
