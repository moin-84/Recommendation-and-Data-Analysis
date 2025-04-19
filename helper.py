import plotly.express as px
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

## Search by queries

# Category
def cats_list(store_data):
    cats = np.unique(store_data["Category"].dropna().values).tolist()
    cats.sort()
    cats.insert(0, "All")

    return cats

# Rating
def rats_list(store_data):
    rats = np.unique(store_data["Rating"].dropna().values).tolist()
    rats.sort()
    rats.insert(0, "All")

    return rats

# Types
def types_list(store_data):
    types = np.unique(store_data["Type"].dropna().values).tolist()
    types.sort()
    types.insert(0, "All")

    return types

# Content For
def contentsFor_list(store_data):
    contentsFor = np.unique(store_data["Content For"].dropna().values).tolist()
    contentsFor.sort()
    contentsFor.insert(0, "All")

    return contentsFor    

# Genre
def genres_list(store_data):
    genres = np.unique(store_data["Genres"].dropna().values).tolist()
    genres.sort()
    genres.insert(0, "All")

    return genres    

# Android Version
def andVers_list(store_data):
    andVers = np.unique(store_data["Android Version"].dropna().values).tolist()
    andVers.sort()
    andVers.insert(0, "All")

    return andVers 


def fetch_bySelection(store_data, sel_cat, sel_rat, sel_type, sel_contentFor, sel_genre, sel_andVer):
    if sel_cat != "All":
        store_data = store_data[store_data["Category"] == sel_cat]
    if sel_rat != "All":
        store_data = store_data[store_data["Rating"] == sel_rat]
    if sel_type != "All":
        store_data = store_data[store_data["Type"] == sel_type]
    if sel_contentFor != "All":
        store_data = store_data[store_data["Content For"] == sel_contentFor]
    if sel_genre != "All":
        store_data = store_data[store_data["Genres"] == sel_genre]
    if sel_andVer != "All":
        store_data = store_data[store_data["Android Version"] == sel_andVer]

    return store_data



## Visual representation of data

# Category
def apps_over_cats(store_data):
    apps_over_cats = store_data.drop_duplicates(["Category", "App Name"])["Category"].value_counts().reset_index().sort_values("Category")
    apps_over_cats = apps_over_cats.rename(columns={"count": "No of apps"})

    return apps_over_cats

# Rating
def apps_over_rats(store_data):
    apps_over_rats = store_data.drop_duplicates(["Rating", "App Name"])["Rating"].value_counts().reset_index().sort_values("Rating")
    apps_over_rats = apps_over_rats.rename(columns={"count": "No of apps"})

    return apps_over_rats

# Price
def apps_over_price(store_data):
    apps_over_price = store_data.drop_duplicates(["Price", "App Name"])["Price"].value_counts().reset_index().sort_values("Price")
    apps_over_price = apps_over_price.rename(columns={"Price": "Price ($)", "count": "No of apps"})

    return apps_over_price

# Content for
def apps_over_conts(store_data):
    apps_over_conts = store_data.drop_duplicates(["Content For", "App Name"])["Content For"].value_counts().reset_index().sort_values("Content For")
    apps_over_conts = apps_over_conts.rename(columns={"count": "No of apps"})

    return apps_over_conts

# Android version
def apps_over_vers(store_data):
    apps_over_vers = store_data.drop_duplicates(["Android Version", "App Name"])["Android Version"].value_counts().reset_index().sort_values("Android Version")
    apps_over_vers = apps_over_vers.rename(columns={"count": "No of apps"})

    return apps_over_vers
