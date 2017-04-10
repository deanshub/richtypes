# start with rnn which takes an input of a sample data (word\number\...)
# and predicts which class it is
# after that do a cnn of a set of samples to indicate the column best prediction

# constants for files and labels

# randomly choose file

# read the data from the file
    # Load CSV file, indicate that the first column represents labels
    from tflearn.data_utils import load_csv
    data, labels = load_csv('titanic_dataset.csv', target_column=0,
                            categorical_labels=True, n_classes=2)

# pre process
    # take random sample from the data as a list
    # add the label to the list
        # Preprocessing function
        def preprocess(data, columns_to_ignore):
            # Sort by descending id and delete columns
            for id in sorted(columns_to_ignore, reverse=True):
                [r.pop(id) for r in data]
            for i in range(len(data)):
              # Converting 'sex' field to float (id is 1 after removing labels column)
              data[i][1] = 1. if data[i][1] == 'female' else 0.
            return np.array(data, dtype=np.float32)

        # Ignore 'name' and 'ticket' columns (id 1 & 6 of data array)
        to_ignore=[1, 6]

        # Preprocess data
        data = preprocess(data, to_ignore)

# build rnn model
