import math
import datetime as dt
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px


class Bonds:

    def __init__(self):
        pass

    @staticmethod
    def bonds_section():
        with st.sidebar:
            st.title("Bonds Sections")
            sections = st.selectbox("Select a section", ["Fixed Income Secondary Market", "Primary Issuances",
                                                         "Primary Issuances - TTA", "Fixed Income Yield and Volume",
                                                         "Debt Investor Holdings"])

        def sortBonds(bonds):
            lookup = {}
            interim = []
            for item in bonds:
                if item[-1] == 's':
                    value = item.replace('s', '')
                    if value not in lookup:
                        lookup[value] = [item]
                    else:
                        lookup[value].append(item)

                if 'ESLA' in item:
                    value = item[-2:]
                    if value not in lookup:
                        lookup[value] = [item]
                    else:
                        lookup[value].append(item)

                interim.append(value)

            interim = list(set(interim))
            interim.sort()
            result = []
            for item in interim: result += lookup[item]
            return result

        def dateToString(date):
            date = str(date).split(' ')
            date = date[0]
            date = date.split('-')
            date.reverse()
            date = '-'.join(date)
            return date

        def fixed_income():
            st.header('Fixed Income')
            st.info('A bond is a fixed-income instrument that represents a loan made by an investor to a borrower (typically corporate or governmental).\
                Reference: https://www.investopedia.com/terms/b/bond.asp')

            # File path filepath
            file = "Dataset/Bonds/bbns.csv"

            df = pd.read_csv(file)
            df = df.loc[:, ~df.columns.str.contains('^Unnamed')]


            try:
                try:
                    df['Trade Date'] = pd.to_datetime(df['Trade Date'], format='%dd-%mm-%YYYY').dt.date
                except:
                    df['Trade Date'] = pd.to_datetime(df['Trade Date'], format='%d/%m/%Y').dt.date
            except:
                st.error(
                    "Please ensure that the column 'Trade Date' is present and all dates are in the format dd/mm/yyyy")
                return 0

            df['Month'] = pd.DatetimeIndex(df['Trade Date']).month
            df['Year'] = pd.DatetimeIndex(df['Trade Date']).year

            # Dictionaries converting from numbers to months and vice versa
            num_to_month = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug', 9: 'Sep',
                            10: 'Oct', 11: 'Nov', 12: 'Dec'}
            month_to_num = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6, 'Jul': 7, 'Aug': 8, 'Sep': 9,
                            'Oct': 10, 'Nov': 11, 'Dec': 12}

            # Getting the list of tenors
            all_tenors = list(set(list(df['Tenor'])))

            all_tenors = sortBonds(all_tenors)

            tenors = st.multiselect('Select Tenors', all_tenors, default=all_tenors)

            # Extracting all the months present in the data
            all_months = list(df['Month'])
            all_years = list(df['Year'])
            month_choices = []

            # Generating a list of month year pairs. eg Sep 2020, Oct 2020
            for i in range(len(all_months)):
                month_value = num_to_month[all_months[i]] + ' ' + str(all_years[i])
                if month_value not in month_choices:
                    month_choices.append(month_value)

            line_chart = st.container()
            pie_chart = st.container()

            with line_chart:
                # Allowing the user to select a month range
                ll, lm, m, rm, rr = st.columns(5)
                list_of_start_months = [] + month_choices
                list_of_start_months.reverse()

                start_month_year = ll.selectbox("Start month", list_of_start_months)
                end_month_year = lm.selectbox("End month", list_of_start_months)

                if month_choices.index(end_month_year) < month_choices.index(start_month_year):
                    st.error(
                        "Please ensure that the selected 'End month' does not come before the selected 'Start month'")
                    return 0

                specific_months = month_choices[
                                  month_choices.index(start_month_year):month_choices.index(end_month_year) + 1]
                results = {'Names': tenors, 'Month': specific_months, 'Values': []}

                for item in results['Names']:
                    tenor_count = []
                    for month in specific_months:
                        specific_month = month_to_num[month.split(' ')[0]]
                        specific_year = int(month.split(' ')[1])
                        specific_data = df[(df['Year'] == specific_year) & (df['Month'] == specific_month)]
                        tenor_data = specific_data[(specific_data['Tenor'] == item)]
                        tenor_count.append(len(list(tenor_data['Tenor'])))
                    results['Values'].append(tenor_count)

                # Plotting a Bar chart
                fig = make_subplots()
                for i in range(len(tenors)):
                    trace = go.Scatter(x=results['Month'], y=results['Values'][i], name=results['Names'][i])
                    fig.add_trace(trace)

                fig.update_layout(title={'text': f"Traded Volumes", 'x': 0.5})
                fig.update_xaxes(title_text="Trade Month")
                fig.update_yaxes(title_text="Volume")
                # fig.update_layout(width=1300, height=500)
                st.plotly_chart(fig, use_container_width=True)

            with pie_chart:
                # PLOTTING A PIE CHART
                pll, plm, pm, prm, prr = st.columns(5)

                # Allowing the user to select a month range
                list_of_start_months = [] + month_choices
                list_of_start_months.reverse()

                pie_start_month_year = pll.selectbox("Pie chart Start month ", list_of_start_months)
                pie_end_month_year = plm.selectbox("Pie chart End month ", list_of_start_months)

                if month_choices.index(pie_end_month_year) < month_choices.index(pie_start_month_year):
                    st.error(
                        "Please ensure that the selected 'End month' does not come before the selected 'Start month'")
                    return 0

                # Extracting the data for the specified range
                pie_specific_months = month_choices[
                                      month_choices.index(start_month_year):month_choices.index(end_month_year) + 1]
                results = {'Names': tenors, 'Month': pie_specific_months, 'Values': []}

                for item in results['Names']:
                    pie_tenor_count = []
                    for month in pie_specific_months:
                        pie_specific_month = month_to_num[month.split(' ')[0]]
                        pie_specific_year = int(month.split(' ')[1])
                        pie_specific_data = df[(df['Year'] == pie_specific_year) & (df['Month'] == pie_specific_month)]
                        pie_tenor_data = pie_specific_data[(pie_specific_data['Tenor'] == item)]
                        pie_tenor_count.append(len(list(pie_tenor_data['Tenor'])))
                    results['Values'].append(sum(pie_tenor_count))

                names = results['Names']
                Values = results['Values']
                pie_chart_result = {'Names': names, 'Values': Values}
                pie_result = pd.DataFrame(pie_chart_result)

                pie_fig = px.pie(pie_result, values="Values", names='Names')
                pie_fig.update_traces(textposition='inside', textinfo='percent+label')
                pie_fig.update_layout(
                    title={'text': f"Tenor Volumes between {pie_start_month_year} and {pie_end_month_year}", 'x': 0.45})
                st.plotly_chart(pie_fig, use_container_width=True)

        def primary_issuances():
            st.header('Primary Issuances')
            # File path filepath
            # filename = "Data/Bond/Debt Investor Holdings.csv"
            filename = "Dataset/Bonds/pis.csv"
            df = pd.read_csv(filename)
            df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

            try:
                try:
                    df['Trade Date'] = pd.to_datetime(df['Trade Date'], format='%d-%m-%Y').dt.date
                except:
                    df['Trade Date'] = pd.to_datetime(df['Trade Date'], format='%d/%m/%Y').dt.date
            except:
                pass

            # Extracting the list of securites from the csv file
            all_columns = list(df.columns)
            all_securities = list(set(df[all_columns[2]]))  # list of all securities
            date_column_name = all_columns[0]  # Name of the dates column
            all_dates = list(df[date_column_name])

            # Sorting the bonds into ascending order
            yr = []
            d = []
            for item in all_securities:
                if item[-1] == 'R':
                    temp = item.split(' ')
                    try:
                        yr.append(int(temp[0]))
                    except:
                        yr.append(int(temp[1]))

                elif item[-1] == 'D':
                    temp = item.split('D')
                    try:
                        d.append(int(temp[0]))
                    except:
                        d.append(int(temp[1]))
            yr.sort()
            d.sort()

            new_yr = [str(item) + ' YR' for item in yr]
            new_d = [str(item) + 'D' for item in d]

            all_securities = new_d + new_yr
            # End of bond sorting

            line_chart = st.container()
            with line_chart:
                (start_date, end_date) = st.slider('Adjust the range', all_dates[0], all_dates[-1],
                                                   (all_dates[0], all_dates[-1]))
                # ll,lm,m,rm,rr = st.columns(5)
                selected_securities = st.multiselect('Select', all_securities, default=all_securities)
                fig = make_subplots()

                for selected_security in selected_securities:
                    specific_data = df[(df[date_column_name] >= start_date) & (df[date_column_name] <= end_date) & (
                                df[all_columns[2]] == selected_security)]
                    interest_rates = [float(item) for item in list(specific_data[all_columns[-1]])]
                    specific_dates = list(specific_data[date_column_name])

                    # Sorting dates
                    date_to_rate = {}
                    for i in range(len(specific_dates)):
                        date_to_rate[specific_dates[i]] = interest_rates[i]

                    specific_dates.sort()
                    sorted_interest_rates = [date_to_rate[specific_dates[i]] for i in range(len(specific_dates))]
                    # End of sorting dates

                    fig.add_trace(go.Scatter(x=specific_dates, y=sorted_interest_rates, name=selected_security))
                fig.update_xaxes(title="Date")
                fig.update_yaxes(title="Yield - (%)")
                fig.update_layout(title={'text': f"Tenor Yields over time", 'x': 0.5})
                st.plotly_chart(fig, use_container_width=True)

        def tta():
            st.header('Primary Issuances: Tendered, Target, Accepted')

            '''File path filepath'''
            filename = "Dataset/Bonds/tta.csv"

            df = pd.read_csv(filename)
            df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

            try:
                try:
                    df['Date'] = pd.to_datetime(df['Date'], format='%d-%m-%Y').dt.date
                except:
                    df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y').dt.date
            except:
                st.error(
                    "Please ensure that the column 'Trade Date' is present and all dates are in the format dd/mm/yyyy")
                return 0

            num_to_month = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug', 9: 'Sep',
                            10: 'Oct', 11: 'Nov', 12: 'Dec'}
            month_to_num = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6, 'Jul': 7, 'Aug': 8, 'Sep': 9,
                            'Oct': 10, 'Nov': 11, 'Dec': 12}
            all_variables = list(df.columns)
            all_variables.pop(0)
            selected_variables = st.multiselect('Variables', all_variables, default=all_variables)
            ll, lm, m, rm, rr = st.columns(5)
            # Creating new month and year columns in the dataframe
            df['Month'] = pd.DatetimeIndex(df['Date']).month
            df['Year'] = pd.DatetimeIndex(df['Date']).year

            # Extracting all the months present in the data
            all_months = list(df['Month'])
            all_years = list(df['Year'])
            month_choices = []

            for i in range(len(all_months)):
                try:
                    month_value = num_to_month[all_months[i]] + ' ' + str(int(all_years[i]))
                    if month_value not in month_choices:
                        month_choices.append(month_value)
                except:
                    pass

            list_of_start_months = [] + month_choices
            list_of_start_months.reverse()

            start_month_year = ll.selectbox("Start month", list_of_start_months)

            end_month_year = lm.selectbox("End month", list_of_start_months)
            specific_months = month_choices[
                              month_choices.index(start_month_year):month_choices.index(end_month_year) + 1]
            if month_choices.index(end_month_year) < month_choices.index(start_month_year):
                st.error("Please ensure that the selected 'End month' does not come before the selected 'Start month'")
                return 0

            variable_values = {}
            for variable in selected_variables:
                variable_values[variable] = []

            for month in specific_months:
                specific_month = month_to_num[month.split(' ')[0]]
                specific_year = int(month.split(' ')[1])
                specific_data = df[(df['Year'] == specific_year) & (df['Month'] == specific_month)]

                for variable in selected_variables:
                    variable_values[variable].append(sum(list(specific_data[variable])))

            results = {'Months': specific_months}
            for variable in selected_variables:
                results[variable] = variable_values[variable]

            # Plotting a Bar chart
            fig = make_subplots()
            for i in selected_variables:
                trace = go.Scatter(x=results['Months'], y=results[i], name=i)
                fig.add_trace(trace)

            fig.update_xaxes(title_text="Trade Month")
            fig.update_yaxes(title_text="Amount - GHS(M)")
            st.plotly_chart(fig, use_container_width=True)

        def fixed_income_yield_volume():
            # filepath file path
            yield_filename = 'Dataset/Bonds/yields.csv'
            volume_filename = 'Dataset/Bonds/volumes.csv'

            # Opening the file and removing Unnamed columns
            yield_df = pd.read_csv(yield_filename)
            yield_df = yield_df.loc[:, ~yield_df.columns.str.contains('^Unnamed')]

            # Opening the file and removing Unnamed columns

            try:
                volume_df = pd.read_csv(volume_filename)
                volume_df = volume_df.loc[:, ~volume_df.columns.str.contains('^Unnamed')]
            except:
                st.error(f"The file, '{volume_filename}', was not found")
                return 0

            # Changing the dates to datetime objects
            try:
                try:
                    yield_df['Date/tenure'] = pd.to_datetime(yield_df['Date/tenure'], format='%d-%m-%Y').dt.date
                except:
                    yield_df['Date/tenure'] = pd.to_datetime(yield_df['Date/tenure'], format='%d/%m/%Y').dt.date
            except:
                st.error(
                    f"Ensure that '{yield_filename}' contains the column 'Date/tenure', and that dates are formatted as dd-mm-yyyy")
                return 0

            try:
                try:
                    volume_df['Date/tenure'] = pd.to_datetime(volume_df['Date/tenure'], format='%d-%m-%Y').dt.date
                except:
                    volume_df['Date/tenure'] = pd.to_datetime(volume_df['Date/tenure'], format='%d/%m/%Y').dt.date
            except:
                st.error(
                    f"Ensure that '{volume_filename}' contains the column 'Date/tenure', and that dates are formatted as dd-mm-yyyy")
                return 0

            # Dictionaries for converting numbers to months and vice versa
            num_to_month = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug', 9: 'Sep',
                            10: 'Oct', 11: 'Nov', 12: 'Dec'}
            month_to_num = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6, 'Jul': 7, 'Aug': 8, 'Sep': 9,
                            'Oct': 10, 'Nov': 11, 'Dec': 12}

            # Getting a list of columns and removing the date columns to get the list of tenors
            yield_all_tenors = list(yield_df.columns)
            yield_all_tenors.pop(0)  # Removing the date column

            volume_all_tenors = list(volume_df.columns)
            volume_all_tenors.pop(0)  # Removing the date column
            volume_all_tenors.pop(-1)  # Removing the total volume column

            # Adding year and month columns
            yield_df['Month'] = pd.DatetimeIndex(yield_df['Date/tenure']).month
            yield_df['Year'] = pd.DatetimeIndex(yield_df['Date/tenure']).year

            volume_df['Month'] = pd.DatetimeIndex(volume_df['Date/tenure']).month
            volume_df['Year'] = pd.DatetimeIndex(volume_df['Date/tenure']).year

            # Extracting all dates, months and years
            yield_all_dates = list(yield_df['Date/tenure'])
            yield_all_years = list(yield_df['Year'])
            yield_all_months = list(yield_df['Month'])

            volume_all_dates = list(volume_df['Date/tenure'])
            volume_all_years = list(volume_df['Year'])
            volume_all_months = list(volume_df['Month'])

            # Creating expanders for viewing multiple and single tenors
            multi_tenor_yield = st.expander('Multi tenor yield data')
            single_tenor_yield = st.expander('Single tenor year-on-year yield data')
            multi_tenor_volume = st.expander('Multi tenor volume data')

            with multi_tenor_yield:
                selected_tenors = st.multiselect('Select Tenors', yield_all_tenors, default=yield_all_tenors)
                multi_tenor_yield_monthly = st.container()
                multi_tenor_yield_yearly = st.container()
                multi_tenor_yield_daily = st.container()

                with multi_tenor_yield_monthly:
                    ll, lm, m, rm, rr = st.columns(5)
                    available_months = []  # All months available in the dataset

                    # Finding and storiing all months available in the dataset
                    for i in range(len(yield_all_months)):
                        month_value = num_to_month[yield_all_months[i]] + ' ' + str(yield_all_years[i])
                        if month_value not in available_months:
                            available_months.append(month_value)

                    # Creating a list of start months the user can select
                    list_of_start_months = [] + available_months
                    list_of_start_months.reverse()  # Reversing the order so the last month available appears first
                    start_month = ll.selectbox("Start month", list_of_start_months)

                    # Creating a list of end months
                    list_of_end_months = available_months[available_months.index(start_month):]

                    end_month = lm.selectbox("End month", list_of_start_months)
                    if available_months.index(end_month) < available_months.index(start_month):
                        st.error(
                            "Please ensure that the selected 'End month' does not come before the selected 'Start month'")
                        return 0

                    # Extracting all months greater between start_month and end_month inclusive
                    specific_months = available_months[
                                      available_months.index(start_month):available_months.index(end_month) + 1]

                    # Creating a dictionary for plotting the graphs
                    result = {'Names': selected_tenors, 'Months': specific_months}

                    # Initializing the arrays corresponding to different tenors to empty
                    for tenor in result['Names']:
                        result[tenor] = []

                    # Appending the yield for each month to the list of their respoective tenors
                    for item in range(len(specific_months)):
                        date_info = specific_months[item].split(
                            ' ')  # Getting the month and the year from a given date value
                        month = month_to_num[date_info[0]]

                        # Filtering out data that is not from the specified month and year
                        specific_month_data = yield_df[
                            (yield_df['Month'] == month) & (yield_df['Year'] == int(date_info[1]))]

                        # Extracting the data for specific tenors and removing the percentage sign
                        for tenor in selected_tenors:
                            specific_tenor_data = list(specific_month_data[tenor])
                            raw_tenor_data = specific_tenor_data
                            all_refined_tenor_data = []
                            for value in raw_tenor_data:
                                try:
                                    refined_value = value.replace("%", '')
                                    all_refined_tenor_data.append(float(refined_value))
                                except:
                                    pass

                            avg = sum(all_refined_tenor_data) / len(raw_tenor_data)
                            result[tenor].append(avg)

                    # Figure for plotting the monthly data
                    multi_monthly_data_fig = make_subplots()
                    for tenor in result['Names']:
                        trace = go.Scatter(x=result['Months'], y=result[tenor], name=tenor)
                        multi_monthly_data_fig.add_trace(trace)

                    multi_monthly_data_fig.update_layout(title={'text': f'Monthly Average Yield Prices', 'x': 0.5})
                    multi_monthly_data_fig.update_xaxes(title_text="Month")
                    multi_monthly_data_fig.update_yaxes(title_text="Yield - (%)")
                    st.plotly_chart(multi_monthly_data_fig, use_container_width=True)

                with multi_tenor_yield_daily:
                    specific_date_range = st.slider('Adjust the date range', yield_all_dates[0], yield_all_dates[-1],
                                                    (yield_all_dates[0], yield_all_dates[-1]))
                    specific_data = yield_df[(yield_df['Date/tenure'] >= specific_date_range[0]) & (
                                yield_df['Date/tenure'] <= specific_date_range[-1])]
                    multi_daily_data_fig = make_subplots()

                    # Extracting the data for specific tenors and removing the percentage sign
                    for item in selected_tenors:
                        raw_yvals = list(specific_data[item])
                        refined_yvals = []
                        for raw_value in raw_yvals:
                            try:
                                new_value = raw_value.replace("%", "")
                                refined_yvals.append(float(new_value))
                            except:
                                refined_yvals.append(raw_value)

                        trace = go.Scatter(x=specific_data['Date/tenure'], y=refined_yvals, name=item)
                        multi_daily_data_fig.add_trace(trace)

                    multi_daily_data_fig.update_layout(title={'text': f'Daily Yield Prices', 'x': 0.5})
                    multi_daily_data_fig.update_xaxes(title_text="Day")
                    multi_daily_data_fig.update_yaxes(title_text="Yield - (%)")
                    st.plotly_chart(multi_daily_data_fig, use_container_width=True)

            with single_tenor_yield:
                ll, lm, m, rm, rr = st.columns(5)
                specific_tenor = ll.selectbox('Select a tenor', yield_all_tenors)
                list_of_years = list(yield_df['Year'].unique())
                years_to_include = st.multiselect('Select years to view', list_of_years, default=list_of_years)

                single_tenor_yield_monthly = st.container()
                single_tenor_yield_daily = st.container()

                with single_tenor_yield_monthly:
                    ll, lm, m, rm, rr = st.columns(5)
                    available_months = list(range(1, 13))

                    result = {'Year': years_to_include,
                              'Months': ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov",
                                         "Dec"]}
                    # Initializing the arrays corresponding to different years to empty
                    for year in result['Year']:
                        result[year] = []

                    # Looping through the months to get extract data from each month
                    for item in range(len(available_months)):
                        month = available_months[item]

                        # Looping through the years to extract data for the month specified above in each year
                        for year in years_to_include:
                            specific_month_data = yield_df[(yield_df['Month'] == month) & (yield_df['Year'] == year)]
                            all_refined_year_data = []
                            # Data for the month and the year specified
                            specific_year_data = list(specific_month_data[specific_tenor])

                            # Extracting the data for the specified tenor for each year and removing the percentage sign
                            try:
                                raw_tenor_data = specific_year_data  # Using the data value for the last day of the month
                            except:
                                raw_tenor_data = None

                            for value in raw_tenor_data:
                                try:
                                    refined_value = float(value.replace("%", ''))
                                    all_refined_year_data.append(refined_value)
                                except:
                                    pass

                            try:
                                avg = sum(all_refined_year_data) / len(all_refined_year_data)
                            except:
                                avg = None
                            result[year].append(avg)

                    # Figure for plotting monthly data
                    single_monthly_fig = make_subplots()
                    for year in result['Year']:
                        trace = go.Scatter(x=result['Months'], y=result[year], name=str(year))
                        single_monthly_fig.add_trace(trace)

                    single_monthly_fig.update_layout(
                        title={'text': f'Monthly Average Yield Prices of {specific_tenor}', 'x': 0.5})
                    single_monthly_fig.update_xaxes(title_text="Month")
                    single_monthly_fig.update_yaxes(title_text="Yield - (%)")
                    st.plotly_chart(single_monthly_fig, use_container_width=True)

                # Year on Year
                with single_tenor_yield_daily:
                    single_daily_fig = make_subplots(shared_xaxes=True)
                    leap_year_dates = pd.date_range(start=dt.date(2020, 1, 1), end=dt.date(2020, 12, 31))
                    for year in years_to_include:
                        xvals = leap_year_dates
                        yvals = []
                        count = 0
                        for item in xvals:
                            last_date = list(yield_df['Date/tenure'])[-1]
                            try:
                                date_data = yield_df[(
                                            pd.to_datetime(yield_df['Date/tenure']).dt.date == dt.date(year, item.month,
                                                                                                       item.day))]
                                value = list(date_data[specific_tenor])[0]
                                value = value.replace("%", '')
                                yvals.append(float(value))
                            except:
                                try:
                                    current_date = dt.date(year, item.month, item.day)
                                except:
                                    current_date = last_date

                                if count != 0 and current_date <= last_date:
                                    yvals.append(yvals[count - 1])
                                else:
                                    yvals.append(None)
                            count += 1

                        xvals = pd.to_datetime(xvals)
                        trace = go.Scatter(x=xvals.strftime("%b-%d"), y=yvals, name=str(year))
                        single_daily_fig.add_trace(trace)

                    single_daily_fig.update_layout(title={'text': f'Daily Yield Prices of {specific_tenor}', 'x': 0.5})
                    single_daily_fig.update_xaxes(title_text="Day")
                    single_daily_fig.update_yaxes(title_text="Yield - (%)")
                    st.plotly_chart(single_daily_fig, use_container_width=True)

            with multi_tenor_volume:
                selected_multi_volume_tenors = st.multiselect('Select Tenors', volume_all_tenors,
                                                              default=volume_all_tenors)

                present_previous_day = st.container()
                volume_piechart = st.container()

                with present_previous_day:
                    specific_date = st.slider('Select a date', volume_all_dates[0], volume_all_dates[-1])
                    result = {'Tenors': selected_multi_volume_tenors, 'Current': [], 'Previous': []}
                    for tenor in result['Tenors']:
                        current_data = volume_df[(volume_df['Date/tenure'] == specific_date)]
                        previous_data = volume_df[(volume_df['Date/tenure'] == specific_date + dt.timedelta(days=-1))]

                        try:
                            current_date_volume = float(list(current_data[tenor])[0])
                        except:
                            current_date_volume = None

                        try:
                            previous_date_volume = float(list(previous_data[tenor])[0])
                        except:
                            previous_date_volume = None

                        result['Current'].append(current_date_volume)
                        result['Previous'].append(previous_date_volume)

                    # Figure for plotting the monthly data
                    multi_tenor_fig = make_subplots()

                    previous_trace = go.Bar(x=result['Tenors'], y=result['Previous'],
                                            name=str(specific_date + dt.timedelta(days=-1)))
                    current_trace = go.Bar(x=result['Tenors'], y=result['Current'], name=str(specific_date))

                    multi_tenor_fig.add_trace(previous_trace)
                    multi_tenor_fig.add_trace(current_trace)

                    multi_tenor_fig.update_layout(title={'text': 'Two-Day Tenor Volumes', 'x': 0.5})
                    multi_tenor_fig.update_xaxes(title_text="Tenor")
                    multi_tenor_fig.update_yaxes(title_text="Volume")
                    st.plotly_chart(multi_tenor_fig, use_container_width=True)

                with volume_piechart:
                    pie_specific_date = st.slider('Select a date range   ', volume_all_dates[0], volume_all_dates[-1],
                                                  (volume_all_dates[0], volume_all_dates[-1]))
                    pie_specific_data = volume_df[(volume_df['Date/tenure'] >= pie_specific_date[0]) & (
                                volume_df['Date/tenure'] <= pie_specific_date[-1])]
                    pie_result = {'Tenors': selected_multi_volume_tenors, 'Total Volume': []}
                    for tenor in pie_result['Tenors']:
                        pie_tenor_data = list(pie_specific_data[tenor])
                        all_raw_tenor_data = [0]

                        for value in pie_tenor_data:
                            try:
                                if math.isnan(float(value)):
                                    float_value = 0
                                else:
                                    float_value = float(value)
                            except:
                                float_value = 0

                            all_raw_tenor_data.append(float_value)

                        total_volume = sum(all_raw_tenor_data)
                        pie_result['Total Volume'].append(total_volume)

                    pie_start_date = dateToString(pie_specific_date[0])
                    pie_end_date = dateToString(pie_specific_date[-1])

                    piechart_df = pd.DataFrame(pie_result)
                    volume_piechart_fig = px.pie(piechart_df, values="Total Volume", names="Tenors")
                    volume_piechart_fig.update_traces(textposition='inside', textinfo='percent+label')
                    volume_piechart_fig.update_layout(
                        title={'text': f"Total Traded Tenor Volumes from '{pie_start_date}' to '{pie_end_date}'",
                               'x': 0.5})
                    st.plotly_chart(volume_piechart_fig, use_container_width=True)

        def debt_investor_holdings():
            st.header('Debt Investor Holdings')
            # File path filepath
            filename = "Dataset/Bonds/dih.csv"

            df = pd.read_csv(filename)
            df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

            try:
                try:
                    df['Date'] = pd.to_datetime(df['Date'], format='%d-%m-%Y').dt.date
                except:
                    df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y').dt.date
            except:
                self.missing_column_error(column='Date', filename=filename)

            # Extracting the list of securites from the csv file
            all_securities = list(df.columns)  # list of all securities and the investor and date column names
            date_column_name = all_securities[0]  # Name of the dates column
            investor_column_name = all_securities[1]  # Name of the column with investors

            # Removing the investor and date column names from the list of securities
            for i in range(2): all_securities.pop(0)
            # Removing the 'Total' column name from the list of securities
            all_securities.pop(-1)

            # Creating month and year columns in the dataframe
            df['Month'] = pd.DatetimeIndex(df['Date']).month
            df['Year'] = pd.DatetimeIndex(df['Date']).year

            num_to_month = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug', 9: 'Sep',
                            10: 'Oct', 11: 'Nov', 12: 'Dec'}
            month_to_num = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6, 'Jul': 7, 'Aug': 8, 'Sep': 9,
                            'Oct': 10, 'Nov': 11, 'Dec': 12}

            # Extracting all the months present in the data
            all_months = list(df['Month'])
            all_years = list(df['Year'])

            # Getting a list of all available months in the dataset
            month_choices = []
            for i in range(len(all_months)):
                month_value = num_to_month[all_months[i]] + ' ' + str(all_years[i])
                if month_value not in month_choices:
                    month_choices.append(month_value)

            # Creating the list of months to choose from
            list_of_start_months = [] + month_choices
            list_of_start_months.reverse()

            single_investor_charts = st.expander('Single Investor Charts')
            single_security_charts = st.expander('Single Security Charts')
            investor_security_charts = st.expander("Single Investor Single Security Waterfall Chart")
            total_chart = st.expander('Total Security Charts')

            with total_chart:

                total_line_chart = st.container()
                total_pie_chart = st.container()

                with total_line_chart:
                    # List of securites selected by the user
                    selected_securities = st.multiselect('', all_securities, default=all_securities)

                    # Columns to hold the start and end date selection boxes
                    ll, lm, m, rm, rr = st.columns(5)
                    # This stores the users choices for start and end months
                    start_month_year = ll.selectbox("Start month", list_of_start_months)
                    end_month_year = lm.selectbox("End month", list_of_start_months)

                    # Checking if the end month comes before the start month and producing an error
                    if month_choices.index(end_month_year) < month_choices.index(start_month_year):
                        st.error(
                            "Please ensure that the selected 'End month' does not come before the selected 'Start month'")
                        return 0

                    # Getting a list of months within the range of the start and end months selected by the user
                    specific_months = month_choices[
                                      month_choices.index(start_month_year):month_choices.index(end_month_year) + 1]

                    # Separating the month and year for the start and end month selected by the user
                    start_month = month_to_num[start_month_year.split(' ')[0]]
                    start_year = int(start_month_year.split(' ')[1])
                    end_month = month_to_num[end_month_year.split(' ')[0]]
                    end_year = int(end_month_year.split(' ')[1])

                    # Getting 'Total' data from within the selected start and end month range
                    specific_data = df[
                        (df[investor_column_name] == 'Total') &
                        (df[date_column_name] >= dt.date(start_year, start_month, 1)) &
                        (df[date_column_name] <= dt.date(end_year, end_month, 1))
                        ]

                    # Extracting the total values for each selected security and storing them in a dictionary
                    total_chart_result = {'Name': selected_securities, 'Months': specific_months, 'Values': []}
                    for security in selected_securities:
                        all_values = list(
                            specific_data[security])  # total values for the selected security selected range
                        total_chart_result['Values'].append(all_values)

                    # LINECHART
                    total_chart_fig = make_subplots()
                    for i in range(len(total_chart_result['Name'])):
                        total_chart_fig.add_trace(go.Scatter(x=total_chart_result['Months'],
                                                             y=total_chart_result['Values'][i],
                                                             name=total_chart_result['Name'][i]))
                    total_chart_fig.update_layout(title={'text': f"Total Debt Investor Holdings", 'x': 0.5})
                    total_chart_fig.update_xaxes(title_text="Month")
                    total_chart_fig.update_yaxes(title_text="Amount - (GHS)")
                    st.plotly_chart(total_chart_fig, use_container_width=True)

                with total_pie_chart:
                    all_investors = list(df[investor_column_name].unique())
                    all_investors.pop(all_investors.index('Total'))

                    # List of investors selected by the user
                    selected_investors = st.multiselect('Select Investors', all_investors, default=all_investors)

                    # columns that contain the select boxes
                    pll, plm, pm, prm, prr = st.columns(5)

                    # Storing the start and end months selected for the pie chart
                    pie_start_month_year = pll.selectbox("Pie chart Start month ", list_of_start_months)
                    pie_end_month_year = plm.selectbox("Pie chart End month", list_of_start_months)

                    # Checking if the end month comes before the start month and throwing an error
                    if month_choices.index(pie_end_month_year) < month_choices.index(pie_start_month_year):
                        st.error(
                            "Please ensure that the selected 'End month' does not come before the selected 'Start month'")
                        return 0

                    # List of monthe within the range of the selected start and end months
                    specific_months = month_choices[month_choices.index(pie_start_month_year):month_choices.index(
                        pie_end_month_year) + 1]

                    # Separating the year and the month from the selected start and the end months
                    pie_start_month = month_to_num[pie_start_month_year.split(' ')[0]]
                    pie_start_year = int(pie_start_month_year.split(' ')[1])
                    pie_end_month = month_to_num[pie_end_month_year.split(' ')[0]]
                    pie_end_year = int(pie_end_month_year.split(' ')[1])

                    # Extracting data within the range of the start and end months
                    specific_data = df[
                        (df[date_column_name] >= dt.date(pie_start_year, pie_start_month, 1)) &
                        (df[date_column_name] <= dt.date(pie_end_year, pie_end_month, 1))
                        ]

                    # Extracing the total values from the 'specific_data'
                    total_pie_result = {'Name': selected_investors, 'Values': []}
                    for investor in selected_investors:
                        investor_total_value = 0
                        specific_investor_data = specific_data[(specific_data[investor_column_name] == investor)]
                        specific_investor_totals = specific_investor_data['Total']
                        for value in specific_investor_totals:
                            try:
                                investor_total_value += value
                            except:
                                continue
                        total_pie_result['Values'].append(investor_total_value)

                    pie_fig = px.pie(total_pie_result, values="Values", names='Name')
                    pie_fig.update_traces(textposition='inside', textinfo='percent+label')
                    pie_fig.update_layout(title={
                        'text': f"Total Holdings of selected investors from {pie_start_month_year} to {pie_end_month_year}",
                        'x': 0.45})
                    st.plotly_chart(pie_fig, use_container_width=True)

            with single_investor_charts:
                single_line_chart = st.container()
                single_pie_chart = st.container()

                with single_line_chart:
                    # Columns containing the select boxes
                    sll, slm, sm, srm, srr = st.columns(5)

                    # List of securities selected by the user
                    single_selected_securities = st.multiselect(' ', all_securities, default=all_securities)
                    # Investor selected by the user
                    single_selected_investor = sll.selectbox('Select Investor', all_investors)
                    # Start month and end month selected by the user
                    single_start_month_year = slm.selectbox(" Start month", list_of_start_months)
                    single_end_month_year = sm.selectbox(" End month", list_of_start_months)

                    # Checking if the end month comes before the start month and throwing an error
                    if month_choices.index(single_end_month_year) < month_choices.index(single_start_month_year):
                        st.error(
                            "Please ensure that the selected 'End month' does not come before the selected 'Start month'")
                        return 0

                    # List of months withing the range of the selected start and end months
                    single_specific_months = month_choices[
                                             month_choices.index(single_start_month_year):month_choices.index(
                                                 single_end_month_year) + 1]

                    # Separating the month and the year for the start and end months
                    single_start_month = month_to_num[single_start_month_year.split(' ')[0]]
                    single_start_year = int(single_start_month_year.split(' ')[1])
                    single_end_month = month_to_num[single_end_month_year.split(' ')[0]]
                    single_end_year = int(single_end_month_year.split(' ')[1])

                    # Extracting data for the selected investor within the start and end month
                    specific_data = df[
                        (df[investor_column_name] == single_selected_investor) &
                        (df[date_column_name] >= dt.date(single_start_year, single_start_month, 1)) &
                        (df[date_column_name] <= dt.date(single_end_year, single_end_month, 1))
                        ]

                    single_result = {'Name': single_selected_securities, 'Months': single_specific_months, 'Values': []}
                    for security in single_selected_securities:
                        # List of security values for the chosen investor within the range of the start and end month
                        single_security_values = list(specific_data[security])
                        single_result['Values'].append(single_security_values)

                    single_fig = make_subplots()
                    for i in range(len(single_result['Name'])):
                        single_fig.add_trace(go.Scatter(x=single_result['Months'],
                                                        y=single_result['Values'][i],
                                                        name=single_result['Name'][i]))

                    single_fig.update_layout(title={'text': f"{single_selected_investor} Holdings", 'x': 0.5})
                    single_fig.update_xaxes(title_text="Month")
                    single_fig.update_yaxes(title_text="Amount - (GHS)")
                    st.plotly_chart(single_fig, use_container_width=True)

                with single_pie_chart:
                    # Columns for the selectboxes
                    psll, pslm, psm, psrm, psrr = st.columns(5)

                    # List of selected securities to view data for
                    pie_single_selected_securities = st.multiselect('  ', all_securities, default=all_securities)

                    # selected investor to view data for
                    pie_single_selected_investor = psll.selectbox(' Select Investor', all_investors)
                    # Selected start and end months
                    pie_single_start_month_year = pslm.selectbox(" Pie chart Start month", list_of_start_months)
                    pie_single_end_month_year = psm.selectbox(" Pie chart End month", list_of_start_months)

                    # Checking if the end month comes before the start month and throwing an error
                    if month_choices.index(pie_single_end_month_year) < month_choices.index(
                            pie_single_start_month_year):
                        st.error(
                            "Please ensure that the selected 'End month' does not come before the selected 'Start month'")
                        return 0

                    # Getting the all the months within the range of the start and end month
                    pie_single_specific_months = month_choices[
                                                 month_choices.index(pie_single_start_month_year):month_choices.index(
                                                     pie_single_end_month_year) + 1]

                    # Separating the month and the year for the selected start and end months
                    pie_single_start_month = month_to_num[pie_single_start_month_year.split(' ')[0]]
                    pie_single_start_year = int(pie_single_start_month_year.split(' ')[1])
                    pie_single_end_month = month_to_num[pie_single_end_month_year.split(' ')[0]]
                    pie_single_end_year = int(pie_single_end_month_year.split(' ')[1])

                    # Getting data for the selected investor within the range of the selected start and end months
                    pie_single_specific_data = df[
                        (df[investor_column_name] == pie_single_selected_investor) &
                        (df[date_column_name] >= dt.date(pie_single_start_year, pie_single_start_month, 1)) &
                        (df[date_column_name] <= dt.date(pie_single_end_year, pie_single_end_month, 1))
                        ]

                    # Extracting the summing the data for each security for the period between the start and end months
                    pie_single_result = {'Name': pie_single_selected_securities, 'Values': []}
                    for security in pie_single_selected_securities:
                        security_total_value = 0
                        specific_security_data = pie_single_specific_data[security]
                        for value in specific_security_data:
                            try:
                                security_total_value += value
                            except:
                                continue
                        pie_single_result['Values'].append(security_total_value)

                    pie_single_fig = px.pie(pie_single_result, values="Values", names='Name')
                    pie_single_fig.update_traces(textposition='inside', textinfo='percent+label')
                    pie_single_fig.update_layout(title={
                        'text': f"Total Debt Holdings of {pie_single_selected_investor} between {pie_single_start_month_year} and {pie_single_end_month_year}",
                        'x': 0.45})
                    st.plotly_chart(pie_single_fig, use_container_width=True)

            with single_security_charts:
                single_security_line_chart = st.container()
                single_security_waterfall_chart = st.container()
                single_security_pie_chart = st.container()

                with single_security_line_chart:
                    # Columns for the selectboxes
                    ssll, sslm, ssm, ssrm, ssrr = st.columns(5)

                    # List of investors selected by the user
                    single_security_selected_investors = st.multiselect('   ', all_investors, default=all_investors)

                    # Selected security
                    single_security_selected_securities = ssll.selectbox('Select a Security', all_securities)

                    # Selected start and end months
                    single_security_start_month_year = sslm.selectbox("  Start month", list_of_start_months)
                    single_security_end_month_year = ssm.selectbox("  End month", list_of_start_months)

                    # Checking if the end month comes before the start month
                    if month_choices.index(single_security_end_month_year) < month_choices.index(
                            single_security_start_month_year):
                        st.error(
                            "Please ensure that the selected 'End month' does not come before the selected 'Start month'")
                        return 0

                    # List of months between the start and the end month inclusive
                    single_security_specific_months = month_choices[month_choices.index(
                        single_security_start_month_year):month_choices.index(single_security_end_month_year) + 1]

                    # Separating the month and the year for the start and end months
                    single_security_start_month = month_to_num[single_security_start_month_year.split(' ')[0]]
                    single_security_start_year = int(single_security_start_month_year.split(' ')[1])
                    single_security_end_month = month_to_num[single_security_end_month_year.split(' ')[0]]
                    single_security_end_year = int(single_security_end_month_year.split(' ')[1])

                    # Getting the data withing the start and end month range
                    single_security_specific_data = df[
                        (df[date_column_name] >= dt.date(single_security_start_year, single_security_start_month, 1)) &
                        (df[date_column_name] <= dt.date(single_security_end_year, single_security_end_month, 1))
                        ]

                    single_security_result = {'Name': single_security_selected_investors,
                                              'Months': single_security_specific_months, 'Values': []}
                    for investor in single_security_selected_investors:
                        # Getting the data for a specific investor within the start and end month range
                        single_security_investor_data = single_security_specific_data[
                            (single_security_specific_data[investor_column_name] == investor)]
                        # List of values of the selected security withing the selected range for the selected investor
                        single_investor_values = list(
                            single_security_investor_data[single_security_selected_securities])
                        single_security_result['Values'].append(single_investor_values)

                    single_security_fig = make_subplots()
                    for i in range(len(single_security_selected_investors)):
                        single_security_fig.add_trace(go.Scatter(x=single_security_result['Months'],
                                                                 y=single_security_result['Values'][i],
                                                                 name=single_security_result['Name'][i]))

                    single_security_fig.update_layout(
                        title={'text': f"{single_security_selected_securities} Holders", 'x': 0.5})
                    single_security_fig.update_xaxes(title_text="Month")
                    single_security_fig.update_yaxes(title_text="Amount - (GHS)")
                    st.plotly_chart(single_security_fig, use_container_width=True)

                with single_security_pie_chart:
                    # Columns for the selectboxes
                    pssll, psslm, pssm, pssrm, pssrr = st.columns(5)

                    # List of investors selected by the user
                    pie_single_security_selected_investors = st.multiselect('  ', all_investors, default=all_investors)

                    # Selected security
                    pie_single_security_selected_security = pssll.selectbox('  Select Security', all_securities)

                    # Selected start and end month
                    pie_single_security_start_month_year = psslm.selectbox("  Pie chart Start month",
                                                                           list_of_start_months)
                    pie_single_security_end_month_year = pssm.selectbox("  Pie chart End month", list_of_start_months)

                    # Checking if the end month comes before the start month
                    if month_choices.index(pie_single_security_end_month_year) < month_choices.index(
                            pie_single_security_start_month_year):
                        st.error(
                            "Please ensure that the selected 'End month' does not come before the selected 'Start month'")
                        return 0

                    # List of months between the start and end months
                    pie_single_security_specific_months = month_choices[month_choices.index(
                        pie_single_security_start_month_year):month_choices.index(
                        pie_single_security_end_month_year) + 1]

                    # Separating the month and the year for the start and end month
                    pie_single_security_start_month = month_to_num[pie_single_security_start_month_year.split(' ')[0]]
                    pie_single_security_start_year = int(pie_single_security_start_month_year.split(' ')[1])
                    pie_single_security_end_month = month_to_num[pie_single_security_end_month_year.split(' ')[0]]
                    pie_single_security_end_year = int(pie_single_security_end_month_year.split(' ')[1])

                    # Selecting data between the starting date and the end date
                    pie_single_security_specific_data = df[
                        (df[date_column_name] >= dt.date(pie_single_security_start_year,
                                                         pie_single_security_start_month, 1)) &
                        (df[date_column_name] <= dt.date(pie_single_security_end_year, pie_single_security_end_month,
                                                         1))
                        ]

                    pie_single_security_result = {'Name': pie_single_security_selected_investors, 'Values': []}
                    for investor in pie_single_security_selected_investors:
                        investor_total_value = 0

                        # Selecting data for the selected investor within the selected month range
                        specific_investor_data = pie_single_security_specific_data[
                            (pie_single_security_specific_data[investor_column_name] == investor)]

                        # Getting the values for selected securities for the selected investor within the month range
                        specific_investor_security_values = specific_investor_data[
                            pie_single_security_selected_security]
                        for value in specific_investor_security_values:
                            try:
                                investor_total_value += value
                            except:
                                continue
                        pie_single_security_result['Values'].append(investor_total_value)

                    pie_single_security_fig = px.pie(pie_single_security_result, values="Values", names='Name')
                    pie_single_security_fig.update_traces(textposition='inside', textinfo='percent+label')
                    pie_single_security_fig.update_layout(title={
                        'text': f"Proportion of {pie_single_security_selected_security} holders between {pie_single_security_start_month_year} and {pie_single_security_end_month_year}",
                        'x': 0.45})
                    st.plotly_chart(pie_single_security_fig, use_container_width=True)

                with single_security_waterfall_chart:
                    wll, wlm, wm, wrm, wrr = st.columns(5)
                    w_all_investors = list(df[investor_column_name])
                    w_all_investors.pop(w_all_investors.index('Total'))

                    w_security = wll.selectbox(' Select a security ', all_securities)
                    w_start_month_year = wlm.selectbox('   Start Month   ', list_of_start_months)
                    w_end_month_year = wm.selectbox('   End Month   ', list_of_start_months)

                    if month_choices.index(w_end_month_year) < month_choices.index(w_start_month_year):
                        st.error(
                            "Please Ensure that the selected 'End Month' does not come before the selected 'Start Month'")
                        return 0

                    w_specific_months = month_choices[month_choices.index(w_start_month_year):month_choices.index(
                        w_end_month_year) + 1]

                    w_start_month = month_to_num[w_start_month_year.split(' ')[0]]
                    w_start_year = int(w_start_month_year.split(' ')[1])

                    w_end_month = month_to_num[w_end_month_year.split(' ')[0]]
                    w_end_year = int(w_end_month_year.split(' ')[1])

                    w_specific_data = df[
                        (df[investor_column_name] == 'Total') &
                        (df[date_column_name] >= dt.date(w_start_year, w_start_month, 1)) &
                        (df[date_column_name] <= dt.date(w_end_year, w_end_month, 1))
                        ]

                    w_security_values = list(w_specific_data[w_security])
                    initial = w_security_values[0]
                    if initial == None: initial = 0

                    w_change_values = []
                    w_measure = []
                    prev = initial
                    for i in range(len(w_security_values)):
                        if w_security_values[i] == None:
                            change = 0
                        else:
                            change = w_security_values[i] - prev
                            prev = w_security_values[i]
                        w_change_values.append(change)
                        w_measure.append('relative')

                    # Waterfall
                    w_fig = go.Figure(go.Waterfall(x=w_specific_months + ['Total'], measure=w_measure + ['total'],
                                                   y=w_change_values + [None], base=initial))

                    w_fig.update_layout(
                        title_text=f"Total {w_security} Holdings from {w_start_month_year} to {w_end_month_year}",
                        title_x=0.5)
                    w_fig.update_xaxes(title='Month')
                    w_fig.update_yaxes(title='Amount - (GHS)')
                    w_fig.update_layout(waterfallgap=0.3)
                    st.plotly_chart(w_fig, use_container_width=True)

            with investor_security_charts:
                isll, islm, ism, isrm, isrr = st.columns(5)
                is_all_investors = list(df[investor_column_name])
                is_all_investors.pop(is_all_investors.index('Total'))

                is_investor = isll.selectbox('Select an investor', is_all_investors)
                is_security = islm.selectbox('Select a security', all_securities)
                is_start_month_year = ism.selectbox('  Start Month  ', list_of_start_months)
                is_end_month_year = isrm.selectbox('  End Month  ', list_of_start_months)

                if month_choices.index(is_end_month_year) < month_choices.index(is_start_month_year):
                    st.error(
                        "Please Ensure that the selected 'End Month' does not come before the selected 'Start Month'")
                    return 0

                is_specific_months = month_choices[month_choices.index(is_start_month_year):month_choices.index(
                    is_end_month_year) + 1]

                is_start_month = month_to_num[is_start_month_year.split(' ')[0]]
                is_start_year = int(is_start_month_year.split(' ')[1])

                is_end_month = month_to_num[is_end_month_year.split(' ')[0]]
                is_end_year = int(is_end_month_year.split(' ')[1])

                is_specific_data = df[
                    (df[investor_column_name] == is_investor) &
                    (df[date_column_name] >= dt.date(is_start_year, is_start_month, 1)) &
                    (df[date_column_name] <= dt.date(is_end_year, is_end_month, 1))
                    ]

                is_security_values = list(is_specific_data[is_security])
                initial = is_security_values[0]
                if initial == None: initial = 0

                is_change_values = []
                is_measure = []
                prev = initial
                for i in range(len(is_security_values)):
                    if is_security_values[i] == None:
                        change = 0
                    else:
                        change = is_security_values[i] - prev
                        prev = is_security_values[i]
                    is_change_values.append(change)
                    is_measure.append('relative')

                # Waterfall
                is_fig = go.Figure(go.Waterfall(x=is_specific_months + ['Total'], measure=is_measure + ['total'],
                                                y=is_change_values + [None], base=initial))

                is_fig.update_layout(
                    title_text=f"{is_investor} {is_security} Holdings from {is_start_month_year} to {is_end_month_year}",
                    title_x=0.5)
                is_fig.update_xaxes(title='Month')
                is_fig.update_yaxes(title='Amount - (GHS)')
                is_fig.update_layout(waterfallgap=0.3)
                st.plotly_chart(is_fig, use_container_width=True)

        if sections == "Fixed Income Secondary Market":
            fixed_income()
        elif sections == "Primary Issuances":
            primary_issuances()
        elif sections == "Primary Issuances - TTA":
            tta()
        elif sections == "Fixed Income Yield and Volume":
            fixed_income_yield_volume()
        elif sections == "Debt Investor Holdings":
            debt_investor_holdings()

