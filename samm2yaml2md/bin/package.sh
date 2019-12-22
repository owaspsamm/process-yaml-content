#!/bin/bash

# samm2-yaml2pdf release base dir
rb=./samm2yaml2pdf/

# source base dir
sb=.

rm -rf $rb/
mkdir -p $rb/{bin,pdf,web}

cp $sb/bin/cleanup_env_for_make_pdf.sh $rb/bin/
cp $sb/bin/cleanup_env_for_make_web.sh $rb/bin/
cp $sb/bin/collate_pdf_pages.sh $rb/bin/
cp $sb/bin/copy_static_files.sh $rb/bin/
cp $sb/bin/customize_file_ordering.sh $rb/bin/
cp $sb/bin/fixup_web_markdown.sh $rb/bin/
cp $sb/bin/make_markdown.py $rb/bin/
cp $sb/bin/make_namespaces.py $rb/bin/
cp $sb/bin/make_pdf_with_toc.sh $rb/bin/
cp $sb/bin/map_ns2template.sh $rb/bin/
cp $sb/bin/map_web_ns2template.sh $rb/bin/
cp $sb/bin/package.sh $rb/bin/

cp $sb/Makefile $rb/
cp $sb/make.env $rb/
cp $sb/create_make_markdown_script.sh $rb/
cp $sb/create_make_web_markdown_script.sh $rb/

cp $sb/make_pdf.sh $rb/
cp $sb/make_web.sh $rb/

#cp -r $sb/Datafiles $rb/
#cp -r $sb/pdf/css $rb/pdf/
cp -r $sb/pdf/static.content $rb/pdf/
cp -r $sb/pdf/static.markdown $rb/pdf/
cp -r $sb/pdf/static.templates $rb/pdf/
#cp -r $sb/pdf/static.working $rb/pdf/
cp -r $sb/samm-icons $rb/

cp -r $sb/web/static.templates $rb/web/

cp $sb/README $rb/

tar czf samm2yaml2pdf.tgz $rb/

echo bundled all the code into samm2yamml2pdf.tgz
