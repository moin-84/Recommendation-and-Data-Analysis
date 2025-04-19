import streamlit as st
from streamlit_option_menu import option_menu
import home, account, activity

st.set_page_config(
    page_title="Data Analysis - Google Play Store",
    page_icon="sunglasses"
)


class MultiApp:
    def __init__(self):
        self.apps = []

    def add_app(self, title, func):
        self.apps.append({
            "title": title,
            "function": func
        })

    def run():
        with st.sidebar:        
            app = option_menu(
                menu_icon = "None",
                menu_title = 'Data Analysis - GPS',
                options = ['Home','Account','My Activity'],
                icons = ['house-fill','person-circle','bar-chart'],
                
                default_index = 1,
                styles = {
                    "container": {"padding-top": "5px !important", "background-color":'black'},
                    "icon": {"color": "white", "font-size": "20px"},
                    "nav-link": {"color":"white","font-size": "18px", "text-align": "left", "margin":"-1px"},
                    "nav-link-selected": {"background-color": "#ab4002"},
                }            
            )
    
        if app == "Home":
            home.app()
        if app == "Account":
            account.app()          
        if app == 'My Activity':
            activity.app() 
                    
    run()            
