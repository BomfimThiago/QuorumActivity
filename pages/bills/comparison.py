import streamlit as st
import pandas as pd
import plotly.express as px
from utils.data_loader import load_data, merge_data

def main():
    st.title("Bill Comparison")

    # Load and merge data
    legislators, bills, votes, vote_results = load_data()
    merged_data = merge_data(legislators, bills, votes, vote_results)

    # Bill selection filters
    st.subheader("Select Bills to Compare")
    selected_bills = st.multiselect(
        "Select Bills",
        options=bills['title'].unique(),
        default=bills['title'].unique()[:2]  # Default to first two bills
    )

    if len(selected_bills) < 2:
        st.warning("Please select at least two bills to compare.")
    else:
        # Create comparison data
        comparison_data = []
        for bill in selected_bills:
            bill_data = merged_data[merged_data['title'] == bill]
            total_votes = len(bill_data)
            yes_votes = len(bill_data[bill_data['vote_type'] == 1])
            no_votes = len(bill_data[bill_data['vote_type'] == 2])
            
            comparison_data.append({
                'Bill': bill,
                'Total Votes': total_votes,
                'Yes Votes': yes_votes,
                'No Votes': no_votes,
                'Yes Percentage': (yes_votes / total_votes * 100) if total_votes > 0 else 0
            })

        # Create comparison DataFrame
        comparison_df = pd.DataFrame(comparison_data)
        
        # Display comparison table
        st.subheader("Vote Statistics Comparison")
        st.dataframe(comparison_df) 