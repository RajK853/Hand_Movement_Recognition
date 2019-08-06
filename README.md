# Hand_Movement_Recognition
 Classify hand movements (up, down, left, right, ideal) from a BBC Micro:bit by analysing the x, y and z plane acceleration readings.

## Installation
**Requirements**
- Python 3.6.7
- Keras 2.2.4
- Microfs 1.3.1
- Mu-Editor 1.0.2
- Pyserial 3.4
- Numpy 1.16.2
- Pandas 0.24.1
- Matplotlib 2.2.2
- Scikit-learn 0.20.3

## Usage
> Make sure that **BBC Micro:bit** mode is selected in the Mu-Editor.

**Data collection in BBC Micro:bit**
1. Plug in a Micro:bit via USB to the computer
2. Load the source code from *src/Collect Data.py* in Mu-Editor
3. Flash it on the Micro:bit
4. Restart the Micro:bit
5. Hold the Micro:bit such that the buttons are on top and button B points away from you
6. Select number of data to collect by pressing button A and B (max 14 data)
7. Press both button A and B to start collecting data
8. Press button A to start the countdown
9. After the countdown, perform the movement (data sampled for 1.5 seconds at sample rate of 10 Hz)
10. Press button B to check remaining number of data to collect
12. Repeat steps 5-9 to collect further data
13. Once all data is collected, a smiley face will be displayed

**Data transfer from BBC Micro:bit to computer**
1. Plug in the BBC Micro:bit via USB to the computer
2. On the terminal, run the command 
```python "src/Read Microbit.py"```
3. Enter the name of the movement data collected in the BBC Micro:bit
4. Now all the data are moved to the *RAW_Data* directory in following subdirectory ```Name given at step 3``` ```Date``` ```Time``` 