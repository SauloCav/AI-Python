import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.layers import Embedding, LSTM, Dense, Bidirectional
from tensorflow.keras.models import Sequential
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Passo 1: Importar bibliotecas

# Passo 2: Carregar e Preprocessar os Dados

data = pd.read_csv('train.csv')  # Substitua 'train.csv' pelo seu conjunto de dados
tokenizer = Tokenizer(num_words=10000, oov_token="<OOV>")
tokenizer.fit_on_texts(data['comment_text'])
sequences = tokenizer.texts_to_sequences(data['comment_text'])
padded_sequences = pad_sequences(sequences, maxlen=150, padding='post', truncating='post')
labels = data['toxic']
X_train, X_test, y_train, y_test = train_test_split(padded_sequences, labels, test_size=0.2)

# Passo 3: Construir o Modelo de Toxicidade

model = Sequential([
    Embedding(input_dim=10000, output_dim=16, input_length=150),
    Bidirectional(LSTM(64, return_sequences=True)),
    Bidirectional(LSTM(64)),
    Dense(1, activation='sigmoid')
])
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

# Passo 4: Treinar o Modelo

history = model.fit(
    X_train, y_train,
    epochs=5,
    batch_size=64,
    validation_data=(X_test, y_test)
)

# Passo 5: Avaliar o Modelo

y_pred = (model.predict(X_test) > 0.5).astype(int)
accuracy = accuracy_score(y_test, y_pred)
print(f'Accuracy: {accuracy * 100:.2f}%')
classification_rep = classification_report(y_test, y_pred)
print('Classification Report:\n', classification_rep)
confusion_mat = confusion_matrix(y_test, y_pred)
print('Confusion Matrix:\n', confusion_mat)
