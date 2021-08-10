import fnmatch
import glob
from dataclasses import dataclass
import re
import json

LIST_WORD = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
             'v', 'w', 'h', 'y', 'z']

# Import Module
import os

# Folder Path
path = "C:\\Users\\Omer\\Documents\\bootKamp\\2021-archive"

# Change the directory
os.chdir(path)


# Read text File


@dataclass
class Description:
    name_file: str
    row_number: int
    offset: int

    def show(self):
        return "( " + str(self.offset) + " " + self.name_file + " )"


@dataclass
class VectorWord:
    num_char: int
    word: str
    DescriptionVector: Description


def findfiles(path, filter):
    for root, dirs, files in os.walk(path):
        for file in fnmatch.filter(files, filter):
            yield os.path.join(root, file)


@dataclass
class Table:
    _row: int
    _path: str
    _table_map: dict

    def do_table(self):
        try:
            for root, dirs, files in os.walk(self._path):
                for file in files:
                    if file.endswith(".txt"):
                        with open(os.path.join(root, file)) as file2:
                            line = file2.readline()
                            offset_in_txt = 0
                            while line:
                                line_without_tv = ''.join(e for e in line if e.isalnum())
                                for tv1 in LIST_WORD:
                                    for tv2 in LIST_WORD:
                                        key_word = tv1 + tv2
                                        for offset_in_line in range(len(line_without_tv)-1):
                                            word = str(line_without_tv[offset_in_line] + line_without_tv[offset_in_line + 1])
                                            if key_word == word.lower():
                                                if key_word not in self._table_map.keys():
                                                    self._table_map.update({key_word: [""]})
                                                self._table_map[key_word].append([offset_in_line, offset_in_line + offset_in_txt, file, line])
                                offset_in_txt += len(line)
                                line = file2.readline()
#= ''.join(e for e in prefix if e.isalnum())
                        file2.close()

        except Exception:
            pass

        with open("C:\\networks\\sample.json", "w") as outfile:
            json.dump(self._table_map, outfile)
        outfile.close()


Table(2, "C:\\Users\\Omer\\Documents\\bootKamp\\2021-archive", {}).do_table()