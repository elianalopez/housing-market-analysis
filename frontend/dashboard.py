import plotly.express as px
import pandas as pd
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

def create_dashboard(df):
    app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

    # Define available options for filters
    zip_options = [{'label': zip_code, 'value': zip_code} for zip_code in df['ZIP Code'].unique()]
    bedroom_options = [{'label': str(bedrooms), 'value': bedrooms} for bedrooms in sorted(df['Bedrooms'].unique())]
    bathroom_options = [{'label': str(bathrooms), 'value': bathrooms} for bathrooms in sorted(df['Bathrooms'].unique())]
    min_date, max_date = df['Date'].min(), df['Date'].max()

    app.layout = dbc.Container([
        html.H1("Real Estate Market Dashboard", className="text-center my-4"),

        dbc.Row([
            dbc.Col([
                html.Label("Select ZIP Code:"),
                dcc.Dropdown(
                    id='zip-dropdown',
                    options=zip_options,
                    multi=True,
                    placeholder="Select ZIP Code(s)"
                )
            ], width=3),
            dbc.Col([
                html.Label("Select Bedrooms:"),
                dcc.Dropdown(
                    id='bedroom-dropdown',
                    options=bedroom_options,
                    multi=True,
                    placeholder="Select Bedrooms"
                )
            ], width=3),
            dbc.Col([
                html.Label("Select Bathrooms:"),
                dcc.Dropdown(
                    id='bathroom-dropdown',
                    options=bathroom_options,
                    multi=True,
                    placeholder="Select Bathrooms"
                )
            ], width=3),
            dbc.Col([
                html.Label("Select Date Range:"),
                dcc.DatePickerRange(
                    id='date-picker-range',
                    start_date=min_date,
                    end_date=max_date,
                    display_format='YYYY-MM-DD'
                )
            ], width=3)
        ], className="mb-4"),

        dcc.Graph(
            id='scatter-plot',
            figure=px.scatter(
                df,
                x='Date',
                y='Closing Price',
                title='Housing Price Trend Over Time',
                labels={'Date': 'Sale Date', 'Closing Price': 'Price'},
                hover_data=['ZIP Code', 'Bedrooms', 'Bathrooms']
            )
        ),
    ])

     # Define the callback to update the graph based on filter selections
    @app.callback(
        Output('scatter-plot', 'figure'),
        [
            Input('zip-dropdown', 'value'),
            Input('bedroom-dropdown', 'value'),
            Input('bathroom-dropdown', 'value'),
            Input('date-picker-range', 'start_date'),
            Input('date-picker-range', 'end_date')
        ]
    )
    def update_graph(selected_zips, selected_bedrooms, selected_bathrooms, start_date, end_date):
        filtered_df = df.copy()

        # Apply filters based on user selections
        if selected_zips:
            filtered_df = filtered_df[filtered_df['ZIP Code'].isin(selected_zips)]
        if selected_bedrooms:
            filtered_df = filtered_df[filtered_df['Bedrooms'].isin(selected_bedrooms)]
        if selected_bathrooms:
            filtered_df = filtered_df[filtered_df['Bathrooms'].isin(selected_bathrooms)]
        if start_date and end_date:
            filtered_df = filtered_df[(filtered_df['Date'] >= start_date) & (filtered_df['Date'] <= end_date)]

        # Create the scatter plot with the filtered data
        fig = px.scatter(
            filtered_df,
            x='Date',
            y='Closing Price',
            title='Housing Price Trend Over Time',
            labels={'Date': 'Sale Date', 'Closing Price': 'Price'},
            hover_data=['ZIP Code', 'Bedrooms', 'Bathrooms']
        )

        return fig

    return app