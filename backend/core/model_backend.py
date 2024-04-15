# import libraries
import pandas as pd

import tensorflow as tf
from sklearn.model_selection                  import train_test_split
# from tensorflow.keras.preprocessing.text      import Tokenizer
from tensorflow.keras.preprocessing.sequence  import pad_sequences

from tensorflow.keras.preprocessing.text import Tokenizer as BaseTokenizer

class Tokenizer(BaseTokenizer):
    def __init__(self, num_words=None, oov_token=None, **kwargs):
        super().__init__(num_words=num_words, oov_token=oov_token, **kwargs)
        self.next_index = 1  # Initialize the index for unseen words

    def texts_to_sequences(self, texts):
        sequences = []
        for text in texts:
            sequence = []
            for word in text.split():
                index = self.word_index.get(word)
                # print(self.word_index)
                if index is None:
                    index = self.document_count
                    self.word_index[word] = index
                    self.index_word[index] = word
                    self.document_count += 1
                    # print(self.index_word)
                sequence.append(index)
            sequences.append(sequence)
        return sequences
    
def train_from_dataset():
    # Load the dataset
    data = pd.read_csv('../model-dev/dataset/Meta -2.csv')

    tokenizer = Tokenizer(num_words=10000, oov_token=None)
    tokenizer.fit_on_texts(data['query'] + ' ' + data['liked_keywords'])

    return tokenizer
