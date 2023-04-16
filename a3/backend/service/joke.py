import pandas as pd
import numpy as np
import random
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.layers.experimental import preprocessing
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences


jokes_df = pd.read_csv('funny.csv')

data = jokes_df['Joke'] + ' endjoke'


tokenizer = Tokenizer(filters='', lower=False)
tokenizer.fit_on_texts(data)


sequences = tokenizer.texts_to_sequences(data)


max_sequence_len = max([len(seq) for seq in sequences])
sequences_padded = pad_sequences(sequences, maxlen=max_sequence_len, padding='post', truncating='post')


input_data = sequences_padded[:, :-1]  
output_data = sequences_padded[:, 1:]  
num_words = len(tokenizer.word_index) + 1  


output_data_int = np.argmax(output_data, axis=1).reshape(-1)



output_data = tf.keras.utils.to_categorical(output_data_int, num_classes=num_words)



model = keras.Sequential()
model.add(layers.Embedding(num_words, 64, input_length=max_sequence_len - 1))
model.add(LSTM(128))
model.add(layers.Dense(num_words, activation='softmax'))



model.compile(loss='categorical_crossentropy', optimizer='adam')


model.fit(input_data, output_data, epochs=10, verbose=2)


#model.save('joke_model.h5')


def generate_joke(tag):
    tag_jokes = jokes_df[jokes_df['Joke'].str.contains(tag)]['Joke'].values.tolist()

    if not tag_jokes:
        prompt = random.choice(jokes_df['Joke'].values.tolist())
    else:
        prompt = random.choice(tag_jokes)

    prompt_seq = tokenizer.texts_to_sequences([prompt])[0]

    predicted_word = None
    joke = prompt

    while predicted_word != 'endjoke' and len(joke.split()) < 20:
        sequence_so_far = tokenizer.texts_to_sequences([joke])[0]

        sequence_so_far_padded = pad_sequences([sequence_so_far], maxlen=max_sequence_len - 1, padding='post', truncating='post')

        predicted_probabilities = model.predict(sequence_so_far_padded)[0]
        predicted_word_index = np.argmax(predicted_probabilities)
        predicted_word = None

        for word, index in tokenizer.word_index.items():
            if index == predicted_word_index:
                predicted_word = word
                break
            
        if predicted_word != 'endjoke':
            joke += ' ' + predicted_word

    joke = joke.replace(' endjoke', '')

    return joke




