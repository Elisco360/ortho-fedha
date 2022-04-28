import streamlit as st
import webbrowser
import requests
import pycountry

from streamlit_option_menu import option_menu

from economics import Economics as ec
from forex import Forex as fx
from bonds import Bonds as bnds
from equity import Equity as qt

st.set_page_config(page_icon='assets/icon.png', page_title='Ortho Fedha', layout='wide')

with st.sidebar:
    options = option_menu('Menu', ['Home', 'Markets', 'News'],
                          icons=['house', 'boxes', 'activity'],
                          menu_icon='dot')


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


if options == "Home":
    home()
elif options == "Markets":
    markets()
elif options == "News":
    st.title("News")
    ll, rr = st.columns([3, 1])
    ll.multiselect("Select a country", ["Ghana 🇬🇭", "Nigeria 🇳🇬", "Egypt 🇪🇬", "South Africa 🇿🇦", "Algeria 🇩🇿", "Morocco 🇲🇦",
                                        "Kenya 🇰🇪", "Ethiopia 🇪🇹", "Ivory Coast 🇨🇮", "Angola 🇦🇴", "China 🇨🇳", "United States 🇺🇸 ",
                                        "Russia 🇷🇺"])
    rr.selectbox("Select a news category", ["Business", "Technology", "Politics"])
    query = True

    if query:
        url = f"https://newsapi.org/v2/top-headlines?country=us&category=business&apiKey={apiKEY}"

