import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px


class Economics:
    def __init__(self):
        pass

    @staticmethod
    def economics_section():
        with st.sidebar:
            st.title("Economic Markers")
            markers = st.selectbox("Select a marker", ["Real Sector Indicator", "Government Fiscal Operations",
                                                       "Interest Rates", "Merchandise Trade Flows (USD 'M)",
                                                       "Gross domestic Products", "Balance of Payments",
                                                       "Commodities"])

        def get_monthly_data(df, start_month, end_month, variables, include, months):
            # Getting specific data based on user input
            start_year = int(start_month.split(' ')[-1])
            end_year = int(end_month.split(' ')[-1])
            year_data = df[(df['Year'] >= start_year) & (df['Year'] <= end_year)]

            # Getting the values to plot based on user input
            result = {}
            reversed_months = months
            reversed_months.reverse()
            for item in variables:
                if item not in include: continue
                x_values = []
                y_values = []
                i = start_year
                while i <= end_year:
                    full_set_x = [month + ' ' + str(i) for month in reversed_months]
                    try:
                        full_set_y = list(
                            year_data[(year_data['Year'] == i) & (year_data['Variables'] == item)][months].values[0])
                    except:
                        full_set_y = [None for number in full_set_x]

                    if i == start_year:
                        start_index = full_set_x.index(start_month)
                        full_set_x = full_set_x[start_index:]
                        full_set_y = full_set_y[start_index:]

                    if i == end_year:
                        end_index = full_set_x.index(end_month)
                        full_set_x = full_set_x[:end_index + 1]
                        full_set_y = full_set_y[:end_index + 1]

                    x_values += full_set_x
                    y_values += full_set_y
                    i += 1

                if len(y_values) > 0: result[item] = {'x': x_values, 'y': y_values}

            return result

        def get_year_data(df, years):
            data = df[
                (df["Year"] >= years[0]) & (
                            df['Year'] <= years[-1])]  # Filters the data for rows from the year provided
            return data

        def yearly_comparison(df, variable_to_plot):
            result = {}
            year = list(df['Year'])[0]
            variables = list(df["Year"].unique())  # Getting a list of all the available variables
            result['variables'] = variables  # Assigning that list to a key in a dictionary
            result['monthly data'] = []  # Initializing a list to store the monthly data for each variable
            months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            for variable in result['variables']:
                monthly_amount = []  # Empty array to store the amount for January to December
                sliced = df.loc[(df['Variables'] == variable_to_plot) & (
                        df['Year'] == variable)]  # Isolate the data for a specific variable
                monthly_data = sliced[months]  # Isolate the monthly data for a specific variable
                for month in months:
                    try:
                        monthly_amount.append(float(monthly_data[month]))  # Getting the amount for each month
                    except:
                        monthly_amount.append(None)
                result['monthly data'].append(monthly_amount)  # Adding the list of months to main dictionary

            return result

        def plot_monthly_linechart(result, variables, include, y_label_text=None, x_label_text=None):
            # Plotting the values
            fig = make_subplots(specs=[[{"secondary_y": True}]])
            for item in variables:
                if item not in include: continue
                trace = go.Scatter(x=result[item]['x'], y=result[item]['y'], name=str(item))
                if item == 'CIEA(Index)':
                    fig.add_trace(trace, secondary_y=True)
                else:
                    fig.add_trace(trace, secondary_y=False)

            fig.update_xaxes(title_text="Month")

            fig.update_yaxes(title_text="Amount", secondary_y=False)
            fig.update_yaxes(title_text="Amount - (Index)", secondary_y=True)

            if x_label_text is not None: fig.update_xaxes(title_text=x_label_text)
            if y_label_text is not None: fig.update_xaxes(title_text=y_label_text)

            st.plotly_chart(fig, use_container_width=True)

        def plot_linechart(result, include=None, legend=True):
            traces = []
            names = list(result["variables"])  # Getting a list of variable names for the legend
            if include == None: include = names
            monthly_data = result['monthly data']  # Getting the amounts from Jan to Dec for each variable
            months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov',
                      'Dec']  # Months for the x axis

            for i in range(len(names)):
                if names[i] not in include: continue
                traces.append(go.Scatter(x=months, y=monthly_data[i],
                                         name=str(names[i])))  # Getting the individual bars for each variable
            fig = make_subplots()
            for trace in traces:
                fig.add_trace(trace)

            fig.update_xaxes(title_text="Month")
            fig.update_yaxes(title_text="Amount")
            if legend == False: fig.update_layout(showlegend=False)

            st.plotly_chart(fig, use_container_width=True)

        def plot_monthly_barchart(result, variables, include, y_label_text=None, x_label_text=None):
            # Plotting the values
            fig = make_subplots()
            for item in variables:
                if item not in include: continue
                trace = go.Bar(x=result[item]['x'], y=result[item]['y'], name=str(item))
                if item != 'CIEA(Index)': fig.add_trace(trace)

            fig.update_xaxes(title_text="Month")
            fig.update_yaxes(title_text="Amount")
            if x_label_text != None: fig.update_xaxes(title_text=x_label_text)
            if y_label_text != None: fig.update_xaxes(title_text=y_label_text)

            st.plotly_chart(fig, use_container_width=True)

        def list_vals_to_string(information):
            for i in range(len(information)):
                information[i] = str(information[i])
            return information

        def real_sector_indicators():
            st.header("Real Sector Indicator")
            st.info(" An economic indicator is a piece of economic data, usually of macroeconomic scale, that is used by analysts to interpret current or future investment possibilities.\
                    These indicators also help to judge the overall health of an economy.\
                        Reference: https://www.investopedia.com/terms/e/economic_indicator.asp")
            file = "Dataset/Economics/rsi.csv"
            dataframe = pd.read_csv(file)
            dataframe = dataframe.loc[:, ~dataframe.columns.str.contains('^Unnamed')]

            # getting key variables
            years = dataframe['Year'].unique()
            months = list(dataframe.columns[2:])
            variables = dataframe['Variables'].unique()

            reversed_months = months
            reversed_months.reverse()

            # Getting months for specific years
            d_months = []
            for year in years:
                d_months += [month + ' ' + str(year) for month in reversed_months]

            checkbox = st.sidebar.checkbox("Show data")
            if checkbox:
                st.write(dataframe)

            multivariate_expander = st.expander("Multivariate Comparison")
           
            year_on_year_expander = st.expander("Univariate Comparison")

            multi_variate_comparison = multivariate_expander.container()
            single_variable_comparison = year_on_year_expander.container()

            with multi_variate_comparison:
                # Allowing the user to choose variables
                include = st.multiselect("Variables", tuple(dataframe['Variables'].unique()),
                                         default=list(dataframe['Variables'].unique()))

                ll, lm, m, rm, rr = st.columns(5)
                list_of_months = list(d_months)
                start_month = ll.selectbox("Start Month", tuple(list_of_months))
                list_of_end_months = list_of_months[list_of_months.index(start_month):]
                # list_of_end_months = list_of_months[list_of_months.index(start_month):]
                end_month = lm.selectbox("End Month", tuple(list_of_months))

                if list_of_months.index(end_month) > list_of_months.index(start_month):
                    st.error(
                        "Please ensure that the selected 'End month' does not come before the selected 'Start month'")
                    return 0

                data = get_monthly_data(df=dataframe,
                                        start_month=start_month,
                                        end_month=end_month,
                                        variables=variables,
                                        include=include,
                                        months=months)

                # self.plot_monthly_barchart(result=data,variables=variables,include=include)
                plot_monthly_linechart(result=data, variables=variables, include=include)
                pie_chart = st.container()

                with pie_chart:
                    pll, plm, pm, prm, prr = st.columns(5)
                    pie_chart_month = pll.selectbox('Select a month', list_of_months)
                    pie_data = get_monthly_data(df=dataframe,
                                                start_month=pie_chart_month,
                                                end_month=pie_chart_month,
                                                variables=variables,
                                                include=include,
                                                months=months)
                    names = []
                    Quarters = []
                    Values = []
                    for item in data:
                        names.append(item)
                        Quarters.append(pie_data[item]['x'][0])
                        Values.append(pie_data[item]['y'][0])
                    result = {'Names': names, 'Quarters': Quarters, 'Values': Values}
                    result = pd.DataFrame(result)

                    fig = px.pie(result, values="Values", names='Names')
                    fig.update_traces(textposition='inside', textinfo='percent+label')

                    fig.update_layout(title={'text': str(pie_chart_month) + ' Real Sector Indicators', 'x': 0.45})
                    st.plotly_chart(fig, use_container_width=True)

            with single_variable_comparison:
                # GRAPH TO COMPARE SINGLE VARIABLE AGAINST ITSELF ACROSS THE YEARS
                yearly_comparison_values = st.slider('Select a year range',
                                                     list(dataframe["Year"])[-1],
                                                     list(dataframe["Year"])[0],
                                                     (list(dataframe["Year"])[-1],
                                                      list(dataframe["Year"])[0]))

                # Filtering the data by year
                mll, mrr = st.columns(2)
                year_comparison_data = get_year_data(df=dataframe, years=yearly_comparison_values)
                variable_to_plot = mll.selectbox("Select a variable", tuple(dataframe['Variables'].unique()))

                # Plotting the actual graph
                result = yearly_comparison(year_comparison_data, variable_to_plot=variable_to_plot)
                plot_linechart(result=result)

        def government_fiscal_operations():
            # Reading data from the csv file
            st.header('Government Fiscal Operations')
            file = "Dataset/Economics/gfo.csv"

            df = pd.read_csv(file,
                             header=None,
                             skiprows=1,
                             names=['Year', 'Variables', 'Amount'])
            df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

            # Get the date range for the data
            ll, lm, m, rm, rr = st.columns(5)
            values = st.slider('Select a year range', list(df["Year"])[-1], list(df["Year"])[0],
                               (list(df["Year"])[-1], list(df["Year"])[0]))
            # Filtering the data by year
            year_data = get_year_data(df=df, years=list(values))
            variables = list(df["Variables"].unique())
            data = {'variables': variables}

            checkbox = st.sidebar.checkbox("Show data")
            if checkbox:
                st.write(df)

            for item in variables:
                specific_data = year_data[
                    year_data['Variables'] == item]  # Getting all the years data for a specific variable
                x_vals = list_vals_to_string(list(specific_data['Year']))  # setting the years as the x variables
                y_vals = list(specific_data['Amount'])  # setting the amounts as the y variables

                x_vals.reverse()
                y_vals.reverse()
                data[item] = {'x values': x_vals, 'y values': y_vals}
                pass

            include = st.multiselect('Variables', data['variables'],
                                     default=data['variables'])  # Select box for variables to show
            exclude = []  # Variables to exclude from the charts
            for variable in variables:
                if variable not in include:
                    exclude.append(variable)

            line_chart = st.container()
            pie_chart = st.container()

            with line_chart:
                # PLOTTING A BAR CHART
                traces = []
                names = data["variables"]  # Getting a list of variable names for the legend

                for i in range(len(names)):
                    if names[i] not in include: continue
                    traces.append(go.Scatter(x=data[names[i]]["x values"], y=data[names[i]]["y values"],
                                             name=names[i]))  # Getting the individual bars for each variable
                fig = make_subplots()
                for trace in traces:
                    fig.add_trace(trace)

                fig.update_xaxes(title_text="Year")
                fig.update_yaxes(title_text="Amount")
                st.plotly_chart(fig, use_container_width=True)

            with pie_chart:
                pie_year_value = st.slider('Select a year', list(df["Year"])[-1], list(df["Year"])[0])
                specific_year_data = get_year_data(df=df, years=[pie_year_value])
                for item in exclude:
                    specific_year_data = specific_year_data[(specific_year_data['Variables'] != item)]

                fig = px.pie(specific_year_data, values="Amount", names='Variables')
                fig.update_traces(textposition='inside', textinfo='percent+label')

                fig.update_layout(title={'text': 'Government Fiscal Operations for ' + str(pie_year_value), 'x': 0.28})
                st.plotly_chart(fig, use_container_width=True)

        def interest_rates():
            # Reading data from the csv file
            st.header('Interest Rates')
            file = "Dataset/Economics/ir.csv"

            df = pd.read_csv(file,
                             header=None,
                             skiprows=1,
                             names=['Year', 'Variables', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug',
                                    'Sep', 'Oct', 'Nov', 'Dec'])
            df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

            # Getting the years, variables and the months present
            years = df['Year'].unique()
            months = list(df.columns[2:])
            variables = df['Variables'].unique()

            reversed_months = months
            reversed_months.reverse()

            # Getting months for specific years
            d_months = []
            for year in years:
                d_months += [month + ' ' + str(year) for month in reversed_months]

            checkbox = st.sidebar.checkbox("Show data")
            if checkbox:
                st.write(df)

            multivariate_expander = st.expander("Multivariate Comparison")
            year_on_year_expander = st.expander("Single Variable Comparison")

            multi_variate_comparison = multivariate_expander.container()
            single_variable_comparison = year_on_year_expander.container()

            with multi_variate_comparison:
                # Allowing the user to choose variables
                include = st.multiselect("Variables", tuple(df['Variables'].unique()),
                                         default=list(df['Variables'].unique()))

                ll, lm, m, rm, rr = st.columns(5)
                list_of_months = list(d_months)
                start_month = ll.selectbox("Start Month", tuple(list_of_months))
                list_of_end_months = list_of_months[list_of_months.index(start_month):]
                end_month = lm.selectbox("End Month", tuple(list_of_months))
                if list_of_months.index(end_month) > list_of_months.index(start_month):
                    st.error(
                        "Please ensure that the selected 'End month' does not come before the selected 'Start month'")
                    return 0

                data = get_monthly_data(df=df,
                                        start_month=start_month,
                                        end_month=end_month,
                                        variables=variables,
                                        include=include,
                                        months=months)

                # self.plot_monthly_barchart(result=data,variables=variables,include=include)
                plot_monthly_linechart(result=data, variables=variables, include=include)
                pie_chart = st.container()
                with pie_chart:
                    pll, plm, pm, prm, prr = st.columns(5)
                    pie_chart_month = pll.selectbox('Pie Chart Month', list_of_months)
                    pie_data = get_monthly_data(df=df,
                                                start_month=pie_chart_month,
                                                end_month=pie_chart_month,
                                                variables=variables,
                                                include=include,
                                                months=months)
                    names = []
                    Months = []
                    Values = []
                    for item in pie_data:
                        names.append(item)
                        Months.append(pie_data[item]['x'][0])
                        Values.append(pie_data[item]['y'][0])
                    result = {'Names': names, 'Months': Months, 'Values': Values}
                    result = pd.DataFrame(result)

                    total_values = []
                    for value in Values:
                        if value is not None: total_values.append(value)
                    if sum(total_values) == 0:
                        st.success('No data available')
                    else:
                        fig = px.pie(result, values="Values", names='Names')
                        fig.update_traces(textposition='inside', textinfo='percent+label')

                        fig.update_layout(title={'text': str(pie_chart_month) + ' Interest Rates', 'x': 0.28})
                        st.plotly_chart(fig, use_container_width=True)

            with single_variable_comparison:
                # GRAPH TO COMPARE SINGLE VARIABLE AGAINST ITSELF ACROSS THE YEARS
                yearly_comparison_values = st.slider('Select a year range',
                                                     list(df["Year"])[-1],
                                                     list(df["Year"])[0],
                                                     (list(df["Year"])[-1],
                                                      list(df["Year"])[0]))

                # Filtering the data by year
                ill, irr = st.columns(2)
                year_comparison_data = get_year_data(df=df, years=yearly_comparison_values)
                variable_to_plot = ill.selectbox("Select a variable", tuple(df['Variables'].unique()))

                # Plotting the actual graph
                result = yearly_comparison(year_comparison_data, variable_to_plot=variable_to_plot)
                plot_linechart(result=result)

        def gdp():
            # Reading data from the csv file
            st.header('Gross Domestic Product')
            file = 'Dataset/Economics/gdp.csv'

            df = pd.read_csv(file,
                             header=None,
                             skiprows=1,
                             names=['Year', 'Variables', 'Amount'])

            df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

            # Get the date range for the data
            ll, lm, m, rm, rr = st.columns(5)

            # Setting up different containers
            checkbox = st.sidebar.checkbox("Show data")
            if checkbox:
                st.write(df)

            # values = ll.selectbox("Select a year",tuple(list(df['Year'].unique())))
            values = st.slider('Select a year range', list(df['Year'])[-1], list(df['Year'])[0],
                               (list(df['Year'])[-1], list(df['Year'])[0]))
            # Filtering the data by year
            year_data = get_year_data(df=df, years=list(values))
            variables = list(df['Variables'].unique())
            percent_variables = [variables.pop(-1), variables.pop(-1)]

            prices = st.container()
            percentages = st.container()
            with prices:
                data = {'variables': variables}
                for item in variables:
                    specific_data = year_data[
                        year_data['Variables'] == item]  # Getting all the years data for a specific variable
                    x_vals = list_vals_to_string(
                        list(specific_data['Year']))  # setting the years as the x variables
                    y_vals = list(specific_data['Amount'])  # setting the amounts as the y variables

                    x_vals.reverse()
                    y_vals.reverse()
                    data[item] = {'x values': x_vals, 'y values': y_vals}
                    pass

                include = st.multiselect('Variables', data['variables'],
                                         default=data['variables'])  # Select box for variables to show

                # PLOTTING A BAR CHART
                traces = []
                names = data["variables"]  # Getting a list of variable names for the legend

                for i in range(len(names)):
                    if names[i] not in include: continue
                    traces.append(go.Scatter(x=data[names[i]]["x values"], y=data[names[i]]["y values"],
                                             name=names[i]))  # Getting the individual bars for each variable

                fig = make_subplots(specs=[[{"secondary_y": True}]])
                for trace in traces:
                    fig.add_trace(trace, secondary_y=False)

                fig.update_xaxes(title_text="Year")
                fig.update_yaxes(title_text="Amount", secondary_y=False)
                # st.plotly_chart(fig, use_container_width=True)

            with percentages:
                percent_data = {'variables': percent_variables}
                for item in percent_variables:
                    specific_data = year_data[
                        year_data['Variables'] == item]  # Getting all the years data for a specific variable
                    percent_x_vals = list_vals_to_string(
                        list(specific_data['Year']))  # setting the years as the x variables
                    percent_y_vals = list(specific_data['Amount'])  # setting the amounts as the y variables

                    percent_x_vals.reverse()
                    percent_y_vals.reverse()
                    percent_data[item] = {'x values': percent_x_vals, 'y values': percent_y_vals}

                percent_include = st.multiselect('Percentage Variables', percent_data['variables'],
                                                 default=percent_data['variables'])  # Select box for variables to show

                # PLOTTING A BAR CHART
                percent_traces = []
                percent_names = percent_data["variables"]  # Getting a list of variable names for the legend

                for i in range(len(percent_names)):
                    if percent_names[i] not in percent_include: continue
                    percent_traces.append(go.Scatter(x=percent_data[percent_names[i]]["x values"],
                                                     y=percent_data[percent_names[i]]["y values"],
                                                     name=percent_names[
                                                         i]))  # Getting the individual bars for each variable
                for trace in percent_traces:
                    fig.add_trace(trace, secondary_y=True)

                fig.update_yaxes(title_text="Percentage", secondary_y=True)
                st.plotly_chart(fig, use_container_width=True)

        def commodities():
            # Reading data from the csv file
            st.header('Commodities')
            file = "Dataset/Economics/comms.csv"
            df = pd.read_csv(file,
                             header=None,
                             skiprows=1,
                             names=['Year', 'Variables', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug',
                                    'Sep', 'Oct', 'Nov', 'Dec'])
            df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

            # Getting the years, variables and the months present
            years = df['Year'].unique()
            months = list(df.columns[2:])
            variables = df['Variables'].unique()

            reversed_months = months
            reversed_months.reverse()

            # Getting months for specific years
            d_months = []
            for year in years:
                d_months += [month + ' ' + str(year) for month in reversed_months]

            checkbox = st.sidebar.checkbox("Show data")
            if checkbox:
                st.write(df)

            multivariable_expander = st.expander("Multivariable Comparison")
            year_on_year_expander = st.expander("Single Variable Comparison")

            multi_variable_comparison = multivariable_expander.container()
            single_variable_comparison = year_on_year_expander.container()

            with multi_variable_comparison:
                # Allowing the user to choose variables
                include = st.multiselect("Variables", tuple(df['Variables'].unique()),
                                         default=list(df['Variables'].unique()))

                ll, lm, m, rm, rr = st.columns(5)
                list_of_months = list(d_months)
                start_month = ll.selectbox("Start Month", tuple(list_of_months))
                list_of_end_months = list_of_months[list_of_months.index(start_month):]
                end_month = lm.selectbox("End Month", tuple(list_of_months))

                if list_of_months.index(end_month) > list_of_months.index(start_month):
                    st.error(
                        "Please ensure that the selected 'End month' does not come before the selected 'Start month'")
                    return 0

                data = get_monthly_data(df=df,
                                        start_month=start_month,
                                        end_month=end_month,
                                        variables=variables,
                                        include=include,
                                        months=months)

                plot_monthly_barchart(result=data, variables=variables, include=include)
                plot_monthly_linechart(result=data, variables=variables, include=include)

            with single_variable_comparison:
                # GRAPH TO COMPARE SINGLE VARIABLE AGAINST ITSELF ACROSS THE YEARS
                yearly_comparison_values = st.slider('Select a year range',
                                                     list(df["Year"])[-1],
                                                     list(df["Year"])[0],
                                                     (list(df["Year"])[-1],
                                                      list(df["Year"])[0]))

                # Filtering the data by year
                cll, crr = st.columns(2)
                year_comparison_data = get_year_data(df=df, years=yearly_comparison_values)
                variable_to_plot = cll.selectbox("Select a variable", tuple(df['Variables'].unique()))

                # Plotting the actual graph
                result = yearly_comparison(year_comparison_data, variable_to_plot=variable_to_plot)
                plot_linechart(result=result)

        def merchandise_trade_flows():
            # Reading data from the csv file
            st.header('Merchandise Trade Flows')
            file = "Dataset/Economics/mtf.csv"
            df = pd.read_csv(file,
                             header=None,
                             skiprows=1,
                             names=['Year', 'Variables', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug',
                                    'Sep', 'Oct', 'Nov', 'Dec'])
            df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

            # Getting the years, variables and the months present
            years = df['Year'].unique()
            months = list(df.columns[2:])
            variables = df['Variables'].unique()

            reversed_months = months
            reversed_months.reverse()

            # Getting months for specific years
            d_months = []
            for year in years:
                d_months += [month + ' ' + str(year) for month in reversed_months]

            checkbox = st.sidebar.checkbox("Show data")
            if checkbox:
                st.write(df)

            multivariable_expander = st.expander("Multivariable Comparison")
            year_on_year_expander = st.expander("Single Variable Year-on-Year Comparison")

            multi_variable_comparison = multivariable_expander.container()
            single_variable_comparison = year_on_year_expander.container()

            with multi_variable_comparison:
                # Allowing the user to choose variables
                include = st.multiselect("Variables", tuple(df['Variables'].unique()),
                                         default=list(df['Variables'].unique()))

                ll, lm, m, rm, rr = st.columns(5)
                list_of_months = list(d_months)
                start_month = ll.selectbox("Start Month", tuple(list_of_months))
                list_of_end_months = list_of_months[list_of_months.index(start_month):]
                end_month = lm.selectbox("End Month", tuple(list_of_months))
                if list_of_months.index(end_month) > list_of_months.index(start_month):
                    st.error(
                        "Please ensure that the selected 'End month' does not come before the selected 'Start month'")
                    return 0

                data = get_monthly_data(df=df,
                                             start_month=start_month,
                                             end_month=end_month,
                                             variables=variables,
                                             include=include,
                                             months=months)

                # self.plot_monthly_barchart(result=data,variables=variables,include=include)
                plot_monthly_linechart(result=data, variables=variables, include=include)
                pie_chart = st.container()
                with pie_chart:
                    pll, plm, pm, prm, prr = st.columns(5)
                    pie_chart_month = pll.selectbox('Pie Chart Month', list_of_months)
                    pie_data = get_monthly_data(df=df,
                                                     start_month=pie_chart_month,
                                                     end_month=pie_chart_month,
                                                     variables=variables,
                                                     include=include,
                                                     months=months)
                    names = []
                    Months = []
                    Values = []
                    for item in pie_data:
                        names.append(item)
                        Months.append(pie_data[item]['x'][0])
                        Values.append(pie_data[item]['y'][0])
                    result = {'Names': names, 'Months': Months, 'Values': Values}
                    result = pd.DataFrame(result)

                    total_values = []
                    for value in Values:
                        if value != None: total_values.append(value)
                    if sum(total_values) == 0:
                        st.success('No data available')
                    else:
                        fig = px.pie(result, values="Values", names='Names')
                        fig.update_traces(textposition='inside', textinfo='percent+label')

                        fig.update_layout(title={'text': str(pie_chart_month) + ' Merchandise Trade Flows', 'x': 0.28})
                        st.plotly_chart(fig, use_container_width=True)

            with single_variable_comparison:
                # GRAPH TO COMPARE SINGLE VARIABLE AGAINST ITSELF ACROSS THE YEARS
                yearly_comparison_values = st.slider('Select a year range',
                                                     list(df["Year"])[-1],
                                                     list(df["Year"])[0],
                                                     (list(df["Year"])[-1],
                                                      list(df["Year"])[0]))

                # Filtering the data by year
                mll, mrr = st.columns(2)
                year_comparison_data = get_year_data(df=df, years=yearly_comparison_values)
                variable_to_plot = mll.selectbox("Select a variable", tuple(df['Variables'].unique()))

                # Plotting the actual graph
                result = yearly_comparison(year_comparison_data, variable_to_plot=variable_to_plot)
                plot_linechart(result=result)

        if markers == "Real Sector Indicator":
            real_sector_indicators()
        elif markers == "Government Fiscal Operations":
            government_fiscal_operations()
        elif markers == "Merchandise Trade Flows (USD 'M)":
            merchandise_trade_flows()
        elif markers == "Balance of Payments":
            st.title("Balance of Payments")
            st.info("Under Development")
        elif markers == "Interest Rates":
            interest_rates()
        elif markers == "Gross domestic Products":
            gdp()
        elif markers == "Commodities":
            commodities()

