import pprint
from SearchEngine import SearchEngine
from Query import Query
from TF_IDF import TF_IDF
from config import Folder


folder = Folder()
searchEngine = SearchEngine()
searchQuery = Query()
pos = searchEngine.createPositionalIndex()
print("Positional Index")
searchEngine.df_format(pos)

tfIdf = TF_IDF()
# print("Term Frequency")
tf = tfIdf.computeTF()
# tfIdf.tf_format(tf)
# print("Inverse Document Frequency")
idf = tfIdf.computeIDF()
# tfIdf.idf_format(idf)
#
tf_idf = tfIdf.computeTFIDF(tf, idf)
# tfIdf.tf_idf_format(tf_idf)

searchKey = input("Enter a word to search for it: ")
result = searchQuery.Matching_Query(searchKey)
pprint.pprint(result)

