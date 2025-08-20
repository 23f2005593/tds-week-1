import marimo

__generated_with = "0.8.0"
app = marimo.App(width="medium")


@app.cell
def __():
    # Author: 23f2005593@ds.study.iitm.ac.in
    # Interactive Data Analysis with Marimo
    # This notebook demonstrates reactive programming with variable dependencies
    
    import marimo as mo
    import numpy as np
    import pandas as pd
    import plotly.express as px
    import plotly.graph_objects as go
    from datetime import datetime, timedelta
    
    mo.md("""
    # Interactive Data Analysis with Marimo
    
    **Author:** 22f1000662@ds.study.iitm.ac.in  
    **Date:** August 16, 2025
    
    This notebook demonstrates Marimo's reactive programming capabilities with:
    - Variable dependencies between cells
    - Interactive widgets
    - Dynamic markdown output
    - Real-time data visualization
    """)
    return datetime, go, mo, np, pd, px, timedelta


@app.cell
def __(np, pd):
    # Cell 1: Data Generation (Base Data)
    # This cell generates synthetic sales data that other cells depend on
    # Data Flow: This cell → sample_size slider → filtered_data → visualizations
    
    np.random.seed(42)  # For reproducible results
    
    # Generate synthetic sales data for analysis
    dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='D')
    base_sales = np.random.normal(1000, 200, len(dates))  # Base daily sales
    seasonal_factor = 1 + 0.3 * np.sin(2 * np.pi * np.arange(len(dates)) / 365)  # Annual seasonality
    trend = np.linspace(0, 500, len(dates))  # Growth trend
    noise = np.random.normal(0, 50, len(dates))  # Random noise
    
    # Combine all factors
    daily_sales = base_sales * seasonal_factor + trend + noise
    daily_sales = np.maximum(daily_sales, 0)  # Ensure non-negative sales
    
    # Create DataFrame
    raw_data = pd.DataFrame({
        'date': dates,
        'daily_sales': daily_sales,
        'month': dates.month,
        'day_of_week': dates.day_name(),
        'quarter': dates.quarter
    })
    
    print(f"Generated dataset with {len(raw_data)} records")
    print(f"Sales range: ${raw_data['daily_sales'].min():.2f} - ${raw_data['daily_sales'].max():.2f}")
    
    raw_data
    return base_sales, daily_sales, dates, noise, raw_data, seasonal_factor, trend


@app.cell
def __(mo):
    # Cell 2: Interactive Controls
    # These widgets control the analysis parameters
    # Data Flow: User input → widgets → dependent cells (filtered_data, analysis_results)
    
    # Sample size slider - controls how much data to analyze
    sample_size_slider = mo.ui.slider(
        start=50, 
        stop=365, 
        step=10, 
        value=200, 
        label="Sample Size (days)"
    )
    
    # Analysis type selector
    analysis_type = mo.ui.dropdown(
        options=['trend', 'seasonal', 'quarterly'], 
        value='trend',
        label="Analysis Type"
    )
    
    # Threshold slider for highlighting significant values
    threshold_slider = mo.ui.slider(
        start=500,
        stop=2000,
        step=50,
        value=1200,
        label="Sales Threshold ($)"
    )
    
    mo.md(f"""
    ## Interactive Controls
    
    Use these controls to modify the analysis:
    
    {sample_size_slider}
    
    {analysis_type}
    
    {threshold_slider}
    """)
    return analysis_type, sample_size_slider, threshold_slider


@app.cell
def __(raw_data, sample_size_slider):
    # Cell 3: Data Processing (Depends on raw_data and sample_size_slider)
    # This cell filters the data based on the sample size slider
    # Data Flow: raw_data + sample_size_slider → filtered_data → visualizations
    
    # Get the slider value
    sample_size = sample_size_slider.value
    
    # Filter data based on sample size
    filtered_data = raw_data.head(sample_size).copy()
    
    # Add derived columns for analysis
    filtered_data['rolling_avg_7'] = filtered_data['daily_sales'].rolling(window=7, center=True).mean()
    filtered_data['rolling_avg_30'] = filtered_data['daily_sales'].rolling(window=30, center=True).mean()
    filtered_data['sales_category'] = filtered_data['daily_sales'].apply(
        lambda x: 'High' if x > 1200 else 'Medium' if x > 800 else 'Low'
    )
    
    print(f"Filtered data contains {len(filtered_data)} records")
    print(f"Average daily sales: ${filtered_data['daily_sales'].mean():.2f}")
    
    filtered_data
    return filtered_data, sample_size


