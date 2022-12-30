#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 25 20:50:37 2022

@author: dylancai
"""

import sys
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import filedialog
from pymodm import connect, MongoModel, fields
import ssl
from database_definition import User
from datetime import datetime
import requests
import base64
sys.path.insert(0, '/Users/dylancai/BME547_repo/ecg-analysis-dylcai85/')
medical_image_string = ""
medical_image_name = ""
ecg_image_string = ""


def reset_globals():
    """
    sets the global variables for medical image name, string, and
    ecg string to empty strings

    uses global keyword to edit the strings

    Args:
        none

    Returns:
        returns true if done correctly
    """
    global medical_image_string
    medical_image_string = ""
    global medical_image_name
    medical_image_name = ""
    global ecg_image_string
    ecg_image_string = ""
    return True


def upload_cmd(patient_name, patient_id, heart_rate,
               mi_string, ei_string, mi_name,
               timestamp):
    """
    makes a post request to the server with a dictionary that contains all of
    the necessary information for a patient

    uses requests and the server url to make the post request

    Args:
        in_data: dictionary that has patient_name, patinet_id, heart_rate,
        medical_image, ecg_image, medical_image_name, and timestamp
        patient_name is a string
        patient_id is an int
        heart_rate is an int
        medical_image, ecg_image, medical_image_name, and timestamp
        are all strings

    Returns:
        string and 200 status code if done correctly
    """
    if patient_id != 0 and patient_id:
        out_data = {"name": patient_name, "id": patient_id,
                    "heart_rate": heart_rate,
                    "medical_image": mi_string,
                    "ecg_image": ei_string,
                    "m_i_name": mi_name,
                    "timestamp": timestamp}
        r = requests.post("http://vcm-29737.vm.duke.edu:5000/new_patient",
                          json=out_data)
        reset_globals()
        return r.text, r.status_code
    elif patient_id == 0 or patient_id is None:
        return "medical record number was not entered"


def convert_file_to_b64(filename):
    """
    converts image file to b64 string

    uses base64 functions to encode the image into a string

    Args:
        filename: the filename of the image, code opens and converts
        given the filename

    Returns:
        b64 string of the given file
    """
    with open(filename, "rb") as image_file:
        b64_bytes = base64.b64encode(image_file.read())
    b64_string = str(b64_bytes, encoding='utf-8')
    return b64_string


def main_window():
    """
    defines the gui and displays all the necessary fields for a user to enter
    in their patient data. Not all fields need to be filled before uploading.
    The only necessary field is the medical record number

    uses tkinter and PIL to display and process all data

    Args:
        none

    Returns:
        none
    """
    def ok_cmd():
        """
        activates the upload command when the ok button is pressed,
        also prints out the entered data from the gui. Also updates the status
        label on the gui to reflect the status message of the upload

        uses try except blocks to catch the instances when one datafield is not
        entered which should be allowed for the gui

        Args:
            none

        Returns:
            none
        """
        # get data from interface
        patient_name = patient_name_entry.get()
        try:
            patient_id = patient_id_entry.get()
        except tk.TclError:
            patient_id = 0
        try:
            heart_rate = heart_rate_entry.get()
        except tk.TclError:
            heart_rate = 0
        timestamp = str(datetime.now())
        # call other testable functions to do all the work
        msg = upload_cmd(patient_name, patient_id, heart_rate,
                         medical_image_string,
                         ecg_image_string, medical_image_name, timestamp)
        # update gui based on results of other functions
        print(patient_name)
        print(patient_id)
        print(heart_rate)
        print(medical_image_string)
        print(ecg_image_string)
        print(medical_image_name)
        print(timestamp)
        print("Clicked Ok button")
        status_label.configure(text=msg)

    def cancel_cmd():
        """
        destroys the gui and turns it off

        uses root.destroy command to cancel the gui

        Args:
            none

        Returns:
            none
        """
        root.destroy()

    def clear_cmd():
        """
        clears the entries in the gui, including the images that may have been
        selected

        uses .delete and .configure functions to clear out the entryfields

        Args:
            none

        Returns:
            none
        """
        # name.pack()
        name_clear.delete(0, tk.END)
        # pid.pack()
        pid_clear.delete(0, tk.END)
        heart_rate_entry.set(0)
        image_label.configure(image='')
        image_label1.configure(image='')
        print("GUI cleared")

    def picture_button_cmd():
        """
        opens a filedialog box and allows user to select a medical image
        from local computer and resizes the iamge to fit into the gui display

        uses imagetk and tkinter features to process the image and display it

        Args:
            none

        Returns:
            none
        """
        # new_file = "painting_pics/pic1"
        new_file = filedialog.askopenfilename()
        if new_file:
            global medical_image_string
            medical_image_string = convert_file_to_b64(new_file)
            global medical_image_name
            medical_image_name = new_file
            print("Filename: {}".format(new_file))
            pil_image = Image.open(new_file)
            xsize, ysize = pil_image.size
            new_y = 200
            new_x = new_y * xsize / ysize
            pil_image = pil_image.resize((round(new_x), round(new_y)))
            tk_image = ImageTk.PhotoImage(pil_image)
            image_label.configure(image=tk_image)
            image_label.image = tk_image

    def ecg_upload():
        """
        opens a filedialog box and allows user to select a csv file with an ecg
        from local computer. Calls the gui_command from ecg_analysis script
        to calculate the heart rate of the ecg file and sets it in the gui
        display. The function also plots the ecg data and displays it in the
        gui.

        uses imagetk and tkinter features to process the image and display it,
        also uses gui_command from ecg_analysis to do the necessary
        calculations

        Args:
            none

        Returns:
            none
        """
        from ecg_analysis import gui_command
        filename = filedialog.askopenfilename()
        if filename:
            patient_hr = gui_command(filename)
            new_file = "ecg_plot.jpeg"
            global ecg_image_string
            ecg_image_string = convert_file_to_b64(new_file)
            pil_image1 = Image.open(new_file)
            xsize, ysize = pil_image1.size
            new_y = 200
            new_x = new_y * xsize / ysize
            pil_image1 = pil_image1.resize((round(new_x), round(new_y)))
            tk_image1 = ImageTk.PhotoImage(pil_image1)
            image_label1.configure(image=tk_image1)
            image_label1.image = tk_image1
            heart_rate_entry.set(round(patient_hr))

    root = tk.Tk()
    root.title("Patient-side GUI")
    # root.geometry("600x300")
    ttk.Label(root, text="Medical Information for Patient").grid(column=0,
                                                                 row=0,
                                                                 columnspan=2,
                                                                 sticky="w")
    # patient name entry
    ttk.Label(root, text="Patient Name:").grid(column=0, row=1)
    patient_name_entry = tk.StringVar()
    name_clear = ttk.Entry(root, width=50, textvariable=patient_name_entry)
    name_clear.grid(column=1, row=1)

    # medical record number entry
    patient_id_entry = tk.IntVar()
    ttk.Label(root, text="Patient Medical Record Number:").grid(column=0,
                                                                row=2,
                                                                sticky="e")
    # heart rate entry
    ttk.Label(root, text="ECG Heart Rate:").grid(column=1, row=4, sticky="e")
    heart_rate_entry = tk.IntVar()
    heart_rate_clear = ttk.Label(root, width=10, textvariable=heart_rate_entry)
    heart_rate_clear.grid(column=2, row=4)

    pid_clear = ttk.Entry(root, textvariable=patient_id_entry)
    pid_clear.grid(column=1, row=2, sticky="w")
    # ok and and cancel and clear and load picture button
    ttk.Button(root, text="Ok", command=ok_cmd).grid(column=2, row=5)
    ttk.Button(root, text="Clear", command=clear_cmd).grid(column=2, row=6)
    ttk.Button(root, text="Cancel", command=cancel_cmd).grid(column=3, row=6)
    picture_button = ttk.Button(root, text="Load Medical Image",
                                command=picture_button_cmd)
    picture_button.grid(column=0, row=3)

    # ecg analysis button

    ecg_button = ttk.Button(root, text="Load ECG data",
                            command=ecg_upload)
    ecg_button.grid(column=0, row=4)

    image_label = ttk.Label(root)

    image_label.grid(column=1, row=3, sticky='w')

    image_label1 = ttk.Label(root)

    image_label1.grid(column=1, row=4, sticky='w')

    # create status label
    status_label = ttk.Label(root, text="Status")
    status_label.grid(column=0, row=8)

    root.mainloop()


if __name__ == '__main__':
    main_window()
