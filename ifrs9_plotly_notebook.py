# IFRS 9 Credit Risk Analysis - Vertex AI Workbench (Plotly Version)
# Advanced Python analytics with interactive Plotly visualizations

"""
This notebook demonstrates:
1. Fetching loan portfolio data from BigQuery
2. Performing risk analytics with Pandas
3. Creating interactive visualizations with Plotly
4. Advanced ECL analysis
5. Portfolio segmentation and insights
"""

# +
# Install Chrome and dependencies for Plotly image export
import sys
import subprocess

print("Installing Chrome and dependencies...")

# Install Chrome
# !wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
# !apt-get update -qq
# !apt-get install -y -qq ./google-chrome-stable_current_amd64.deb > /dev/null 2>&1
# !rm google-chrome-stable_current_amd64.deb

# Install kaleido
# !{sys.executable} -m pip install kaleido --quiet

print("✅ Chrome and Kaleido installed!")
# -

# =============================================================================
# SETUP & IMPORTS
# =============================================================================

# Install required packages
print("Installing packages...")
import sys
# !{sys.executable} -m pip install google-cloud-bigquery pandas plotly kaleido --quiet

import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from google.cloud import bigquery
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

print("✅ Packages imported successfully")

# =============================================================================
# CONFIGURATION
# =============================================================================

# Replace with your actual Project ID
PROJECT_ID = "ifrs9-analytics"
DATASET_ID = "credit_risk_ifrs9"
TABLE_ID = "loan_portfolio"

print(f"\n📊 Project: {PROJECT_ID}")
print(f"📊 Dataset: {DATASET_ID}")
print(f"📊 Table: {TABLE_ID}")

# =============================================================================
# 1. FETCH DATA FROM BIGQUERY
# =============================================================================

print("\n" + "="*60)
print("STEP 1: Fetching Data from BigQuery")
print("="*60)

# Initialize BigQuery client
client = bigquery.Client(project=PROJECT_ID)

# Query to fetch all loan data
query = f"""
SELECT *
FROM `{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}`
"""

print("Executing query...")
df = client.query(query).to_dataframe()

print(f"\n✅ Data loaded successfully!")
print(f"   Rows: {len(df):,}")
print(f"   Columns: {len(df.columns)}")

# Display first few rows
print("\nFirst 5 rows:")
print(df.head())

# =============================================================================
# 2. DATA EXPLORATION & SUMMARY STATISTICS
# =============================================================================

print("\n" + "="*60)
print("STEP 2: Data Exploration")
print("="*60)

# Portfolio summary
print("\n💰 Portfolio Summary:")
print(f"Total Loans: {len(df):,}")
print(f"Total Exposure: ${df['outstanding_balance'].sum():,.2f}")
print(f"Total ECL: ${df['ecl_amount'].sum():,.2f}")
print(f"Average ECL Rate: {df['ecl_rate'].mean():.2f}%")
print(f"Coverage Ratio: {(df['ecl_amount'].sum() / df['outstanding_balance'].sum() * 100):.2f}%")

# Staging distribution
print("\n📋 IFRS 9 Staging Distribution:")
staging_summary = df.groupby('ifrs9_stage').agg({
    'loan_id': 'count',
    'outstanding_balance': 'sum',
    'ecl_amount': 'sum'
}).round(2)
staging_summary.columns = ['Loan Count', 'Total Exposure', 'Total ECL']
staging_summary['Coverage %'] = (staging_summary['Total ECL'] / staging_summary['Total Exposure'] * 100).round(2)
print(staging_summary)

# =============================================================================
# 3. VISUALIZATION 1 - STAGING DISTRIBUTION
# =============================================================================

print("\n" + "="*60)
print("STEP 3: Creating Staging Distribution Charts")
print("="*60)

# Prepare data
stage_counts = df['ifrs9_stage'].value_counts().sort_index()
stage_labels = [f'Stage {s}' for s in stage_counts.index]
colors = ['#2ecc71', '#f39c12', '#e74c3c']

# Create subplots
fig = make_subplots(
    rows=1, cols=2,
    subplot_titles=('Loan Distribution by IFRS 9 Stage', 'ECL Amount by Stage'),
    specs=[[{'type': 'pie'}, {'type': 'bar'}]]
)

# Pie chart - Loan count by stage
fig.add_trace(
    go.Pie(
        labels=stage_labels,
        values=stage_counts.values,
        marker=dict(colors=colors),
        textinfo='label+percent',
        hovertemplate='%{label}<br>Count: %{value}<br>Percent: %{percent}<extra></extra>'
    ),
    row=1, col=1
)

