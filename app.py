import os
import pickle
import streamlit as st
from dotenv import load_dotenv
from utils.b2 import B2
import folium
from streamlit_folium import folium_static




# ------------------------------------------------------
#                      APP CONSTANTS
# ------------------------------------------------------
REMOTE_DATA = 'NPS.ipynbnational_parks.csv'


# ------------------------------------------------------
#                        CONFIG
# ------------------------------------------------------
load_dotenv()

# load Backblaze connection
b2 = B2(endpoint=os.environ['B2_ENDPOINT'],
        key_id=os.environ['B2_KEYID'],
        secret_key=os.environ['B2_APPKEY'])

# ------------------------------------------------------
#                        CACHING
# ------------------------------------------------------
@st.cache_data
def get_data():
#     # collect data frame of reviews and their sentiment
    b2.set_bucket(os.environ['B2_BUCKETNAME'])
    df = b2.get_df(REMOTE_DATA)
    
    return df



# ------------------------------------------------------
#                         APP
# ------------------------------------------------------
# ------------------------------
# PART 0 : Overview
# ------------------------------
st.title('National Parks Data')
st.subheader('Distribution of Parks by States')

st.subheader('This is a view of a subset of National park data ')
df_park = get_data()


state = st.selectbox("Select a State", sorted(df_park['address_stateCode'].unique()))

# Filter DataFrame based on selected state
filtered_df = df_park[df_park['address_stateCode'] == state]

# Display list of national parks in the selected state
st.subheader("National Parks in {}".format(state))
st.write(filtered_df['fullName'].unique())

# Select a national park
selected_park = st.selectbox("Select a National Park", sorted(filtered_df['fullName'].unique()))

# Filter DataFrame based on selected national park
park_details = filtered_df[filtered_df['fullName'] == selected_park].iloc[0]

st.subheader(selected_park)
st.write("**Designation:**", park_details['designation'])
st.write("**Description:**", park_details['description'])
st.write("**Weather Info:**", park_details['weatherInfo'])
st.write("**Direction Info:**", park_details['directionsInfo'])

st.subheader("Location Map")
map_center = (park_details['latitude'], park_details['longitude'])
m = folium.Map(location=map_center, zoom_start=10)
folium.Marker(location=map_center, popup=selected_park).add_to(m)
folium_static(m)


st.subheader("Next Steps :")
multiline_text = '''
1. Need to add more features/functionalities, this web-app has only basic features
2. Need to add color, styling, layout.
'''
st.write(multiline_text)
