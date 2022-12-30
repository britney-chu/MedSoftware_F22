#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 27 16:06:00 2022

@author: dylancai
"""

import requests


out_data = {"username": "Lee.J", "email": "bukatea@gmail.com",
            "phone": "614-649-1987"}
out_data_interval = {"patient_id": 1,
                     "heart_rate": 50000}
r = requests.get("http://vcm-29737.vm.duke.edu:5000/api/status/1")
print(r.status_code)
print(r.text)
