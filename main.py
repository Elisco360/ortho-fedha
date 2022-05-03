import streamlit as st
import webbrowser
import requests
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
from annotated_text import annotated_text
from streamlit_option_menu import option_menu
import pandas as pd

from economics import Economics as ec
from forex import Forex as fx
from bonds import Bonds as bnds
from equity import Equity as qt
import performance as pf
import risk as rs

apiKEY = "ca5ccfad28074a4f92436e2e56afad2c"
st.set_page_config(page_icon='assets/icon.png', page_title='Ortho Fedha', layout='wide')

with st.sidebar:
    st.title("Menu")
    options = option_menu('',['Home', 'Markets', 'News', 'Analytics'],
                          icons=['house', 'boxes', 'activity', 'bar-chart'])


def home():
    ll, lb, bb = st.columns(3)
    lb.image("assets/logo.png")
    st.title(" ")
    st.title("Home")
    st.title(" ")
    with st.expander('About Us'):
        st.subheader("Ortho Fedha")
        st.markdown("<hr>", unsafe_allow_html=True)
        st.write("""Orthofedha is a research portal for stakeholders and clients(mostly Africans), to analyze secondary 
                    and primary market bond transactions in terms of yield and volumes traded among financial markets 
                    in Africa and might scale worldwide.""")

        st.caption("""This will enable the businesses and interested individuals to monitor governments' fiscal targets 
                    and the percentage that has been met on the primary market as well as bonds traded and price 
                    movements on the secondary market as well as educate them on general financial literacy and build 
                    up their interest in investment and Africa's financial structuring. The system will also contain an 
                    attribution system to compare the strength of funds to allow clients to make the best investment 
                    decision possible as well as provide worldwide news on financial trends and various related update
                    """)

        a, b, c, d = st.columns(4)
        join = d.button("Become a contributor - Join our community")
        if join:
            webbrowser.open('https://ortho.jetbrains.space/')

    with st.expander('Contact Us'):
        with st.form("myform"):
            st.markdown("Feedback Form")
            m, n = st.columns(2)
            user_name = m.text_input('Name')
            user_email = n.text_input('Email')
            feedback = st.text_area("Feedback")
            st.form_submit_button("Submit Feedback")

    st.markdown("<hr>", unsafe_allow_html=True)
    lll, llw, lwl, wll, www = st.columns(5)
    lll.write('Follow us on')
    lll.image('assets/twitter.png')
    lll.image('assets/facebook.png')
    lll.image('assets/instagram.png')


def markets():
    ll, lb, bb = st.columns(3)
    lb.image("assets/market.png")
    market_options = option_menu('Markets', ['Economics', 'Forex', 'Bonds', 'Equity'],
                                 icons=['basket', 'currency-exchange', 'list-nested', 'grid'],
                                 menu_icon='boxes',
                                 orientation='horizontal')

    if market_options == "Economics":
        ec.economics_section()

    if market_options == "Forex":
        fx.foreign_exchange()

    if market_options == "Bonds":
        bnds.bonds_section()

    if market_options == "Equity":
        qt.equities()

