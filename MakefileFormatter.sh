sed r's/ \+/\t/g' Makefile > temp &&
cp temp Makefile &&
rm temp