# Bar chart - ECL by stage
stage_ecl = df.groupby('ifrs9_stage')['ecl_amount'].sum() / 1000000  # Convert to millions
fig.add_trace(
    go.Bar(
        x=stage_labels,
        y=stage_ecl.values,
        marker=dict(color=colors),
        text=[f'${v:.2f}M' for v in stage_ecl.values],
        textposition='outside',
        hovertemplate='%{x}<br>ECL: $%{y:.2f}M<extra></extra>'
    ),
    row=1, col=2
)

fig.update_layout(
    title_text="IFRS 9 Staging Analysis",
    showlegend=False,
    height=500,
    font=dict(size=12)
)

fig.update_yaxes(title_text="ECL Amount ($ Millions)", row=1, col=2)

# Save as image
# fig.write_image('staging_distribution.png', width=1400, height=500)
print("✅ Saved: staging_distribution.png")

# Display in notebook
fig.show()

# =============================================================================
# 4. VISUALIZATION 2 - PRODUCT RISK ANALYSIS
# =============================================================================

print("\n" + "="*60)
print("STEP 4: Product Risk Analysis")
print("="*60)

# Product-level metrics
product_analysis = df.groupby('product_type').agg({
    'loan_id': 'count',
    'outstanding_balance': 'sum',
    'ecl_amount': 'sum',
    'pd_12m': 'mean',
    'lgd': 'mean',
    'credit_score_current': 'mean'
}).round(2)

product_analysis['ECL Rate %'] = (product_analysis['ecl_amount'] / product_analysis['outstanding_balance'] * 100).round(2)
product_analysis = product_analysis.sort_values('ECL Rate %', ascending=False)

print("\n📊 Product Risk Metrics:")
print(product_analysis)

# Create horizontal bar chart
fig = go.Figure()

# Color gradient from red to green
colors_list = ['#e74c3c', '#e67e22', '#f39c12', '#2ecc71', '#27ae60']

fig.add_trace(go.Bar(
    y=product_analysis.index,
    x=product_analysis['ECL Rate %'],
    orientation='h',
    marker=dict(
        color=colors_list,
        line=dict(color='white', width=1)
    ),
    text=[f'{v:.2f}%' for v in product_analysis['ECL Rate %']],
    textposition='outside',
    hovertemplate='%{y}<br>ECL Rate: %{x:.2f}%<extra></extra>'
))

fig.update_layout(
    title='Risk Profile by Product Type',
    xaxis_title='ECL Rate (%)',
    yaxis_title='',
    height=500,
    font=dict(size=12),
    showlegend=False
)

# fig.write_image('product_risk_analysis.png', width=1200, height=500)
print("✅ Saved: product_risk_analysis.png")
fig.show()

# =============================================================================
# 5. VISUALIZATION 3 - CREDIT QUALITY DISTRIBUTION
# =============================================================================

print("\n" + "="*60)
print("STEP 5: Credit Quality Analysis")
print("="*60)

# Create credit score bands
df['credit_band'] = pd.cut(df['credit_score_current'], 
                           bins=[0, 600, 650, 700, 750, 1000],
                           labels=['Very Poor (<600)', 'Poor (600-649)', 
                                  'Fair (650-699)', 'Good (700-749)', 
                                  'Excellent (750+)'])

# Credit quality summary
credit_summary = df.groupby('credit_band', observed=True).agg({
    'loan_id': 'count',
    'outstanding_balance': 'sum',
    'ecl_amount': 'sum',
    'pd_12m': 'mean'
}).round(2)

credit_summary['% of Portfolio'] = (credit_summary['loan_id'] / len(df) * 100).round(1)

print("\n📊 Credit Quality Distribution:")
print(credit_summary)

# Create 2x2 subplot
fig = make_subplots(
    rows=2, cols=2,
    subplot_titles=(
        'Loan Count by Credit Quality',
        'Exposure by Credit Quality ($ Millions)',
        'Average PD by Credit Quality',
        'ECL Concentration by Credit Quality'
    ),
    vertical_spacing=0.15,
    horizontal_spacing=0.12
)

# 1. Loan count
fig.add_trace(
    go.Bar(
        x=credit_summary.index,
        y=credit_summary['loan_id'],
        marker=dict(color='steelblue'),
        showlegend=False,
        hovertemplate='%{x}<br>Loans: %{y}<extra></extra>'
    ),
    row=1, col=1
)

# 2. Exposure
fig.add_trace(
    go.Bar(
        x=credit_summary.index,
        y=credit_summary['outstanding_balance'] / 1000000,
        marker=dict(color='coral'),
        showlegend=False,
        hovertemplate='%{x}<br>Exposure: $%{y:.2f}M<extra></extra>'
    ),
    row=1, col=2
)