def news():
    ll, lb, bb = st.columns(3)
    lb.image("assets/news.png")
    st.title("News Feed")
    ll, rr = st.columns([0.3, 0.7])
    #countries = {'Argentina 🇦🇷': 'AR', 'Austria 🇦🇹': 'AT', 'Australia 🇦🇺': 'AU', 'Belgium 🇧🇪': 'BE', 'Bulgaria 🇧🇬': 'BG', 
    #             'Brazil 🇧🇷': 'BR', 'Canada 🇨🇦': 'CA', 'China 🇨🇳': 'CN', 'Colombia 🇨🇴': 'CO', 'Cuba 🇨🇺': 'CU', 'Czech Republic 🇨🇿': 'CZ', 
    #             'Germany 🇩🇪': 'DE', 'Egypt 🇪🇬': 'EG', 'France 🇫🇷': 'FR', 'United Kingdom 🇬🇧': 'GB', 'Greece 🇬🇷': 'GR', 'Israel 🇮🇱': 'IL', 
    #             'India 🇮🇳': 'IN', 'Italy 🇮🇹': 'IT', 'Japan 🇯🇵': 'JP', 'Mexico 🇲🇽': 'MX', 'Malaysia 🇲🇾': 'MY', 'Nigeria 🇳🇬': 'NG', 
    #             'Philippines 🇵🇭': 'PH', 'Poland 🇵🇱': 'PL', 'Portugal 🇵🇹': 'PT', 'Romania 🇷🇴': 'RO', 'Russia 🇷🇺': 'RU', 
    #             'Saudi Arabia 🇸🇦': 'SA', 'Singapore 🇸🇬': 'SG', 'Sweden 🇸🇪': 'SE', 'Thailand 🇹🇭': 'TH', 'Turkey 🇹🇷': 'TR', 'UAE 🇦🇪': 'AE', 
    #             'United States of America 🇺🇸': 'US', 'South Africa 🇿🇦': 'ZA'}
    #country = ll.selectbox("Select a country", countries.keys())
    category = ll.selectbox("Select a news category", ["Business", "Technology", "Science", "Health"])
    query = True

    if query:
        #country = countries[country]
        url = f"https://newsapi.org/v2/top-headlines?country=us&category={category}&apiKey={apiKEY}"

        r = requests.get(url)
        r = r.json()
        articles = r['articles']

        for each_article in articles:
            st.markdown('<hr>', unsafe_allow_html=True)
            st.header(each_article['title'])

            if each_article['author']:
                annotated_text((each_article['author'], "AUTHOR", "#BAFFA8"))
            st.markdown("\n")
            annotated_text((each_article['source']['name'], "SOURCE", "#FFEEB3"))
            st.markdown("\n")
            try:
                st.image(each_article['urlToImage'])
            except:
                st.image("assets/news_img.png")
            st.markdown(" ")
            st.write(each_article['description'])
            
            
