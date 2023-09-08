# Dashboard Home Page

import os
import pathlib
from pathlib import Path
import pandas as pd
import plotly.express as px
import dash
from dash import Dash, html, dcc, Input, Output, dash_table
import dash_bootstrap_components as dbc

dash.register_page(__name__, path='/')

layout = html.Div(
    children=[
        html.H1('2023 Prospect League Dashboard',className='text-center text-dark mt-3 mb-2 fs-1'),
        html.P("Welcome to the 2023 Prospect League Baseball Statistics Dashboard! This dashboard has been meticulously created to present a comprehensive outlook of the 2023 Prospect League baseball season. This dashboard serves as a tool for baseball enthusiasts, analysts, and recordkeepers to explore and analyze season statistics. The goal of this dashboard is to expand upon the simplicities of the league to better understand and communicate the league and its performances among players and teams. Data has been gathered from the Prospect League website, where it was (and still is being) expanded and enhanced for further analysis and visualization through Excel and Python. Inside this dashboard, you'll discover a rich collection of statistics presented in intuitive graphs and charts. From player performance trends to team comparisons, we've curated a range of insights that will help you appreciate the talent and dynamics of the 2023 Prospect League season. To get started, use the navigation tab on the top of the page to explore different aspects of the league. I hope that you find this dashboard to be informative and satisfactory towards your needs! Enjoy your exploration of the 2023 Prospect League baseball season!",className='text-center text-dark mb-4 mt-4 fs-6'),
        dbc.Row([
            dbc.Col(
                html.Img(
                    src=dash.get_asset_url('prospect-league-logo-image.png'),
                    style={
                        'width':'100%',
                        'vertical-align':'top',
                        'object-fit':'contain'}
                ),
                width={'size': 5}
            ),
            ],
            justify='center'
        ),
        html.Div(
            children=[
                'Image and Favicon Source: ',
                html.A(
                    'Prospect League',
                    href='https://d2o2figo6ddd0g.cloudfront.net/h/p/iwgjhe5gqqzrfm/primary-logo-newimage.png',className='text-info fs-4'
                ),
        ],
        className='text-dark text-center fs-4 mt-3'
        ),
    ]
)
