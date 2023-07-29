# -*- coding: utf-8 -*-
"""
Created on Sat Jul 29 08:25:38 2023

@author: berar
"""

import dash
from dash import html, dcc

dash.register_page(__name__, path='/')

layout = html.Div(children=[
    html.H1(children='This is our Home page'),

    html.Div(children='''
        This is our Home page content.
    '''),

])