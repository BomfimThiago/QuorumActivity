import streamlit as st
import pandas as pd
import plotly.express as px
from utils.data_loader import load_data, merge_data

def main():
    st.title("Bill Analysis")

    # Load and merge data
    legislators, bills, votes, vote_results = load_data()
    merged_data = merge_data(legislators, bills, votes, vote_results)

    # Bill selection filter
    selected_bill = st.selectbox("Select a Bill to Analyze", bills['title'].unique())

    # Get bill sponsor information
    bill_info = bills[bills['title'] == selected_bill]
    sponsor_id = bill_info['sponsor_id'].iloc[0]

    # Display bill sponsor information
    st.subheader("Bill Information")
    bill_info_col, sponsor_info_col = st.columns(2)
    with bill_info_col:
        st.metric("Bill Title", selected_bill)
    with sponsor_info_col:
        # Check if sponsor exists in legislators table
        sponsor_match = legislators[legislators['id'] == sponsor_id]
        if not sponsor_match.empty:
            sponsor_name = sponsor_match['name'].iloc[0]
            st.metric("Primary Sponsor", sponsor_name)
        else:
            st.metric("Primary Sponsor", "Unknown (Sponsor ID: " + str(sponsor_id) + ")")

    # Filter data for selected bill
    bill_data = merged_data[merged_data['title'] == selected_bill]

    # Calculate vote statistics
    total_votes = len(bill_data)
    yes_votes = len(bill_data[bill_data['vote_type'] == 1])
    no_votes = len(bill_data[bill_data['vote_type'] == 2])
    yes_percentage = (yes_votes / total_votes * 100) if total_votes > 0 else 0

    # Display bill statistics
    st.subheader("Vote Statistics")
    total_votes_col, yes_votes_col, no_votes_col = st.columns(3)
    with total_votes_col:
        st.metric("Total Votes", total_votes)
    with yes_votes_col:
        st.metric("Yes Votes", yes_votes)
    with no_votes_col:
        st.metric("No Votes", no_votes)

    # Create pie chart for vote distribution
    fig = px.pie(
        values=[yes_votes, no_votes],
        names=['Yes', 'No'],
        title=f'Vote Distribution for {selected_bill}'
    )
    st.plotly_chart(fig)

    # Add filters for detailed voting results
    st.subheader("Detailed Voting Results")

    # Create two columns for filters
    legislator_filter_col, vote_type_filter_col = st.columns(2)

    with legislator_filter_col:
        # Legislator search filter
        legislator_search = st.text_input("Search by Legislator Name")

    with vote_type_filter_col:
        # Vote type filter
        vote_type = st.selectbox(
            "Filter by Vote Type",
            options=["All", "Yes", "No"],
            index=0
        )

    # Apply filters to voting results
    filtered_results = bill_data.copy()

    # Apply legislator name filter
    if legislator_search:
        filtered_results = filtered_results[filtered_results['name'].str.contains(legislator_search, case=False, na=False)]

    # Apply vote type filter
    if vote_type != "All":
        vote_value = 1 if vote_type == "Yes" else 2
        filtered_results = filtered_results[filtered_results['vote_type'] == vote_value]

    # Display filtered results
    if not filtered_results.empty:
        voting_results_df = filtered_results[['name', 'vote_type']].rename(
            columns={'name': 'Legislator', 'vote_type': 'Vote'}).replace(
            {1: 'Yes', 2: 'No'})
        st.dataframe(voting_results_df)
        
        # Show quick statistics for filtered results
        filtered_total = len(filtered_results)
        filtered_yes = len(filtered_results[filtered_results['vote_type'] == 1])
        filtered_no = len(filtered_results[filtered_results['vote_type'] == 2])
        
        st.write(f"Showing {filtered_total} results:")
        st.write(f"- {filtered_yes} Yes votes")
        st.write(f"- {filtered_no} No votes")
    else:
        st.warning("No voting results match the selected filters.") 