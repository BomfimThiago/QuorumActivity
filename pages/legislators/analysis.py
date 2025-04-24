import streamlit as st
import pandas as pd
import plotly.express as px
from utils.data_loader import load_data, merge_data

def main():
    st.title("Legislator Analysis")

    # Load and merge data
    legislators, bills, votes, vote_results = load_data()
    merged_data = merge_data(legislators, bills, votes, vote_results)

    # Create tabs for individual and summary views
    individual_analysis_tab, all_legislators_summary_tab = st.tabs(["Individual Analysis", "All Legislators Summary"])

    with individual_analysis_tab:
        # Legislator selection filter
        selected_legislator = st.selectbox("Select a Legislator to Analyze", legislators['name'].unique())
        
        # Filter data for selected legislator
        legislator_data = merged_data[merged_data['name'] == selected_legislator]
        
        # Calculate voting statistics
        total_votes = len(legislator_data)
        yes_votes = len(legislator_data[legislator_data['vote_type'] == 1])
        no_votes = len(legislator_data[legislator_data['vote_type'] == 2])
        yes_percentage = (yes_votes / total_votes * 100) if total_votes > 0 else 0
        
        # Display legislator statistics
        st.subheader("Voting Statistics")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Votes", total_votes)
        with col2:
            st.metric("Yes Votes", yes_votes)
        with col3:
            st.metric("No Votes", no_votes)
        
        # Create pie chart for vote distribution
        fig = px.pie(
            values=[yes_votes, no_votes],
            names=['Yes', 'No'],
            title=f'Vote Distribution for {selected_legislator}'
        )
        st.plotly_chart(fig)
        
        # Display voting history
        st.subheader("Voting History")
        voting_history = legislator_data[['title', 'vote_type']].rename(
            columns={'title': 'Bill', 'vote_type': 'Vote'}).replace(
            {1: 'Yes', 2: 'No'})
        st.dataframe(voting_history)

    with all_legislators_summary_tab:
        # Calculate statistics for all legislators
        all_legislators_stats = []
        for legislator in legislators['name'].unique():
            legislator_data = merged_data[merged_data['name'] == legislator]
            total_votes = len(legislator_data)
            yes_votes = len(legislator_data[legislator_data['vote_type'] == 1])
            no_votes = len(legislator_data[legislator_data['vote_type'] == 2])
            yes_percentage = (yes_votes / total_votes * 100) if total_votes > 0 else 0
            
            all_legislators_stats.append({
                'Legislator': legislator,
                'Total Votes': total_votes,
                'Yes Votes': yes_votes,
                'No Votes': no_votes,
                'Yes Percentage': yes_percentage
            })
        
        # Create summary DataFrame
        summary_df = pd.DataFrame(all_legislators_stats)
        
        # Display summary table
        st.subheader("All Legislators Summary")
        st.dataframe(summary_df)
