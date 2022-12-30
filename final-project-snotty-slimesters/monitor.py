import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import filedialog
import requests
from database_definition import User
import json
import base64
import io
import matplotlib.image as mpimg


def main_window():
    """ Defines main montior window of GUI

    The function creates the widgets and layout for the main window of the
    Database entry GUI.  After the root window is defined, each widget is
    created and added to the Grid Layout Manager.  For widgets that will
    receive some sort of input, tkinter.StringVars are created to hold that
    input.  Some widgets have "command" functions linked to them, and those
    command functions can be found as "sub-functions" of this function.

    This GUI creates a widget for the user to select the medical record that
    they would like to view. Then it updates with the latest information
    uploaded to this record. The user can also choose to select ECG data
    to compare to this and can view stored medical images. The user has the
    option to save any of the images locally.

    Returns:
        None
    """
    def update_id_list():
        """ Gets list of newest medical records from server

        This function gets a list of the medical records from
        the server which is accessing the mongodb. It then puts
        these in list of and creates an option menu with the the
        results. The times of the uploaded ECG records are then
        retreived from the server and put in an option menu.
        The same is done for medical images. Then afer function
        is used to call this function again to repeat the process
        in 30 seconds.

        Returns:
            None
        """
        id_list, code = get_all_ids()
        if code == 200 and len(id_list) > 0:
            drop = ttk.OptionMenu(root, clicked, *id_list)
            time_list_strip = get_time_list(time_list.get())
            drop_time = ttk.OptionMenu(root, clicked_time, *time_list_strip)
            drop_time.configure(width=6)
            med_im_list, code = get_med_img_names(patient_id.get())
            drop_med_im = ttk.OptionMenu(root, clicked_med_im, *med_im_list)
            drop_med_im.configure(width=6)
        root.after(30000, update_id_list)

    show_ECG_done = False

    def save_file(b64_string):
        """ Convert base64 string to file and save locally

        This function opens a save as window where the user is prompted
        for the name for the file to be saved as. If a file name is
        selected, the function then calls a separate function which
        saves this string.

        Returns:
            None
        """
        file = filedialog.asksaveasfile(mode='w', defaultextension=".jpg")
        if file:
            b64_string_to_file(b64_string, file.name)

    def update_monitor():
        """ Show latest ECG data and retrieve options for comparison

        When user chooses a patient they would like to view, this function
        gets the heart rate, time, and ecg image of the latest upload, if
        this exists. If more records exist, the user can also both
        choose to select ECG data to compare to this and view stored medical
        images. The user has the option to save any of the images locally.
        When this function is called all of these functionalities become
        available if there are records to show. The variable to save the
        image locally is also set in this function to be used later to save
        the image.

        Returns:
            None
        """
        # show save button
        patient_id.set(clicked.get())
        record_number_label.config(textvariable=patient_id)
        name, code = get_patient_name(patient_id.get())
        if name:
            name_val.set(name)
        hr, code = get_hr(patient_id.get())
        if hr:
            latest_hr = hr[-1]
        else:
            latest_hr = "No heart rate uploaded"
        hr_val.set(str(latest_hr) + " bpm")
        if get_ecg_times(patient_id.get())[1] == 200 and\
           len(get_ecg_times(patient_id.get())[0]) > 0:
            print(get_ecg_times(patient_id.get())[0])
            button_time.grid(column=3, row=2)
            ecg_img = get_ecg_image(patient_id.get(), -1)
            ecg_label.configure(image=ecg_img)
            ecg_label.image = ecg_img
            save_latest_ecg_btn.grid(column=1, row=9)
            time_list.set(get_ecg_times(patient_id.get())[0])
            time_list_strip = get_time_list(time_list.get())
            drop_time = ttk.OptionMenu(root, clicked_time, time_list_strip[0],
                                       *time_list_strip)
            drop_time.configure(width=6)
            drop_time.grid(column=2, row=2)
            latest_time.set("Uploaded at " + time_list_strip[-1])
            latest_time_label.grid(column=0, row=7)
            b64_string_ecg.set(get_ecg(patient_id.get())[0][-1])

        med_im_list, med_im_list_code = get_med_img_names(patient_id.get())
        if med_im_list_code == 200 and len(med_im_list) > 0:
            button_med_im.grid(column=2, row=12)
            drop_med_im = ttk.OptionMenu(root, clicked_med_im, med_im_list[0],
                                         *med_im_list)
            drop_med_im.grid(column=2, row=11)
            drop_med_im.configure(width=6)

    def update_ecg():
        """ Update GUI when comparison ECG image is chosen by user

        The function is called when a time is chosen from the list
        of available ECG time stamps for comparison to the latest
        record. When a time is chosen, the heart rate, image and
        option to save the image locally are displayed. The variable to
        save the image locally is also set in this function to be
        used later to save the image.

        Returns:
            None
        """
        # If there are ECG records uploaded
        if get_ecg_times(patient_id.get())[1] == 200 and\
           len(get_ecg_times(patient_id.get())[0]) > 0:

            save_comp_img_btn.grid(column=4, row=9)
            ecg_time = clicked_time.get()
            comp_record_number_label.set("Uploaded at " + ecg_time)
            ecg_index = get_time_list(time_list.get()).index(ecg_time)
            hr, code = get_hr(patient_id.get())
            paired_hr = hr[ecg_index]
            paired_hr_val.set(str(paired_hr) + " bpm")
            ecg_img_comp = get_ecg_image(patient_id.get(), ecg_index)
            ecg_comp_label.configure(image=ecg_img_comp)
            ecg_comp_label.image = ecg_img_comp
            b64_string_ecg_comp.set(get_ecg(patient_id.get())[0][ecg_index])

    def update_med_im():
        """ Update GUI when medical image is selected by user

        The function is called when a medical image is chosen
        from the list of available medical image names retreived
        from the database. When an image is chosen, the name,
        image, and button to save the image locally appear. The
        variable used to save the image locally is set in this
        function to be used later to save the image.

        Returns:
            None
        """
        save_med_im_btn.grid(column=3, row=15)
        med_im_name = clicked_med_im.get()
        med_im_name_var.set(med_im_name[-15:])
        med_im_index = get_med_img_names(patient_id
                                         .get())[0].index(med_im_name)
        med_img = get_med_image(patient_id.get(), med_im_index)
        med_im_label.configure(image=med_img)
        med_im_label.image = med_img
        b64_string_med_image.set(get_med_img_str(patient_id.get())
                                 [0][med_im_index])

    # Define Main Window
    root = tk.Tk()
    root.title("Blood Donor Database Window")
    root.geometry("1400x700")
    # Use the line above if you want to define window to a particular size.
    patient_id = tk.StringVar()
    # Title Label
    ttk.Label(root, text="Monitoring Station").grid(column=0, row=0,
                                                    columnspan=2,
                                                    sticky=tk.W)

    # Name Widgets
    ttk.Label(root, text="Medical Record Number:").grid(column=0, row=1,
                                                        sticky='e')
    # get options from mongodb
    id_list, code = get_all_ids()
    clicked = tk.StringVar()
    if code == 200 and len(id_list) > 0:
        drop = ttk.OptionMenu(root, clicked, id_list[0], *id_list)
        drop.grid(column=0, row=2)
        button = ttk.Button(root, text="Update Monitor",
                            command=update_monitor)
        button.grid(column=1, row=2)
    record_number_label = ttk.Label(root, text=" ")
    record_number_label.grid(column=1, row=1, sticky='w')

    # name label
    name_val = tk.StringVar()
    name_val.set("")
    ttk.Label(root, text="Name: ").grid(column=0, row=3, sticky='e')
    name_label = ttk.Label(root, textvariable=name_val).grid(column=1, row=3,
                                                             sticky='w')

    # Latest HR
    hr_val = tk.StringVar()
    hr_val.set("")
    ttk.Label(root, text="Latest Heart Rate: ").grid(column=0, row=5,
                                                     sticky='e')
    hr_label = ttk.Label(root, textvariable=hr_val).grid(column=1, row=5,
                                                         sticky='w')

    # Latest ECG
    ttk.Label(root, text="ECG").grid(column=0, row=6)
    latest_time = tk.StringVar()
    latest_time_label = ttk.Label(root, textvariable=latest_time)
    b64_string_ecg = tk.StringVar()
    ecg_label = ttk.Label(root, image=None)
    ecg_label.grid(column=1, row=6, rowspan=3)
    save_latest_ecg_btn = tk.Button(root, text="Save ECG Image",
                                    command=lambda:
                                    save_file(b64_string_ecg.get()))

    # Drop down to view other ECG
    ttk.Label(root, text="Compare to Historic ECG: ").grid(column=2, row=1,
                                                           sticky='e')
    paired_hr_val = tk.StringVar()
    paired_hr_val.set("")
    ttk.Label(root, text="ECG Comparison Heart Rate: ").grid(column=3, row=5,
                                                             sticky='e')
    paired_hr_label = ttk.Label(root, textvariable=paired_hr_val)
    paired_hr_label.grid(column=4, row=5, sticky='w')
    ttk.Label(root, text="ECG Comparison").grid(column=3, row=6)
    comp_record_number_label = tk.StringVar()
    comp_ecg_label = ttk.Label(root, textvariable=comp_record_number_label)
    comp_ecg_label.grid(column=3, row=7, sticky="w")
    time_list = tk.StringVar()
    clicked_time = tk.StringVar()
    button_time = ttk.Button(root, text="Compare ECG", command=update_ecg)
    b64_string_ecg_comp = tk.StringVar()
    ecg_comp_label = tk.Label(root, image=None)
    ecg_comp_label.grid(column=4, row=6, rowspan=3, sticky='w')
    save_comp_img_btn = tk.Button(root, text="Save Comparison Image",
                                  command=lambda:
                                  save_file(b64_string_ecg_comp.get()))

    # View Saved Medical Image
    tk.Label(root, text="View Medical Image").grid(column=2, row=10)
    clicked_med_im = tk.StringVar()
    button_med_im = ttk.Button(root, text="Show Medical Image",
                               command=update_med_im)

    b64_string_med_image = tk.StringVar()
    med_im_name_var = tk.StringVar()
    med_im_name_var.set("")
    med_im_name_label = ttk.Label(root, textvariable=med_im_name_var)
    med_im_name_label.grid(column=3, row=11)
    b64_string_med_im = tk.StringVar()
    med_im_label = ttk.Label(root, image=None)
    med_im_label.grid(column=3, row=12, rowspan=3)
    save_med_im_btn = tk.Button(root, text="Save Medical Image",
                                command=lambda:
                                save_file(b64_string_med_image.get()))

    # Start recurring function call
    root.after(30000, update_id_list)

    # Activate GUI Loop (should always be the last command in this function)
    root.mainloop()


