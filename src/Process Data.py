import os.path
import argparse
import pandas as pd
from time import time
from random import shuffle
from datetime import datetime
from Utils import getLabel, normalize, movingAvg, getFileNames, load_raw_data

TITLE = ("\n\t\t\t\t\t################" 
         "\n\t\t\t\t\t# Process Data #" 
         "\n\t\t\t\t\t################\n")

def main(dataDir, movingAvgWindow, normalizeData):
    print(TITLE)
    rootDir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))		# Main directory of the project
    print(" Moving Average Window: {}, Normalize Data: {}".format(movingAvgWindow, normalizeData))
    dataDir = os.path.join(rootDir, dataDir)         						# Go one directory back from rootDir and go to /Data/%data_type%
    if not os.path.exists(dataDir):
        raise OSError("Invalid directory: {}".format(dataDir))
    print(" Data directory: {}".format(dataDir))
    files = getFileNames(dataDir)                                               # Get file names (with full address) from dataDir directory
    shuffle(files)
    out_f_name = "Processed Data {}.csv".format(datetime.now().strftime("%d.%m.%Y %H.%M"))
    fileFullPath = os.path.join(rootDir, out_f_name)           					# Create full path of the output csv file
    with open(fileFullPath, "w") as csv_file:
        print(" Saving data at: {}".format(fileFullPath))
        total_files = len(files)
        for i, f_name in enumerate(files):
            label = getLabel(f_name)                                            # Get label of the data from its file name
            df = pd.read_csv(f_name)                                            # Load given csv file as pandas.DataFrame
            df.columns = pd.Index(i.strip() for i in df.columns)                # Strip redundant spaces from column names
            data = load_raw_data(df, cols=("x", "y", "z"), movingAvgWindow=movingAvgWindow, normalizeData=normalizeData)
            str_data = ",".join(map(str, data))                                 # Convert values in data into string and join with ','
            csv_file.write("{},{}\n".format(str_data, label))                   # Write data and label to the csv file 
            progress_ratio = (i+1)/total_files                                  # Calculate current progress
            print(" Progress : {:░<30} {:>6.2f}% ({:>3}/{:<3})".format(
            	"█"*int(30*progress_ratio), 100*progress_ratio, i+1, total_files), end="\r")
    print("\n")

if __name__ == "__main__":
    # Getting arguments from the command prompt
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--data", help="Directory with data", type=str, default="RAW_Data")
    parser.add_argument("-w", "--width", help="Moving average window width", type=int, default=13)
    parser.add_argument("-n", "--normalize", help="True to normalize data", type=bool, default=True)
    args = parser.parse_args()
    t0 = time()    
    try:
        main(dataDir=args.data, movingAvgWindow=args.width, normalizeData=args.normalize)
    except Exception as ex:
        print("\n ERROR: {}".format(ex.args))
    finally:
        print(" Time taken: {:.2f} s".format(time()-t0))
        input(" Press Enter to exit ")