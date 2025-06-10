import streamlit as st # Import Streamlit library for creating web apps
import pandas as pd # Import Pandas for data manipulation and analysis
import io # Import io for handling in-memory binary streams
import random # Import random for generating random numbers
from datetime import datetime, timedelta # Import datetime and timedelta for date and time manipulations
import plotly.express as px # Import Plotly Express for creating interactive plots

# --- Internal Module Imports ---
from data_handler import DataHandler
from data_processor import DataProcessor
from dashboard_renderer import DashboardRenderer

# --- Page Configuration ---
# Set the configuration for the Streamlit page
st.set_page_config(
    page_title="DashWise | Local BI for SMEs", # Title that appears in the browser tab
    layout="wide", # Use a wide layout for the page content
    initial_sidebar_state="expanded", # Ensure the sidebar is expanded by default
    page_icon="📊" # Set an icon for the page (appears in browser tab)
)

# --- Login Functionality ---
def display_login_form():
    """Displays the login form and handles authentication."""
    st.markdown("<h1 style='text-align: center; color: white;'>Welcome to DashWise</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #cccccc;'>Your Local Business Intelligence Co-Pilot</h3>", unsafe_allow_html=True)
    st.markdown("---")

    with st.form("login_form", clear_on_submit=True):
        st.subheader("🔑 Login to Access Dashboard")
        username = st.text_input("Username", key="login_username_input", placeholder="Enter username")
        password = st.text_input("Password", type="password", key="login_password_input", placeholder="Enter password")
        submitted = st.form_submit_button("Login")

        if submitted:
            # Simple hardcoded credentials
            if username == "guest" and password == "guest":
                st.session_state.logged_in = True
                st.session_state.login_attempted = True # To avoid re-showing error after successful login then failed upload
                st.rerun()
            else:
                st.error("Incorrect username or password. Please try again.")
                st.session_state.logged_in = False
                st.session_state.login_attempted = True

    st.sidebar.info("ℹ️ Use credentials: guest / guest")

# --- Main Application Logic ---
def main():
    """
    Main function to run the Streamlit application.
    Orchestrates data handling, processing, and dashboard rendering.
    """
    # Initialize session state for login if not already present
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'login_attempted' not in st.session_state:
        st.session_state.login_attempted = False

    if not st.session_state.logged_in:
        display_login_form()
    else:
        # User is logged in, proceed to dashboard logic
        data_handler = DataHandler()
        data_processor = DataProcessor()
        dashboard_renderer = DashboardRenderer()

        # Sidebar elements for data upload/demo
        uploaded_file_or_buffer = data_handler.handle_upload_and_demo()

        final_df = None
        final_metrics = None
        data_load_attempted = False

        if uploaded_file_or_buffer:
            data_load_attempted = True
            df = data_handler.load_data(uploaded_file_or_buffer)
            if df is not None:
                processed_df, metrics = data_processor.process_and_calculate_metrics(df)
                if processed_df is not None:
                    final_df = processed_df
                    final_metrics = metrics
        
        # Always render the dashboard structure (title will show)
        # Charts and AI insights will adapt based on final_df and final_metrics
        dashboard_renderer.render(final_df, final_metrics)

        # Provide contextual messages if data isn't fully loaded/processed
        if final_df is None:
            if data_load_attempted: # User tried to load data, but it failed at some stage
                # Errors from DataHandler or DataProcessor should already be visible
                st.error("Data could not be fully loaded or processed. Please check any error messages above and verify your file.")
            else: # User is logged in, but hasn't uploaded/selected demo data yet
                st.info("📊 Welcome! Please upload your data or use the demo data via the sidebar to populate the dashboard.")

if __name__ == "__main__":
    main()
