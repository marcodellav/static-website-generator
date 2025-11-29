import sys
from copy_source_to_dest import copy_source_to_dest
from generate_pages_recursive import generate_pages_recursive

def main():
    basepath = ""
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    else:
        basepath = "/"
    copy_source_to_dest("./static/", "./docs")
    generate_pages_recursive( "./content", "template.html", "./docs", basepath)

main()