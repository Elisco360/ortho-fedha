import time
import streamlit as st
import webbrowser
import requests
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
from annotated_text import annotated_text
from streamlit_option_menu import option_menu
import pandas as pd
import re
from economics import Economics as ec
from forex import Forex as fx
from bonds import Bonds as bnds
from equity import Equity as qt
import performance as pf
import risk as rs

import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

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
            form= st.form("myform", clear_on_submit=True)
            form.markdown("Feedback Form")
            m, n = form.columns(2)
            user_name = m.text_input('Name')
            user_email = n.text_input('Email(Gmail)')
            feedback = form.text_area("Feedback")
            submit = form.form_submit_button("Submit Feedback")

    st.markdown("<hr>", unsafe_allow_html=True)
    lll, llw, lwl, wll, www = st.columns(5)
    lll.write('Follow us on')
    lll.image('assets/twitter.png')
    lll.image('assets/facebook.png')
    lll.image('assets/instagram.png')
    
    def send_umail(receiver, name):
        sender_email = "orthofedha@gmail.com"
        receiver_email = receiver
        password = "Thegodsare@1234"

        message = MIMEMultipart("alternative")
        message["Subject"] = "Feedback Appreciation"
        message["From"] = sender_email
        message["To"] = receiver_email

        # Create the plain-text and HTML version of your message
        text = f"""\
Dear {name},
        
Thank you for your feedback on Ortho Fedha. Our software engineering and data analytics team highly
appreciate your input and will keep you in touch with any updates with our software. 
Thank you for being part of us.
        
Best,
Team Ortho.
    """

        part1 = MIMEText(text, "plain")
        message.attach(part1)

        # Create secure connection with server and send email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(
                sender_email, receiver_email, message.as_string()
            )
    
    def send_omail(name, email, feedback):
        sender_email = "orthofedha@gmail.com"
        receiver_email = "orthofedha@gmail.com"
        password = "Thegodsare@1234"

        message = MIMEMultipart("alternative")
        message["Subject"] = "User Feedback"
        message["From"] = sender_email
        message["To"] = receiver_email

        # Create the plain-text and HTML version of your message
        text = f"""\
From {name},
Email {email},
    
    {feedback}
    """

        part1 = MIMEText(text, "plain")
        message.attach(part1)

        # Create secure connection with server and send email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(
                sender_email, receiver_email, message.as_string()
            )
            
    def check_email(email):
        regex = r'\b[A-Za-z0-9._%+-]+@gmail.com\b'
        if re.fullmatch(regex, email):
            return True
        return False

    if submit and check_email(user_email):
        send_umail(user_email,user_name)
        send_omail(user_name, user_email ,feedback)
        form.success('Thank you for your feedback')
        st.experimental_rerun()
    elif submit and not check_email(user_email):
        form.error("Kindly enter a valid email. Preferably gmail.")
        time.sleep(2)
        st.experimental_rerun()

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
    category = ll.selectbox("Select a news category", ["Business 🏛️", "Technology 💻", "Science 🔬", "Health 🧑🏾‍⚕️"])
    category = category[:-2]
    print(category)
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
	
    with st.expander(f"Performance Analytics"):
        st.header("Performance Indexes")
        st.markdown("<hr>", unsafe_allow_html=True)
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
        
        left.markdown("\n\n")
        if one_month_return_1 != None: left.metric("1 month return", str(round(one_month_return_1,3))+"%",round(one_month_return_1/100, 3))
        if two_month_return_1 != None: left.metric("2 month return", str(round(two_month_return_1,3))+"%",round(two_month_return_1/100, 3))
        if three_month_return_1 != None: left.metric("3 month return", str(round(three_month_return_1,3))+"%",round(three_month_return_1/100, 3))
        if six_month_return_1 != None: left.metric("6 month return", str(round(six_month_return_1,3))+"%",round(six_month_return_1/100, 3))
        mid.markdown("\n\n")
        if one_year_return_1 != None: mid.metric("One year return", str(round(one_year_return_1,3))+"%",round(one_year_return_1/100, 3))
        if compound_average_return_1 != None: mid.metric("Compound average return", str(round(compound_average_return_1,3))+"%",round(compound_average_return_1/100, 3))
        if year_to_date_1 != None: mid.metric("Year to date", str(round(year_to_date_1,3))+"%",round(year_to_date_1/100, 3))
        right.markdown("\n\n")
        if average_return_1 != None: right.metric("Average return", str(round(average_return_1,3))+"%",round(average_return_1/100, 3))
        if average_gain_1 != None: right.metric("Average gain", str(round(average_gain_1,3))+"%",round(average_gain_1/100, 3))
        if average_loss_1 != None: right.metric("Average loss", str(round(average_loss_1,3))+"%",round(average_loss_1/100, 3))

        st.markdown("<hr>", unsafe_allow_html=True)
        
        p_trace_1 = go.Scatter(x=months_1, y=vami_1)
        
        p_fig = make_subplots()
        p_fig.add_trace(p_trace_1)

        p_fig.update_xaxes(title_text="Month")
        p_fig.update_yaxes(title_text="Amount - ($)")
        p_fig.update_layout(width=1300, height=500)
        p_fig.update_layout(title={'text':'Value Added Monthly Index', 'x':0.5})
        st.plotly_chart(p_fig, use_container_width=True)

    with st.expander(f"Risk Analytics"):
        st.header("Risk Indexes")
        st.markdown("<hr>", unsafe_allow_html=True)
        
        myDay_1 = date_range_1[-1].day
        myMonth_1 = date_range_1[-1].month
        myYear_1 = date_range_1[-1].year

        dates_1 = all_dates_1[start_index_1:end_index_1+1]
        prices_1 = all_prices_1[start_index_1:end_index_1+1]

        ll,lm,m,rm,rr = st.columns(5)
        minimumAcceptableReturn = ll.number_input("Minimum Acceptable Return (%)",1.0)
        riskFreeReturn = lm.number_input("Risk Free Return (%)",1.0)
        left_risk,mid_risk,right_risk = st.columns(3)

        # Risk analytics
        standard_deviation_1 = rs.standardDeviation(prices=prices_1,dates=dates_1)
        gain_standard_deviation_1 = rs.gainStandardDeviation(prices=prices_1,dates=dates_1)
        loss_standard_deviation_1 = rs.lossStandardDeviation(prices=prices_1,dates=dates_1)
        downside_deviation_1 = rs.downsideDeviation(prices=prices_1,dates=dates_1,minimumAcceptableReturn=minimumAcceptableReturn)
        semi_deviation_1 = rs.semiDeviation(prices=prices_1,dates=dates_1)

        sharpe_ratio_1 = rs.sharpeRatio(prices=prices_1,dates=dates_1,riskFreeReturn=riskFreeReturn)
        sortino_ratio_1 = rs.sortinoRatio(prices=prices_1,dates=dates_1,minimumAcceptableReturn=minimumAcceptableReturn)
        calmar_ratio_1 = rs.calmarRatio(prices=prices_1,dates=dates_1)
        sterling_ratio_1 = rs.sterlingRatio(prices=prices_1,dates=dates_1,year=myYear_1)
        gain_to_loss_ratio_1 = rs.gainToLossRatio(prices=prices_1,dates=dates_1)

        losing_streak_1 = rs.losingStreak(prices=prices_1,dates=dates_1)
        skewness_1 = rs.skewness(prices=prices_1,dates=dates_1)
        kurtosis_1 = rs.kurtosis(prices=prices_1,dates=dates_1)
        profit_to_loss_ratio_1 = rs.profitToLossRatio(prices=prices_1,dates=dates_1)
        max_drawdown_1 = rs.maxDrawdown(prices=prices_1)
        
        left_risk.markdown("\n\n")
        if standard_deviation_1 != None: left_risk.metric("Standard Deviation", str(round(standard_deviation_1,3)))
        if gain_standard_deviation_1 != None: left_risk.metric("Gain Standard Deviation", str(round(gain_standard_deviation_1,3)))
        if loss_standard_deviation_1 != None: left_risk.metric("Loss Standard Deviation", str(round(loss_standard_deviation_1,3)))
        if downside_deviation_1 != None: left_risk.metric("Downside Deviation", str(round(downside_deviation_1,3)))
        if semi_deviation_1 != None: left_risk.metric("Semi Deviation", str(round(semi_deviation_1,3)))
        
        mid_risk.markdown("\n\n")
        if sharpe_ratio_1 != None: mid_risk.metric("Sharpe Ratio", str(round(sharpe_ratio_1,3)))
        if sortino_ratio_1 != None: mid_risk.metric("Sortino Ratio", str(round(sortino_ratio_1,3)))
        if calmar_ratio_1 != None: mid_risk.metric("Calmer Ratio", str(round(calmar_ratio_1,3)))
        if sterling_ratio_1 != None: mid_risk.metric("Sterling Ratio", str(round(sterling_ratio_1,3)))
        if gain_to_loss_ratio_1 != None: mid_risk.metric("Gain to loss Ratio", str(round(gain_to_loss_ratio_1,3)))
        
        right_risk.markdown("\n\n")
        if skewness_1 != None: right_risk.metric("Skewness", str(round(skewness_1,3)),round(skewness_1,3))
        if kurtosis_1 != None: right_risk.metric("Kurtosis", str(round(kurtosis_1,3)),round(kurtosis_1,3))
        if profit_to_loss_ratio_1 != None: right_risk.metric("Profit to loss Ratio", str(round(profit_to_loss_ratio_1,3)))
        if max_drawdown_1 != None: right_risk.metric("Maximum Drawdown", str(round(max_drawdown_1,3)), round(max_drawdown_1,3))
    
if options == "Home":
    home()
elif options == "Markets":
    markets()
elif options == "News":
    news()
elif options == "Analytics":
    analytics()
