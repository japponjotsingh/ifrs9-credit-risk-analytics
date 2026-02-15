-- IFRS 9 Analytics SQL Queries for BigQuery
-- Replace {project_id}.{dataset_id} with your actual values

-- ============================================================================
-- 1. PORTFOLIO OVERVIEW
-- ============================================================================

-- Overall portfolio summary
SELECT 
    reporting_date,
    COUNT(*) as total_loans,
    SUM(outstanding_balance) as total_exposure,
    SUM(ecl_amount) as total_ecl,
    AVG(ecl_rate) as avg_ecl_rate,
    SUM(ecl_amount) / SUM(outstanding_balance) * 100 as coverage_ratio
FROM `{project_id}.{dataset_id}.loan_portfolio`
GROUP BY reporting_date
ORDER BY reporting_date DESC;


-- ============================================================================
-- 2. STAGING ANALYSIS
-- ============================================================================

-- ECL by IFRS 9 Stage
SELECT 
    ifrs9_stage,
    COUNT(*) as loan_count,
    SUM(outstanding_balance) as total_exposure,
    SUM(ecl_amount) as total_ecl,
    AVG(pd_12m) as avg_pd_12m,
    AVG(pd_lifetime) as avg_pd_lifetime,
    AVG(lgd) as avg_lgd,
    SUM(ecl_amount) / SUM(outstanding_balance) * 100 as coverage_ratio
FROM `{project_id}.{dataset_id}.loan_portfolio`
WHERE reporting_date = '2024-12-31'
GROUP BY ifrs9_stage
ORDER BY ifrs9_stage;


-- Stage migration analysis (requires historical data)
SELECT 
    CASE 
        WHEN ifrs9_stage = 1 THEN 'Stage 1 - Performing'
        WHEN ifrs9_stage = 2 THEN 'Stage 2 - SICR'
        WHEN ifrs9_stage = 3 THEN 'Stage 3 - Default'
    END as stage_description,
    COUNT(*) as count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 2) as percentage,
    SUM(outstanding_balance) as exposure,
    SUM(ecl_amount) as ecl
FROM `{project_id}.{dataset_id}.loan_portfolio`
WHERE reporting_date = '2024-12-31'
GROUP BY ifrs9_stage
ORDER BY ifrs9_stage;


-- ============================================================================
-- 3. PRODUCT ANALYSIS
-- ============================================================================

-- ECL by product type
SELECT 
    product_type,
    COUNT(*) as loan_count,
    SUM(outstanding_balance) as total_exposure,
    SUM(ecl_amount) as total_ecl,
    AVG(pd_12m) as avg_pd,
    AVG(lgd) as avg_lgd,
    SUM(ecl_amount) / SUM(outstanding_balance) * 100 as coverage_ratio,
    AVG(credit_score_current) as avg_credit_score,
    AVG(days_past_due) as avg_dpd
FROM `{project_id}.{dataset_id}.loan_portfolio`
WHERE reporting_date = '2024-12-31'
GROUP BY product_type
ORDER BY total_exposure DESC;


-- Product vs Stage matrix
SELECT 
    product_type,
    SUM(CASE WHEN ifrs9_stage = 1 THEN outstanding_balance ELSE 0 END) as stage1_exposure,
    SUM(CASE WHEN ifrs9_stage = 2 THEN outstanding_balance ELSE 0 END) as stage2_exposure,
    SUM(CASE WHEN ifrs9_stage = 3 THEN outstanding_balance ELSE 0 END) as stage3_exposure,
    SUM(outstanding_balance) as total_exposure
FROM `{project_id}.{dataset_id}.loan_portfolio`
WHERE reporting_date = '2024-12-31'
GROUP BY product_type
ORDER BY total_exposure DESC;


-- ============================================================================
-- 4. VINTAGE ANALYSIS
-- ============================================================================

-- ECL by vintage (origination year)
SELECT 
    EXTRACT(YEAR FROM origination_date) as vintage_year,
    COUNT(*) as loan_count,
    SUM(outstanding_balance) as total_exposure,
    SUM(ecl_amount) as total_ecl,
    AVG(ecl_rate) as avg_ecl_rate,
    SUM(CASE WHEN ifrs9_stage = 3 THEN 1 ELSE 0 END) as defaulted_count,
    SUM(CASE WHEN ifrs9_stage = 3 THEN 1 ELSE 0 END) * 100.0 / COUNT(*) as default_rate
FROM `{project_id}.{dataset_id}.loan_portfolio`
WHERE reporting_date = '2024-12-31'
GROUP BY vintage_year
ORDER BY vintage_year DESC;


-- ============================================================================
-- 5. GEOGRAPHIC ANALYSIS
-- ============================================================================

-- ECL by geography
SELECT 
    geography,
    COUNT(*) as loan_count,
    SUM(outstanding_balance) as total_exposure,
    SUM(ecl_amount) as total_ecl,
    SUM(ecl_amount) / SUM(outstanding_balance) * 100 as coverage_ratio,
    AVG(pd_12m) as avg_pd,
    SUM(CASE WHEN ifrs9_stage = 3 THEN outstanding_balance ELSE 0 END) / 
        SUM(outstanding_balance) * 100 as stage3_ratio
FROM `{project_id}.{dataset_id}.loan_portfolio`
WHERE reporting_date = '2024-12-31'
GROUP BY geography
ORDER BY total_exposure DESC;


-- ============================================================================
-- 6. CREDIT QUALITY ANALYSIS
-- ============================================================================

