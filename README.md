# Hand Movement Recognition
 Classify hand movements (up, down, left, right, ideal) from a BBC Micro:bit by analysing the x, y and z plane acceleration readings.

## Installation
**Software Requirements**
- Python 3.6.7
- Keras 2.2.4
- Microfs 1.3.1
- Mu-Editor 1.0.2
- Pyserial 3.4
- Numpy 1.16.2
- Pandas 0.24.1
- Matplotlib 2.2.2
- Scikit-learn 0.20.

**Hardware Requirements**
- 2 BBC Micro:bits
- 2 USB Type A to Micro B 5-pin cables

## Compiling source code to BBC Micro:bit
**Using Mu-Editor**

Mu-Editor provides easy way code and compile python source codes for BBC Micro:bit.
To see the installation instruction of it, click [here](https://codewith.mu/en/download).
> Make sure that **BBC Micro:bit** mode is selected in the Mu-Editor.
1. Connect BBC Micro:bit to computer via USB
2. Open code in Mu-Editor
3. Flash it on the micro:bit
---
**Using online editor**

There are several online editors to code and compile source codes for BBC Micro:bit.
This [official website](https://microbit.org/code/) provides online python editor to compile the code.

However, I prefer this [site](https://create.withcode.uk/) as it also let's you simulate your code 
depending on the code complexitiy.
> The USB cable should support data transfer
1. Write python code in a online editor
2. Download the hex file
4. Connect BBC Micro:bit to computer via USB
3. Paste the hex file to the micro:bit hard drive

## Usage
**Data collection in BBC Micro:bit**
1. Plug in the Micro:bit via USB to the computer
2. Flash the source code *src/Collect Data.py* on the Micro:bit
4. Restart the Micro:bit
5. Hold the Micro:bit such that the buttons are on top and button B points away from you
6. Select number of data to collect by pressing button A and B (max 14 data)
7. Press both button A and B to start collecting data
8. Press button A to start the countdown
9. After the countdown, perform the movement (data sampled for 1.5 seconds at sample rate of 10 Hz)
10. Press button B to check remaining number of data to collect
12. Repeat steps 5-9 to collect further data
13. Once all data is collected, a smiley face will be displayed
---
**Data transfer from BBC Micro:bit to computer**
1. Plug in the Micro:bit via USB to the computer
2. On the terminal, run the command ```python "src/Read Microbit.py"```
3. Enter the name of the movement data collected in the BBC Micro:bit
4. Now all the data are moved to the *RAW_Data* directory in following subdirectory *{movement_name} {date} {time}* 
---
**Processing the raw data**
1. On the terminal, run the command ```python "src/Read Microbit.py" --data "RAW_Data" --width 13 --normalize true``` to look for data in *RAW_Data* directory, use moving average window of *13* and normalize the values between 0-1
2. The processed data from all collected raw data will be in *Processed Data {date} {time}.csv* file.
---
**Train and test model**
1. Open the *Train Gesture Reader.ipynb* in Jupyter Notebook
2. Select a processed file for training and testing the model
3. Give threshold accuracy to save the trained model
4. Run all the cells
---
**Test trained model**
> Recommended to power both micro:bit via USB
1. Flash “src/Data Sender.py” in one BBC Micro:bit and “src/Data Receiver.py” in another one.
2. Connect the receiver micro:bit via USB to the computer
3. Open the *Test Gesture Reader.ipynb* in Jupyter Notebook
4. Load the trained model from the *Models* directory
5. Configure the serial port settings of the receiver micro:bit
6. In one cell, the program waits for data from receiver mircro:bit via USB
7. Press button A in the sender micro:bit to start countdown
8. Perform the hand movement
9. The transmitter sends an end token at the end of transmission and the receiver displays a tick sign when it receives it. Press button B on transmitter if the end token was lost and not received by the receiver
10. Run remaining cells in Jupyter Notebook to process the data, plot its graph and display the predicted movement.