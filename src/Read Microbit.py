from microfs import ls, get, rm
from datetime import datetime
import sys
import os

output_extension = ".csv"
TITLE = ("\n\t\t\t\t\t#################" 
         "\n\t\t\t\t\t# Read Microbit #" 
         "\n\t\t\t\t\t#################\n")

def main():
    print(TITLE)
    csv_files = [file for file in ls() if file.endswith(output_extension)]          # Load all csv file names from the Microbit
    if not csv_files:
        print(" No '{}' files to copy!".format(output_extension))
        return 0
    name = input(" Enter target name: ")
    name = name.capitalize() if name else "Unnamed"
    # Create sub-directory in RAW_Data directory 
    dir_name = os.path.join("RAW_Data", "{} {}".format(name, datetime.now().strftime("%d %m %Y %H-%M")))
    try:
        os.makedirs(dir_name)                                                       # Make the sub-directory if it doesn't exist                                            
    except OSError:
        pass
    print()
    for i, file in enumerate(csv_files):
        print(" Progress: {:<50}  ({}/{})".format("█"*int(50*(i+1)/len(csv_files)), i+1, len(csv_files)), end="\r")
        f_name = "{}{}{}".format(name, i, output_extension)                         # Prepare file name at destination directory
        get(file, os.path.join(dir_name, f_name))                                   # Copy file from Microbit to given directory as f_name
        rm(file)                                                                    # Remove file from Microbit
    print("\n\n {} files moved to '{}'".format(i+1, dir_name))
    return 0

if __name__ == "__main__":
    try:
        main()
    except Exception as ex:
        print("\n ERROR: {}".format(ex.args))
    finally:
        input(" Press Enter to exit")
