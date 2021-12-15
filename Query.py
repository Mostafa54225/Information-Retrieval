from SearchEngine import SearchEngine


class Query:
    document_class = SearchEngine()
    pos_intersection = {}
    Key_ID = 0
    store_exist_terms = {}
    termQueryFreq = {}

    def __init__(self):
        pass

    def Dict_KeyID_similar_terms(self, query):
        tokens = self.document_class.preprocessing(query)
        for term in tokens:
            if term in self.document_class.pos_index:
                if term not in self.store_exist_terms:
                    self.store_exist_terms[self.Key_ID] = []
                    self.store_exist_terms[self.Key_ID].append(term)
                    self.store_exist_terms[self.Key_ID].append(self.document_class.pos_index[term])
                    self.Key_ID += 1

        return self.store_exist_terms

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

    def duplicate_terms_in_query(self, q):
        query = self.document_class.preprocessing(q)
        for term in query:
            if term in self.termQueryFreq:
                self.termQueryFreq[term] += 1
            else:
                self.termQueryFreq[term] = 1

        return self.termQueryFreq


