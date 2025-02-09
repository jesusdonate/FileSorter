from enum import Enum
from pathlib import Path
import json
from typing import Optional
import re


class DirectoryNotFound(Exception):
    pass


class MappingError(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class TokenType(Enum):
    EXT = 1
    COMMA = 2
    INTO = 3
    FOLDER_NAME = 4
    ERROR = 5


class Token:
    def __init__(self, token_type, literal):
        self.type: TokenType = token_type
        self.literal: str = literal

    def __str__(self):
        return f"Type: {self.type}, Literal: {self.literal}"


class Lexer:
    def __init__(self, line):
        self.line: str = line  # The input is usually the whole source code file
        self.pos: int = 0  # current position in input (points to current char)
        self.next_pos: int = 0  # current reading position in input (after current char)
        self.char: str = ''  # current char under examination
        self.tokenized_line = []  # Store the tokens in the order of their appearance
        self.read_char()  # initializes the position, readPosition, ch properties

    '''
    Token lines are lists of tokens from one specific line in the file.
    '''
    def get_tokenized_line(self) -> list[Token]:
        while self.char != '':
            token = self.next_token()
            if token:
                self.tokenized_line.append(token)
        return self.tokenized_line

    def next_token(self) -> Optional[Token]:
        self.skip_whitespace()

        # Checks if there are not more tokens to read
        if self.char == '':
            return None

        # Checks if next token is a file extension (EXT type)
        elif self.char == '.':
            self.read_char()
            if self.char.isalpha():
                name: str = self.read_ext_name()
                token = Token(TokenType.EXT, '.' + name)
            else:
                token = Token(TokenType.ERROR, 'There is not file extension name after a period.')

        # Checks if next token is a COMMA type
        elif self.char == ',':
            token = Token(TokenType.COMMA, ',')

        # Checks if next token is an INTO type
        elif self.char == '-':
            self.read_char()
            if self.char == '>':
                token = Token(TokenType.INTO, '->')
            else:
                token = Token(TokenType.ERROR, 'Missing > after the hyphen (-)')

        # Checks if next token is FOLDER_NAME type
        elif self.char.isalpha():
            name: str = self.read_folder_name()
            token = Token(TokenType.FOLDER_NAME, name)

        # The char is not allowed in the file
        else:
            token = Token(TokenType.ERROR, "There are characters that are not allowed inside the file.")
        self.read_char()
        return token

    # Reads the next char in the line
    def read_char(self) -> None:
        if self.next_pos >= len(self.line):
            self.char = ''
        else:
            self.char = self.line[self.next_pos]
        self.pos = self.next_pos
        self.next_pos += 1

    # Reverts to the previous char in line
    def unread_char(self) -> None:
        self.next_pos = self.pos
        self.pos -= 1
        if self.pos >= 0:
            self.char = self.line[self.pos]

    # Moves pos and char to the next non-whitespace character in line
    def skip_whitespace(self) -> None:
        while self.char == ' ' or self.char == '\t':
            self.read_char()

    # Reads name of the extension
    def read_folder_name(self) -> str:
        start = self.pos
        valid_chars = r'[a-zA-Z0-9 _-]'
        while bool(re.match(valid_chars, self.char)):
            self.read_char()
        self.unread_char()
        return self.line[start:self.next_pos]

    # Reads name of the folder
    def read_ext_name(self) -> str:
        start = self.pos
        valid_chars = r'[a-zA-Z.0-9]'
        while bool(re.match(valid_chars, self.char)):
            self.read_char()
        self.unread_char()
        return self.line[start:self.next_pos]


def is_valid_path(path: str) -> bool:
    return Path(path).is_dir()


def find_mapping_errors(tok_line: list[Token]) -> Optional[str]:
    """
    Checks if the file is correctly formatted. If not, it will return a error message. Else, return None
    Token lines can only have the following structure:
    EXT INTO FOLDER_NAME
    EXT [COMMA EXT ...can_repeat] INTO FOLDER_NAME

    We can create a Context Free Grammar to get desired structure.
    Let EXT = E, COMMA = C, INTO = I, FOLDER_NAME = f, where E,C,I are variables and f is a terminal.
    E -> C|I
    C -> E
    I -> f
    Input: tok_line - Tokenized line from file (got line from get_tokenized_line() from Lexer class)
    Returns: String of error message, or None if no errors found
    """
    for i, tok in enumerate(tok_line):
        if tok.type == TokenType.ERROR:
            return tok.literal

        # EXT is always the first TokenType in a line.
        if i == 0 and tok.type != TokenType.EXT:
            return 'A file extension must be the first entry in each line.'

        elif i == len(tok_line) - 1:
            # FOLDER_NAME must be the last element, or there will be an error.
            if tok.type == TokenType.FOLDER_NAME:
                return None
            else:
                return 'The custom folder name must be the last element in each line.'

        # We can confidently get the next token because current index is not the last index.
        next_tok: Token = tok_line[i + 1]

        # COMMA and INTO can only come after EXT. Anything else, return error.
        if tok.type == TokenType.EXT and next_tok.type not in {TokenType.COMMA, TokenType.INTO}:
            return 'A comma or a pointer (->) must come after a file extension type. A comma separates multiple ' \
                   'extensions being assigned to one folder name and the pointer (->) assigns the extension(s) into ' \
                   'a folder name.'

        # EXT comes after COMMA. Anything else, return error.
        elif tok.type == TokenType.COMMA and next_tok.type != TokenType.EXT:
            return f'A file extension type must come after a comma. Got {next_tok.literal} instead.'

        # FOLDER_NAME comes after INTO. Anything else, return error.
        elif tok.type == TokenType.INTO and next_tok.type != TokenType.FOLDER_NAME:
            return 'The pointer (->) must point to the custom folder name you want to store your file extension in.'

        # FOLDER_NAME is not the last element in tok_line, so return error
        elif tok.type == TokenType.FOLDER_NAME:
            return 'The custom folder name must be the last element in each line.'


# Returns a list of all extensions inside the tok_line
def get_extensions(tok_line: list[Token]) -> list[str]:
    exts = []
    for tok in tok_line:
        if tok.type == TokenType.EXT:
            exts.append(tok.literal)
    return exts


# Returns the folder name of the tok_line
def get_folder_name(tok_line: list[Token]) -> str:
    return tok_line[-1].literal  # FOLDER_NAME will always be the last token in tok_line


def create_mapping(tok_lines: list[list[Token]]) -> dict[str:list[str]]:
    mapping: dict[str:list[str]] = {}
    for tok_line in tok_lines:
        extensions = get_extensions(tok_line)
        folder_name = get_folder_name(tok_line)
        if folder_name not in mapping:
            mapping[folder_name] = []
        mapping[folder_name].extend(extensions)
    return mapping


class FileParser:
    """
    Extracts information from the input file.
    The file must contain a destination directory, and below the directory should be lines, where the file extension
    and the folder name are provided. The output is a JSON, just because I wanted to practice it.

    Example of File.txt:
    | --------------------- |
    | directory path        |
    | --------------------- |
    | .txt -> Texts         |
    | .png, .jpg -> Photos  |
    | .py -> Coding Files   |
    | .java -> Coding Files |
    |         ...           |

    Example of JSON output:
    {
        "directory": "/some/path/",
        "mappings": {
            "Texts": [".txt"],
            "Photos": [".png", ".jpeg"]
            "Coding Files": [".py", ".java"]
            More mappings...
        }
    }

    """

    def __init__(self, file_path: str = None):
        self.file_path: str = file_path
        self.mappings = {}

    def set_file_path(self, file_path):
        self.file_path = file_path

    def parse(self) -> json:
        file_path = self.file_path
        try:
            with open(file_path, "r") as file:
                lines = [line.strip() for line in file if line.strip()]

                # Checks first line for valid directory path
                dir_path = lines[0]
                if not is_valid_path(dir_path):
                    raise DirectoryNotFound
                self.mappings["directory"] = dir_path

                # Reads all lines in file and each line will be tokenized and stored in the tok_lines list
                tok_lines = []
                for line in lines[1:]:
                    tok_line: list[Token] = Lexer(line).get_tokenized_line()

                    # Prints all the token in the line
                    # for token in tok_line:
                    #     print(token, end="\n\n")

                    # Checks if there are any syntax errors in file. If so, raises Exception with a custom error message
                    map_err_msg = find_mapping_errors(tok_line)
                    if map_err_msg:
                        raise MappingError(map_err_msg)

                    tok_lines.append(tok_line)

                self.mappings['mappings'] = create_mapping(tok_lines)

                return json.dumps(self.mappings, indent=4)  # Returns json string. Using json just for practice

        except FileNotFoundError:
            print("File path was not found. Set file path using set_file_path(str) or when initializing FileParser "
                  "object.")

        except DirectoryNotFound:
            print("Directory path was not found. Directory path is not valid or path is not on the first line "
                  "of the text file.")

        except MappingError as e:
            print("Error in file:", e)
