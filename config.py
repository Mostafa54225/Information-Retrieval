from natsort import natsorted
import os


class Folder:
    folder_names = ["Documents", "docs2"]

    def __init__(self):
        pass

    def numberOfDocs(self, folder_names):
        noOfDocs = 0
        for folder_name in folder_names:
            noOfDocs += len(natsorted(os.listdir(folder_name)))
        return noOfDocs
