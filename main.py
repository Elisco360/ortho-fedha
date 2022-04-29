import streamlit as st
import webbrowser
import requests
from annotated_text import annotated_text
from streamlit_option_menu import option_menu

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
    lb.image("assets/logo.png")
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
                st.image("assets/news.png")
            st.markdown(" ")
            st.write(each_article['description'])
            
            
def analytics():
    st.title("Analytics")
    ll, rr = st.columns(2)

    file = st.file_uploader("Choose your CSV file", accept_multiple_files=False, help="Please make sure your file is in csv format.")
    
    try:
        pd.dataframe = pd.read_csv(uploaded_file)
     	st.write(dataframe)
    except:
        st.error("Please make sure your file is in CSV format and has at least 2 columns.\n 
                 "The first column should contain dates and the second should contain prices.")

    
if options == "Home":
    home()
elif options == "Markets":
    markets()
elif options == "News":
    news()
elif options == "Analytics":
    analytics()
