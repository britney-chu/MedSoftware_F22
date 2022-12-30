# Heart Rate Sentinel Server Assignment

- This program was written by Dylan Cai and Britney Chu,
AKA the Snotty Slimesters


- This code was written to create a server environment that allows the storage
and manipulation of patient and attending user data. The patients have
characteristics of patient_id, age, attending username, heart rate, status,
and timestamp. The attenders have characteristics of username, email, and phone
number. The server allows for heart rates to be tracked along with time stamps of these heart rates and the status of this heart rate given the patients age. If a heart rate is registered for a patient that is considered tachycardic, the attending assigned to this patient will be notified.

- This program is already running on a server at the address `http://vcm-29737.vm.duke.edu:5000/`. At this address several paths can be accessed for each functionality described above. There is also an example client code included which is currently written to access this server and get the last status of patient 1. The user can run this by starting a virtual environment with everything included in the requirements.txt. Then run `python3 client.py`. The user can also access this server in the browser at the same address.

- Dylan wrote the code regarding attending users while Britney wrote the code
regarding patients. We also split the rest of the server routes by alternating
based on the order given in the git hub issues.

- Overall, our program offers four opportunities for post requests, to add new
patients, attending users, heart rates for patients, and a timestamp to
calculate the average heart rate since that time. The program also has four get
routes that offer information on the tachycardic status of a given patient,
the overall heart rates of a patient, the average heart rate of a patient, and
the list of patients that are being treated by a given attender. A more detailed account of the APIs can be found at the bottom of this document and is taken directly from the assignment specifications from github user `dward2`.

- For our VCM, the hostname and port in which our code is running is:
- http://vcm-29737.vm.duke.edu:5000/

- MIT License

Copyright (c) [year] [fullname]

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


### Routes
Your Flask web service should implement the following API routes.  Please note
that the `/api` at the start of the routes given below should be included
in your route name.

* `POST /api/new_attending` that takes a JSON input as follows:
  ```
  {
      "attending_username": <attending_username_string>,
      "attending_email": <attending_email_string>, 
      "attending_phone": <attending_phone_string>
  }
  ```
  where
  + `<attending_username_string>` is a string in the format 
    "LastName.FirstInitial" such as `"Smith.J"`
  + `<attending_email_string>` is a string containing an e-mail address such
    as `"DrSmith@my_hospital.com"`
  + `<attending_phone_string>` is a string containing a 10 digit phone number
    such as `"919-555-1212"`
    
  The e-mail provided here will be used to send notifications to the physician
  that is registered for each patient.  While the e-mail should be of the
  correct syntax (i.e., name@domain.com), it does not need to be an active
  e-mail address as we will be using a simulated email system for this 
  assignment.  The value for the
  `"attending_username"` key will be used in the `api/new_patient` route below 
  for linking a patient with an attending physician.  The only verification
  needed for the values of this dictionary is that they are all strings.
  Verification that the strings meet the formats above is not necessary.
  
* `POST /api/new_patient` that takes a JSON input as follows:
  ```
  {
      "patient_id": <patient_id>,
      "attending_username": <attending_username_string>, 
      "patient_age": <patient_age>, # in years
  }
  ```
  where
  + `<patient_id>` is the patient medical record number.  The actual medical
    record number will always be an integer.  However, the value sent as the 
    `<patient_id>` value in the above dictionary may be an integer, a numeric 
    string, or a string with letters and numbers.  Your code must be prepared
    to parse this input and determine whether the id is acceptable (i.e.,
    can be turned into an integer) or rejected (if it contains any letters).
    So, `123` or `"123"` should be accepted as patient_ids (although the string 
    `"123"` should be converted into the integer `123` for storage), while 
    `"a54"`, `"aj"`, or `"54a"` should be rejected.
  + `<attending_username_string>` is a string following the 
    "LastName.FirstInitial" format as described in the `/api/add_attending` 
    route above.
  + `<patient_age>` is the patient's age in years.  The actual age will always
    be an integer, but as with the `<patient_id>`, the value in the dictionary 
    may be an integer (which should be accepted), a numeric string (which
    should be accepted and converted into an integer), or a string with letters 
    and numbers (which should be rejected).  Again, your code must distinguish 
    between acceptable and unacceptable inputs.

  This route is called to register a new patient with your server.  This would
  occur when a heart rate monitor is checked out and attached 
  to a particular patient.  This will allow you to initialize a patient in
  your server and be able to accept future heart rate measurements for this 
  patient.  The `"attending_username"` key contains a string that will be used 
  to match with an attending physician as described in the `/api/add_attending`
  route.
   
