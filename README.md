# File Sorter

## Description
This Python script is a **File Sorter** that organizes files in a given directory by their extensions. It categorizes files into folders based on predefined mappings and can also provide statistics on the directory, such as:
- Folder name
- Date last modified
- Total directory size
- Number of files
- Number of subdirectories
- Largest file in the directory

The script can be executed via **command-line arguments**.


⚠ **Warning: Sorting files can potentially disorganize your directory structure. Ensure you have backups or verify paths before running the script.**

---

## Features 📃
- Reads a directory and retrieves files and subdirectories.
- Moves files into categorized folders based on their extensions.
- Supports custom mappings via a `.txt` file.
- Provides statistics on the directory.
- Uses efficient data structures for optimal performance.

---

## Installation & Requirements 🛠️
**Python Version:** Ensure you have **Python 3.6+** installed.

The script uses built-in Python modules, so no additional dependencies are required.

---

## Usage 
You can run this script from the command line using different options.

### **Basic Command Structure:**
```sh
python main.py --PATH "<directory_path>" --STATS --SORT
```

### **Command-Line Arguments:**
| Argument | Description |
|----------|-------------|
| `--FILE "<file_path>.txt"` | Reads a `.txt` file to customize sorting rules. |
| `--PATH "<directory_path>"` | Specifies the directory to analyze or sort. |
| `--STATS` | Displays statistics of the directory. |
| `--SORT` | Sorts files into categorized folders based on extensions. ⚠ Use with caution.|

---

## Example Usage
### **1️⃣ Get Statistics of a Folder:**
```sh
python main.py --PATH "C:/Users/Documents" --STATS
```
**Output:**
```
Directory Name:              Documents
Time last modified:          Fri Jan 24 22:20:10 2025
Size of directory:           73.6KB
Number of files:             15
Number of sub-directories:   5
Largest file:                report.pdf (5.2MB)
```

### **2️⃣ Sort Files into Categorized Folders:**
```sh
python main.py --PATH "C:/Users/Documents" --SORT
```
**Result:**
```
All files will be moved to their respective folders based on their extensions.
Example:
- `.txt` files → "Texts/"
- `.jpg`, `.png` → "Photos/"
- `.mp3`, `.wav` → "Music/"
```
⚠ Warning: This action will move files and may affect the organization of your directory. Double-check before running
### **3️⃣ Use a Custom Mapping from a `.txt` File:**
```sh
python main.py --FILE "C:/Users/Documents/mapping.txt"
```
This allows **custom file-to-folder mapping**, specified in a `.txt` file.
### **📌 `.txt` File Format**
- The first line must contain the **destination directory** where files will be sorted.
- Each subsequent line maps **file extensions** to **folder names**.
- Use `->` to assign extensions to a folder.
- Separate multiple extensions with a comma `,`.

**Example `mapping.txt`:**
```
C:/Users/Documents/Sorted_Files  # Destination directory (First line)
.txt -> Texts
.png, .jpg -> Photos
.py -> Coding Files
.java -> Coding Files
```
This ensures:
- `.txt` files go into `Texts/`
- `.png` and `.jpg` files go into `Photos/`
- `.py` and `.java` files go into `Coding Files/`

---


## Customization
You can modify the default extension-to-folder **mapping** in `explorer.py` under:
```python
MAPPINGS = {
    "Texts": [".txt", ".md", ".pdf"],
    "Photos": [".png", ".jpeg", ".jpg"],
    "Videos": [".mp4", ".mkv"],
    "Music": [".mp3", ".wav"]
}
```
To add more categories, simply append new extensions to the dictionary.

---

## Error Handling
- If the provided **directory does not exist**, an error will be displayed.
- If the **file mappings format is incorrect**, an error will be raised.
- If no `--PATH` or `--FILE` argument is provided, the script will prompt the user.

---

### What I Learned
* How to manipulate file paths with pathlib.
* How to move files using shutil.move().
* How to parse and validate structured data from a text file using a Parser, Lexer, and Token classes and using context-free grammar (CFG) concepts.
* How to implement a priority queue (heap) to find the largest files in a directory.
* The importance of using types throughout my code.
* How to use the Enum class.
* How to convert dictionaries to JSON and vice versa.
