import streamlit as st
from pages.bills.analysis import main as show_bill_analysis
from pages.bills.comparison import main as show_bill_comparison
from pages.legislators.analysis import main as show_legislator_analysis

# Set page config
st.set_page_config(page_title="Legislative Data Analysis", layout="wide")

# Title
st.title("Legislative Data Analysis Dashboard")

# Create tabs
bill_analysis_tab, legislator_analysis_tab, bill_comparison_tab = st.tabs(["Bill Analysis", "Legislator Analysis", "Bill Comparison"])

# Tab 1: Bill Analysis
with bill_analysis_tab:
    show_bill_analysis()

# Tab 2: Legislator Analysis
with legislator_analysis_tab:
    show_legislator_analysis()

# Tab 3: Bill Comparison
with bill_comparison_tab:
    show_bill_comparison() 