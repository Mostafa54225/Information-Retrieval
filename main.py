# from nltk.corpus import stopwords
# from nltk.tokenize import word_tokenize
#
# text = "my name is Nick likes to play football, however he is not too fond of tennis."
# text_tokens = word_tokenize(text)
#
# print(text_tokens)
# tokens_without_sw = [word for word in text_tokens if not word in stopwords.words()]
#
# print(tokens_without_sw)
#
# print(stopwords.words('english'))

from SearchEngine import SearchEngine
from Query import Query

# Sample positional index to test the code.
searchEngine = SearchEngine()
searchQuery = Query()
searchEngine.createPositionalIndex()
print(searchEngine.pos_index)

searchKey = input("Enter a word to search for it: ")
result = searchQuery.Matching_Query(searchKey)
print(result.keys())
# searchKey = searchEngine.preprocessing(searchKey)
# print(searchKey)
# sample_pos_idx = searchEngine.pos_index[searchKey[0]]
#
# print("Positional Index")
# print(sample_pos_idx)
#
# file_list = sample_pos_idx[1]
#
# print("Filename, [Positions]")
# for searchEngine.fileNo, positions in file_list.items():
#     print(searchEngine.file_map[searchEngine.fileNo], positions)