def get_patient_name(patient_id):
    """ Get patient name by patient ID from server

        The function uses the patient ID to make a get request
        to the server. The server then retrieves the name
        associated with this ID. It returns this as a string
        and a status code.

    Args:
        patient_id (str): medical record ID

    Returns:
        str: the text of the request (name or error )
    """
    r = requests.get("http://vcm-29737.vm.duke.edu:5000/get_name_by_id/"
                     + str(patient_id))
    return r.text, r.status_code


def get_hr(patient_id):
    """ Get heart rate by patient ID from server

        The function uses the patient ID to make a get request
        to the server. The server then retrieves the heart rate
        records associated with this ID. It returns this as a
        json list. The function then reads this and returns the
        result as a list and the status code as an integer.

    Args:
        patient_id (str): medical record ID

    Returns:
        list: list of heart rates (strings)
        int: status code (200 is OK, 400 is Bad Request)
    """
    r = requests.get("http://vcm-29737.vm.duke.edu:5000/get_hr/"
                     + str(patient_id))
    return r.json(), r.status_code


def get_ecg(patient_id):
    """ Get ecg image strings by patient ID from server

        The function uses the patient ID to make a get request
        to the server. The server then retrieves the ECG images,
        encoded as a base64 string, associated with this ID.
        The server returns a json list. The function then reads
        this and returns the result as a list of base64 images
        and a status code as an integer

    Args:
        patient_id (str): medical record ID

    Returns:
        list: list of base64 encoded ECG images (strings)
        int: status code (200 is OK, 400 is Bad Request)
        """
    r = requests.get("http://vcm-29737.vm.duke.edu:5000/get_ecg/"
                     + str(patient_id))
    return r.json(), r.status_code