@app.cell
def __(analysis_type, filtered_data, mo, threshold_slider):
    # Cell 4: Dynamic Analysis Results (Depends on filtered_data, analysis_type, threshold_slider)
    # This cell performs different analyses based on the selected type
    # Data Flow: filtered_data + analysis_type + threshold_slider → analysis_results → dynamic_output
    
    analysis_choice = analysis_type.value
    threshold_value = threshold_slider.value
    
    if analysis_choice == 'trend':
        # Trend analysis
        correlation = filtered_data['daily_sales'].corr(filtered_data.index)
        trend_direction = "increasing" if correlation > 0 else "decreasing"
        analysis_results = {
            'type': 'Trend Analysis',
            'correlation': correlation,
            'direction': trend_direction,
            'avg_sales': filtered_data['daily_sales'].mean(),
            'above_threshold': len(filtered_data[filtered_data['daily_sales'] > threshold_value])
        }
        
    elif analysis_choice == 'seasonal':
        # Seasonal analysis
        monthly_avg = filtered_data.groupby('month')['daily_sales'].mean()
        best_month = monthly_avg.idxmax()
        worst_month = monthly_avg.idxmin()
        analysis_results = {
            'type': 'Seasonal Analysis',
            'best_month': best_month,
            'worst_month': worst_month,
            'seasonal_variation': monthly_avg.std(),
            'above_threshold': len(filtered_data[filtered_data['daily_sales'] > threshold_value])
        }
        
    else:  # quarterly
        # Quarterly analysis
        quarterly_avg = filtered_data.groupby('quarter')['daily_sales'].mean()
        best_quarter = quarterly_avg.idxmax()
        analysis_results = {
            'type': 'Quarterly Analysis',
            'best_quarter': f"Q{best_quarter}",
            'quarterly_growth': quarterly_avg.pct_change().mean() * 100,
            'total_quarters': len(quarterly_avg),
            'above_threshold': len(filtered_data[filtered_data['daily_sales'] > threshold_value])
        }
    
    analysis_results
    return (
        analysis_choice,
        analysis_results,
        best_month,
        best_quarter,
        correlation,
        monthly_avg,
        quarterly_avg,
        threshold_value,
        trend_direction,
        worst_month,
    )


@app.cell
def __(analysis_results, mo, sample_size, threshold_value):
    # Cell 5: Dynamic Markdown Output (Depends on analysis_results, sample_size, threshold_value)
    # This cell creates dynamic markdown based on the analysis results and widget states
    # Data Flow: analysis_results + widget values → dynamic_output (final presentation)
    
    results = analysis_results
    
    # Create dynamic content based on analysis type
    if results['type'] == 'Trend Analysis':
        dynamic_content = f"""
        ## 📈 {results['type']} Results
        
        **Sample Size:** {sample_size} days  
        **Threshold:** ${threshold_value}
        
        ### Key Findings:
        - **Trend Direction:** Sales are {results['direction']} over time
        - **Correlation Coefficient:** {results['correlation']:.4f}
        - **Average Daily Sales:** ${results['avg_sales']:.2f}
        - **Days Above Threshold:** {results['above_threshold']} days
        
        {"📈 **Positive trend detected!**" if results['correlation'] > 0 else "📉 **Negative trend detected**"}
        """
        
    elif results['type'] == 'Seasonal Analysis':
        dynamic_content = f"""
        ## 🌟 {results['type']} Results
        
        **Sample Size:** {sample_size} days  
        **Threshold:** ${threshold_value}
        
        ### Key Findings:
        - **Best Performing Month:** Month {results['best_month']}
        - **Worst Performing Month:** Month {results['worst_month']}
        - **Seasonal Variation (Std Dev):** ${results['seasonal_variation']:.2f}
        - **Days Above Threshold:** {results['above_threshold']} days
        
        🎯 **Seasonal patterns identified in the data!**
        """
        
    else:  # Quarterly Analysis
        dynamic_content = f"""
        ## 📊 {results['type']} Results
        
        **Sample Size:** {sample_size} days  
        **Threshold:** ${threshold_value}
        
        ### Key Findings:
        - **Best Quarter:** {results['best_quarter']}
        - **Average Quarterly Growth:** {results['quarterly_growth']:.2f}%
        - **Quarters Analyzed:** {results['total_quarters']}
        - **Days Above Threshold:** {results['above_threshold']} days
        
        {"🚀 **Positive growth trajectory!**" if results['quarterly_growth'] > 0 else "⚠️ **Declining quarterly performance**"}
        """
    
    mo.md(dynamic_content)
    return dynamic_content, results