# 3. Average PD
fig.add_trace(
    go.Bar(
        x=credit_summary.index,
        y=credit_summary['pd_12m'],
        marker=dict(color='indianred'),
        showlegend=False,
        hovertemplate='%{x}<br>Avg PD: %{y:.4f}<extra></extra>'
    ),
    row=2, col=1
)

# 4. ECL concentration
ecl_pct = (credit_summary['ecl_amount'] / credit_summary['ecl_amount'].sum() * 100)
fig.add_trace(
    go.Bar(
        x=credit_summary.index,
        y=ecl_pct,
        marker=dict(color='darkgreen'),
        showlegend=False,
        hovertemplate='%{x}<br>ECL %: %{y:.1f}%<extra></extra>'
    ),
    row=2, col=2
)

fig.update_layout(
    title_text='Credit Quality Analysis',
    height=800,
    font=dict(size=11)
)

# Update y-axes labels
fig.update_yaxes(title_text="Number of Loans", row=1, col=1)
fig.update_yaxes(title_text="Exposure ($ Millions)", row=1, col=2)
fig.update_yaxes(title_text="Probability of Default", row=2, col=1)
fig.update_yaxes(title_text="% of Total ECL", row=2, col=2)

# Rotate x-axis labels
fig.update_xaxes(tickangle=45)

# fig.write_imagefig.write_image('credit_quality_analysis.png', width=1400, height=800)
print("✅ Saved: credit_quality_analysis.png")
fig.show()

# =============================================================================
# 6. VISUALIZATION 4 - CORRELATION HEATMAP
# =============================================================================

print("\n" + "="*60)
print("STEP 6: Correlation Analysis")
print("="*60)

# Select numerical columns
numerical_cols = ['outstanding_balance', 'credit_score_current', 'days_past_due', 
                 'pd_12m', 'pd_lifetime', 'lgd', 'ecl_amount', 'ecl_rate']

correlation_matrix = df[numerical_cols].corr()

# Create heatmap
fig = go.Figure(data=go.Heatmap(
    z=correlation_matrix.values,
    x=correlation_matrix.columns,
    y=correlation_matrix.columns,
    colorscale='RdBu',
    zmid=0,
    text=correlation_matrix.values.round(2),
    texttemplate='%{text}',
    textfont={"size": 10},
    colorbar=dict(title="Correlation")
))

fig.update_layout(
    title='Correlation Matrix - Risk Metrics',
    height=700,
    width=800,
    font=dict(size=11)
)

# fig.write_image('correlation_heatmap.png', width=800, height=700)
print("✅ Saved: correlation_heatmap.png")
fig.show()

print("\n🔍 Key Correlations:")
corr_pairs = correlation_matrix.unstack()
corr_pairs = corr_pairs[corr_pairs < 1].sort_values(ascending=False)
print("\nStrongest positive correlations:")
print(corr_pairs.head(5))

# =============================================================================
# 7. VISUALIZATION 5 - VINTAGE ANALYSIS
# =============================================================================

print("\n" + "="*60)
print("STEP 7: Vintage Analysis")
print("="*60)

# Convert dates
df['origination_date'] = pd.to_datetime(df['origination_date'])
df['vintage_year'] = df['origination_date'].dt.year

# Vintage summary
vintage_summary = df.groupby('vintage_year').agg({
    'loan_id': 'count',
    'outstanding_balance': 'sum',
    'ecl_amount': 'sum',
    'ifrs9_stage': lambda x: (x == 3).sum()
}).round(2)

vintage_summary['Default Rate %'] = (vintage_summary['ifrs9_stage'] / vintage_summary['loan_id'] * 100).round(2)
vintage_summary['ECL Rate %'] = (vintage_summary['ecl_amount'] / vintage_summary['outstanding_balance'] * 100).round(2)

print("\n📊 Vintage Performance:")
print(vintage_summary)

# Create dual axis chart
fig = make_subplots(
    rows=1, cols=2,
    subplot_titles=('Default Rate by Vintage Year', 'ECL Rate by Vintage Year')
)

fig.add_trace(
    go.Bar(
        x=vintage_summary.index,
        y=vintage_summary['Default Rate %'],
        marker=dict(color='crimson'),
        showlegend=False,
        hovertemplate='Year: %{x}<br>Default Rate: %{y:.2f}%<extra></extra>'
    ),
    row=1, col=1
)

fig.add_trace(
    go.Bar(
        x=vintage_summary.index,
        y=vintage_summary['ECL Rate %'],
        marker=dict(color='darkorange'),
        showlegend=False,
        hovertemplate='Year: %{x}<br>ECL Rate: %{y:.2f}%<extra></extra>'
    ),
    row=1, col=2
)

fig.update_layout(
    title_text='Vintage Analysis',
    height=500,
    font=dict(size=12)
)

