import pprint
from SearchEngine import SearchEngine
from Query import Query
from TF_IDF import TF_IDF
from config import Folder


folder = Folder()
searchEngine = SearchEngine()
searchQuery = Query()
pos = searchEngine.createPositionalIndex()
pprint.pprint(pos)

# searchEngine.df_format()

tfIdf = TF_IDF()
tf = tfIdf.computeTF()
pprint.pprint(tf)
idf = tfIdf.computeIDF()
pprint.pprint(idf)

tf_idf = tfIdf.computeTFIDF(tf, idf)
pprint.pprint(tf_idf)

searchKey = input("Enter a word to search for it: ")
result = searchQuery.Matching_Query(searchKey)
print(result)