@app.cell
def __(filtered_data, go, mo, px, threshold_value):
    # Cell 6: Interactive Visualization (Depends on filtered_data and threshold_value)
    # This cell creates visualizations that update based on the filtered data and threshold
    # Data Flow: filtered_data + threshold_value → interactive_chart (visual output)
    
    # Create interactive plot with threshold line
    fig = px.line(
        filtered_data, 
        x='date', 
        y='daily_sales',
        title='Daily Sales Over Time with Interactive Threshold',
        labels={'daily_sales': 'Daily Sales ($)', 'date': 'Date'},
        line_shape='linear'
    )
    
    # Add rolling averages
    if 'rolling_avg_7' in filtered_data.columns:
        fig.add_scatter(
            x=filtered_data['date'], 
            y=filtered_data['rolling_avg_7'],
            mode='lines',
            name='7-day Average',
            line=dict(dash='dash', color='orange')
        )
    
    if 'rolling_avg_30' in filtered_data.columns:
        fig.add_scatter(
            x=filtered_data['date'], 
            y=filtered_data['rolling_avg_30'],
            mode='lines',
            name='30-day Average',
            line=dict(dash='dot', color='red')
        )
    
    # Add threshold line
    fig.add_hline(
        y=threshold_value, 
        line_dash="dash", 
        line_color="green",
        annotation_text=f"Threshold: ${threshold_value}"
    )
    
    # Highlight points above threshold
    above_threshold_data = filtered_data[filtered_data['daily_sales'] > threshold_value]
    if len(above_threshold_data) > 0:
        fig.add_scatter(
            x=above_threshold_data['date'],
            y=above_threshold_data['daily_sales'],
            mode='markers',
            marker=dict(color='red', size=8, symbol='circle-open'),
            name=f'Above ${threshold_value}',
            showlegend=True
        )
    
    # Update layout
    fig.update_layout(
        height=500,
        hovermode='x unified',
        showlegend=True,
        xaxis_title="Date",
        yaxis_title="Daily Sales ($)"
    )
    
    mo.ui.plotly(fig)
    return above_threshold_data, fig


@app.cell
def __(filtered_data, mo, px):
    # Cell 7: Summary Statistics Table (Depends on filtered_data)
    # This cell provides a summary table that updates with the filtered data
    # Data Flow: filtered_data → summary_stats (tabular output)
    
    # Calculate summary statistics
    summary_stats = filtered_data['daily_sales'].describe()
    
    # Create a more detailed summary
    summary_data = {
        'Statistic': ['Count', 'Mean', 'Std Dev', 'Min', '25%', '50%', '75%', 'Max'],
        'Value': [
            f"{summary_stats['count']:.0f} days",
            f"${summary_stats['mean']:.2f}",
            f"${summary_stats['std']:.2f}",
            f"${summary_stats['min']:.2f}",
            f"${summary_stats['25%']:.2f}",
            f"${summary_stats['50%']:.2f}",
            f"${summary_stats['75%']:.2f}",
            f"${summary_stats['max']:.2f}"
        ]
    }
    
    # Distribution by sales category
    category_counts = filtered_data['sales_category'].value_counts()
    
    mo.md(f"""
    ### 📊 Summary Statistics
    
    | Statistic | Value |
    |-----------|-------|
    | Count | {summary_stats['count']:.0f} days |
    | Mean | ${summary_stats['mean']:.2f} |
    | Std Dev | ${summary_stats['std']:.2f} |
    | Min | ${summary_stats['min']:.2f} |
    | 25% | ${summary_stats['25%']:.2f} |
    | 50% | ${summary_stats['50%']:.2f} |
    | 75% | ${summary_stats['75%']:.2f} |
    | Max | ${summary_stats['max']:.2f} |
    
    ### 🎯 Sales Categories
    
    | Category | Count | Percentage |
    |----------|-------|------------|
    | High (>$1200) | {category_counts.get('High', 0)} | {category_counts.get('High', 0)/len(filtered_data)*100:.1f}% |
    | Medium ($800-$1200) | {category_counts.get('Medium', 0)} | {category_counts.get('Medium', 0)/len(filtered_data)*100:.1f}% |
    | Low (<$800) | {category_counts.get('Low', 0)} | {category_counts.get('Low', 0)/len(filtered_data)*100:.1f}% |
    """)
    return category_counts, summary_data, summary_stats


@app.cell
def __(mo):
    # Cell 8: Footer with Documentation
    # This cell provides information about the notebook structure and dependencies
    
    mo.md("""
    ---
    
    ## 📋 Notebook Structure & Dependencies
    
    This Marimo notebook demonstrates reactive programming with the following cell dependencies:
    
    1. **Cell 1** (Data Generation) → **Cell 3** (Data Processing)
    2. **Cell 2** (Interactive Controls) → **Cell 3, 4, 5, 6** (Processing & Visualization)
    3. **Cell 3** (Filtered Data) → **Cell 4, 5, 6, 7** (Analysis & Output)
    4. **Cell 4** (Analysis Results) → **Cell 5** (Dynamic Output)
    
    ### 🔄 Reactive Features:
    - **Sample Size Slider**: Updates filtered dataset and all dependent visualizations
    - **Analysis Type**: Changes the type of analysis performed and output format
    - **Threshold Slider**: Updates visualizations and highlights data points
    - **Dynamic Markdown**: Content changes based on analysis results and widget states
    
    ### 📈 Data Flow:
    ```
    Raw Data → User Controls → Filtered Data → Analysis → Visualizations & Reports
    ```
    
    **Author**: 23f2005593@ds.study.iitm.ac.in 
    **Created with**: Marimo v0.8.0  
    **Date**: August 16, 2025
    """)
    return


if __name__ == "__main__":
    app.run()
