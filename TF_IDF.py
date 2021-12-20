from SearchEngine import SearchEngine
import os

from natsort import natsorted
from config import Folder
import numpy as np

import pandas as pd

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)


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

    def compute_weight_TF(self):
        docs = self.getDocs()
        tf = {}
        docSize = []
        for i in range(len(docs)):
            docSize.append(len(docs[i]))

        for term in self.pos_index:
            for docId in range(self.folder.numberOfDocs(self.folder.folder_names)):

                if self.pos_index[term][1].get(docId + 1) is not None:
                    # term frequency TF => len(self.pos_index[term][1].get(docId + 1))
                    tfNo = 1 + np.log10(len(self.pos_index[term][1].get(docId + 1)))
                    # print(docSize[docId])
                    checkTermInObject(term, tf, docId, round(tfNo, 5))

                else:
                    checkTermInObject(term, tf, docId, 0)
        return tf

    def computeIDF(self):
        idf = {}
        for term in self.pos_index:
            if self.pos_index[term][1] is not None:
                # DF for a term = self.pos_index[term][0]
                n = np.log10(self.folder.numberOfDocs(self.folder.folder_names) / self.computeDF(term))
                idf[term] = round(n, 5)

        return idf

    def computeDF(self, term):
        return self.pos_index[term][0]

    def computeTFIDF_weight(self, tf, idf):
        tfIdf = {}
        for term in tf:
            for docId in range(self.folder.numberOfDocs(self.folder.folder_names)):
                tfIdfNo = tf[term][0].get(docId + 1) * idf[term]
                checkTermInObject(term, tfIdf, docId, round(tfIdfNo, 5))

        return tfIdf

    def normalized_tfidf(self, tf_idf, document_length):
        normalized_tf_idf = {}
        docs_length = list(document_length.values())
        for i in range(len(docs_length)):
            for term in tf_idf:
                n_tfidf = tf_idf[term][0].get(i + 1) / docs_length[i]
                checkTermInObject(term, normalized_tf_idf, i, round(n_tfidf, 5))

        return normalized_tf_idf

    def tf_format(self, tf):
        terms_list = list(tf.keys())
        tfNo = []
        for term in terms_list:
            tfNo.append(list(tf[term][0].values()))

        df = pd.DataFrame(tfNo, columns=self.folder.fileNames(self.folder.folder_names), index=terms_list)
        print(df)

    def idf_format(self, idf):
        terms_list = list(idf.keys())
        tfNo = []
        dfTerms = []
        for term in terms_list:
            tfNo.append(idf[term])
            dfTerms.append(self.computeDF(term))

        data = {'Term ': terms_list, ' df ': dfTerms, ' IDF ': tfNo}
        df = pd.DataFrame(data, columns=['Term ', ' df ', ' IDF '])
        print(df)

    def tf_idf_format(self, tfIDF):
        terms_list = list(tfIDF.keys())
        tf_idf = []
        for term in terms_list:
            tf_idf.append(list(tfIDF[term][0].values()))

        df = pd.DataFrame(tf_idf, columns=self.folder.fileNames(self.folder.folder_names), index=terms_list)
        print(df)

    def normalized_tf_idf_format(self, normalized_tfidf):
        terms_list = list(normalized_tfidf.keys())
        n_tf_idf = []
        for term in terms_list:
            n_tf_idf.append((list(normalized_tfidf[term][0].values())))
        print(n_tf_idf)

        df = pd.DataFrame(n_tf_idf, columns=self.folder.fileNames(self.folder.folder_names), index=terms_list)
        print(df)