-- Distribution by credit score bands
SELECT 
    CASE 
        WHEN credit_score_current >= 750 THEN 'Excellent (750+)'
        WHEN credit_score_current >= 700 THEN 'Good (700-749)'
        WHEN credit_score_current >= 650 THEN 'Fair (650-699)'
        WHEN credit_score_current >= 600 THEN 'Poor (600-649)'
        ELSE 'Very Poor (<600)'
    END as credit_band,
    COUNT(*) as loan_count,
    SUM(outstanding_balance) as total_exposure,
    SUM(ecl_amount) as total_ecl,
    AVG(pd_12m) as avg_pd,
    SUM(CASE WHEN ifrs9_stage >= 2 THEN 1 ELSE 0 END) * 100.0 / COUNT(*) as stage2_3_pct
FROM `{project_id}.{dataset_id}.loan_portfolio`
WHERE reporting_date = '2024-12-31'
GROUP BY credit_band
ORDER BY 
    CASE 
        WHEN credit_score_current >= 750 THEN 1
        WHEN credit_score_current >= 700 THEN 2
        WHEN credit_score_current >= 650 THEN 3
        WHEN credit_score_current >= 600 THEN 4
        ELSE 5
    END;


-- Credit migration (score deterioration)
SELECT 
    CASE 
        WHEN credit_score_current - credit_score_origination >= 50 THEN 'Improved (50+)'
        WHEN credit_score_current - credit_score_origination >= 0 THEN 'Stable/Slight improvement'
        WHEN credit_score_current - credit_score_origination >= -50 THEN 'Moderate decline'
        ELSE 'Severe decline (50+)'
    END as credit_migration,
    COUNT(*) as loan_count,
    SUM(outstanding_balance) as total_exposure,
    SUM(ecl_amount) as total_ecl,
    AVG(ifrs9_stage) as avg_stage
FROM `{project_id}.{dataset_id}.loan_portfolio`
WHERE reporting_date = '2024-12-31'
GROUP BY credit_migration
ORDER BY avg_stage DESC;


-- ============================================================================
-- 7. DELINQUENCY ANALYSIS
-- ============================================================================

-- Distribution by DPD buckets
SELECT 
    CASE 
        WHEN days_past_due = 0 THEN 'Current'
        WHEN days_past_due <= 30 THEN '1-30 DPD'
        WHEN days_past_due <= 60 THEN '31-60 DPD'
        WHEN days_past_due <= 90 THEN '61-90 DPD'
        ELSE '90+ DPD'
    END as dpd_bucket,
    COUNT(*) as loan_count,
    SUM(outstanding_balance) as total_exposure,
    SUM(ecl_amount) as total_ecl,
    AVG(pd_12m) as avg_pd
FROM `{project_id}.{dataset_id}.loan_portfolio`
WHERE reporting_date = '2024-12-31'
GROUP BY dpd_bucket
ORDER BY 
    CASE 
        WHEN days_past_due = 0 THEN 1
        WHEN days_past_due <= 30 THEN 2
        WHEN days_past_due <= 60 THEN 3
        WHEN days_past_due <= 90 THEN 4
        ELSE 5
    END;


-- ============================================================================
-- 8. HIGH RISK LOANS
-- ============================================================================

-- Top high-risk loans (Stage 3 or high ECL)
SELECT 
    loan_id,
    product_type,
    outstanding_balance,
    ecl_amount,
    ecl_rate,
    ifrs9_stage,
    days_past_due,
    credit_score_current,
    pd_lifetime,
    lgd
FROM `{project_id}.{dataset_id}.loan_portfolio`
WHERE reporting_date = '2024-12-31'
    AND (ifrs9_stage = 3 OR ecl_rate > 10)
ORDER BY ecl_amount DESC
LIMIT 100;


-- ============================================================================
-- 9. CONCENTRATION RISK
-- ============================================================================

-- Top 10 largest exposures
SELECT 
    loan_id,
    product_type,
    outstanding_balance,
    ecl_amount,
    ecl_rate,
    ifrs9_stage,
    outstanding_balance / SUM(outstanding_balance) OVER() * 100 as pct_of_portfolio
FROM `{project_id}.{dataset_id}.loan_portfolio`
WHERE reporting_date = '2024-12-31'
ORDER BY outstanding_balance DESC
LIMIT 10;


-- Industry concentration (for SME loans)
SELECT 
    industry_sector,
    COUNT(*) as loan_count,
    SUM(outstanding_balance) as total_exposure,
    SUM(ecl_amount) as total_ecl,
    AVG(pd_12m) as avg_pd
FROM `{project_id}.{dataset_id}.loan_portfolio`
WHERE reporting_date = '2024-12-31'
    AND product_type = 'SME Loan'
GROUP BY industry_sector
ORDER BY total_exposure DESC;


-- ============================================================================
-- 10. ECL SENSITIVITY ANALYSIS
-- ============================================================================

-- Simulate ECL under stressed PD scenario (PD increased by 50%)
SELECT 
    'Base Case' as scenario,
    SUM(ecl_amount) as total_ecl
FROM `{project_id}.{dataset_id}.loan_portfolio`
WHERE reporting_date = '2024-12-31'

UNION ALL

SELECT 
    'Stressed PD (+50%)' as scenario,
    SUM(outstanding_balance * (pd_12m * 1.5) * lgd) as total_ecl
FROM `{project_id}.{dataset_id}.loan_portfolio`
WHERE reporting_date = '2024-12-31'
    AND ifrs9_stage = 1

UNION ALL

SELECT 
    'Stressed PD (+50%) - All Stages' as scenario,
    SUM(CASE 
        WHEN ifrs9_stage = 1 THEN outstanding_balance * (pd_12m * 1.5) * lgd
        ELSE outstanding_balance * (pd_lifetime * 1.5) * lgd
    END) as total_ecl
FROM `{project_id}.{dataset_id}.loan_portfolio`
WHERE reporting_date = '2024-12-31';
