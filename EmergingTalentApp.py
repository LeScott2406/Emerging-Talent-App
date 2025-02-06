#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
import pandas as pd
import numpy as np
import requests
import io

# Streamlit app setup
st.set_page_config(page_title="Emerging Talent Tracker", layout="wide")
st.title("Emerging Talent Tracker")

@st.cache_data
def load_data():
    file_url = 'https://github.com/LeScott2406/Model-App/raw/refs/heads/main/value_added_model%202.xlsx'
    response = requests.get(file_url)
    file_content = io.BytesIO(response.content)
    data = pd.read_excel(file_content)
    data.fillna(0, inplace=True)
    return data

# Load data
data = load_data()

# Filter for players aged 20 and under
data = data[data['Age'] <= 20]

# Sidebar filters
st.sidebar.header('Filters')

# Position filter with "All" option
position_options = ["All"] + list(data['Position'].unique())
position_filter = st.sidebar.multiselect('Select Position', position_options, default=["All"])
if "All" in position_filter:
    filtered_positions = data['Position'].unique()
else:
    filtered_positions = position_filter

# Usage filter (slider)
usage_filter = st.sidebar.slider('Select Usage Range', int(data['Usage'].min()), int(data['Usage'].max()), (int(data['Usage'].min()), int(data['Usage'].max())))

# Minutes p[layed filter (slider)
minutes_filter = st.sidebar.slider('Select Minutes Played Range', int(data['Minutes played'].min()), int(data['Minutes played'].max()), (int(data['Minutes played'].min()), int(data['Minutes played'].max())))

# Tier filter with "All" option
tier_options = ["All"] + list(data['Tier'].unique())
tier_filter = st.sidebar.multiselect('Select Tier', tier_options, default=["All"])
if "All" in tier_filter:
    selected_tiers = data['Tier'].unique()
else:
    selected_tiers = tier_filter

# League filter with "All" option
league_options = ["All"] + list(data['League'].unique())
league_filter = st.sidebar.multiselect('Select League', league_options, default=["All"])
if "All" in league_filter:
    selected_leagues = data['League'].unique()
else:
    selected_leagues = league_filter

# Apply filters
filtered_data = data[
    (data['Position'].isin(filtered_positions)) &
    (data['Usage'] >= usage_filter[0]) & (data['Usage'] <= usage_filter[1]) &
    (data['Minutes played'] >= minutes_filter[0]) & (data['Minutes played'] <= minutes_filter[1]) &
    (data['Tier'].isin(selected_tiers)) &
    (data['League'].isin(selected_leagues))
]

# Define role categories
role_mapping = {
    'Rightback': ['Attacking FB Score (0-100)', 'Inverted FB Score (0-100)', 'Defensive FB Score (0-100)'],
    'Leftback': ['Attacking FB Score (0-100)', 'Inverted FB Score (0-100)', 'Defensive FB Score (0-100)'],
    'Centreback': ['Defensive CB Score (0-100)', 'Ball playing CB Score (0-100)', 'Wide CB Score (0-100)'],
    'Midfielder': ['Distributor Score (0-100)', 'Defensive CM Score (0-100)', 'Number 6 Score (0-100)', 'Playmaker Score (0-100)', 'Ball Progressor Score (0-100)', 'Link Midfielder Score (0-100)', 'Chance creator Score (0-100)', 'True 10 Score (0-100)', 'Half space creator Score (0-100)'],
    'Left Winger': ['Half space creator Score (0-100)', 'Inverted Winger Score (0-100)', 'Winger Score (0-100)', 'Inside Forward Score (0-100)'],
    'Right Winger': ['Half space creator Score (0-100)', 'Inverted Winger Score (0-100)', 'Winger Score (0-100)', 'Inside Forward Score (0-100)'],
    'Striker': ['Advanced Striker Score (0-100)', 'Deep Striker Score (0-100)', 'Physical Striker Score (0-100)', 'Creative Striker Score (0-100)', 'False 9 Score (0-100)']
}

# Function to determine best role
def get_best_role(row):
    position = row['Position']
    if position in role_mapping:
        roles = role_mapping[position]
        best_role = max(roles, key=lambda role: row.get(role, 0))  # Get role with highest value
        return best_role.replace(" Score (0-100)", "")  # Remove score text
    return "Unknown"

filtered_data['Best Role'] = filtered_data.apply(get_best_role, axis=1)

# Display data
st.dataframe(filtered_data[['Player', 'Team', 'Age', 'Position', 'Minutes Played', 'Usage', 'Best Role']])

