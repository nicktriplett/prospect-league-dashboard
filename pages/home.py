# Dashboard Home Page

import pandas as pd
import plotly.express as px
import dash
from dash import Dash, html, dcc, Input, Output, State
import dash_bootstrap_components as dbc

dash.register_page(__name__, path='/')

layout = html.Div(
    children=[
        html.H1('2023 Prospect League Dashboard',className='text-center text-dark mt-3 mb-2 fs-1'),
    ]
)