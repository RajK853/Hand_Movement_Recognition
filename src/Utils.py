import os.path
import numpy as np

LABELS = ("ideal","up", "down", "left", "right")

def getLabel(file_name):
    """
    Returns the label index from the file name
    @param file_name : Name of file with acceleration data
    @return          : Integer value: -1 for invalid file_name, else 0-4 for different gestures 
    """
    file_name = os.path.split(file_name)[-1].lower()
    for i, label in enumerate(LABELS):
        if file_name.startswith(label):
            return i
    return -1

def normalize(data):
    """
    Normalize a 1D numpy array to the value range 0-1
    @param data : 1D numpy array with values
    @return     : 1D numpy array with normalized values
    """
    min_val, max_val = min(data), max(data)
    return (data - min_val)/(max_val - min_val)

def movingAvg(data, window=5):
    """
    Moving average function for smoothing the data with given window width
    @param data   : 1D array
    @param window : Window size for calculating average
    @return       : Smooth 1D numpy array
    """
    return np.array([np.ma.average(data[i : i+window]) for i in range(len(data))])

def getFileNames(dataDir, extension=".csv"):
    """
    Returns the list of files of given format from the given directory and all of its subdirectories using recursion
    @param dataDir   : Root direcory path to search for files
    @param extension : Extension of the file format
    @return          : List of file names (with subdirectory addresses)
    """
    file_names = []
    for name in os.listdir(dataDir):
        abs_path = os.path.join(dataDir, name)              # Absolute address of current file/directory
        if os.path.isdir(abs_path):
            file_names += getFileNames(abs_path, extension=extension)
        elif abs_path.endswith(extension):
            file_names.append(abs_path)
    return file_names

def pad_constant(array, max_length, pad_pos="end"):
    """
    Pad given array with a constant value to achieve given maximum length
    @param array      : Array to pad
    @param max_length : Maximum length of the array after padding
    @param pad_pos    : "start" - Pad at the beginning with initial value
                        "end"   - Pad at the end with ending value
    @return           : Padded array
    """
    pad_pos = pad_pos.lower()
    padLen = max_length-len(array) if (len(array) < max_length) else 0
    if pad_pos == "start":
        padValue = array[0]
        padWidth = (padLen, 0)
    else:
        padValue = array[-1]
        padWidth = (0, padLen)
    array = np.pad(array, padWidth, mode="constant", constant_values=padValue)
    return array

def load_processed_data(f_name, review_length, pad_pos="end", train_ratio=0.75):
    """
    Loads acceleration data from processed file
    @param f_name       : File name
    @para review_length : Max number of sample points for acceleration of each axis; padding length 
    @param pad_pos      : "start" - Pad at the beginning with initial value
                          "end"   - Pad at the end with ending value
    @param train_ratio  : Percentage of total data to use for training
    @return             : (train data, train labels, test data, test labels) where data = acceleration x, y, z and labels = one-hot-encoded labels
    """
    from keras.utils import to_categorical
    # Load the csv file, extract data and labels from it and format them
    with open(f_name, "r") as csv_file:
        data = [[], [], []]
        labels = []
        for row in csv_file:
            _data = list(map(float, row.split(",")))                # Load acceleration reading as float
            _data, _label = np.array(_data[: -1]), _data[-1]
            _data = uniform_split(_data, parts=3)                   # Split acceleration data into 3 equal parts
            # Pad axis readings and reshape them
            for i, axis_array in enumerate(_data):
                axis_array = pad_constant(axis_array, max_length=review_length, pad_pos=pad_pos)
                axis_array = np.reshape(axis_array, (1, axis_array.shape[0]))
                data[i].append(axis_array)
            labels.append(_label)
    # Split the data and labels for training and testing
    label_counter = {label:0 for label in set(labels)}              # Counter for each label saved for training; default count value is zero
    train_amount = round(train_ratio*len(labels)/len(set(labels)))  # Amount of training data
    train_indexes = np.zeros(len(labels))                           # Index value of 1 refers to training data
    for i, label in enumerate(labels):
        if label_counter[label] < train_amount:
            label_counter[label] += 1
            train_indexes[i] = 1
            if all(count>=train_amount for count in label_counter.values()):
                # All labels have required amount of training data
                break
    train_indexes = (train_indexes == 1)
    data = np.array(data)
    labels = to_categorical(labels)
    return data[:,train_indexes], labels[train_indexes], data[:,~train_indexes], labels[~train_indexes]

def uniform_split(array, parts=1):
    """
    Splits a given array into given equal parts
    @param array : Array to split
    @param parts : Number of parts the array should be splitted to; (0 < parts <= length of array)
    @return      : Splitted array (number of items = parts)
    """
    ARRAY_LENGTH = len(array)
    assert parts <= ARRAY_LENGTH, "Number of parts exceedes array langth; should be max {}, but got {}".format(ARRAY_LENGTH, parts)
    if parts > 1:
        interval = round(ARRAY_LENGTH/parts)
        array = np.split(array, range(interval, ARRAY_LENGTH, interval))[: parts]
    return array

def load_raw_data(dataframe, cols=None, movingAvgWindow=5, normalizeData=True):
    """
    Load raw data from given pandas.DataFrame object
    @param dataframe       : Pandas dataframe with data
    @param cols            : Columns of the csv file to load
    @param movingAvgWindow : Window width for the moving average
    @param normalizeData   : True to normalize data
    @return                : Numpy array after smoothing (and normalizing) the raw data
    """
    if cols is None:
        cols = ("x","y","z")
    # Perform columnwise moving window average on given columns
    data = np.array([movingAvg(dataframe[col], window=movingAvgWindow) for col in cols])
    data = data.flatten()
    if normalizeData:
        data = normalize(data)
    return data