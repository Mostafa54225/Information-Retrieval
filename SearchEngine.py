import os
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from natsort import natsorted
import string
from config import Folder
import pandas as pd


class SearchEngine:
    # folder_names = ["Documents"]
    fileNo = 1
    pos_index = {}
    # Initialize the file mapping (fileno -> file name).
    file_map = {}
    folder = Folder()

    def __init__(self):
        pass

    def read_file(self, filename):
        with open(filename, 'r', encoding="ascii", errors="surrogateescape") as f:
            stuff = f.read()
        f.close()
        return stuff

    def convert_tokens_to_lower_case(self, token_list):
        return [word.lower() for word in token_list]

    def remove_punctiations(self, token_list):
        table = str.maketrans('', '', '\t')
        token_list = [word.translate(table) for word in token_list]

        # get all punctuations
        punctuations = string.punctuation.replace("'", "")
        trans_table = str.maketrans('', '', punctuations)
        stripped_words = [word.translate(trans_table) for word in token_list]
        return [word for word in stripped_words if word]

    def stem_tokens(self, tokens):
        stemmer = PorterStemmer()
        return [stemmer.stem(token) for token in tokens]

    def preprocessing(self, final_string):
        # Tokenize.
        token_list = word_tokenize(final_string)
        # remove punctuations
        token_list = self.remove_punctiations(token_list)
        # Change to lowercase.
        token_list = self.convert_tokens_to_lower_case(token_list)
        # stem tokens
        token_list = self.stem_tokens(token_list)
        return token_list

    def createPositionalIndex(self):
        for folder_name in self.folder.folder_names:
            # # Open files.
            file_names = natsorted(os.listdir(folder_name))
            # For every file.
            for file_name in file_names:
                # Read file contents.
                stuff = self.read_file(folder_name + '/' + file_name)
                final_token_list = self.preprocessing(stuff)

                # For position and term in the tokens.
                for pos, term in enumerate(final_token_list):
                    # If term already exists in the positional index dictionary.
                    if term in self.pos_index:
                        # self.pos_index[term][0] = self.pos_index[term][0] + 1
                        # Check if the term has existed in that DocID before.
                        if self.fileNo in self.pos_index[term][1]:
                            self.pos_index[term][1][self.fileNo].append(pos)
                        else:
                            self.pos_index[term][1][self.fileNo] = [pos]
                            # Increment total freq by 1.
                            self.pos_index[term][0] = self.pos_index[term][0] + 1

                    # If term does not exist in the positional index dictionary
                    # (first encounter).
                    else:
                        # Initialize the list.
                        self.pos_index[term] = []
                        # The total frequency is 1.
                        self.pos_index[term].append(1)
                        # The postings list is initially empty.
                        self.pos_index[term].append({})

                        # Add doc ID to postings list.
                        self.pos_index[term][1][self.fileNo] = [pos]
                # Map the file no. to the file name.
                self.file_map[self.fileNo] = folder_name + "/" + file_name
                # Increment the file no. counter for document ID mapping
                self.fileNo += 1
        return self.pos_index

    def df_format(self):
        terms_list = list(self.pos_index.keys())
        doc_freq_list = []
        # doc_ids =[]
        # positions = []
        Doc_ids_Positions = []
        for term in terms_list:
            doc_freq_list.append(self.pos_index[term][0])
            # doc_ids.append(list(Positional_index[term][1].keys()))
            # positions.append(list(Positional_index[term][1].values()))
            Doc_ids_Positions.append(self.pos_index[term][1])

        data = {'Term': terms_list, 'Doc_Freq': doc_freq_list, ' Doc_Ids : [Positions] ': Doc_ids_Positions}
        df = pd.DataFrame(data, columns=['Term', 'Doc_Freq', ' Doc_Ids : [Positions] '])
        print(df)
