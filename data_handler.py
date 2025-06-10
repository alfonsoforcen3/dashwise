
class DataHandler:
    """
    Handles file uploading, demo data generation, template creation,
    and loading data into a Pandas DataFrame.
    """
    def handle_upload_and_demo(self, st_module=None, datetime_module=None, timedelta_module=None, random_module=None, pd_module=None, io_module=None):
        """
        Manages file uploading from the user and provides an option to use demo data.
        It also offers a template file for download.
        Returns:
            An uploaded file object (from Streamlit uploader) or an in-memory BytesIO buffer (for demo data).
        """
        # Fallback imports if modules are not passed (less ideal but makes it runnable standalone for testing)
        if st_module is None: import streamlit as st_module
        if datetime_module is None: from datetime import datetime as datetime_module
        if timedelta_module is None: from datetime import timedelta as timedelta_module
        if random_module is None: import random as random_module
        if pd_module is None: import pandas as pd_module
        if io_module is None: import io as io_module

        st_module.sidebar.subheader("📁 Upload your data")
        uploaded_file = st_module.sidebar.file_uploader("Upload your Excel file", type=["xlsx"], key="upload_gym")

        if st_module.sidebar.button("✨ Use Demo Data", key="demo_gym"):
            demo_buf = self._create_demo_data(datetime_module, timedelta_module, random_module, pd_module, io_module, st_module)
            st_module.session_state['demo_data_buffer'] = demo_buf
            st_module.session_state['use_demo_data'] = True
            st_module.success("✅ Realistic demo data loaded successfully")
        self._create_template(datetime_module, pd_module, io_module, st_module)

        if st_module.session_state.get('use_demo_data'):
            return st_module.session_state.get('demo_data_buffer')

        return uploaded_file

    # Pass necessary modules as arguments if they are no longer imported directly
    def _create_demo_data(self, datetime_module, timedelta_module, random_module, pd_module, io_module, st_module=None):
        """Creates a realistic in-memory demo DataFrame and returns it as a BytesIO buffer."""
        num_days = 30
        base_date = datetime_module.now() - timedelta_module(days=num_days)
        records = []

        for i in range(num_days):
            current_date = base_date + timedelta_module(days=i)
            weekday = current_date.weekday()
            for hour in range(6, 22):
                if weekday < 5:  # Weekdays
                    if 6 <= hour < 7: visitors = random_module.randint(5, 15)
                    elif 7 <= hour < 10: visitors = random_module.randint(60, 80)
                    elif 10 <= hour < 13: visitors = random_module.randint(25, 40)
                    elif 13 <= hour < 17: visitors = random_module.randint(40, 60)
                    elif 17 <= hour < 20: visitors = random_module.randint(70, 95)
                    else: visitors = random_module.randint(25, 45)
                elif weekday == 5: # Saturday
                    if 6 <= hour < 8: visitors = random_module.randint(5, 15)
                    elif 8 <= hour < 12: visitors = random_module.randint(45, 70)
                    elif 12 <= hour < 17: visitors = random_module.randint(50, 75)
                    elif 17 <= hour < 19: visitors = random_module.randint(15, 30)
                    else: visitors = random_module.randint(3, 10)
                else: # Sunday
                    if 6 <= hour < 8: visitors = random_module.randint(5, 10)
                    elif 8 <= hour < 13: visitors = random_module.randint(55, 80)
                    elif 13 <= hour < 18: visitors = random_module.randint(45, 65)
                    elif 18 <= hour < 20: visitors = random_module.randint(20, 35)
                    else: visitors = random_module.randint(10, 20)

                for _ in range(visitors):
                    client_id = random_module.randint(1000, 3000)
                    service = random_module.choices(
                        ['Workout', 'Yoga', 'CrossFit', 'Zumba', 'Personal Training', 'Pilates'],
                        weights=[70, 8, 8, 4, 6, 4], k=1
                    )[0]
                    membership = random_module.choices(['Standard', 'Premium', 'Pay-as-you-go'], [6, 3, 1])[0]

                    if service == 'Personal Training':
                        revenue = random_module.uniform(60, 85)
                    else:
                        revenue = 30 if membership == 'Standard' else 45 if membership == 'Premium' else 18

                    add_on = random_module.choices([0, 3, 5, 8], weights=[55, 20, 15, 10])[0]
                    supp = random_module.choices([0, 2, 4, 6], weights=[60, 25, 10, 5])[0]

                    if service == 'Personal Training':
                        session_cost = random_module.uniform(25, 40)
                    elif service in ['CrossFit']:
                        session_cost = random_module.uniform(15, 25)
                    elif service in ['Yoga', 'Zumba', 'Pilates']:
                        session_cost = random_module.uniform(10, 18)
                    elif service == 'Workout':
                        session_cost = random_module.uniform(5, 10)
                    else:
                        session_cost = random_module.uniform(8, 15)

                    profit = revenue - session_cost

                    records.append({
                        'Date': current_date.replace(hour=hour),
                        'Client ID': client_id,
                        'Service': service,
                        'Revenue': revenue,
                        'Membership Type': membership,
                        'Add-on Sales (€)': add_on,
                        'Supplements (€)': supp,
                        'Session Cost (€)': round(session_cost, 2),
                        'Profit (€)': round(profit, 2)
                    })

        df_demo = pd_module.DataFrame(records)
        demo_buf = io_module.BytesIO()
        with pd_module.ExcelWriter(demo_buf, engine='xlsxwriter') as writer:
            df_demo.to_excel(writer, sheet_name='Sheet1', index=False) # Added sheet_name for clarity
        demo_buf.seek(0)

        # Download button for generated demo data (appears only if demo data is used)
        if st_module is None: import streamlit as st_module # Fallback

        if 'demo_data_buffer' in st_module.session_state and st_module.session_state.get('use_demo_data', False):
             st_module.sidebar.download_button( # Changed st to st_module
                label="📥 Download Current Demo Data",
                data=st_module.session_state['demo_data_buffer'], # Changed st to st_module
                file_name="current_gym_demo_data.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                key="download_current_demo"
            )

        return demo_buf

    def _create_template(self, datetime_module, pd_module, io_module, st_module=None):
        """Creates a sample DataFrame for the template and provides a download button."""
        df_template = pd_module.DataFrame({
            'Date': [datetime_module.now()],
            'Client ID': [1234],
            'Service': ['Workout'],
            'Revenue': [30.0],
            'Membership Type': ['Standard'],
            'Add-on Sales (€)': [5.0],
            'Supplements (€)': [3.0],
            'Session Cost (€)': [7.50],
            'Profit (€)': [22.50]
        })
        template_buf = io_module.BytesIO()
        with pd_module.ExcelWriter(template_buf, engine='xlsxwriter') as writer:
            df_template.to_excel(writer, sheet_name='Sheet1', index=False) # Added sheet_name
        template_buf.seek(0)

        if st_module is None: import streamlit as st_module # Fallback

        st_module.sidebar.download_button(
            label="⬇️ Download Template",
            data=template_buf,
            file_name="gym_template.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    def load_data(self, file_object, pd_module=None, st_module=None):
        """
        Loads data from a file-like object (uploaded file or BytesIO buffer)
        into a Pandas DataFrame.
        Args:
            file_object: The file object or BytesIO buffer.
        Returns:
            A Pandas DataFrame if successful, None otherwise.
        """
        if pd_module is None: # Fallback if not passed, relying on global import from main
            import pandas as pd_module
        if st_module is None: import streamlit as st_module # Fallback for error display
        try:
            return pd_module.read_excel(file_object, sheet_name=0, engine='openpyxl')
        except Exception as e:
            st_module.error(f"❌ Failed to load Excel file: {e}")
            return None