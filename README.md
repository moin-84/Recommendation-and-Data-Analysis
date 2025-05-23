Google Play Store Data Analysis App<br>
This is a Streamlit-based web application for analyzing Google Play Store app data. It allows users to sign up, log in, explore app data through visualizations, and manage their activity history. The app uses Firebase for authentication and Firestore for storing user data, with data processing and visualization powered by pandas, Plotly, and Streamlit.

<br>
<br>
Features
<br>
User Authentication: Sign up and log in using Firebase Authentication.
<br>
Data Exploration: Filter and visualize Google Play Store app data (e.g., by category, rating, or genre) using interactive charts. <br>
Activity Management: View and delete user activity records stored in Firestore.<br>
Data Source: Analyzes a dataset (gps.csv) containing details like app names, categories, ratings, and Android versions. <br>
<br><br>
Project Structure
<br>
main.py: Entry point for the Streamlit app, handling navigation and page routing.<br>
home.py: Displays the main dashboard with data filtering and visualization options.<br>
helper.py: Contains utility functions for data processing and generating Plotly charts.<br>
activity.py: Manages user activity history, allowing users to view and delete records.<br>
account.py: Handles user authentication (signup/login) using Firebase.<br>
gps.csv: Dataset containing Google Play Store app data.<br>
data-analysis---gps84-9724330a2ca9.json: Firebase credentials file (not included in the repository for security).<br>
<br><br>
Prerequisites <br>
<br>
Python 3.8+ <br>
A Firebase project with Authentication and Firestore enabled.<br>
A Firebase Web API key and service account credentials file.<br>
<br>
Setup Instructions<br>

Clone the Repository:<br>
git clone https://github.com/your-username/your-repo-name.git<br>
cd your-repo-name<br>
<br>

Install Dependencies:Create a virtual environment and install the required packages:<br>
python -m venv venv<br>
source venv/bin/activate  # On Windows: venv\Scripts\activate<br>
pip install -r requirements.txt<br>
<br>
<br>
Set Up Firebase:<br>

Create a Firebase project at Firebase Console.<br>
Enable Email/Password Authentication in the Authentication section.<br>
Set up Firestore in the Database section.<br>
Download your service account key (your-firebase-credentials.json) and place it in the project root.<br>
Update account.py with your Firebase Web API key (replace the existing key in the sign_up_with_email_and_password and sign_in_with_email_and_password functions).<br>
<br>
<br>
Add the Dataset:<br>

Ensure gps.csv is in the project root. This file contains the Google Play Store data used by the app.<br>
<br>

Run the Application:<br>
streamlit run main.py<br>
<br>
The app will open in your default browser at http://localhost:8501.<br>
<br>

Requirements<br>
Install the following dependencies using pip install -r requirements.txt. The requirements.txt file should include:<br>
streamlit<br>
pandas<br>
plotly<br>
firebase-admin<br>
requests<br>
<br>
Usage<br>

Login/Signup: Use the sidebar to sign up with a username, email, and password, or log in with existing credentials.<br>
Explore Data: On the Home page, filter the dataset by category, rating, or other attributes, and view interactive visualizations.<br>
View Activity: Check your activity history on the Activity page, where you can delete specific records.<br>
Sign Out: Log out from the account page to end your session.<br>

Dataset
The gps.csv file contains Google Play Store app data with columns such as:

App Name
Category
Rating
Type
Content For
Genre
Android Version

The app uses this data for filtering and visualization.
Notes

Ensure the Firebase credentials file is not committed to the repository. Add it to .gitignore:*.json


The app assumes a Firestore collection named all_data for storing user activity. Ensure this collection exists or modify activity.py accordingly.
For production, consider securing the Firebase API key and credentials using environment variables.


Built with Streamlit for the web interface.
Uses Firebase for authentication and data storage.
Data analysis powered by pandas and Plotly.