* `POST /api/heart_rate` that takes a JSON as follows:
  ```
  {
      "patient_id": <patient_id>,
      "heart_rate": <heart_rate>
  }
  ```
  where
  + `<patient_id>` is the patient medical record numbers
  + `<heart_rate>` is the patient heart rate being recorded.
  
  As with the `/api/new_patient` route, the `<patient_id>` or `<heart_rate>`
  values may be sent as an integer, a string containing an integer, or a string
  containing numbers and letters.  And, it may not necessarily be the same type
  as was sent in the `/api/new_patient` call.  For example, the id might be 
  sent as a string such as `"1501"` in the `new_patient` call, but sent as an 
  integer such as `1501` in the `heart_rate` call.  Integers and numeric 
  strings should be accepted.  Strings of mixed numbers and integers should be
  rejected.  The actual heart rate will only be integers, not decimals.  
  
  This route should store the sent heart rate
  measurement as an integer in the record for the specified patient.  The 
  [current date/time stamp](https://github.com/dward2/BME547/blob/main/Assignments/time_server_project.md#getting-current-datetime) 
  of when the POST was received should also be stored with the heart rate
  measurement.  If the posted heart rate is tachycardic for the specified 
  patient and patient age, an e-mail should be sent to the attending physician
  whose e-mail address was registered in the `api/add_attending` route. 
  This e-mail should include the patient_id, the tachycardic heart rate, and 
  the date/time stamp of that heart rate.  See below for information on how to
  simulate the sending of this e-mail.
  
* `GET /api/status/<patient_id>`  
  should return a dictionary in a JSON string containing the latest heart rate, 
  as an integer, for the specified patient, whether this patient is 
  currently tachycardic based on this most recently posted heart rate, and 
  a string containing the date and time of this most recent heart rate 
  formatted as shown in the example below.  
  The return dictionary/JSON string should look like:
  ```
  {
      "heart_rate": <heart_rate_integer>,
      "status":  <status_string>, 
      "timestamp": <time_stamp_string>   
  }
  ```
  where
  + `<heart_rate_integer>` the most recent heart rate as an integer 
    (ex., `100`)
  + `<status_string>` is either the string `"tachycardic"` or 
    `"not tachycardic"` based on the most recent heart rate,
  + `<time_stamp_string>` is a string indicating the date/time of the most
    recent heart rate.  It should be in the format as shown by the example
    "2018-03-09 11:00:36".
 
* `GET /api/heart_rate/<patient_id>` should return a list of all the previous 
  heart rate measurements for that patient, as a list of integers.  Timestamps 
  are not required.  The list should be returned as a JSON string.

* `GET /api/heart_rate/average/<patient_id>` should return the patient's 
  average heart rate, as an integer, of all measurements you have stored for 
  this patient.  The integer should be returned as a JSON string.
 
* `POST /api/heart_rate/interval_average` that takes a JSON as follows: 
  ```
  {
      "patient_id": <patient_id>,
      "heart_rate_average_since": <time_stamp_string>
  }
  ```
  where
  + `<patient_id>` is the patient medical record number,
  + `<time_stamp_string>` is a string containing a date/time following the
  format as shown by the example "2018-03-09 11:00:36".  
  As above, the patient_id may be sent as an integer or a string, and not 
  necessarily in the same format as previously sent.  The
  heart_rate_average_since will be a string containing a date and time in the 
  format shown.
  This POST should return the average, as an integer, of all the heart rates that have been
  posted for the specified patient since the given date/time.  Note that
  the given time stamp could be any time, and not necessarily the time of a 
  previous heart rate.  The integer average should be returned as a JSON string.
  
* `GET /api/patients/<attending_username>` returns information on all the 
patients of the attending physician with the given `attending_username`.  This
route should return a list of dictionaries, in a JSON string, where each 
  dictionary in the list represents data from a patient of this physician.  
  The patient dictionaries should be in the following format:
  ```
  {
      "patient_id": <patient_id>,
      "last_heart_rate": <heart_rate_integer>,
      "last_time": <time_stamp_string>,
      "status": <status_string>
  }
  ```
  where
  + `<patient_id>` is the patient medical record number,
  + `<heart_rate_integer>` the most recent heart rate as an integer 
    (ex., `100`)
  + `<time_stamp_string>` is a string containing a date/time following the
  format as shown by the example "2018-03-09 11:00:36",  
  + `<status_string>` is either the string `"tachycardic"` or 
    `"not tachycardic"` based on the most recent heart rate.
 
  If no patients exist for a physician, an empty
   list should be returned.  If the `attending_username` does not exist in the
   database, an appropriate error should be returned.

### Logging   
The server should write to a log file when the following events occur:
* A new attending physician is registered.  The log entry should include the
attending username and e-mail.
* A new patient is registered.  The log entry should include the patient ID.
* A heart rate is posted that is tachycardic.  The log entry should include the 
patient ID, the heart rate, and the attending physician e-mail.

### Status Codes & Data Validation
All the above routes should return an appropriate status code depending on
the outcome.  For example, successful requests should return a 200 status code.
Request that are unsuccessful (for example, when the input JSON is incorrect)
should return a 400 (or other appropriate) status code.

All the above routes should have input data validation making sure that
the appropriate keys in JSON inputs exist and that the data types are
correct.  If the input is incorrect, a non-2xx status code should be returned.  

Also, the routes should return the appropriate status codes if a 
request asks for a patient or attending physician that does not exist.  It is 
not appropriate for data
validation and error returns from your server be 500 "Internal Server Error" 
codes caused by exceptions
raised by your server.  You must handle exceptions and return a non-500 error code, 
rather than having the server return a 500 error because it had an unhandled 
exception.

### Modular Code & Testing  
Be sure to write modular code. This means your handler 
functions for routes should be calling other independent functions as 
frequently as possible. All of those other independent functions 
should be tested. As mentioned above, you should also remember to validate user 
inputs that come 
from `request.get_json()` to ensure the right fields exist in the data and 
that they are the right type. These validations should be done in 
functions that can be tested.

You do not have to test the Flask 
handler functions directly (the functions associated with the `@app.route` 
decorator), assuming that they have limited code and primarily call other
functions to do the work.  All of these other functions should be tested.
(In other words, your route functions should do nothing more than receive
the input, call other functions, and return the results).

### Data Storage
For this assignment, your server will need to keep the information
it is sent.  You can choose to store this information by using an in-memory
data structure like Python lists, dictionaries, or classes.  You could also
choose to use an external database.

### E-mail Server
I have set up a server to simulate accessing a third-party webservice for 
sending e-mails.  When your program needs to send an e-mail, it should make
a POST request to the following URL:
```
http://vcm-7631.vm.duke.edu:5007/hrss/send_email
```
**NOTE**: The port is `5007`.  This POST request should be sent a JSON with the
following dictionary contents:
```
{
 "from_email": <from_email_str>,
 "to_email": <to_email_str>,
 "subject": <subject_str>,
 "content": <content_str>
}
```
where `<from_email_str>` is a string containing the e-mail address from which
the message is being sent, `<to_email_str>` is a string containing the e-mail
address to which the message is being sent, `<subject_str>` is a string
containing the subject of the e-mail, and `<content_str>` is a string 
containing the content of the e-mail.

If the request is successful, a string will be returned indicating that the
e-mail was sent and the from and to address.  The status code will be 200.

If the request is bad (i.e., there is a problem with the dictionary being sent, 
or the e-mail addresses in it), a status code of 400 will be returned along
with a string describing the error.
