"""

Sets up the logic for getting all files in directory and moving files to new folders.
Stores list of files and subdirectories.
We can also get some stats from the directory. For example:
    Gets Folder name, Date last modification, Total directory size, Number of files inside, Number of subdirectories,
    and nth largest files in folder.

"""
from pathlib import Path
import shutil
import time
import heapq

MAPPINGS = {
    "Texts": [".txt", ".md", ".rtf", ".doc", ".docx", ".pdf"],
    "Photos": [".png", ".jpeg", ".jpg", ".gif", ".bmp", ".svg", ".tiff", ".webp"],
    "Videos": [".mp4", ".mkv", ".avi", ".mov", ".flv", ".wmv"],
    "Music": [".mp3", ".wav", ".aac", ".flac", ".ogg"],
    "Compressed": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Coding Files": [".py", ".java", ".cpp", ".c", ".cs", ".js", ".html", ".css", ".sh", ".rb", ".php", ".swift",
                     ".go"],
    "Spreadsheets": [".xls", ".xlsx", ".csv", ".ods"],
    "Presentations": [".ppt", ".pptx", ".odp"]
}


def format_byte_size(bytes: int) -> str:
    size_suffix = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
    suffix_index = 0
    while bytes >= 1000 and suffix_index < len(size_suffix):
        bytes = bytes / 1024
        suffix_index += 1
    return f'{bytes:.1f}{size_suffix[suffix_index]}'


def move_file_to_folder(file: Path, folder: Path):
    shutil.move(str(file), str(folder / file.name))


class Explorer:
    """
    The Explorer class is responsible for analyzing and organizing files within a directory.

    Features:
    - Retrieves files and subdirectories in a directory.
    - Moves files into categorized folders based on extensions.
    - Computes directory stats: name, size, last modified time, file count, and largest files.

    Attributes:
    - dir_path (Path): Target directory.
    - mappings (dict): File extension to folder mapping.
    - subdir (list[Path]): Subdirectories in the directory.
    - files (list[Path]): Files in the directory.
    - largest_files (list[Path]): Top N largest files.
    """

    def __init__(self, dir_path='', mappings=None):
        if mappings:
            self.dir_path = Path(mappings['directory'])
            self.mappings: dict[str: list[str]] = mappings['mappings']
        else:
            self.dir_path = Path(dir_path)
            self.mappings = MAPPINGS
        self.subdir = self.get_subdirs()
        self.files_ext = self.get_files()  # Files at top-level of directory
        self.largest_files = self.get_largest_n_files()

    def create_folder(self, folder_name: str) -> Path:
        destination_folder = self.dir_path / folder_name
        destination_folder.mkdir(exist_ok=True)
        return destination_folder

    def sort_extensions(self):
        """Sorts and moves files into folders based on extensions."""
        ext_to_folder = {ext: folder for folder, extensions in self.mappings.items() for ext in extensions}

        for file, ext in self.files_ext:
            if ext in ext_to_folder:
                folder_name = ext_to_folder[ext]
                folder_path = self.create_folder(folder_name)
                move_file_to_folder(file, folder_path)

    def get_num_size_files(self) -> tuple[int, int]:
        """ Returns number_of_files and size_of_directory """
        num = 0
        size = 0
        for f in self.dir_path.glob('*'):
            if f.is_file():
                num += 1
                size += f.stat().st_size
        return num, size

    def get_subdirs(self) -> list[Path]:
        """Returns list of subdirectories within directory. They are of type Path"""
        return [d for d in self.dir_path.iterdir() if d.is_dir()]

    def get_files(self) -> list[tuple[Path, str]]:
        """Returns a list of files within directory. They are of type Path"""
        return [(f, f.suffix) for f in self.dir_path.iterdir() if f.is_file()]

    def get_largest_n_files(self, n=1) -> list[Path]:
        """
        Input: number of nth largest files to return.
        Return: List of Path files.
        """
        # Negating size because I want a max-heap based on size
        heap = [(-file.stat().st_size, file) for file, _ in self.files_ext]
        heapq.heapify(heap)
        largest_files = []
        for i in range(n):
            _, file = heapq.heappop(heap)
            largest_files.append(file)
        return largest_files

    def stats(self):
        """
        Prints all the Stats of the directory
        :return:
        """
        dir_name = self.dir_path.name
        mod_time = self.dir_path.stat().st_ctime
        num_of_files, size = self.get_num_size_files()

        print(f"{'Directory Name:'.ljust(30)} {dir_name}")
        print(f"{'Time last modified:'.ljust(30)} {time.ctime(mod_time)}")
        print(f"{'Size of directory:'.ljust(30)} {format_byte_size(size)}")
        print(f"{'Number of files:'.ljust(30)} {num_of_files}")
        print(f"{'Number of sub-directories:'.ljust(30)} {sum(1 for sd in self.subdir)}")
        print(
            f"{'Largest file:'.ljust(30)} {self.largest_files[0].name} ({format_byte_size(self.largest_files[0].stat().st_size)})")
