from SearchEngine import SearchEngine
import os

from natsort import natsorted
from config import Folder
import numpy as np


def checkTermInObject(term, obj, docId, calcNo):
    if term in obj:
        obj[term][0][docId + 1] = calcNo
    else:
        obj[term] = []
        obj[term].append({})
        obj[term][0][docId + 1] = calcNo


class TF_IDF:
    se = SearchEngine()
    folder = Folder()
    docs = []
    docID = 1
    pos_index = se.pos_index

    # Number of Docs => self.folder.numberOfDocs(self.folder.folder_names)
    def getDocs(self):
        for folder_name in self.folder.folder_names:
            # # Open files.
            file_names = natsorted(os.listdir(folder_name))
            # For every file.
            for file_name in file_names:
                # Read file contents.
                stuff = self.se.read_file(folder_name + '/' + file_name)
                final_token_list = self.se.preprocessing(stuff)
                self.docs.append(final_token_list)
        return self.docs

    def computeTF(self):
        docs = self.getDocs()
        tf = {}
        docSize = []
        for i in range(len(docs)):
            docSize.append(len(docs[i]))

        for term in self.pos_index:
            for docId in range(self.folder.numberOfDocs(self.folder.folder_names)):

                if self.pos_index[term][1].get(docId + 1) is not None:
                    # term frequency TF => len(self.pos_index[term][1].get(docId + 1))
                    tfNo = len(self.pos_index[term][1].get(docId + 1)) / docSize[docId]
                    checkTermInObject(term, tf, docId, tfNo)

                else:
                    checkTermInObject(term, tf, docId, 0)
        return tf

    def computeIDF(self):
        idf = {}
        for term in self.pos_index:
            if self.pos_index[term][1] is not None:
                # DF for a term = self.pos_index[term][0]
                n = np.log10(self.folder.numberOfDocs(self.folder.folder_names) / self.pos_index[term][0])
                idf[term] = n

        return idf

    def computeTFIDF(self, tf, idf):
        tfIdf = {}
        for term in tf:
            for docId in range(self.folder.numberOfDocs(self.folder.folder_names)):
                tfIdfNo = tf[term][0].get(docId + 1) * idf[term]
                checkTermInObject(term, tfIdf, docId, tfIdfNo)

        return tfIdf
