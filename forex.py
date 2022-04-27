import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import datetime as dt


class Forex:

    def __init__(self):
        pass

    @staticmethod
    def foreign_exchange():
        st.header("Foreign Exchange")
        # Reading the file
        filename = "Dataset/Fx/fx.csv"
        df = pd.read_csv(filename)
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

        # Getting the dates
        dates = pd.to_datetime(df['Trade Date'])

        # getting the user date input
        range_start = tuple(dates)[0].to_pydatetime()
        range_end = tuple(dates)[-1].to_pydatetime()
        date_range = st.slider("Adjust the date range", range_start, range_end, (range_start, range_end))

        # Extracting the data based on the date
        df['Trade Date'] = dates
        specific_data = df[(df['Trade Date'] >= date_range[0]) & (df['Trade Date'] <= date_range[-1])]

        # Extracting all important values
        result = {}
        variables = list(df['Currency'].unique())

        names = {}

        # Initializing the different figures
        buy_fig = make_subplots()
        sell_fig = make_subplots()

        for item in variables:
            # Getting the data for a specific currency
            item_specific_data = specific_data[(specific_data['Currency'] == item)]

            # Extracting the individual values from the data extracted
            date_values = item_specific_data['Trade Date']
            buy_values = item_specific_data['Buying']
            sell_values = item_specific_data['Selling']
            mid_values = item_specific_data['Mid Rate']

            # Attaching a pairs code to the name of the currency - result can be seen in the legend
            names[item] = (item + ' (' + list(item_specific_data['Pairs code'].unique())[0] + ')')

            buy_trace = go.Scatter(x=date_values, y=buy_values, name=names[item])
            sell_trace = go.Scatter(x=date_values, y=sell_values, name=names[item])

            buy_fig.add_trace(buy_trace)
            sell_fig.add_trace(sell_trace)

            result[item] = {'date values': date_values, 'buy_values': buy_values, 'sell_values': sell_values,
                            'mid_values': mid_values}

        buy_info = st.container()
        sell_info = st.container()
        year_compare = st.container()

        with buy_info:
            buy_fig.update_xaxes(title_text="Date")
            buy_fig.update_yaxes(title_text="Amount - (GHS)")

            buy_fig.update_layout(title="Buying Rate", title_x=0.5)
            st.plotly_chart(buy_fig, use_container_width=True)

        with sell_info:
            sell_fig.update_xaxes(title_text="Date")
            sell_fig.update_yaxes(title_text="Amount - (GHS)")

            sell_fig.update_layout(title="Selling Rate", title_x=0.5)
            st.plotly_chart(sell_fig, use_container_width=True)

        with year_compare:
            # Getting a list of years from the data
            years = list(set([year.to_pydatetime().year for year in tuple(dates)]))
            year_range = st.slider("Select a range", years[0], years[-1], (years[0], years[-1]))

            ll, lm, m, rm, rr = st.columns(5)
            start_date = dt.datetime(year_range[0], 1, 1)
            end_date = dt.datetime(year_range[-1], 12, 31)

            # Getting specific data for the period selected by the user
            year_range_data = df[(df['Trade Date'] >= start_date) & (df['Trade Date'] <= end_date)]
            currency_choice = ll.selectbox("Select a Currency", df['Currency'].unique())

            i = year_range[0]
            # Initializing the plot for the year comparison
            year_compare_fig = make_subplots()
            while i <= year_range[-1]:
                # intializing the january 1st and december 31st as the minimum and maximum dates
                temporary_start_date = dt.datetime(i, 1, 1)
                temporary_end_date = dt.datetime(i, 12, 31)

                # Getting data between the min and max for a particular year
                temporary_specific_data = df[
                    (df['Trade Date'] >= temporary_start_date) & (df['Trade Date'] <= temporary_end_date) & (
                            df['Currency'] == currency_choice)]
                mid_values = temporary_specific_data['Mid Rate']
                temporary_date_values = temporary_specific_data['Trade Date']

                # Creating a list of datetime objects - 2016 is used as a standard because it is a leap year
                temporary_x_values = [dt.datetime(2016, mydate.month, mydate.day) for mydate in
                                      list(temporary_date_values)]

                trace = go.Scatter(x=temporary_x_values, y=mid_values, name=str(i))
                year_compare_fig.add_trace(trace)
                i += 1

            year_compare_fig.update_xaxes(title_text="Date")
            year_compare_fig.update_yaxes(title_text="Amount - (GHS)")

            year_compare_fig.update_layout(title="Year-on-Year Comparison of '" + currency_choice + "'", title_x=0.5)
            year_compare_fig.update_layout(xaxis=dict(tickformat="%B-%d"))
            st.plotly_chart(year_compare_fig, use_container_width=True)