import random

class AISuggestionEngine:
    """
    Generates AI-like strategic suggestions based on calculated metrics.
    """
    def generate_suggestions(self, df, metrics):
        """
        Generates a list of strategic suggestions based on the provided metrics.
        Args:
            df: The processed Pandas DataFrame (used for checks like df.empty).
            metrics: A dictionary containing key performance indicators.
        Returns:
            A list of suggestion strings.
        """
        suggestions = []

        # Ensure metrics are available before generating suggestions
        if not metrics or df is None or df.empty:
             return ["No specific AI insights available at this moment. Data might be insufficient or processing failed."]

        # Suggestion 1: Peak Day
        if metrics.get('top_day') != 'N/A':
            suggestions.append(
                f"📈 Our advanced algorithms indicate that **{metrics['top_day']}** is a peak performance day, consistently driving maximum revenue. "
                f"Strategic amplification of marketing initiatives or exclusive promotions leading into **{metrics['top_day']}** could unlock further growth."
            )
        # Suggestion 2: Top Service Revenue
        if metrics.get('top_service_revenue') != 'N/A':
            suggestions.append(
                f"🚀 Data intelligence highlights **{metrics['top_service_revenue']}** as a core revenue engine. "
                f"Elevating this service's visibility and refining the customer journey here promises substantial ROI."
            )
        # Suggestion 3: Most Profitable Service
        if metrics.get('most_profitable_service') != 'N/A':
            suggestions.append(
                f"💰 Profitability matrix analysis reveals **{metrics['most_profitable_service']}** as your prime asset, averaging "
                f"a remarkable **€{metrics['avg_profit_most_profitable']:.2f}** profit per session. Devise targeted campaigns to channel more clientele towards this high-margin offering."
            )
        # Suggestion 4: Least Profitable Service
        if metrics.get('least_profitable_service') != 'N/A':
            if metrics['avg_profit_least_profitable'] < 0:
                profit_text = f"an average deficit of **€{abs(metrics['avg_profit_least_profitable']):.2f}**"
            else:
                profit_text = f"a modest average profit of **€{metrics['avg_profit_least_profitable']:.2f}**"
            suggestions.append(
                f"📉 Our system flags **{metrics['least_profitable_service']}** with {profit_text} per session. "
                f"A deep dive into its cost architecture, pricing strategy, or its role as a potential gateway service for other offerings is recommended."
            )
        # Suggestion 5: Premium Members
        if metrics.get('premium_members', 0) > 0:
            suggestions.append(
                f"👑 Your elite cohort of **{metrics['premium_members']}** premium members represents significant value. "
                f"Cultivating this segment with bespoke benefits and personalized engagement can amplify loyalty and lifetime customer value. Consider exploring tiered premium structures."
            )
        # Suggestion 6: Peak Hour Focus
        if metrics.get('peak_hour_overall') is not None:
            peak_hour = metrics['peak_hour_overall']
            suggestions.append(
                f"⏱️ Predictive temporal analysis pinpoints **{peak_hour:02d}:00 - {peak_hour+1:02d}:00** as a consistent high-density traffic window. "
                f"Optimizing resource deployment and ensuring peak operational readiness during this 'golden hour' is crucial for service excellence and revenue capture."
            )
        # Suggestion 7: Weekend Strategy
        saturday_revenue = metrics.get('saturday_revenue', 0)
        sunday_revenue = metrics.get('sunday_revenue', 0)
        if saturday_revenue > 0 or sunday_revenue > 0:
            busier_weekend_day = "Saturday" if saturday_revenue >= sunday_revenue else "Sunday"
            quieter_weekend_day = "Sunday" if saturday_revenue >= sunday_revenue else "Saturday"
            suggestions.append(
                f"🗓️ Weekend Dynamics Model: **{busier_weekend_day}** currently exhibits stronger revenue performance. "
                f"Consider A/B testing unique value propositions for **{quieter_weekend_day}** or further leveraging **{busier_weekend_day}**'s established momentum with enhanced experiences."
            )
        # Suggestion 8: Add-on Sales Opportunity
        if metrics.get('service_low_addons') != 'N/A':
             suggestions.append(
                f"🛒 Ancillary Revenue Optimization: Clients engaging with **{metrics['service_low_addons']}** "
                f"currently average only €{metrics['lowest_addon_avg']:.2f} in add-on sales per interaction. "
                f"Implementing intelligent bundling, incentivizing staff for upselling, or enhancing product visibility at point-of-service could significantly boost this metric."
            )

        # Fallback if no specific suggestions were generated (e.g., minimal data)
        if not suggestions:
             return ["Analyzing data... More insights will appear as data volume increases."]

        return suggestions