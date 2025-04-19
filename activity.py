import streamlit as st
import pandas as pd
from firebase_admin import firestore

def app():
    db = firestore.client()

    radio_css = """<style>
                    .stButton {
                        text-align: center;
                        padding: 0px 250px;
                    }
                    .stNumberInput {
                        text-align: center;
                        padding: 0px 210px;
                    }
                </style>"""
    st.sidebar.markdown(radio_css, unsafe_allow_html=True)

    if st.session_state.username != "":
        try:
            st.markdown(f"<p style='font-size: 30px;'>Activity of <span style='text-transform: uppercase;'>{st.session_state['username']}</span></p>", unsafe_allow_html=True)
            data = db.collection("all_data").document(st.session_state.username).get()
            if data.exists:
                info = data.to_dict()
                activity = pd.DataFrame(info)
                activity = activity[["Time", "Category", "Rating", "Type", "Content For", "Genre", "Android Version"]]
                if len(activity) > 0:
                    st.write(activity)
                    index_to_delete = st.number_input('Enter the index of the row to delete:', min_value=0, max_value=len(activity)-1, step=1)
                    if st.button("Delete", use_container_width=1):
                        for key, value in info.items():
                            if isinstance(value, list) and len(value) > 0 and key != "Username":
                                del value[index_to_delete]
                        st.warning("Data of selected index has been deleted. Click My Activity option in side bar to see the change.")
                        db.collection("all_data").document(st.session_state.username).set(info)
                else:
                    st.write("Nothing to show!")         
            else:
                st.write("Nothing to show!")
        except:
            st.text("Getting Error!")
    else:
        st.text('Please login first')
