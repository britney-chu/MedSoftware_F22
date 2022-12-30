# CPAP Analysis Assignment

### Author: Britney Chu

## Background
Obstructive sleep apnea is a condition in which breathing stops involuntarily for brief periods of time during sleep. The flow of air stops because the airways may constrict due to "floppy" muscles that do not keep the airways open. This disruption of airflow can lead to periods of decreased oxygen supply to the brain and other parts of the body, as well as poor sleep quality leading to daytime drowsiness. (Source: https://www.healthline.com/health/sleep/obstructive-sleep-apnea)

Obstructive sleep apnea is often treated with the use of a continuous positive airway pressure (CPAP) machine. The patient wears a mask connected to the CPAP. The mask provides pressurized air for the patient to breath. The pressure is set high enough to help keep open the airways so that they cannot collapse and block air flow. Breathing is not interrupted.

Most CPAPs collect some data during sleep. This can include:

the number of hours of use per night
the amount of air leakage from the system (indicating poor mask fit)
the number of "events per hour" in which the patient stops breathing for 10 seconds or more
During sleep studies, a pulse oximeter may also be used to continuously measure the oxygen saturation of the blood.

The data collected by the CPAP is then usually sent to a central server for analysis and storage.

For this assignment, we will be writing some code that reads in CPAP data for a variety of patients from an input file, analyzes these results, and then creates separate output files for each patient.

## How to start the code

The input is a text file, in the same directory as this code, called `sample_data.txt`.
This must be in the following format:

```FirstName LastName
Hours
Seal, s1, s2, s3, s4, etc.
Events, e1, e2, e3, e4, etc.
O2, o1, o2, o3, o4, etc.
```

### To run the code:

Create a virtual environment with python 3.10 or greater. Then install all modules in the requirements.txt file. Activate your virtual environment and at the command line
 type `python cpap_analysis.py` and hit enter. The output of this will appear in the directory as `Firstname-Lastname.json` which will include all of the sleep data collected as well as a diagnosis. 