fig.update_yaxes(title_text="Default Rate (%)", row=1, col=1)
fig.update_yaxes(title_text="ECL Rate (%)", row=1, col=2)
fig.update_xaxes(title_text="Origination Year")

# fig.write_image('vintage_analysis.png', width=1400, height=500)
print("✅ Saved: vintage_analysis.png")
fig.show()

# =============================================================================
# 8. VISUALIZATION 6 - GEOGRAPHIC ANALYSIS
# =============================================================================

print("\n" + "="*60)
print("STEP 8: Geographic Risk Distribution")
print("="*60)

# Geographic summary
geo_summary = df.groupby('geography').agg({
    'loan_id': 'count',
    'outstanding_balance': 'sum',
    'ecl_amount': 'sum'
}).round(2)

geo_summary['ECL Rate %'] = (geo_summary['ecl_amount'] / geo_summary['outstanding_balance'] * 100).round(2)
geo_summary = geo_summary.sort_values('ECL Rate %', ascending=True)

print("\n📊 Geographic Distribution:")
print(geo_summary)

# Create horizontal bar chart
fig = go.Figure()

fig.add_trace(go.Bar(
    y=geo_summary.index,
    x=geo_summary['ECL Rate %'],
    orientation='h',
    marker=dict(color='teal'),
    text=[f'{v:.2f}%' for v in geo_summary['ECL Rate %']],
    textposition='outside',
    hovertemplate='%{y}<br>ECL Rate: %{x:.2f}%<extra></extra>'
))

fig.update_layout(
    title='Risk by Geographic Region',
    xaxis_title='ECL Rate (%)',
    yaxis_title='',
    height=500,
    font=dict(size=12),
    showlegend=False
)

# fig.write_image('geographic_analysis.png', width=1200, height=500)
print("✅ Saved: geographic_analysis.png")
fig.show()

# =============================================================================
# 9. HIGH-RISK WATCHLIST
# =============================================================================

print("\n" + "="*60)
print("STEP 9: High-Risk Loan Watchlist")
print("="*60)

# Identify high-risk loans
high_risk = df[(df['ifrs9_stage'] == 3) | (df['ecl_rate'] > 10)].copy()
high_risk = high_risk.sort_values('ecl_amount', ascending=False)

print(f"\n⚠️ High-Risk Loans Identified: {len(high_risk)}")
print(f"   Total Exposure: ${high_risk['outstanding_balance'].sum():,.2f}")
print(f"   Total ECL: ${high_risk['ecl_amount'].sum():,.2f}")

print("\n📋 Top 10 High-Risk Loans:")
watchlist = high_risk[['loan_id', 'product_type', 'outstanding_balance', 
                       'ecl_amount', 'ecl_rate', 'ifrs9_stage', 
                       'days_past_due']].head(10)
print(watchlist.to_string(index=False))

# =============================================================================
# 10. EXPORT RESULTS
# =============================================================================

print("\n" + "="*60)
print("STEP 10: Export Results")
print("="*60)

# Export summary statistics
summary_stats = {
    'Total_Loans': len(df),
    'Total_Exposure': df['outstanding_balance'].sum(),
    'Total_ECL': df['ecl_amount'].sum(),
    'Coverage_Ratio': (df['ecl_amount'].sum() / df['outstanding_balance'].sum() * 100),
    'Stage_1_Count': len(df[df['ifrs9_stage'] == 1]),
    'Stage_2_Count': len(df[df['ifrs9_stage'] == 2]),
    'Stage_3_Count': len(df[df['ifrs9_stage'] == 3]),
    'Avg_Credit_Score': df['credit_score_current'].mean(),
    'Analysis_Date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
}

summary_df = pd.DataFrame([summary_stats])
summary_df.to_csv('portfolio_summary.csv', index=False)
print("✅ Saved: portfolio_summary.csv")

# Export high-risk watchlist
high_risk.to_csv('high_risk_watchlist.csv', index=False)
print("✅ Saved: high_risk_watchlist.csv")

# Export product analysis
product_analysis.to_csv('product_risk_analysis.csv')
print("✅ Saved: product_risk_analysis.csv")

print("\n" + "="*60)
print("✅ ANALYSIS COMPLETE!")
print("="*60)
print(f"\nFiles created:")
print("  📊 staging_distribution.png")
print("  📊 product_risk_analysis.png")
print("  📊 credit_quality_analysis.png")
print("  📊 correlation_heatmap.png")
print("  📊 vintage_analysis.png")
print("  📊 geographic_analysis.png")
print("  📄 portfolio_summary.csv")
print("  📄 high_risk_watchlist.csv")
print("  📄 product_risk_analysis.csv")
print("\n🎉 All charts saved as PNG files!")
print("📥 Download them from the file browser on the left")






