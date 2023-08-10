# Thrillville Thrillbillies Dashboard

import pathlib
from pathlib import Path
import pandas as pd
import plotly.express as px
import dash
from dash import Dash, html, dcc, Input, Output, dash_table
import dash_bootstrap_components as dbc

main_file_path = pathlib.Path(__file__)
parent_folder = main_file_path.parent

data_file1 = parent_folder / 'pl_player_hitting_stats.csv'
data_file1.is_file()
player_hitting_stats = pd.read_csv(data_file1)
player_hitting_stats

data_file2 = parent_folder / 'pl_team_hitting_stats.csv'
team_hitting_stats = pd.read_csv(data_file2)
team_hitting_stats

data_file3 = parent_folder / 'pl_player_pitching_stats.csv'
player_pitching_stats = pd.read_csv(data_file3)
player_pitching_stats

data_file4 = parent_folder / 'pl_team_pitching_stats.csv'
team_pitching_stats = pd.read_csv(data_file4)
team_pitching_stats

# Instantiating the Dashboard
dashboard = Dash(__name__,external_stylesheets=[dbc.themes.JOURNAL],use_pages=True)
server = app.server
dashboard.title = 'Prospect League Dashboard'

# The Dashboard Layout
dashboard.layout = dbc.Container(
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
    dashboard.run_server(debug=True)
server=dashboard.server
