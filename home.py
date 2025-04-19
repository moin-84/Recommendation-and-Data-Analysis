import streamlit as st
from firebase_admin import firestore
import pandas as pd
import re, helper, datetime
import plotly.express as px
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def app():
    if 'db' not in st.session_state:
        st.session_state.db = ''
    
    db = firestore.client()
    st.session_state.db = db

    store_data = pd.read_csv("gps.csv")
    store_data.drop_duplicates(inplace=True)
    store_data.dropna(inplace=True)

    radio_css = """<style>
                    .stRadio {
                        color: #fff;
                        background-color: #000;
                        padding: 10px 20px;
                        border-radius: 8px;
                        margin-top: -20px;
                        margin-bottom: 20px;
                    }
                    .stSelectbox {
                        padding: 0px 20px;
                        margin-top: -10px;
                    }
                    .stButton {
                        text-align: center;
                        padding: 0px 40px;
                    }
                </style>"""
    st.sidebar.markdown(radio_css, unsafe_allow_html=True)

    def save_data(now, sel_cat, sel_rat, sel_type, sel_contentFor, sel_genre, sel_andVer, add_data):
        info = db.collection("all_data").document(st.session_state.username).get()
        if info.exists:
            exist_data = info.to_dict()
            exist_data["Time"].append(now)
            exist_data["Category"].append(sel_cat)
            exist_data["Rating"].append(sel_rat)
            exist_data["Type"].append(sel_type)
            exist_data["Content For"].append(sel_contentFor)
            exist_data["Genre"].append(sel_genre)
            exist_data["Android Version"].append(sel_andVer)
            exist_data["Tags"].append(add_data)
            exist_data["Username"] = st.session_state.username

            db.collection("all_data").document(st.session_state.username).set(exist_data)
        else:
            data = {"Time":[now], "Category":[sel_cat], "Rating":[sel_rat], "Type":[sel_type], "Content For":[sel_contentFor], "Genre":[sel_genre], "Android Version":[sel_andVer], "Tags":[add_data], "Username":st.session_state.username}
            db.collection("all_data").document(st.session_state.username).set(data)

    user_menu = st.sidebar.radio (
        "Select Options",
        ("Search By Queries", "Visual Representaion of Data", "Recommendations")
    )

    if user_menu == "Search By Queries":
        if st.session_state.username == "":
            st.write("Login to save your work.")

        cats = helper.cats_list(store_data)
        sel_cat = st.sidebar.selectbox("Select Category", cats)
        ssel_cat = re.sub(r'\s', '', str(sel_cat))

        rats = helper.rats_list(store_data)
        sel_rat = st.sidebar.selectbox("Select Rating", rats)
        ssel_rat = re.sub(r'\s', '', str(sel_rat))

        types = helper.types_list(store_data)
        sel_type = st.sidebar.selectbox("Select Type", types)
        ssel_type = re.sub(r'\s', '', str(sel_type))

        contentsFor = helper.contentsFor_list(store_data)
        sel_contentFor = st.sidebar.selectbox("Select Content For", contentsFor)
        ssel_contentFor = re.sub(r'\s', '', str(sel_contentFor))

        genres = helper.genres_list(store_data)
        sel_genre = st.sidebar.selectbox("Select Genre", genres)
        ssel_genre = re.sub(r'\s', '', str(sel_genre))

        andVers = helper.andVers_list(store_data)
        sel_andVer = st.sidebar.selectbox("Select Android Version", andVers)
        ssel_andVer = re.sub(r'\s', '', str(sel_andVer))

        if not st.sidebar.button("Search", use_container_width=5):
            st.dataframe(store_data, height=850)
        else:
            temp_data = helper.fetch_bySelection(store_data, sel_cat, sel_rat, sel_type, sel_contentFor, sel_genre, sel_andVer)
            st.dataframe(temp_data, height=850)

            ssel_cat = "" if ssel_cat == "All" else ssel_cat
            ssel_rat = "" if ssel_rat == "All" else ssel_rat
            ssel_type = "" if ssel_type == "All" else ssel_type
            ssel_contentFor = "" if ssel_contentFor == "All" else ssel_contentFor
            ssel_genre = "" if ssel_genre == "All" else ssel_genre
            ssel_andVer = "" if ssel_andVer == "All" else ssel_andVer

            now = datetime.datetime.now().strftime("%Y-%m-%d__%H:%M:%S")
            add_data = ssel_cat +" "+ ssel_rat +" "+ ssel_type +" "+ ssel_contentFor +" "+ ssel_genre +" "+ ssel_andVer
            add_data = add_data.strip()
            
            save_data(now, str(sel_cat), str(sel_rat), str(sel_type), str(sel_contentFor), str(sel_genre), str(sel_andVer), str(add_data))

            info = db.collection("all_data").document(st.session_state.username).get()

    if user_menu == "Visual Representaion of Data":
        apps_over_cats = helper.apps_over_cats(store_data)
        figure_cats = px.line(apps_over_cats, x="Category", y="No of apps")
        st.markdown("<p style='font-size: 30px; text-align: center;'>Number of apps by Category</p>", unsafe_allow_html=True)
        st.plotly_chart(figure_cats)

        apps_over_rats = helper.apps_over_rats(store_data)
        figure_rats = px.line(apps_over_rats, x="Rating", y="No of apps")
        st.markdown("<p style='font-size: 30px; text-align: center; padding-top: 100px;'>Number of apps by Rating</p>", unsafe_allow_html=True)
        st.plotly_chart(figure_rats)

        apps_over_price = helper.apps_over_price(store_data)
        figure_price = px.line(apps_over_price, x="Price ($)", y="No of apps")
        st.markdown("<p style='font-size: 30px; text-align: center; padding-top: 100px;'>Number of apps by Price</p>", unsafe_allow_html=True)
        st.plotly_chart(figure_price)

        apps_over_conts = helper.apps_over_conts(store_data)
        figure_conts = px.line(apps_over_conts, x="Content For", y="No of apps")
        st.markdown("<p style='font-size: 30px; text-align: center; padding-top: 100px;'>Number of apps by Contents For</p>", unsafe_allow_html=True)
        st.plotly_chart(figure_conts)

        apps_over_vers = helper.apps_over_vers(store_data)
        figure_vers = px.line(apps_over_vers, x="Android Version", y="No of apps")
        st.markdown("<p style='font-size: 30px; text-align: center; padding-top: 100px;'>Number of apps by Android Version</p>", unsafe_allow_html=True)
        st.plotly_chart(figure_vers)

    if user_menu == "Recommendations":
        new_data = store_data[["App Name", "Category", "Rating", "Type", "Content For", "Genres", "Android Version"]]
        new_data.dropna(inplace=True) # droping null values

        new_data["Category"] = new_data["Category"].apply(lambda x:str(x)) # converting to string
        new_data["Rating"] = new_data["Rating"].apply(lambda x:str(x))
        new_data["Type"] = new_data["Type"].apply(lambda x:str(x))
        new_data["Content For"] = new_data["Content For"].apply(lambda x:str(x))
        new_data["Genres"] = new_data["Genres"].apply(lambda x:str(x))
        new_data["Android Version"] = new_data["Android Version"].apply(lambda x:str(x))

        new_data["Content For"] = new_data["Content For"].apply(lambda x:x.replace(" ", "")) # removing empty space
        new_data["Genres"] = new_data["Genres"].apply(lambda x:x.replace(" ", ""))
        new_data["Android Version"] = new_data["Android Version"].apply(lambda x:x.replace(" ", ""))

        new_data02 = new_data[["App Name"]]
        new_data02["Tags"] = new_data["Category"] +" "+ new_data["Rating"] +" "+ new_data["Type"] +" "+ new_data["Content For"] +" "+ new_data["Genres"] +" "+ new_data["Android Version"]
        
        info = db.collection("all_data").document(st.session_state.username).get()
        if info.exists:
            tags = ""
            data = info.to_dict()
            length = len(data.get("Tags"))

            if length != 0:
                for i in range(0, length):
                    tags = tags +" "+ (data.get("Tags")[i])

                new_row = {
                    "App Name": "MoinME",
                    "Tags": tags
                }
                new_data02.loc[len(new_data02)] = new_row
                new_data02["Tags"] = new_data02["Tags"].apply(lambda x:x.lower())  # lowering charecters

                def custom_tokenizer(text): # tokenize only if a word contains "." or ";"
                    return re.findall(r'\w+\.\w+|\w+;\w+|\w+', text)

                cv = CountVectorizer(max_features=206, tokenizer=custom_tokenizer)
                vectors = cv.fit_transform(new_data02["Tags"]).toarray()

                similarity = cosine_similarity(vectors)
                app_index = new_data02[new_data02["App Name"] == "MoinME"].index[0]
                app_list = sorted(list(enumerate(similarity[app_index])), reverse=True, key=lambda x:x[1])[1:11]

                rec_apps = pd.DataFrame(columns=store_data.columns)
                for i in app_list:
                    rec_apps.loc[len(rec_apps)] = store_data.iloc[i[0]]

                rec_apps.index = rec_apps.index + 1
                st.write(rec_apps)
            else:
                st.write("Nothing to recommend.")
        else:
            st.write("Nothing to recommend.")
