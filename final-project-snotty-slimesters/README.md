# final_project_template
BME 547 Final Project

#### This program was written by Dylan Cai and Britney Chu,
#### AKA The Snotty Slimesters
<br/>

### Background
This code was written to create a dual-GUI, Server, and Database system where
all four components work together to create a Patient Monitoring System. The
patient-side GUI allows the patient to enter their full name, a medical record
number, upload a medical image from their local computer, and a csv file
containing ECG data. The code processes the ECG data and plots the graph as
well as calculates a heart rate for the plot. You can then upload this data to
the database which is hosted by Mongo DB. The monitor GUI can then get the data
from the database and display the patient data. It also gives the user the
option to save this image this locally. This monitor updates constantly to get
new data that was uploaded to the databse.
<br/>

### Install
First create a virtual environment. The install the required packages by
accessing the requirements.txt file found in this repo and using
`pip3 install -r requirements.txt`. Once all packages have installed you
can run the patient gui using `python3 patient_gui.py`. To run the monitoring
station use `python3 monitor.py` at the terminal. There are files within this
repository that can be used to upload to the database and can be found in the
images folder. Otherwise you can use images from your local device.
<br/>

### Usage
#### Monitoring Station
* begin by following install instructions
* run `python3 monitor.py` at the terminal
* choose a medical record number to view then hit the `Update Monitor` button.
This will update the GUI with the relevant information and allow the
user to select historic ECG or medical images found in the database.
* To save any of these images click the save image button below
the desired image. Then complete the save as dialog. You have the option of
adding a `.jpg ` suffix to the name or the program will do it for you. You
can also select the location to save this image.

#### Patient-side GUI
* begin by following install instructions
* run `python3 patient_gui.py` in the terminal
- Once on the patient gui interface, enter all information that you would like.
Not all the fields need to be filled. However, you do need to input a medical
record number in order for a patient to added or updated in the database. The
clear button in the bottom right of the gui will allow you to clear the data fields
and enter new information. The bottom left status label shows the status after the 'ok'
button is clicked. The label should either show that the patient was successfully
updated or added into the database along with the status code.


### API
Our server.py script contains a route to add or update a user in the database.
The route receives an in_data dictionary that is posted from the gui, and
processes this data and sends it to the mongoDB which creates a new user or
updates an old one based on whether the medical record number exists in the
DB. The in_data variable that is put in the post request is a dictionary that
contains the following format:
in_data:
    [{"name": <string>
    "id": <integer>
    "heart_rate": <int1>
    "medical_image": <string1>
    "ecg_image": <string1>
    "m_i_name": <string1>
    "timestamp": <string1> }]
The server.py file also validates this in_data by checking for the correct
data types, and whether the data contains the correct keys. There is also
validation in place to allow certain data fields to be empty when uploading.
This is especially helpful when you need to update a specific field for a
certain patient.
    
There are also multiple routes that make get requests to the server to
pull information from the MongoDB to be displayed on the monitor-side GUI.
The information being pulled includes the ECG images (base64 string encoded image),
ECG time of upload (string), medical image names (string), medical images
(base64 string encoded image), patient name (string) and heart_rates (int).
These are stored in the database as a list. Often these are accessed using the
patient ID which is included in the route. 

#### Monitor accessed APIs:
get_patient_name(patient_id)<br />
get_hr(patient_id)<br />
get_ecg(patient_id)<br />
get_ecg_times(patient_id)<br />
get_med_img_names(patient_id)<br />
get_med_img_str(patient_id)<br />
get_all_ids()<br />

These requests all return a json response and a integer status code.
The patient ID can be passed as a string or an int. It will be type
cast to a string when it is sent to the server. The server will return
an error if the patient ID is non-numeric or if it is not found in the
database.

A request is made to the server using `requests` package. The request is
fulfilled by the server which contacts the Mongo DB gui. The information or
the error message is sent as json with a accompanying status code as an
int. this is then received by the monitor GUI which can process the data to
display to the user.

### Video
- https://drive.google.com/file/d/1j0dTHQw-ZZbcfbK1e0j
rVN06QoPYxmO4/view?usp=sharing
This link is to the video of our demo of the project. It should take you
to a google drive video that is accessible to everyone with the link.

### MIT License

Copyright (c) [2022]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.