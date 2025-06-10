from ai_suggestion_engine import AISuggestionEngine

class DashboardRenderer:
    """
    Handles the rendering of the dashboard elements: title, AI insights, and charts.
    """
    def __init__(self):
        self.ai_engine = AISuggestionEngine()

    def render(self, df, metrics, st_module=None, pd_module=None, px_module=None, random_module=None):
        """
        Renders the main dashboard content.
        Args:
            df: The processed Pandas DataFrame.
            metrics: A dictionary containing key performance indicators.
        """
        self._render_title()
        self._render_ai_insights(df, metrics, st_module, random_module)
        if st_module: # Check if st_module is provided
            st_module.markdown("---") # Add a horizontal rule for separation
        else: # Fallback to global import if not provided (less ideal)
            import streamlit as st
            st.markdown("---")
        self._render_charts(df, st_module, pd_module, px_module)

    def _render_title(self, st_module=None):
        """Displays the main dashboard title and subtitle."""
        if st_module is None:
            import streamlit as st_module # Fallback

        st_module.markdown("""
            <h1 style='text-align: center; color: white;'>🏋️ Gym Dashboard</h1>
            <h4 style='text-align: center; color: white;'>Local Business Intelligence for Fitness Studios</h4>
        """, unsafe_allow_html=True)

    def _render_ai_insights(self, df, metrics, st_module=None, random_module=None):
        """Displays the AI insights section with a random suggestion."""
        all_ai_suggestions = self.ai_engine.generate_suggestions(df, metrics)

        # Initialize session state for AI suggestions
        if 'current_ai_suggestion' not in st.session_state or st.session_state.current_ai_suggestion is None:
            if all_ai_suggestions:
                st.session_state.current_ai_suggestion = random.choice(all_ai_suggestions)
                # Ensure random is available
                if random_module:
                    st.session_state.current_ai_suggestion = random_module.choice(all_ai_suggestions)
                else: # Fallback
                    import random as random_module
                    st.session_state.current_ai_suggestion = random_module.choice(all_ai_suggestions)
                # Check if current_ai_suggestion is in the list before finding index
                if st.session_state.current_ai_suggestion in all_ai_suggestions:
                    st.session_state.last_suggestion_index = all_ai_suggestions.index(st.session_state.current_ai_suggestion)
                else: # Should not happen if random.choice worked from the list
                    st.session_state.last_suggestion_index = -1
            else:
                st.session_state.current_ai_suggestion = "No specific AI insights available at this moment. Analyzing data..."
                st.session_state.last_suggestion_index = -1

        # Display the current insight
        st_markdown_content = f"""
            <div style='background-color: rgba(0,0,0,0.7); padding: 1.5em; border-radius: 15px; margin-bottom: 1em; box-shadow: 0 4px 15px rgba(0,123,255,0.3);'>
                <h3 style='color: #00BFFF; text-align: center; margin-bottom: 0.75em; font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;'>🚀 AI Co-Pilot Insights</h3>
                <div style='color: #E0E0E0; font-size: 1.05em; min-height: 120px; display: flex; align-items: center; justify-content: center; text-align: center; padding: 15px; border: 1px dashed #007bff; border-radius: 8px; background-color: rgba(20,30,40,0.5); font-family: "Consolas", "Courier New", monospace;'>
                    {st.session_state.current_ai_suggestion}
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        if st_module:
            st_module.markdown(st_markdown_content, unsafe_allow_html=True)
        else: # Fallback
            import streamlit as st
            st.markdown(st_markdown_content, unsafe_allow_html=True)

        # Button to get a new suggestion
        if st.button("🔮 Unveil New AI Perspective", key="next_insight_button", help="Click to consult the AI for a fresh strategic viewpoint!", use_container_width=True):
            if all_ai_suggestions and len(all_ai_suggestions) > 1:
                available_indices = list(range(len(all_ai_suggestions)))
                # Try not to repeat the immediately previous suggestion if possible
                if st.session_state.last_suggestion_index in available_indices:
                     available_indices.remove(st.session_state.last_suggestion_index)

                if not available_indices: # Fallback if only one suggestion or after removing last one
                     new_index = st.session_state.last_suggestion_index if st.session_state.last_suggestion_index != -1 else 0
                else:
                    # Ensure random is available
                    if random_module:
                        new_index = random_module.choice(available_indices)
                    else: # Fallback
                        import random as random_module
                        new_index = random_module.choice(available_indices)

                st.session_state.current_ai_suggestion = all_ai_suggestions[new_index]
                st.session_state.last_suggestion_index = new_index
            elif all_ai_suggestions: # Only one suggestion available
                 st.session_state.current_ai_suggestion = all_ai_suggestions[0]
                 st.session_state.last_suggestion_index = 0
            else:
                st.session_state.current_ai_suggestion = "No new insights available at the moment. Data might be insufficient."
                st.session_state.last_suggestion_index = -1
            
            if st_module:
                st_module.rerun()
            else: # Fallback
                import streamlit as st
                st.rerun()

    def _render_charts(self, df, st_module=None, pd_module=None, px_module=None):
        """Renders the various charts for the dashboard."""
        if st_module is None: import streamlit as st_module # Fallback
        if pd_module is None: import pandas as pd_module # Fallback
        if px_module is None: import plotly.express as px_module # Fallback

        if df is None or df.empty:
            st_module.info("No data available to display charts.")
            return

        col1, col2 = st.columns(2)

        # --- Chart 1: Service Counts (Bar Chart) ---
        with col1:
            service_counts = df['Service'].value_counts().reset_index()
            service_counts.columns = ['Service', 'Count']
            fig1 = px_module.bar(service_counts, x='Service', y='Count', color='Service', title="Service Popularity")
            fig1.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st_module.plotly_chart(fig1, use_container_width=True)

        # --- Chart 2: Visits Heatmap (DataFrame Styled) ---
        with col2:
            heatmap_data = df.groupby(['Day', 'Hour']).size().reset_index(name='Visits')
            days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            heatmap_data['Day'] = pd_module.Categorical(heatmap_data['Day'], categories=days_order, ordered=True)
            pivot = heatmap_data.pivot(index='Hour', columns='Day', values='Visits').fillna(0).astype(int)
            st_module.subheader("Hourly Visits Heatmap")
            st_module.dataframe(pivot.style.format("{:.0f}").background_gradient(cmap='BuGn'), height=400)

        col3, col4 = st.columns(2)

        # --- Chart 3: Revenue Breakdown (Pie Chart) ---
        with col3:
            pie_data = pd_module.DataFrame({
                'Type': ['Membership Revenue', 'Add-on Sales', 'Supplements'],
                'Total (€)': [df['Revenue'].sum(), df['Add-on Sales (€)'].sum(), df['Supplements (€)'].sum()]
            })
            fig2 = px_module.pie(pie_data, names='Type', values='Total (€)', hole=0.4, title="Revenue Sources")
            fig2.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st_module.plotly_chart(fig2, use_container_width=True)

        # --- Chart 4: Average Profit Per Service Session (Actionable Insight) ---
        with col4:
            profit_by_service = df.groupby('Service')['Profit (€)'].mean().reset_index()
            profit_by_service = profit_by_service.sort_values(by='Profit (€)', ascending=False)

            fig3 = px_module.bar(profit_by_service,
                          x='Service',
                          y='Profit (€)',
                          color='Service',
                          title="Average Profit Per Service Session",
                          labels={'Profit (€)': 'Average Profit per Session (€)'})
            fig3.update_traces(texttemplate='%{y:.2f}€', textposition='outside')
            fig3.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', bargap=0.2)
            st_module.plotly_chart(fig3, use_container_width=True)