"""
Simple Zip archive.
Writes json/text files into zip file.
Reads files from zip file

Deleting files in the archive is not supported

Usage

z = ZipArchive("test.zip")

y = { ... }

if not z.contains("y.json"):
    z.add("y.json", y)

...

y = z.get("y.json")

"""

import zipfile
import json
import os

class ZipArchive(zipfile.ZipFile):

    def __init__(self, filepath, overwrite=False):
        self.filepath = filepath
        if not os.path.exists(filepath) or overwrite:
            super().__init__(filepath, "w", zipfile.ZIP_DEFLATED)
        else:
            super().__init__(filepath, "a", zipfile.ZIP_DEFLATED)

    def add(self, filepath, data):
        """
        Add data (str, data or list) to zip file.
        """

        if not self.contains(filepath):

            if isinstance(data, list) or isinstance(data, dict):
                data = json.dumps(data, indent=4)
            elif not isinstance(data, str):
                raise TypeError("Ziparchive only supports datatypes string, list and dict")
            self.writestr(filepath, data)
        else:
            print("file <{}> already in fetched".format(filepath))

    def get(self, filepath):
        """
        Reads (text-)file from zip file.
        """
        filepath = filepath.replace("\\", "/")
        data = self.read(filepath)
        if filepath.endswith(".json"):
            return json.loads(data.decode("utf-8"))
        else:
            return data.decode("utf-8")

    def contains(self, filepath):
        """
        Check if zip file contains file :filepath:
        """
        if filepath in self.namelist():
            return True
        else:
            return False

    def __iter__(self):
        for filename in self.namelist():
            yield filename

    def __getitem__(self, directory):
        for filename in self:
            if filename.startswith(directory+"/"):
                yield filename[len(directory)+1:]

    def __contains__(self, directory):
        for filename in self:
            if filename.startswith(directory+"/"):
                return True
        return False
