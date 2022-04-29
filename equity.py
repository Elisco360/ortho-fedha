import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
import datetime


class Equity:
    def __init__(self):
        pass

    @staticmethod
    def equities():

        def dateToString(date):
            date = str(date).split(' ')
            date = date[0]
            date = date.split('-')
            date.reverse()
            date = '-'.join(date)
            return date

        def stringToDate(date):
            date = date.split('-')
            date = datetime.date(int(date[2]), int(date[1]), int(date[0]))

            return date

        def monthsFromInception(prices, dates):
            months = []
            for date in dates:
                if date[3:] not in months:
                    months.append(date[3:])
            return months

        def VAMI(prices, dates):
            returns = monthlyReturnsFromInception(prices, dates)
            values = []
            for value in returns:
                vami = (1 + (value / 100)) * 1000
                values.append(vami)

            return values

        def change(startPrice, currentPrice):
            currentPrice = float(currentPrice)
            startPrice = float(startPrice)
            return (((currentPrice) - startPrice) / startPrice) * 100

        def monthlyReturnsFromInception(prices, dates):
            # print(f"prices:{prices}\ndates:{dates}")
            index_value = 0
            startPrice = prices[index_value]
            days = []
            returns = []
            currentMonth = dates[0][3:5]
            for date in dates:
                if date[3:5] == currentMonth:
                    days.append(prices[dates.index(date)])
                else:
                    try:
                        returns.append(change(startPrice=startPrice, currentPrice=days[-1]))
                    except:
                        returns.append(None)
                    days = []
                    currentMonth = date[3:5]
                    days.append(prices[dates.index(date)])

            returns.append(change(startPrice=startPrice, currentPrice=days[-1]))
            return returns

        def vami(specific_dates, share_prices):
            prices = share_prices
            dates = [dateToString(date) for date in specific_dates]
            dates = dates[:len(prices)]
            months = monthsFromInception(prices=prices, dates=dates)
            vami_vals = VAMI(dates=dates, prices=prices)
            return (months, vami_vals)

        # Reading data from the csv file
        st.header('Equity')
        st.success("Equity, typically referred to as shareholders' equity (or owners' equity for privately held companies),\
                   represents the amount of money that would be returned to a company's shareholders if all of the assets were\
                       liquidated and all of the company's debt was paid off in the case of liquidation.\
                       Reference: https://www.investopedia.com/terms/e/equity.asp ")
        file = "Dataset/Equity/eqty.csv"
        # list_of_files = os.listdir('Data/Equity/')
        df = pd.read_csv(file)
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

        # Getting a list of variables from the csv file
        columns = list(df.columns)

        all_prices = list(df[columns[1]])
        all_dates = list(df[columns[0]])

        # Ensuring all dates are in the format dd-mm-yyyy
        for i in range(len(all_dates)):
            split_date = [all_dates[i][:2], all_dates[i][3:5], all_dates[i][6:]]
            all_dates[i] = '-'.join(split_date)

        # Getting the first and last dates of the data in the list
        start_date = stringToDate(all_dates[0])
        end_date = stringToDate(all_dates[-1])

        # Selecting a date range of data to consider date_range = st.slider("Select a date range for file 1: "+str(
        # file),start_date,end_date,(start_date,end_date))
        try:
            try:
                df['Trade Date'] = pd.to_datetime(df['Trade Date'], format='%d-%m-%Y').dt.date
            except:
                df['Trade Date'] = pd.to_datetime(df['Trade Date'], format='%d/%m/%Y').dt.date
        except:
            st.error("Please ensure that the column 'Trade Date' is present and all dates are in the format dd/mm/yyyy")
            return 0

        multi_share_comparison = st.expander('Multi Share Comparison')
        single_share_comparison = st.expander('Single Share Data')

        # Displays Graphs for multiple EQUITIES. Variables include:
        # - Closing Price
        # - Total shares traded
        # - Total value traded
        with multi_share_comparison:
            # Range slider for the range of dates to look at
            multi_date_range = st.slider("Select a date range ", start_date, end_date, (start_date, end_date))

            # Extracting all the share codes available in the data
            all_share_codes = list(df['Share code'].unique())

            # Removing TOTAL because it is not a share
            try:
                all_share_codes.pop(all_share_codes.index('TOTAL'))
            except:
                pass

            # Allowing the user to select shares to compare
            shares_to_include = st.multiselect("Select share codes", all_share_codes, default=all_share_codes)

            # Extracting the data from the specified date range
            multi_specific_data = df[(df['Trade Date'] >= multi_date_range[0]) & (df['Trade Date'] <= multi_date_range[-1])]

            multi_specific_dates = list(multi_specific_data['Trade Date'].unique())
            closing_price_fig = make_subplots()
            total_shares_fig = make_subplots()
            total_value_fig = make_subplots()
            vami_fig = make_subplots()

            for share_code in shares_to_include:
                vami_error = False
                if share_code == 'TOTAL':
                    pass

                # Extracting all data for a specific share
                share_data = multi_specific_data[(multi_specific_data['Share code'] == share_code)]

                share_prices = list(share_data['Closing Price vwap (GHS)'])  # Extracting the closing prices
                share_value = list(share_data['Total value traded (GHS)'])  # Extracting the values for total value traded
                share_volume = list(share_data['Total shares traded'])  # Extracting the values for total volume traded
                try:
                    (mymonths, vami_values) = vami(multi_specific_dates, share_prices)
                except:
                    vami_error = True

                if vami_error != True: vami_trace = go.Scatter(x=mymonths, y=vami_values, name=share_code)
                prices_trace = go.Scatter(x=multi_specific_dates, y=share_prices, name=share_code)
                value_trace = go.Scatter(x=multi_specific_dates, y=share_value, name=share_code)
                volume_trace = go.Scatter(x=multi_specific_dates, y=share_volume, name=share_code)

                closing_price_fig.add_trace(prices_trace)
                total_shares_fig.add_trace(volume_trace)
                total_value_fig.add_trace(value_trace)
                if vami_error != True: vami_fig.add_trace(vami_trace)

            closing_price_fig.update_xaxes(title_text="Date")
            closing_price_fig.update_yaxes(title_text="Amount - (GHS)")
            closing_price_fig.update_layout(title={'text': 'Closing Price', 'x': 0.5})

            total_shares_fig.update_xaxes(title_text="Date")
            total_shares_fig.update_yaxes(title_text="Volume")
            total_shares_fig.update_layout(title={'text': 'Total Shares Traded', 'x': 0.5})

            total_value_fig.update_xaxes(title_text="Date")
            total_value_fig.update_yaxes(title_text="Amount - (GHS)")
            total_value_fig.update_layout(title={'text': 'Total Value Traded', 'x': 0.5})

            vami_fig.update_xaxes(title_text="Month")
            vami_fig.update_yaxes(title_text="Amount - (GHS)")
            vami_fig.update_layout(title={'text': 'Value Added Monthly Index', 'x': 0.5})

            st.plotly_chart(closing_price_fig, use_container_width=True)
            st.plotly_chart(total_value_fig, use_container_width=True)
            st.plotly_chart(total_shares_fig, use_container_width=True)
            st.plotly_chart(vami_fig, use_container_width=True)

            # PIE CHART
            # Using data from the last date in the date range.
            # Extracting all the values for total shares traded for each share
            # Creating a pie chart using that data
            pie_date_range = st.slider("Select a date range for the pie chart", start_date, end_date,
                                       (start_date, end_date))
            pie_chart_df = df[(df['Trade Date'] >= pie_date_range[0]) & (df['Trade Date'] <= pie_date_range[-1])]

            names = shares_to_include

            volume = []
            for item in names:
                specific_share_data = pie_chart_df[(pie_chart_df['Share code'] == item)]
                total_volume = sum(list(specific_share_data['Total shares traded']))

                try:
                    volume.append(float(total_volume))
                except:
                    volume.append(None)

            result = {'Name': names, 'Volume': volume}
            result = pd.DataFrame(result)
            pie_start_date = dateToString(pie_date_range[0])
            pie_end_date = dateToString(pie_date_range[-1])

            pie_fig = px.pie(result, values="Volume", names='Name')
            pie_fig.update_traces(textposition='inside', textinfo='percent+label')
            pie_fig.update_layout(title={'text': f'Total shares traded from {pie_start_date} to {pie_end_date}', 'x': 0.5})
            st.plotly_chart(pie_fig, use_container_width=True)

        with single_share_comparison:
            single_date_range = st.slider("Select a date range", start_date, end_date, (start_date, end_date))
            single_specific_data = df[
                (df['Trade Date'] >= single_date_range[0]) & (df['Trade Date'] <= single_date_range[-1])]
            single_specific_dates = list(single_specific_data['Trade Date'].unique())

            ll, lm, m, rm, rr = st.columns(5)
            selected_share = ll.selectbox('Select a share code', all_share_codes)

            # options = ['Closing Price','Total Shares Traded','Total Value Traded']
            options = ['Closing Price', 'Total Value Traded']
            selected_options = st.multiselect('Select metrics', options, default=options)
            share_data = single_specific_data[(single_specific_data['Share code'] == selected_share)]
            single_fig = make_subplots(specs=[[{"secondary_y": True}]])

            if 'Closing Price' in selected_options:
                share_prices = list(share_data['Closing Price vwap (GHS)'])
                single_fig.add_trace(go.Scatter(x=single_specific_dates, y=share_prices, name='closing price'),
                                     secondary_y=False, )

            # if 'Total Shares Traded' in selected_options:
            #     share_volume = list(share_data['Total shares traded'])
            #     single_fig.add_trace(go.Scatter(x=single_specific_dates,y=share_volume,name='total shares traded'),secondary_y=True,)

            if 'Total Value Traded' in selected_options:
                share_value = list(share_data['Total value traded (GHS)'])
                single_fig.add_trace(go.Scatter(x=single_specific_dates, y=share_value, name='total value traded'),
                                     secondary_y=True, )

            # Add figure title
            single_fig.update_layout(title={'text': selected_share, 'x': 0.5})

            # Set x-axis title
            single_fig.update_xaxes(title_text="Date")

            # Set y-axes titles
            single_fig.update_yaxes(title_text="Closing Price - (GHS)", secondary_y=False)
            single_fig.update_yaxes(title_text="Total Value - (GHS)", secondary_y=True)
            # single_fig.update_yaxes(title_text="Volume", secondary_y=True)

            st.plotly_chart(single_fig, use_container_width=True)



