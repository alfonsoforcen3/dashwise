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
                f"📈 **Peak Performance Day**: Our analysis indicates **{metrics['top_day']}** consistently drives your **maximum revenue**. "
                f"Strategic amplification of marketing initiatives or exclusive promotions leading into **{metrics['top_day']}** could unlock further growth."
            )
        # Suggestion 2: Top Service Revenue
        if metrics.get('top_service_revenue') != 'N/A':
            suggestions.append(
                f"🚀 **Core Revenue Engine**: Data intelligence highlights **{metrics['top_service_revenue']}** as a primary driver of your income. "
                f"Elevating this service's visibility and refining the customer journey here promises substantial ROI."
            )
        # Suggestion 3: Most Profitable Service
        if metrics.get('most_profitable_service') != 'N/A':
            suggestions.append(
                f"💰 **Prime Profit Asset**: Profitability analysis reveals **{metrics['most_profitable_service']}** as your top earner, averaging "
                f"a remarkable **€{metrics['avg_profit_most_profitable']:.2f} profit per session**. Devise targeted campaigns to channel more clientele towards this high-margin offering."
            )
        # Suggestion 4: Least Profitable Service
        if metrics.get('least_profitable_service') != 'N/A':
            if metrics['avg_profit_least_profitable'] < 0:
                profit_text = f"an average **deficit of €{abs(metrics['avg_profit_least_profitable']):.2f}**"
            else:
                profit_text = f"a modest average **profit of €{metrics['avg_profit_least_profitable']:.2f}**"
            suggestions.append(
                f"📉 **Profitability Review Needed**: Our system flags **{metrics['least_profitable_service']}** with {profit_text} per session. "
                f"A deep dive into its cost architecture, pricing strategy, or its role as a potential gateway service for other offerings is recommended."
            )
        # Suggestion 5: Premium Members
        if metrics.get('premium_members', 0) > 0:
            suggestions.append(
                f"👑 **Elite Member Focus**: Your cohort of **{metrics['premium_members']} premium members** represents significant value. "
                f"Cultivating this segment with bespoke benefits and personalized engagement can amplify loyalty and lifetime customer value. Consider exploring tiered premium structures."
            )
        # Suggestion 6: Peak Hour Focus
        if metrics.get('peak_hour_overall') is not None:
            peak_hour = metrics['peak_hour_overall']
            suggestions.append(
                f"⏱️ **Golden Hour Optimization**: Temporal analysis pinpoints **{peak_hour:02d}:00 - {peak_hour+1:02d}:00** as a consistent **high-density traffic window**. "
                f"Optimizing resource deployment and ensuring peak operational readiness during this 'golden hour' is crucial for service excellence and revenue capture."
            )
        # Suggestion 7: Weekend Strategy
        saturday_revenue = metrics.get('saturday_revenue', 0)
        sunday_revenue = metrics.get('sunday_revenue', 0)
        if saturday_revenue > 0 or sunday_revenue > 0:
            busier_weekend_day = "**Saturday**" if saturday_revenue >= sunday_revenue else "**Sunday**"
            quieter_weekend_day = "**Sunday**" if saturday_revenue >= sunday_revenue else "**Saturday**"
            suggestions.append(
                f"🗓️ **Weekend Dynamics**: {busier_weekend_day} currently exhibits **stronger revenue performance**. "
                f"Consider A/B testing unique value propositions for {quieter_weekend_day} or further leveraging {busier_weekend_day}'s established momentum with enhanced experiences."
            )
        # Suggestion 8: Add-on Sales Opportunity
        if metrics.get('service_low_addons') != 'N/A':
             suggestions.append(
                f"🛒 **Boost Add-on Sales**: Clients engaging with **{metrics['service_low_addons']}** "
                f"currently average only **€{metrics['lowest_addon_avg']:.2f} in add-on sales** per interaction. "
                f"Implementing intelligent bundling, incentivizing staff for upselling, or enhancing product visibility at point-of-service could significantly boost this metric."
            )

        # New Suggestion 9: Client Retention based on Service
        if not df.empty and 'Client ID' in df.columns and 'Service' in df.columns:
            service_client_counts = df.groupby('Service')['Client ID'].nunique()
            if not service_client_counts.empty:
                most_engaging_service = service_client_counts.idxmax()
                max_unique_clients = service_client_counts.max()
                suggestions.append(
                    f"🤝 **Client Engagement Champion**: The service **{most_engaging_service}** attracts the **highest number of unique clients ({max_unique_clients})**. "
                    f"Analyze what makes this service so appealing and replicate its success factors across other offerings to improve overall client retention."
                )

        # New Suggestion 10: Underutilized High-Profit Service
        if metrics.get('most_profitable_service') != 'N/A' and not df.empty:
            most_profitable_service_visits = df[df['Service'] == metrics['most_profitable_service']].shape[0]
            total_visits = df.shape[0]
            if total_visits > 0 and (most_profitable_service_visits / total_visits) < 0.1: # If less than 10% of total visits
                suggestions.append(
                    f"💎 **Hidden Gem Alert**: While **{metrics['most_profitable_service']}** is your most profitable service (avg. **€{metrics['avg_profit_most_profitable']:.2f} profit/session**), "
                    f"it currently accounts for a **small fraction of total visits**. Consider targeted promotions or bundling to increase its uptake and significantly boost overall profitability."
                )

        # New Suggestion 11: Membership Tier Analysis
        if not df.empty and 'Membership Type' in df.columns and 'Revenue' in df.columns:
            membership_revenue = df.groupby('Membership Type')['Revenue'].sum()
            if 'Premium' in membership_revenue.index and 'Standard' in membership_revenue.index:
                if membership_revenue['Premium'] > membership_revenue['Standard']:
                    suggestions.append(
                        f"🌟 **Premium Powerhouse**: Your **Premium members** are generating more total revenue than Standard members. "
                        f"Focus on strategies to **upsell Standard members to Premium** and enhance the value proposition for your top-tier clients."
                    )
                else:
                    payg_revenue = membership_revenue.get('Pay-as-you-go', 0)
                    if payg_revenue > 0 and payg_revenue > 0.2 * (membership_revenue.get('Standard', 0) + membership_revenue.get('Premium', 0)):
                         suggestions.append(
                            f"🔄 **Convert Pay-As-You-Go**: A significant portion of revenue comes from **Pay-as-you-go clients**. "
                            f"Implement strategies to convert these users to **Standard or Premium memberships** for more predictable recurring revenue and increased loyalty."
                        )

        # Fallback if no specific suggestions were generated (e.g., minimal data)
        if not suggestions:
             return ["Analyzing data... More insights will appear as data volume increases."]

        return suggestions