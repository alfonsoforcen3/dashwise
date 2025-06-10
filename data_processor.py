import pandas as pd

class DataProcessor:
    """
    Handles data preprocessing and calculation of key metrics
    for the dashboard and AI insights.
    """
    def process_and_calculate_metrics(self, df):
        """
        Performs data preprocessing and calculates metrics.
        Args:
            df: The raw Pandas DataFrame.
        Returns:
            A tuple containing the processed DataFrame and a dictionary of metrics,
            or (None, None) if processing fails.
        """
        try:
            # --- Data Preprocessing ---
            df['Date'] = pd.to_datetime(df['Date'])
            df['Day'] = df['Date'].dt.day_name()
            df['Hour'] = df['Date'].dt.hour
            # Ensure 'Profit (€)' column exists, calculate if not
            if 'Profit (€)' not in df.columns:
                df['Profit (€)'] = df['Revenue'] - df['Session Cost (€)']

            # --- Calculate Metrics ---
            # Handle potential empty DataFrame case
            if df.empty:
                 metrics = {
                    'top_day': 'N/A',
                    'top_service_revenue': 'N/A',
                    'most_profitable_service': 'N/A',
                    'avg_profit_most_profitable': 0.0,
                    'least_profitable_service': 'N/A',
                    'avg_profit_least_profitable': 0.0,
                    'premium_members': 0,
                    'peak_hour_overall': None,
                    'saturday_revenue': 0,
                    'sunday_revenue': 0,
                    'service_low_addons': 'N/A',
                    'lowest_addon_avg': 0.0
                }
            else:
                top_day = df.groupby('Day')['Revenue'].sum().idxmax()
                top_service = df.groupby('Service')['Revenue'].sum().idxmax()

                profit_by_service = df.groupby('Service')['Profit (€)'].mean()
                most_profitable_service = profit_by_service.idxmax() if not profit_by_service.empty else 'N/A'
                avg_profit_most_profitable = profit_by_service.max() if not profit_by_service.empty else 0.0
                least_profitable_service = profit_by_service.idxmin() if not profit_by_service.empty else 'N/A'
                avg_profit_least_profitable = profit_by_service.min() if not profit_by_service.empty else 0.0

                premium_members = df[df['Membership Type'] == 'Premium']['Client ID'].nunique()

                peak_hour_overall = df.groupby('Hour').size().idxmax() if not df.groupby('Hour').size().empty else None

                saturday_revenue = df[df['Day'] == 'Saturday']['Revenue'].sum() if 'Saturday' in df['Day'].unique() else 0
                sunday_revenue = df[df['Day'] == 'Sunday']['Revenue'].sum() if 'Sunday' in df['Day'].unique() else 0

                service_visits = df.groupby('Service').size()
                service_addon_sum = df.groupby('Service')['Add-on Sales (€)'].sum()
                service_addon_per_visit = (service_addon_sum / service_visits).fillna(0)
                service_low_addons = service_addon_per_visit.idxmin() if not service_addon_per_visit.empty else 'N/A'
                lowest_addon_avg = service_addon_per_visit.min() if not service_addon_per_visit.empty else 0.0

                metrics = {
                    'top_day': top_day,
                    'top_service_revenue': top_service,
                    'most_profitable_service': most_profitable_service,
                    'avg_profit_most_profitable': avg_profit_most_profitable,
                    'least_profitable_service': least_profitable_service,
                    'avg_profit_least_profitable': avg_profit_least_profitable,
                    'premium_members': premium_members,
                    'peak_hour_overall': peak_hour_overall,
                    'saturday_revenue': saturday_revenue,
                    'sunday_revenue': sunday_revenue,
                    'service_low_addons': service_low_addons,
                    'lowest_addon_avg': lowest_addon_avg
                }

            return df, metrics

        except Exception as e:
            import streamlit as st # Import st here to avoid circular dependency if not needed elsewhere
            st.error(f"❌ Error during data processing: {e}")
            return None, None