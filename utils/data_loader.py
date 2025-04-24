import pandas as pd
import streamlit as st

@st.cache_data
def load_data():
    legislators = pd.read_csv('assets/legislators.csv')
    bills = pd.read_csv('assets/bills.csv')
    votes = pd.read_csv('assets/votes.csv')
    vote_results = pd.read_csv('assets/vote_results.csv')
    return legislators, bills, votes, vote_results

def merge_data(legislators, bills, votes, vote_results):
    # First merge votes with bills
    votes_bills = votes.merge(bills, left_on='bill_id', right_on='id', how='left', suffixes=('_vote', '_bill'))
    
    # Then merge with vote_results
    merged_data = vote_results.merge(votes_bills, left_on='vote_id', right_on='id_vote', how='left')
    
    # Finally merge with legislators
    merged_data = merged_data.merge(legislators, left_on='legislator_id', right_on='id', how='left', suffixes=('', '_legislator'))
    
    return merged_data 