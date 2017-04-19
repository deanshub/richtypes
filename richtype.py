from __future__ import absolute_import, division, print_function
import tflearn
import random

# start with rnn which takes an input of a sample data (word\number\...)
# and predicts which class it is
# after that do a cnn of a set of samples to indicate the column best prediction

# constants for files and labels
from traindatafiles import getFiles
max_seq_len = 100

# load files
files = getFiles()
n_files = len(files)
labels = list(set([i[0] for i in files]))
n_labels = len(labels)

def getRandomFile():
    num = random.randrange(0, n_files)
    return files[num]

# randomly choose file
# label, filename = getRandomFile()
filename = 'output/pure_sample.csv'

# read the data from the file
# Load CSV file, indicate that the first column represents labels
from tflearn.data_utils import load_csv
from tflearn.data_utils import to_categorical

# trainX, trainY = load_csv(filename, target_column=0, has_header=False,
trainX, trainY = load_csv('output/pure_all.csv', target_column=0, has_header=False,
                        categorical_labels=False, n_classes=n_labels)

# testX, testY = load_csv('output/all1.csv', target_column=0, has_header=False,
testX, testY = load_csv(filename, target_column=0, has_header=False,
                        categorical_labels=False, n_classes=n_labels)

n_labels = len(list(set([i[0] for i in trainY])))
# labels = to_categorical(labels, n_labels)


# pre process
from tflearn.data_utils import string_to_semi_redundant_sequences

letters_dict = {}
def char_to_id(char):
    if not char in letters_dict:
        letters_dict[char] = len(letters_dict.keys()) + 1
    return letters_dict[char]


def word2vec(word):
    return [char_to_id(i) for i in word]

def preprocess_classes(classes):
    dictionary = {}
    dict_id = 0
    for label in classes:
        if not label in dictionary:
            dictionary[label] = dict_id
            dict_id+=1
    return dictionary, [dictionary[label] for label in classes]



def preprocess(trainX):
    trainX = [i[0].lower() for i in trainX]
    trainX = [word2vec(i) for i in trainX]
    return trainX

# Data preprocessing
from tflearn.data_utils import pad_sequences
trainX = preprocess(trainX)
testX = preprocess(testX)

# Sequence padding
trainX = pad_sequences(trainX, maxlen=max_seq_len, value=0.)
testX = pad_sequences(testX, maxlen=max_seq_len, value=0.)
# Converting labels to binary vectors
dictionary, trainY = preprocess_classes(trainY)
_, testY = preprocess_classes(testY)
n_labels = len(dictionary.keys())

trainY = to_categorical(trainY, nb_classes=n_labels)
testY = to_categorical(testY, nb_classes=n_labels)

print('n_labels', n_labels)
# RNN model
net = tflearn.input_data(shape=[None, max_seq_len])
net = tflearn.embedding(net, input_dim=10000, output_dim=128)
net = tflearn.lstm(net, 128, dropout=0.8, return_seq=True)
net = tflearn.lstm(net, 128, dropout=0.8)
net = tflearn.fully_connected(net, n_labels, activation='softmax')
net = tflearn.regression(net, optimizer='adam', learning_rate=0.001,
                         loss='categorical_crossentropy')

# Training
model = tflearn.DNN(net, tensorboard_verbose=3, tensorboard_dir='./tensorboard/')
model.fit(trainX, trainY, validation_set=(testX, testY), show_metric=True,
           n_epoch=10, batch_size=32)
model.save('model_richtypes')
