# ECG Analysis Assignment

### Author: Britney Chu

## Background

An Electrocardiogram or ECG is a valuable tool to physicians around the world. This program will evaluate ECG signal data and report back various metrics that are commonly needed for clinicians 
to assess vitals.
Read ECG data from a CSV file that will have lines with time, voltage. Example data can be found in the test_data/ directory of the repository.
If either value in a time, voltage pair is missing, contains a non-numeric string, or is NaN, the program should recognize that it is missing, log an error to the log file, and skip to the next data pair. (See test_data\README.md for more details.)
If the file contains a voltage reading outside the normal range of +/- 300 mv, add a warning entry to the log file indicating the name of the test file and that voltages exceeded the normal range. This should only be done once per file (in other words, do not log every single voltage excursion). Analysis of the data should still be done as normal.
The following data should be calculated and saved as keys in a Python dictionary called metrics:
duration: time duration of the ECG strip as a numeric value
voltage_extremes: tuple in the form (min, max) where min and max are the minimum and maximum lead voltages as found in the raw data file.
Do not take the absolute value. The min should be that smallest number (even if negative) and max should be the largest number. min and max should be numeric values.
num_beats: number of detected beats in the strip, as a numeric value
mean_hr_bpm: estimated average heart rate over the length of the strip as a numeric value
beats: list of times when a beat occurred. The individual times should be numeric values
Your metrics dictionary should be output as a JSON file. The json file should have the same name as the ECG data file, but with an extension of .json. Example: the dictionary with results from the ECG data found in test_data12.csv should be saved in a json file called test_data12.json.
All numeric values reported above must be reported as numbers (i.e., int or float) not as numeric strings (i.e., not "5.3")


## How to run the code

The input is a CSV file, in a folder called test_data. To change the file to be analyzed, change the path string in the second line of the function `main()`. 

### How to start the code
Create a virtual environment with python 3.10 or greater. Then install all modules in the requirements.txt file. Activate your virtual environment and at the command line
 type python ecg_analysis.py and hit enter. The output of this will appear in the directory as test_dataX.json which will include all of the ECG metrics calculated for the test file test_dataX.csv.

### What is a beat
After DC drift is removed and high frequency noise is removed, the peaks are identified using scipy by their prominence above other peaks as well as their distance from other peaks.
This is meant to ignore small peaks that are not R peaks as well as peaks that are too close together to represent another heart beat.
Beats per minute is calculated as the number of beats divided by the total time in minutes. This gives a mean of the entire ecg records bpm.

### License
This code is protected by the MIT license and all terms included.

