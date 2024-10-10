#!/bin/bash
clear
for pyfile in $(find -D tree . | grep -v __pycache__ | grep -v mako | grep -v test | grep py); do
    echo ""
    echo ""
    echo "file path: $pyfile"
    cat $pyfile
    echo ""
    echo "======"
done
