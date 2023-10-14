# About Page

import os
import pathlib
from pathlib import Path
import pandas as pd
import plotly.express as px
import dash
from dash import Dash, html, dcc, Input, Output, dash_table
import dash_bootstrap_components as dbc

dash.register_page(__name__)

layout = html.Div(
    children=[
        html.H1('About Me',className='text-center text-dark mt-3 mb-2 fs-1'),
        dbc.Row([
            dbc.Col(
                html.Img(
                    src=dash.get_asset_url('my-image.jpg'),
                    style={
                        'width':'250px',
                        'height':'375px',
                        'margin':'auto',
                        'vertical-align':'top',
                        'object-fit':'contain'}
                ),
                width={'size': 2},
                className='d-flex justify-content-center align-items-center'
            ),
            ],
            justify='center'
        ),
        html.P("Hey! My name is Nick Triplett, and I’m the creator of this dashboard! I’m 22 years old, I’m from Southern Illinois, and I’m a current graduate student striving to make a dream come true. Oh, and I’m a HUGE sports fan (no, really… I might be the biggest sports fan I know).",className='text-center text-dark mt-3 mb-2 fs-6'),
        html.P("Growing up, my sports background wasn’t generated through self-competition, but rather inherited through watching occasional events. When I was five years old, my dad introduced me to the world of sports through NASCAR. After watching the final moments of the 2007 Daytona 500, I became hooked to sports, and I never looked back. Since that moment, I’ve found passion in watching St. Louis Blues hockey, keeping ties with prominent sports, such as football, basketball, and world competitions, and learning more about sports around the world. But if there’s one sport that’s controlled my heart, it’s baseball. From being introduced to Albert Pujols, Jim Edmonds, and the 2006 St. Louis Cardinals, my fandom and curiosity for the sport has only increased. I didn’t really know what I wanted to be when I was younger, but I knew that I wanted sports to play a large role in my life.",className='text-center text-dark mt-3 mb-2 fs-6'),
        html.P("In high school, I finally decided that I wanted to work in the sports industry. I became a student-manager for my school’s basketball team, broadcasted many kinds of sporting events, hosted a sports talk show, and even volunteered for collegiate competitions. But after reflecting on all of those opportunities, I wasn’t sure if any of those types of positions was my true calling. What I was sure about was that there was one thing that always garnered my attention when working in these functions (and just from sports in general): the numbers associated with sports. I recognized in college that I was more focused on sports numbers and trends than anything else.",className='text-center text-dark mt-3 mb-2 fs-6'),
        html.P("This led me to pursue a career in analytics. Since then, I received a Bachelor’s degree in Business Analytics from Southern Illinois University – Carbondale (graduating with a 4.00 GPA), and I’ve started working towards an online Master’s degree in Business Analytics from there. During this time, I’ve learned how to clean and manipulate data, formulate code, perform statistical analysis, and apply these resources and information to businesses and their various problems and questions",className='text-center text-dark mt-3 mb-2 fs-6'),
        html.P("All of this prepared me for the summer of 2023, when I received my first opportunity to work alongside a sports team. I became a data analytics intern for the Thrillville Thrillbillies, a summer wood-bat college baseball team located in the Prospect League. There, I experienced what it takes to successfully start up a baseball team and what work is necessary to ensure that everything runs smoothly for an organization. I gained knowledge in working with baseball software, improved my analytical skills, and had significant involvement in operational and technical work. I was welcomed by a great group of individuals running the team, connected with many people across the organization, and made friendships that will last a lifetime.",className='text-center text-dark mt-3 mb-2 fs-6'),
        dbc.Row([
            dbc.Col(
                html.Img(
                    src=dash.get_asset_url('thrillbillies-operation-image.jpg'),
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
        html.P("All of this leads me to who and where I am today. As I continue working towards my degree and bettering my analytical knowledge and skills, I remain committed and motivated towards my dream. Ultimately, I desire to become a data analyst of business analyst in the professional sports industry, where I can not only positively impact the organization that I work for, but also share my love of sports to others. I’m so thankful for God, as well as my family and friends, for establishing who I am today, and I’m excited to see what comes next!",className='text-center text-dark mt-3 mb-2 fs-6'),
        html.P("Colossians 3:23-24",className='text-center text-dark mt-3 mb-2 fs-6'),
    ]
)
