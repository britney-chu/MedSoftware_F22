# Unit Testing and Continuous Integration

### Author: Britney Chu

## Background

With the transition towards electronic medical records, many paper records are being scanned into a digital format. Optical character recognition (OCR) is used so that the scanned text is searchable. Depending on the quality of the paper records (often derived from faxes), the quality of the OCR result may not be perfect. Therefore, any code that is looking to interpret the scanned results needs to be flexible enough to read results that may be slightly off. This assignment simulates a small example of such a problem.

Tachycardia is a heart rate that exceeds the normal resting heart rate. In this assignment, you will be writing a function that could be used to interpret whether a string obtained from OCR of medical records contains the word "tachycardic".


## How to use

Begin by setting up the virtual environment and downloading all requirements in the requirements.txt file. 
To be able to use the `is_tachycardic` function you must `import is_tachycardic from tachycardia`. Then pass 
the function one string. If the string contains "tachycardic" between any amount of white space or punctuation, 
the function will return the boolean `True`, if not it will return `False`.



