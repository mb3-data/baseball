# -*- coding: utf-8 -*-
"""
Created on Sat Jul 29 08:26:07 2023

@author: berar
"""

import dash
from dash import html, dcc

dash.register_page(__name__)

layout = html.Div(children=[
    html.H1(children='This is our Archive page'),

    html.Div(children='''
        This is our Archive page content.
    '''),

])