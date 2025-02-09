"""

This is a file sorter

"""

import argparse
from file_parser import FileParser
import json


def main():
    parser = argparse.ArgumentParser()
    # python main.py --FILE_INPUT "C:/Users/..." --PATH "C:/Users/..." --STATS --CREATE_FOLDERS
    parser.add_argument("--FILE_INPUT", type=str, help="Takes in path of the .txt file that will be read.")
    parser.add_argument("--PATH", type=str, help="Provide path to the director/folder you want to sort/analysis.")
    parser.add_argument("--STATS", action="store_true", help="Returns information on folder such as Folder name, Date created, Total size, Number of files inside...")
    parser.add_argument("--CREATE_FOLDERS", type=list[str], help="Creates folders for specific extension. Creates folders for all extensions if not specified.")

    args = parser.parse_args()

    file_path = args.FILE_INPUT
    file = None
    dir_path = args.PATH

    if not file_path and not dir_path:
        print("Hello :)\n"
              "You must use either --FILE_INPUT or --PATH argument to make this script work as intended.")
        return

    if file_path:
        dir_path = None
        file_parser = FileParser(file_path)
        json_string = file_parser.parse()
        if not json_string:
            return
        mapping = json.loads(json_string)
        print("Parsed mapping:", mapping)


    if dir_path:
        pass


if __name__ == '__main__':
    main()