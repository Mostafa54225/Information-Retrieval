import pprint
from SearchEngine import SearchEngine
from Query import Query
from TF_IDF import TF_IDF

searchEngine = SearchEngine()
searchQuery = Query()
tfIdf = TF_IDF()

pos = searchEngine.createPositionalIndex()
tf = tfIdf.compute_weight_TF()
idf = tfIdf.computeIDF()
tf_idf = tfIdf.computeTFIDF_weight(tf, idf)

while True:
    print("""
        1- Positional Index
        2- Word count of the words in each document
        3- Phrase Query
        4- Compute TF for each term in each document
        5- Compute IDF for each term
        6- Display TF.IDF  
        7- Compute Cosine Similarity between the query and documents
        8- Document Length
        9- Normalized TF.IDF
        0- Exit
        """)

    choice = int(input("Choose "))
    if choice == 1:
        print("Positional Index")
        searchEngine.df_format(pos)
    elif choice == 2:
        df, docs = searchEngine.countWordsInEachDoc()
        print(df)
    elif choice == 3:
        searchKey = input("Enter a word to search for it: ")
        result = searchQuery.Matching_Query(searchKey)
        pprint.pprint(result)
    elif choice == 4:
        print("Term Frequency")
        tfIdf.tf_format(tf)
    elif choice == 5:
        print("Inverse Document Frequency")
        tfIdf.idf_format(idf)
    elif choice == 6:
        print("Term Frequency - Inverse Document Frequency")
        tfIdf.tf_idf_format(tf_idf)
    elif choice == 7:
        query = input("Enter a query: ")
        cosine_similarity = searchQuery.cosine_similarity(query)
        print("Cosine Similarity")
        print(cosine_similarity)
        print("Rank documents based on Cosine Similarity")
        print(searchQuery.rank_documents_based_on_cosine_similarity(cosine_similarity))
    elif choice == 8:
        print(searchEngine.document_length(tf_idf))
    elif choice == 9:
        searchEngine.document_length(tf_idf)
        n_tf_idf = tfIdf.normalized_tfidf(tf_idf, searchEngine.docs_length)
        tfIdf.normalized_tf_idf_format(n_tf_idf)
    elif choice == 0:
        break
    else:
        print("Invalid Choice")

