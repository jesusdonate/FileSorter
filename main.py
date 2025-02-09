"""

This is a file sorter

"""

import argparse
from file_parser import FileParser
from explorer import Explorer
import json


def main():
    parser = argparse.ArgumentParser()
    # python main.py --FILE_INPUT "C:/Users/..." --PATH "C:/Users/..." --STATS --CREATE_FOLDERS
    parser.add_argument("--FILE", type=str, help="Takes in path of the .txt file that will be read.")
    parser.add_argument("--PATH", type=str, help="Provide path to the director/folder you want to sort/analysis.")
    parser.add_argument("--STATS", action="store_true", help="Returns information on folder such as Folder name, Date "
                                                             "created, Total size, Number of files inside...")
    parser.add_argument("--SORT", action="store_true", help="Creates folders for all extensions. Can specific which "
                                                            "extensions to move by providing a .txt file using --FILE "
                                                            "command.")

    args = parser.parse_args()

    if not args.FILE and not args.PATH:
        print("Hello :)\n"
              "You must use either --FILE or --PATH argument to make this script work as intended.")
        return

    if args.FILE:
        file_parser = FileParser(args.FILE)
        json_string = file_parser.parse()
        if not json_string:
            return
        mappings = json.loads(json_string)
        explorer = Explorer(mappings=mappings)
    else:
        try:
            explorer = Explorer(dir_path=args.PATH)
        except FileNotFoundError as e:
            print(e)
            return

    if args.STATS:
        explorer.stats()

    if args.SORT:
        explorer.sort_extensions()


if __name__ == '__main__':
    main()