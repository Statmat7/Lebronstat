#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 27 17:11:23 2018

@author: statmat7
"""

from flask_wtf import FlaskForm
from wtforms import SelectField,SubmitField

class StartForm(FlaskForm):
   lebron_status= SelectField('Lebron Status', choices = [('In', 'In'), ('Out', 'Out')])
   flat_raise= SelectField('Flat Raise', choices = [('None', 'None'),('$2 Million', '$2 Million') ])
   scale_raise= SelectField('Scale Raise', choices = [('None', 'None'),('10%', '10%')])
   reset_salaries= SelectField('Reset Salaries', choices = [('No', 'No'),('Yes', 'Yes')])
   submit = SubmitField("Update Data")

 
    

   