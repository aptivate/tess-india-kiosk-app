#!/bin/sh
if [ ! -d "SiteArchive/generated_content" ]; then
   mkdir SiteArchive/generated_content
fi

find SiteArchive/urls -type f -exec ls -1 {} \; 2> /dev/null > SiteArchive/generated_content/tess_urls_file
cat SiteArchive/generated_content/tess_urls_file | xargs -i cat {} > SiteArchive/generated_content/tess_oer_urls.txt
wget -N --no-remove-listing --adjust-extension --page-requisites --convert-links -np --user-agent=Mozilla -i SiteArchive/generated_content/tess_oer_urls.txt -P SiteArchive/generated_content
