# Thrillville Thrillbillies Dashboard

import pandas as pd
import plotly.express as px
import dash
from dash import Dash, html, dcc, Input, Output, dash_table
import dash_bootstrap_components as dbc

player_hitting_stats = pd.read_csv(r"C:\Users\Nick Triplett\OneDrive\Documents\Thrillville Thrillbillies\pl_player_hitting_stats.csv")
team_hitting_statistics = pd.read_csv(r"C:\Users\Nick Triplett\OneDrive\Documents\Thrillville Thrillbillies\pl_team_hitting_stats.csv")
player_pitching_statistics = pd.read_csv(r"C:\Users\Nick Triplett\OneDrive\Documents\Thrillville Thrillbillies\pl_player_pitching_stats.csv")
team_pitching_statistics = pd.read_csv(r"C:\Users\Nick Triplett\OneDrive\Documents\Thrillville Thrillbillies\pl_team_pitching_stats.csv")

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
