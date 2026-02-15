"""
Generate Synthetic IFRS 9 Loan Portfolio Data
This creates a realistic loan portfolio dataset for credit risk analytics
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

def generate_loan_portfolio(n_loans=5000):
    """Generate synthetic loan portfolio data"""
    
    # Reporting date
    reporting_date = datetime(2024, 12, 31)
    
    # Loan IDs
    loan_ids = [f"LN{str(i).zfill(7)}" for i in range(1, n_loans + 1)]
    
    # Product types
    product_types = ['Mortgage', 'Personal Loan', 'Auto Loan', 'Credit Card', 'SME Loan']
    products = np.random.choice(product_types, n_loans, p=[0.35, 0.25, 0.20, 0.15, 0.05])
    
    # Origination dates (between 1-5 years ago)
    days_ago = np.random.randint(365, 1825, n_loans)
    origination_dates = [reporting_date - timedelta(days=int(d)) for d in days_ago]
    
    # Original loan amounts
    original_amounts = []
    for product in products:
        if product == 'Mortgage':
            amount = np.random.lognormal(12.5, 0.5)  # ~200k-400k
        elif product == 'Personal Loan':
            amount = np.random.lognormal(9.5, 0.6)   # ~10k-30k
        elif product == 'Auto Loan':
            amount = np.random.lognormal(10.3, 0.4)  # ~20k-40k
        elif product == 'Credit Card':
            amount = np.random.lognormal(8.5, 0.5)   # ~3k-10k
        else:  # SME Loan
            amount = np.random.lognormal(11.5, 0.7)  # ~50k-200k
        original_amounts.append(amount)
    
    # Current outstanding balance (EAD)
    outstanding_balances = []
    for i, orig_date in enumerate(origination_dates):
        months_elapsed = (reporting_date - orig_date).days / 30
        # Amortization factor
        amort_factor = max(0.3, 1 - (months_elapsed / 60))  # Linear amortization over 5 years
        outstanding_balances.append(original_amounts[i] * amort_factor * np.random.uniform(0.85, 1.0))
    
    # Credit scores at origination
    credit_scores_orig = np.random.normal(680, 80, n_loans).clip(300, 850)
    
    # Current credit scores (may have deteriorated)
    credit_scores_current = []
    for score in credit_scores_orig:
        change = np.random.normal(0, 30)  # Some volatility
        credit_scores_current.append(max(300, min(850, score + change)))
    
    # Days past due (DPD)
    # Most loans current, some 30-90 DPD, few >90 DPD
    dpd_distribution = np.random.choice(
        [0, 30, 60, 90, 120, 180],
        n_loans,
        p=[0.85, 0.08, 0.03, 0.02, 0.01, 0.01]
    )
    
    # Interest rates
    interest_rates = []
    for product, score in zip(products, credit_scores_orig):
        if product == 'Mortgage':
            base_rate = 4.5
        elif product == 'Personal Loan':
            base_rate = 9.0
        elif product == 'Auto Loan':
            base_rate = 6.5
        elif product == 'Credit Card':
            base_rate = 18.0
        else:  # SME Loan
            base_rate = 7.5
        
        # Risk adjustment based on credit score
        risk_premium = (750 - score) / 100 * 0.5
        interest_rates.append(max(2.0, base_rate + risk_premium + np.random.uniform(-0.5, 0.5)))
    
    # Industry sector (for SME loans)
    sectors = ['Retail', 'Manufacturing', 'Services', 'Construction', 'Technology', 'Healthcare', 'N/A']
    industry_sectors = []
    for product in products:
        if product == 'SME Loan':
            industry_sectors.append(np.random.choice(sectors[:-1]))
        else:
            industry_sectors.append('N/A')
    
    # Geography
    regions = ['North', 'South', 'East', 'West', 'Central']
    geographies = np.random.choice(regions, n_loans, p=[0.25, 0.20, 0.20, 0.20, 0.15])
    
    # Create DataFrame
    df = pd.DataFrame({
        'loan_id': loan_ids,
        'reporting_date': reporting_date,
        'product_type': products,
        'origination_date': origination_dates,
        'original_amount': original_amounts,
        'outstanding_balance': outstanding_balances,
        'credit_score_origination': credit_scores_orig,
        'credit_score_current': credit_scores_current,
        'days_past_due': dpd_distribution,
        'interest_rate': interest_rates,
        'industry_sector': industry_sectors,
        'geography': geographies
    })
    
    # Round numeric columns
    df['original_amount'] = df['original_amount'].round(2)
    df['outstanding_balance'] = df['outstanding_balance'].round(2)
    df['credit_score_origination'] = df['credit_score_origination'].round(0).astype(int)
    df['credit_score_current'] = df['credit_score_current'].round(0).astype(int)
    df['interest_rate'] = df['interest_rate'].round(2)
    
    return df


def calculate_pd_lgd(df):
    """Calculate PD (Probability of Default) and LGD (Loss Given Default)"""
    
    # 12-month PD based on credit score and DPD
    def calculate_12m_pd(row):
        # Base PD from credit score
        if row['credit_score_current'] >= 750:
            base_pd = 0.005  # 0.5%
        elif row['credit_score_current'] >= 700:
            base_pd = 0.01   # 1%
        elif row['credit_score_current'] >= 650:
            base_pd = 0.025  # 2.5%
        elif row['credit_score_current'] >= 600:
            base_pd = 0.05   # 5%
        else:
            base_pd = 0.10   # 10%
        
        # Adjust for DPD
        if row['days_past_due'] == 0:
            dpd_multiplier = 1.0
        elif row['days_past_due'] <= 30:
            dpd_multiplier = 2.0
        elif row['days_past_due'] <= 90:
            dpd_multiplier = 4.0
        else:
            dpd_multiplier = 8.0
        
        # Product risk adjustment
        product_adj = {
            'Mortgage': 0.7,
            'Auto Loan': 0.9,
            'Personal Loan': 1.2,
            'Credit Card': 1.5,
            'SME Loan': 1.3
        }
        
        pd = base_pd * dpd_multiplier * product_adj.get(row['product_type'], 1.0)
        return min(pd, 1.0)  # Cap at 100%
    
    # Lifetime PD (simplified - usually would use term structure)
    def calculate_lifetime_pd(row):
        # Approximate as 12m PD * survival probability over remaining life
        # Simplified model
        return min(row['pd_12m'] * 3.0, 1.0)  # Rough approximation
    
    # LGD based on product type and collateral
    def calculate_lgd(row):
        lgd_by_product = {
            'Mortgage': np.random.uniform(0.15, 0.30),      # Low LGD due to collateral
            'Auto Loan': np.random.uniform(0.25, 0.40),     # Moderate LGD
            'Personal Loan': np.random.uniform(0.50, 0.70), # High LGD, unsecured
            'Credit Card': np.random.uniform(0.60, 0.80),   # Very high LGD
            'SME Loan': np.random.uniform(0.40, 0.60)       # Moderate-high LGD
        }
        return lgd_by_product.get(row['product_type'], 0.50)
    
    df['pd_12m'] = df.apply(calculate_12m_pd, axis=1)
    df['pd_lifetime'] = df.apply(calculate_lifetime_pd, axis=1)
    df['lgd'] = df.apply(calculate_lgd, axis=1)
    
    # Round
    df['pd_12m'] = df['pd_12m'].round(6)
    df['pd_lifetime'] = df['pd_lifetime'].round(6)
    df['lgd'] = df['lgd'].round(4)
    
    return df


def assign_ifrs9_stage(df):
    """Assign IFRS 9 staging (Stage 1, 2, or 3)"""
    
    def determine_stage(row):
        # Stage 3: Default (>90 DPD)
        if row['days_past_due'] > 90:
            return 3
        
        # Stage 2: Significant Increase in Credit Risk (SICR)
        # Criteria: 30+ DPD OR significant PD increase OR credit score drop >100 points
        credit_score_drop = row['credit_score_origination'] - row['credit_score_current']
        pd_increase = row['pd_12m'] > 0.03  # Simplified threshold
        
        if (row['days_past_due'] >= 30 or 
            credit_score_drop > 100 or 
            pd_increase):
            return 2
        
        # Stage 1: Performing
        return 1
    
    df['ifrs9_stage'] = df.apply(determine_stage, axis=1)
    return df


def calculate_ecl(df):
    """Calculate Expected Credit Loss"""
    
    def calc_ecl(row):
        ead = row['outstanding_balance']  # Exposure at Default
        
        if row['ifrs9_stage'] == 1:
            # Stage 1: 12-month ECL
            ecl = ead * row['pd_12m'] * row['lgd']
        else:
            # Stage 2 & 3: Lifetime ECL
            ecl = ead * row['pd_lifetime'] * row['lgd']
        
        return ecl
    
    df['ecl_amount'] = df.apply(calc_ecl, axis=1).round(2)
    df['ecl_rate'] = (df['ecl_amount'] / df['outstanding_balance'] * 100).round(4)
    
    return df


if __name__ == "__main__":
    print("Generating synthetic IFRS 9 loan portfolio data...")
    
    # Generate portfolio
    portfolio_df = generate_loan_portfolio(n_loans=5000)
    
    # Calculate risk parameters
    portfolio_df = calculate_pd_lgd(portfolio_df)
    
    # Assign IFRS 9 stages
    portfolio_df = assign_ifrs9_stage(portfolio_df)
    
    # Calculate ECL
    portfolio_df = calculate_ecl(portfolio_df)
    
    # Save to CSV
    output_file = 'loan_portfolio_data.csv'
    portfolio_df.to_csv(output_file, index=False)
    
    print(f"\nDataset generated successfully: {output_file}")
    print(f"Total loans: {len(portfolio_df)}")
    print("\nStaging distribution:")
    print(portfolio_df['ifrs9_stage'].value_counts().sort_index())
    print("\nProduct distribution:")
    print(portfolio_df['product_type'].value_counts())
    print(f"\nTotal ECL: ${portfolio_df['ecl_amount'].sum():,.2f}")
    print(f"\nSample records:")
    print(portfolio_df.head(10).to_string())
