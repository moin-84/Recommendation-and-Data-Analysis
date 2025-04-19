import streamlit as st
import firebase_admin, json, requests
from firebase_admin import credentials

if not firebase_admin._apps:
    cred = credentials.Certificate("data-analysis---gps84-9724330a2ca9.json")
    firebase_admin.initialize_app(cred)

def app():
    st.markdown("<p style='font-size: 30px; text-align: center;'>Data Analysis - Google Play Store</p>", unsafe_allow_html=True)

    radio_css = """<style>
                    .stButton {
                        text-align: center;
                        padding: 0px 250px;
                    }
                </style>"""
    st.sidebar.markdown(radio_css, unsafe_allow_html=True)


    if 'username' not in st.session_state:
        st.session_state.username = ''
    if 'useremail' not in st.session_state:
        st.session_state.useremail = ''

    def sign_up_with_email_and_password(email, password, username=None, return_secure_token=True):
        try:
            rest_api_url = "https://identitytoolkit.googleapis.com/v1/accounts:signUp"
            payload = {
                "email": email,
                "password": password,
                "returnSecureToken": return_secure_token
            }
            if username:
                payload["displayName"] = username 
            payload = json.dumps(payload)
            r = requests.post(rest_api_url, params={"key": "AIzaSyAFuZwBkzdXM37t5XaSYg89g0JiXI02uRQ"}, data=payload)
            #AIzaSyApr-etDzcGcsVcmaw7R7rPxx3A09as7uw
            try:
                return r.json()['email']
            except:
                st.warning(r.json())
        except:
            st.warning(f'Signup failed!')

    def sign_in_with_email_and_password(email=None, password=None, return_secure_token=True):
        rest_api_url = "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword"

        try:
            payload = {
                "returnSecureToken": return_secure_token
            }
            if email:
                payload["email"] = email
            if password:
                payload["password"] = password
            payload = json.dumps(payload)
            print('payload sigin',payload)
            r = requests.post(rest_api_url, params={"key": "AIzaSyAFuZwBkzdXM37t5XaSYg89g0JiXI02uRQ"}, data=payload)
            try:
                data = r.json()
                user_info = {
                    'email': data['email'],
                    'username': data.get('displayName')  # Retrieve username if available
                }
                return user_info
            except:
                st.warning("Enter correct email and password!")
        except:
            st.warning(f'Signin failed!')


    def logged_in(): 
        try:
            userinfo = sign_in_with_email_and_password(st.session_state.email_input,st.session_state.password_input)
            st.session_state.username = userinfo['username']
            st.session_state.useremail = userinfo['email']

            global Usernm
            Usernm=(userinfo['username'])
            
            st.session_state.signedout = True
            st.session_state.signout = True    
  
        except: 
            st.warning('Login Failed!')


    def logged_out():
        st.session_state.signout = False
        st.session_state.signedout = False   
        st.session_state.username = ''
    
        
    if "signedout" not in st.session_state:
        st.session_state["signedout"] = False
    if 'signout' not in st.session_state:
        st.session_state['signout'] = False    
        

    if not st.session_state["signedout"]: # only show if the state is False, hence the button has never been clicked
        choice = st.selectbox('Login/Signup',['Login','Signup'])
        
        if choice == 'Signup':
            username = st.text_input("Enter a unique username")
            email = st.text_input('Email address')
            password = st.text_input('Password',type='password')

            st.session_state.email_input = email
            st.session_state.password_input = password

            if st.button('Create my account', use_container_width=1):
                user = sign_up_with_email_and_password(email=email, password=password, username=username)
                st.success('Account created successfully.  You can login now using your email and password.')
        else:
            email = st.text_input('Email Address')
            password = st.text_input('Password',type='password')

            st.session_state.email_input = email
            st.session_state.password_input = password

            st.button('Login', on_click=logged_in, use_container_width=1)


    if st.session_state.signout:
        st.text('Name : '+ st.session_state.username)
        st.text('Email: '+ st.session_state.useremail)
        st.button('Sign out', on_click=logged_out) 