def analytics():
    ll, lb, bb = st.columns(3)
    lb.image("assets/analytics.png")
    st.title("Analytics")
    
    file = st.file_uploader("Choose your CSV file", accept_multiple_files=False, help="Please make sure your file is in csv format.")

    file_1 = file

    # Reading the information from the csv file
    try:
        df_1 = pd.read_csv(file_1)
        df_1 = df_1.loc[:, ~df_1.columns.str.contains('^Unnamed')]
    except: 
        st.info(f"Ensure that file is a csv file and has at least 2 columns. The first column should contain dates(dd-mm-yyyy) and the second should contain prices.")
        return 0
        
    columns_1 = list(df_1.columns)

    all_prices_1 = list(df_1[columns_1[1]])
    all_dates_1 = list(df_1[columns_1[0]])


    # Getting the first and last dates of the data in the list
    try: start_date_1 = pf.stringToDate(all_dates_1[0])
    except:
        st.info(f"Ensure that file is a csv file and has at least 2 columns. The first column should contain dates and the second should contain prices.")
        return 0

    end_date_1 = pf.stringToDate(all_dates_1[-1])

    # Selecting the range of dates to consider
    date_range_1 = st.slider("Select a date range for file: ",start_date_1,end_date_1,(start_date_1,end_date_1))

    # Conveting the selected start and end to strings and getting their indexes
    start_date_string_1 = pf.dateToString(date_range_1[0])
    end_date_string_1 = pf.dateToString(date_range_1[-1])

    # Checking if data exists for the selected dates
    try: start_index_1 = all_dates_1.index(start_date_string_1)
    except:
        st.error(f"Data for '{start_date_string_1}' is not present in file. Ensure that dates are in the format 'dd-mm-yyyy'")
        return 0
    
    end_index_1 = all_dates_1.index(end_date_string_1)
    
    with st.expander(f"Monthly Returns Chart"):
        specific_returns_1 = pf.monthlyReturnsFromInception(prices = all_prices_1, dates=all_dates_1)
        specific_months_1 = pf.monthsFromInception(prices=all_prices_1 ,dates=all_dates_1)
        
        file_info_1 = {'Returns':specific_returns_1, 'Months':specific_months_1}
        new_df_1 = pd.DataFrame(file_info_1)

        trace_1 = go.Scatter(x=new_df_1['Months'], y=new_df_1['Returns'])

        fig = make_subplots()
        fig.add_trace(trace_1)

        fig.update_xaxes(title_text="Date")
        fig.update_yaxes(title_text="Return from Inception - (%)")
        fig.update_layout(width=1300, height=500)
        fig.update_layout(title={'text':f"Monthly Returns from Inception", 'x':0.5})
        st.plotly_chart(fig, use_container_width=True)
	
    with st.expander(f"Fund Performance"):
        st.header("Performance Indexes")
        st.markdown("<hr>")
        dates_1 = all_dates_1[start_index_1:end_index_1+1]
        prices_1 = all_prices_1[start_index_1:end_index_1+1]

        # Using the end date of the selected range to calculate the returns
        myDay_1 = date_range_1[-1].day
        myMonth_1 = date_range_1[-1].month
        myYear_1 = date_range_1[-1].year

        year_to_date_1 = pf.YearToDate(prices_1,dates_1,myYear_1)[-1]
        one_month_return_1 = pf.oneMonthReturn(prices_1, dates_1, myDay_1,myMonth_1,myYear_1)
        two_month_return_1 = pf.twoMonthReturn(prices_1, dates_1, myDay_1,myMonth_1,myYear_1)
        three_month_return_1 = pf.threeMonthReturn(prices_1, dates_1, myDay_1,myMonth_1,myYear_1)
        six_month_return_1 = pf.sixMonthReturn(prices_1,dates_1,myDay_1,myMonth_1,myYear_1)
        one_year_return_1 = pf.oneYearReturn(prices_1,dates_1,myDay_1,myMonth_1,myYear_1)
        monthly_returns_1 = pf.monthlyReturns(prices_1,dates_1)
        average_return_1 = pf.averageReturn(prices_1,dates_1)
        average_gain_1 = pf.averageGain(prices_1,dates_1)
        average_loss_1 = pf.averageLoss(prices_1,dates_1)
        compound_average_return_1 = pf.compoundAverageReturn(prices_1,dates_1)
        vami_1 = pf.VAMI(prices_1, dates_1)
        months_1 = pf.monthsFromInception(prices_1, dates_1)

        left,mid,right = st.columns(3)
        price_avg = sum(all_prices_1)/len(all_prices_1)
        left.markdown("\n\n")
        if one_month_return_1 != None: left.metric("1 month return", str(round(one_month_return_1,3))+"%",round(one_month_return_1/100, 3))
        if two_month_return_1 != None: left.metric("2 month return", str(round(two_month_return_1,3))+"%",round(two_month_return_1/100, 3))
		if three_month_return_1 != None: left.metric("3 month return", str(round(three_month_return_1,3))+"%",round(three_month_return_1/100, 3))
        if six_month_return_1 != None: left.metric("6 month return", str(round(six_month_return_1,3))+"%",round(six_month_return_1/100, 3))
        if one_year_return_1 != None: mid.metric("One year return", str(round(one_year_return_1,3))+"%",round(one_year_return_1/100, 3))
        if compound_average_return_1 != None: mid.metric("Compound average return", str(round(compound_average_return_1,3))+"%",round(compound_average_return_1/100, 3))
        if year_to_date_1 != None: mid.metric("Year to date", str(round(year_to_date_1,3))+"%",round(year_to_date_1/100, 3))
        if average_return_1 != None: right.metric("Average return", str(round(average_return_1,3))+"%",round(average_return_1/100, 3))
        if average_gain_1 != None: right.metric("Average gain", str(round(average_gain_1,3))+"%",round(average_gain_1/100, 3))
        if average_loss_1 != None: right.metric("Average loss", str(round(average_loss_1,3))+"%",round(average_loss_1/100, 3))

        p_trace_1 = go.Scatter(x=months_1, y=vami_1)
        
        p_fig = make_subplots()
        p_fig.add_trace(p_trace_1)

        p_fig.update_xaxes(title_text="Month")
        p_fig.update_yaxes(title_text="Amount - ($)")
        p_fig.update_layout(width=1300, height=500)
        p_fig.update_layout(title={'text':'Value Added Monthly Index', 'x':0.5})
        st.plotly_chart(p_fig, use_container_width=True)

        
    
if options == "Home":
    home()
elif options == "Markets":
    markets()
elif options == "News":
    news()
elif options == "Analytics":
    analytics()