def get_ecg_times(patient_id):
    """ Use patient ID to get times that ECG records were recorded

        The function uses the patient ID to make a get request
        to the server. The server then retrieves the list of all
        times that an ECG record was saved to the database. The
        server responds to this request with a json list which is
        then read by the function into a list of strings. The
        status code of the request is also returned as an integer.

    Args:
        patient_id (str): medical record ID

    Returns:
        list: list of ecg times (strings)
        int: status code (200 is OK, 400 is Bad Request)
    """
    r = requests.get("http://vcm-29737.vm.duke.edu:5000/get_ecg_times/"
                     + str(patient_id))
    if r.status_code == 200:
        return r.json(), 200
    else:
        return r.text, 400


def get_med_img_names(patient_id):
    """ Use patient ID to get names of medical images uploaded

        The function uses the patient ID to make a get request
        to the server. The server then retrieves the list of all
        names of medical records that were saved to the database.
        The server responds to the request with a json list which is
        then read by the function into a list of strings. The
        status code of the request is also returned as an integer.

    Args:
        patient_id (str): medical record ID

    Returns:
        list: list of medical image names from databse (strings)
        int: status code (200 is OK, 400 is Bad Request)
    """
    r = requests.get("http://vcm-29737.vm.duke.edu:5000/get_med_img_names/"
                     + str(patient_id))
    if r.status_code == 200:
        return r.json(), 200
    else:
        return r.text, 400


