# Read in this data and plot the signal vs. time.
# Create a sine wave and cosine wave using the formulae above.
# Sum these two waves and compare to the target curve.
# Vary the values for amplitudes and frequencies until the curves match.
# When you have a match, save the code and push it to GitHub.
# Completion of this excerise will be part of the class participation grade.
# Complete before the last day of classes.
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

signal = pd.read_csv('curve_to_match.dat', skiprows=1)
time = pd.read_csv('curve_to_match.dat', nrows=0)
signal = signal.columns.tolist()
time = time.columns.tolist()
signal = [float(x) for x in signal]
time = [float(x) for x in time]
signal = np.array(signal)
time = np.array(time)

amplitude1 = 1
amplitude2 = 2
frequency1 = 2
frequency2 = 3

curve1 = amplitude1 * np.sin (frequency1 * time)
curve2 = amplitude2 * np.cos (frequency2 * time)


plt.plot(time, signal, "bo-")
plt.plot(time, curve1+curve2, "gs--")
plt.xlabel("time")
plt.ylabel("signal")
plt.title("time vs signal")
plt.show()