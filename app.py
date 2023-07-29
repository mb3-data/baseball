# -*- coding: utf-8 -*-
"""
Created on Mon Jul 24 20:41:16 2023

@author: berar

Graph the AL West Race by day
Data Source
https://www.baseball-reference.com/teams
Schedule/results

"""

from dash import Dash, html, dcc, dash_table
import dash
import pandas as pd
import numpy as np
import requests
import io
from plotly.offline import plot
from dash.dependencies import Input, Output, State
import plotly.express as px
import os

app = Dash(__name__, use_pages=True)

app.layout = html.Div([
	html.H1('Multi-page app with Dash Pages'),

    html.Div(
        [
            html.Div(
                dcc.Link(
                    f"{page['name']} - {page['path']}", href=page["relative_path"]
                )
            )
            for page in dash.page_registry.values()
        ]
    ),

	dash.page_container
])

if __name__ == '__main__':
	app.run(debug=True)
