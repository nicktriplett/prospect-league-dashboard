# 2023 Prospect League Statistics Dashboard

import os
import pathlib
from pathlib import Path
import pandas as pd
import plotly.express as px
import dash
from dash import Dash, html, dcc, Input, Output, dash_table
import dash_bootstrap_components as dbc

# Determine the absolute path to the directory containing this script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Determine the path to the "pages" folder
pages_folder = os.path.join(current_dir, 'pages')

# Loading Data for Visualizations
data_file1 = os.path.join(pages_folder, 'pl_player_hitting_stats.csv')
data_file2 = os.path.join(pages_folder, 'pl_team_hitting_stats.csv')
data_file3 = os.path.join(pages_folder, 'pl_player_pitching_stats.csv')
data_file4 = os.path.join(pages_folder, 'pl_team_pitching_stats.csv')

player_hitting_stats = pd.read_csv(data_file1)
player_hitting_stats

team_hitting_stats = pd.read_csv(data_file2)
team_hitting_stats

player_pitching_stats = pd.read_csv(data_file3)
player_pitching_stats

team_pitching_stats = pd.read_csv(data_file4)
team_pitching_stats

# Instantiating the Dashboard
app = Dash(__name__,external_stylesheets=[dbc.themes.JOURNAL],use_pages=True)
server = app.server
app.title = 'Prospect League Dashboard'

# The Dashboard Layout
app.layout = dbc.Container(
    children=[
        # Page Navigation
        dbc.NavbarSimple(
            brand='Prospect League Dashboard',
            children=[
                dbc.NavItem(dbc.NavLink('Home',href='/')),
                dbc.DropdownMenu(
                    children=[
                        dbc.DropdownMenuItem('Player Hitting',href='/phitting'),
                        dbc.DropdownMenuItem('Team Hitting',href='/thitting'),
                    ],
                    nav=True,
                    in_navbar=True,
                    label="Hitting Data"
                ),
                dbc.DropdownMenu(
                    children=[
                        dbc.DropdownMenuItem('Player Pitching',href='/ppitching'),
                        dbc.DropdownMenuItem('Team Pitching',href='/tpitching'),
                    ],
                    nav=True,
                    in_navbar=True,
                    label="Pitching Data"
                ),
                dbc.DropdownMenu(
                    children=[
                        dbc.DropdownMenuItem(dbc.NavLink('About Me',href='/aboutme'))
                    ],
                    nav=True,
                    in_navbar=True,
                    label="About"
                ),
            ],
            color='info',
            dark=True,
            style={'backgroundColor':'info','color':'black'},
            ],
            color='info',
            dark=True,
        ),

        # Page Content
        dash.page_container,
    ],
    fluid=True,
    class_name='px-0'
)


# run the app
if __name__ == '__main__':
    app.run_server(debug=True)
