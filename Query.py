from SearchEngine import SearchEngine
import numpy as np
import pandas as pd
from config import Folder
from sklearn.feature_extraction.text import CountVectorizer



def column(matrix, i):
    return [row[i] for row in matrix]


class Query:
    document_class = SearchEngine()
    pos_intersection = {}
    # Key_ID = 0
    # store_exist_terms = {}
    termQueryFreq = {}
    folder = Folder()

    def __init__(self):
        pass

    def Dict_KeyID_similar_terms(self, query):
        tokens = self.document_class.preprocessing(query)
        store_exist_terms = {}
        Key_ID = 0
        for term in tokens:
            if term in self.document_class.pos_index:
                if term not in store_exist_terms:
                    store_exist_terms[Key_ID] = []
                    store_exist_terms[Key_ID].append(term)
                    store_exist_terms[Key_ID].append(self.document_class.pos_index[term])
                    Key_ID += 1

        return store_exist_terms

    def position_intersect(self, store1, store2, doc_ids_list):
        for doc_id in doc_ids_list:
            i = 0
            j = 0
            pos_list1 = store1[doc_id]
            pos_list2 = store2[doc_id]
            while i < len(pos_list1) and j < len(pos_list2):
                if (pos_list2[j] - pos_list1[i]) == 1:
                    self.pos_intersection[doc_id] = []
                    self.pos_intersection[doc_id].append(pos_list2[j])
                    i += 1
                    j += 1
                else:
                    if pos_list1[i] < pos_list2[j]:
                        i += 1
                    else:
                        j += 1

        return self.pos_intersection

    def intersect_docs(self, store1, store2):
        intersection_docs_list = list(store1.keys() & store2.keys())
        final_result = self.position_intersect(store1, store2, intersection_docs_list)
        return final_result

    def Matching_Query(self, query):
        j = -1
        result = []
        store_terms = self.Dict_KeyID_similar_terms(query)
        try:
            if len(store_terms) == 1:
                return store_terms[0]
            else:
                for i in range(len(store_terms)):
                    if i == 0:
                        store1 = store_terms[i][1][1]
                        store2 = store_terms[i + 1][1][1]
                        result.append(self.intersect_docs(store1, store2))
                        j += 1
                    elif i == 1:
                        continue
                    else:
                        store1 = result[j]
                        store2 = store_terms[i][1][1]
                        result.append(self.intersect_docs(store1, store2))
                        j += 1
                    # print(result)
            return result[j - 1]
        except:
            return "Not Found"

    def duplicate_terms_in_query(self, q):
        query = self.document_class.preprocessing(q)
        for term in query:
            if term in self.termQueryFreq:
                self.termQueryFreq[term] += 1
            else:
                self.termQueryFreq[term] = 1

        return self.termQueryFreq

    def cosine_similarity(self, query):
        docs = self.folder.getDocs()

        query = self.document_class.preprocessing(query)
        print(query)
        df, s = self.document_class.countWordsInEachDoc()
        docs_without_query = np.squeeze(np.asarray(s))
        row, col = docs_without_query.shape
        docs_with_query = np.zeros((row, col + 1))
        docs_with_query[:, :-1] = docs_without_query

        count_vectorizer = CountVectorizer()
        count_vectorizer.fit_transform(docs)
        for i in range(len(query)):
            for j in range(len(df)):
                if query[i] == df.index[j]:
                    docs_with_query[j][col] += 1

        cols = self.folder.fileNames(self.folder.folder_names)
        cols.append("query")

        dfb = pd.DataFrame(docs_with_query, columns=cols, index=self.document_class.preprocessing(count_vectorizer.get_feature_names()))

        print(dfb)

        docs_with_query = docs_with_query.astype(int)
        return self.cos_docs_query(docs_without_query, column(docs_with_query, col))

    def cos_docs_query(self, documents, query):
        row, col = documents.shape
        cosine_similarity = {}

        file_names = self.folder.fileNames(self.folder.folder_names)
        for i in range(col):
            dot_product = np.dot(column(documents, i), query)
            rmsD = sum(x ** 2 for x in column(documents, i)) ** 0.5
            rmsQ = sum(x ** 2 for x in query) ** 0.5
            result = dot_product / (rmsD * rmsQ)
            cosine_similarity[file_names[i]] = round(result, 4)
        return cosine_similarity

    def rank_documents_based_on_cosine_similarity(self, cosine_similarity):
        return sorted(cosine_similarity.items(), key=lambda x: x[1], reverse=True)
