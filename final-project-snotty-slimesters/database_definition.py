
# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  2 16:59:30 2022

@author: dylancai
"""
from pymodm import MongoModel, fields


class User(MongoModel):
    id = fields.IntegerField(primary_key=True)
    name = fields.CharField()
    record_number = fields.ListField(fields.IntegerField())
    medical_image_names = fields.ListField(fields.CharField())
    medical_image_data = fields.ListField(fields.CharField())
    ECG_data = fields.ListField(fields.CharField())
    heart_rates = fields.ListField(fields.IntegerField())
    record_time = fields.ListField(fields.CharField())