def get_med_img_str(patient_id):
    """ Use patient ID to get base64 string of medical images uploaded

        The function uses the patient ID to make a get request
        to the server. The server then retrieves the list of all
        names of medical images that were saved to the database.
        The server responds to the request with a json list which is
        then read by the function into a list of base64 string encoded
        versions of the images. The status code of the request is also
        returned as an integer.

    Args:
        patient_id (str): medical record ID

    Returns:
        list: list of medical images from databse in base64 encoding
              (strings)
        int: status code (200 is OK, 400 is Bad Request)
    """
    r = requests.get("http://vcm-29737.vm.duke.edu:5000/get_med_img/"
                     + str(patient_id))
    if r.status_code == 200:
        return r.json(), 200
    else:
        return r.text, 400


def convert_base64_tkinter(b64_string):
    """ Convert base64 encoded image to tkinter image

        This function uses the base64 to tkinter encoding
        from the image toolbox code in the class repository.
        The image is also resized to fit within the GUI.
        This produces a tkinter image that can be shown in a
        label object

    Args:
        patient_id (str): medical record ID

    Returns:
        ImageTk.PhotoImage object: tkinter image object
            decoding of base64 string
    """
    image_bytes = base64.b64decode(b64_string)
    image_buf = io.BytesIO(image_bytes)
    img_ndarray = mpimg.imread(image_buf, format='JPG')
    image_obj = Image.fromarray(img_ndarray)
    x_size, y_size = image_obj.size
    new_y = 200
    new_x = new_y * x_size / y_size
    image_obj = image_obj.resize((round(new_x), round(new_y)))
    tk_image = ImageTk.PhotoImage(image_obj)
    return tk_image


def get_ecg_image(patient_id, ind):
    """ Use patient ID and record index to get ECG tk image

        This function first calls the get_ecg function which
        uses the patient_id to get from the server the ECG image
        strings

    Args:
        patient_id (str): medical record ID
        ind (int): index of ECG image to be retrieved

    Returns:
        list: list of medical image names from databse (strings)
        int: status code (200 is OK, 400 is Bad Request)
    """
    b64_string, code = get_ecg(patient_id)
    tk_image = convert_base64_tkinter(b64_string[ind])
    return tk_image


def get_all_ids():
    """ Get all medical record IDs from the database

        This function makes a request to the server to get all
        IDs that are stored in the database, each corresponding
        to a medical record. This is sent as a json list of
        strings and a status code. This status code is returned
        as an integer

    Returns:
        list: list of medical record IDs from databse (strings)
        int: status code (200 is OK, 400 is Bad Request)
    """
    r = requests.get("http://vcm-29737.vm.duke.edu:5000/get_all_ids")
    if r.status_code == 200:
        return r.json(), 200
    else:
        return r.text, 400


def b64_string_to_file(b64_string, filename):
    """ Convert Base64 string to image and save file locally

        This function uses a package (base64) to decode
        a base64 string. This image data is then written
        to a file with the name inputted.

    Args:
        b64_string (str): base64 version of image
        filename (str): filename to write file to

    Returns:
        None
    """
    image_bytes = base64.b64decode(b64_string)
    with open(filename, "wb") as out_file:
        out_file.write(image_bytes)
    return None


def file_to_b64_string(filename):
    """ Convert image file to base64 ecoded image string

        This function opens an image file and decodes this
        data into a base64 string. Then returns this string.

    Args:
        filename (str): filename to read file from

    Returns:
        str: base64 encoding of image from file
    """
    with open(filename, "rb") as image_file:
        b64_bytes = base64.b64encode(image_file.read())
    b64_string = str(b64_bytes, encoding='utf-8')
    return b64_string


def get_med_image(patient_id, ind):
    """ Get medical image string, decode, create tkinter im

        This function calls a function which gets all the
        base64 encoded medical images associated with one
        medical record. Then it calls another function to
        decode the image that is at the index desired. This
        function returns a tkinter image.

    Args:
        patient_id (str): medical record ID
        ind (int): index of medical image to be retrieved

    Returns:
        ImageTk.PhotoImage: tkinter object medical image
    """
    b64_string, code = get_med_img_str(patient_id)
    tk_image = convert_base64_tkinter(b64_string[ind])
    return tk_image


def get_time_list(time_list_input):
    """ Convert string list of times to list

        This function takes a string of a list of times.
        It splits this list by comma and strips the leading
        and trailing parentheses from them. It then returns
        these strings as a list

    Args:
        time_list_input (str): string list of times of ECGs

    Returns:
        list: list of strings of times of ECGs
    """
    time_list_convert = time_list_input.split(', ')
    time_list_strip = []
    for time_entry in time_list_convert:
        time_list_strip.append(time_entry.strip('()'))
    return time_list_strip


if __name__ == '__main__':
    main_window()
