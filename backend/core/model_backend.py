
# import libraries
import pandas as pd
import tensorflow as tf

from sklearn.model_selection                  import train_test_split
from tensorflow.keras.preprocessing.text      import Tokenizer
from tensorflow.keras.preprocessing.sequence  import pad_sequences

# configurations
records = 1000
params  = 1000

# Load the dataset
data = pd.read_csv('../../model-dev/dataset/browsing_history_dataset.csv')

data = data[:records]

# Combine the query and past search results into a single text feature
data['combined_text'] = data['query'] + ' ' + data['past_searches']

# Tokenize the text
tokenizer = Tokenizer(num_words=10000, oov_token="<OOV>")
tokenizer.fit_on_texts(data['combined_text'])

# print(tokenizer, dir(tokenizer))
# Assuming `data` is a DataFrame with columns 'query', 'likes', and 'priority_percentage'
tokenizer = Tokenizer(num_words=10000, oov_token="<OOV>")
tokenizer.fit_on_texts(data['query'] + ' ' + data['past_searches'])

# Convert text to sequences
query_sequences = tokenizer.texts_to_sequences(data['query'])
likes_sequences = tokenizer.texts_to_sequences(data['past_searches'])

# print(query_sequences, likes_sequences)

# Pad sequences
query_padded = pad_sequences(query_sequences, padding='post', maxlen = params)
likes_padded = pad_sequences(likes_sequences, padding='post', maxlen = params)

# print(data[['query', 'past_searches', 'priority_score']], query_padded.shape)

import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Embedding, Concatenate, SimpleRNN, Dense

# Define the model architecture
query_input = Input(shape=(None,), dtype='int32')
likes_input = Input(shape=(None,), dtype='int32')

# Embedding layers for both inputs
query_embedding = Embedding(input_dim=params, output_dim=128)(query_input)
likes_embedding = Embedding(input_dim=params, output_dim=128)(likes_input)

# Concatenate the embeddings
merged = Concatenate()([query_embedding, likes_embedding])

# Simple RNN layer
rnn_layer = SimpleRNN(128)(merged)

# Dense layer for regression
output = Dense(1)(rnn_layer)

# Compile the model
model = Model(inputs=[query_input, likes_input], outputs=output)
model.compile(optimizer='adam', loss='mse', metrics=['accuracy'])


# model.fit(X_train, y_train, epochs=10, batch_size=32)
model.fit([query_padded, likes_padded], data['priority_score'], epochs=20, batch_size=32)

keras.saving.save_model(model, 'model1.keras', overwrite=True)
loaded_model = keras.saving.load_model("model1.keras")