from natsort import natsorted
import os


class Folder:
    folder_names = ["docs1"]

    def __init__(self):
        pass

    def numberOfDocs(self, folder_names):
        noOfDocs = 0
        for folder_name in folder_names:
            noOfDocs += len(natsorted(os.listdir(folder_name)))
        return noOfDocs

    def fileNames(self, folder_names):
        file_names = []
        for folder_name in folder_names:
            file_name = natsorted(os.listdir(folder_name))
            file_names.append(file_name)

        return [item for sublist in file_names for item in sublist]

    def read_file(self, filename):
        with open(filename, 'r', encoding="ascii", errors="surrogateescape") as f:
            stuff = f.read()
        f.close()
        return stuff

    def getDocs(self):
        docs = []
        for folder_name in self.folder_names:
            # # Open files.
            file_names = natsorted(os.listdir(folder_name))
            # For every file.
            for file_name in file_names:
                # Read file contents.
                stuff = self.read_file(folder_name + '/' + file_name)
                docs.append(stuff)
        return docs
