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
        st.title("Bonds Sections")

        sections = st.selectbox("Select a section", ["Fixed Income"])


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

        def fixed_income():
            st.header('Fixed Income')

            # File path filepath
            file = "Data/Bond/BBNs.csv"

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

            line_chart = st.beta_container()
            pie_chart = st.beta_container()

            with line_chart:
                # Allowing the user to select a month range
                ll, lm, m, rm, rr = st.beta_columns(5)
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
                pll, plm, pm, prm, prr = st.beta_columns(5)

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

        if sections == "Fixed Income":
            fixed_income()
