# IFRS 9 Automated Credit Risk Analytics

> End-to-end cloud-based credit risk reporting system implementing IFRS 9 Expected Credit Loss calculations on Google Cloud Platform

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![GCP](https://img.shields.io/badge/GCP-BigQuery-orange.svg)](https://cloud.google.com/bigquery)
[![IFRS 9](https://img.shields.io/badge/IFRS%209-Compliant-green.svg)](https://www.ifrs.org/)

---

## 📊 Project Overview

This project demonstrates a production-ready system for IFRS 9 Expected Credit Loss calculation and reporting. Built on Google Cloud Platform, it processes a portfolio of 5,000 loans with automated staging classification and comprehensive risk analytics.

**Portfolio Snapshot:**
- Total Loans: 5,000
- Total Exposure: $259.5M
- Total ECL: $6.7M (2.57% coverage)
- Default Rate: 2.1% (103 loans in Stage 3)

---

## 🎯 Key Results

### IFRS 9 Staging Distribution

| Stage | Description | Loan Count | % Portfolio | Total ECL | Coverage % |
|-------|-------------|------------|-------------|-----------|------------|
| Stage 1 | Performing | 2,531 | 50.6% | $361K | 0.26% |
| Stage 2 | SICR Detected | 2,366 | 47.3% | $5.5M | 4.92% |
| Stage 3 | Default | 103 | 2.1% | $756K | 12.31% |

### Product Risk Analysis

| Product | ECL Rate | Risk Level |
|---------|----------|------------|
| Credit Card | 14.26% | Highest |
| SME Loan | 8.73% | High |
| Personal Loan | 8.55% | High |
| Auto Loan | 3.85% | Moderate |
| Mortgage | 1.85% | Low |

### Credit Quality Distribution

| Credit Band | Score Range | Loan Count | % Portfolio |
|-------------|-------------|------------|-------------|
| Fair (650-699) | 650-699 | 1,158 | 23.2% |
| Good (700-749) | 700-749 | 1,002 | 20.0% |
| Excellent (750+) | 750+ | 1,034 | 20.7% |
| Poor (600-649) | 600-649 | 950 | 19.0% |
| Very Poor (<600) | <600 | 851 | 17.0% |

---

## 🏗️ Technical Implementation

### Phase 1: Data Foundation (Complete)

**Data Infrastructure**
- Generated synthetic loan portfolio (5,000 records)
- Implemented BigQuery data warehouse on GCP
- Automated risk parameter calculations (PD, LGD, EAD)
- Built IFRS 9 staging classification logic
- Developed 10+ analytical SQL queries

### Phase 2: Python Analytics (Complete)

**Advanced Analysis**
- Connected Vertex AI Workbench to BigQuery
- Performed correlation analysis and statistical modeling
- Created 6 interactive Plotly visualizations
- Generated automated CSV exports

**Visualizations Created:**
1. IFRS 9 staging distribution (pie + bar charts)
2. Product risk analysis (ECL rates by product)
3. Credit quality distribution (4-panel analysis)
4. Correlation heatmap (risk parameter relationships)
5. Vintage analysis (performance by origination year)
6. Geographic distribution (risk by region)

**Analysis Outputs:**
- portfolio_summary.csv: Key metrics snapshot
- high_risk_watchlist.csv: Stage 3 and high ECL loans
- product_risk_analysis.csv: Detailed product metrics

### Phase 3: Automation (Planned)

- Cloud Functions for scheduled ECL calculations
- Cloud Scheduler for daily/monthly execution
- Automated alerting for threshold breaches
- Looker Studio dashboards for executive reporting

---

## 💻 Architecture

```
Data Generation (Python) 
    → BigQuery (Data Warehouse)
    → SQL Analytics / Vertex AI Analysis
    → Automated Reports & Dashboards
```

**Technology Stack:**
- **Cloud Platform:** Google Cloud Platform (BigQuery, Vertex AI, Cloud Functions)
- **Languages:** Python 3.8+, SQL
- **Libraries:** Pandas, NumPy, Plotly, google-cloud-bigquery
- **Tools:** Jupyter Notebook, Git/GitHub

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- Google Cloud Platform account (free tier available)
- Basic understanding of SQL and credit risk concepts

### Installation

**1. Clone Repository**
```bash
git clone https://github.com/yourusername/ifrs9-credit-risk-analytics.git
cd ifrs9-credit-risk-analytics
```

**2. Install Dependencies**
```bash
pip install -r requirements.txt
```

**3. Generate Sample Data**
```bash
python generate_sample_data.py
```

**4. Configure GCP**

Create a GCP project and enable BigQuery API:
- Navigate to console.cloud.google.com
- Create new project
- Enable BigQuery API
- Create service account with BigQuery Admin role
- Download JSON key file

Set authentication:
```bash
export GOOGLE_APPLICATION_CREDENTIALS="path/to/key.json"
```

**5. Load Data to BigQuery**
```bash
# Edit setup_bigquery.py with your project ID
python setup_bigquery.py
```

**6. Run Analytics**

Access BigQuery Console and execute queries from `sql_queries.sql`:

```sql
SELECT 
    ifrs9_stage,
    COUNT(*) as loan_count,
    ROUND(SUM(outstanding_balance), 2) as total_exposure,
    ROUND(SUM(ecl_amount), 2) as total_ecl
FROM `your-project-id.credit_risk_ifrs9.loan_portfolio`
GROUP BY ifrs9_stage
ORDER BY ifrs9_stage;
```

---

## 📈 Python Analysis

### Running the Notebook

**File:** `vertex_ai/ifrs9_plotly_notebook.py`

**Functionality:**
- Fetches loan data from BigQuery
- Performs statistical analysis
- Creates interactive visualizations
- Exports results to CSV

**Usage:**

For Vertex AI Workbench:
1. Upload notebook to your instance
2. Update PROJECT_ID (line 33)
3. Run all cells
4. View charts and exports

For local Jupyter:
```bash
pip install google-cloud-bigquery pandas plotly
jupyter notebook
```

**Requirements:**
```
google-cloud-bigquery>=3.11.0
pandas>=2.0.0
plotly>=5.0.0
```

---

## 📂 Project Structure

```
ifrs9-credit-risk-analytics/
├── README.md
├── QUICKSTART.md
├── DATA_SUMMARY.md
├── requirements.txt
├── generate_sample_data.py
├── setup_bigquery.py
├── sql_queries.sql
├── loan_portfolio_data.csv
├── IFRS9_Portfolio_Analysis.pptx
└── vertex_ai/
    ├── ifrs9_plotly_notebook.py
    ├── portfolio_summary.csv
    ├── high_risk_watchlist.csv
    └── product_risk_analysis.csv
```

---

## 📊 Key Findings

### Portfolio Health
- Low default rate (2.1%) indicates effective credit management
- Proactive monitoring of 47.3% in Stage 2 enables early intervention
- Diversified across 5 product types and 5 regions

### Risk Concentrations
- Credit Cards show highest ECL (14.26%) due to unsecured exposure
- Very Poor credit segment (17% of loans) drives 51% of total ECL
- Top exposure (LN0002300): $23,287 ECL

### Strategic Insights
- Fair credit segment (23.2%) represents middle-market opportunity
- Strong correlation between days past due and PD increases
- Newer vintages (2023-2024) show better performance

---

## 💼 Business Applications

**Regulatory Compliance**
- Automated IFRS 9 ECL calculations
- Complete audit trail and data lineage
- Regulatory reporting templates

**Risk Management**
- Early warning through Stage 2 classification
- Portfolio and product-level risk metrics
- Concentration analysis (geographic, sector)

**Operational Efficiency**
- Reduces calculation time from days to minutes
- Scalable cloud architecture
- Real-time risk metrics

---

## 🛠️ Skills Demonstrated

**Technical Skills:**
- Cloud Data Engineering (GCP/BigQuery)
- ETL Pipeline Development
- SQL Analytics (complex queries, CTEs, window functions)
- Python Data Processing (Pandas, NumPy)
- Data Visualization (Plotly)
- API Integration (Google Cloud SDK)
- Version Control (Git/GitHub)

**Domain Knowledge:**
- IFRS 9 Accounting Standards
- Credit Risk Analytics
- Expected Credit Loss Modeling
- Risk Parameter Estimation (PD, LGD, EAD)
- SICR Detection
- Financial Reporting & Compliance
- Portfolio Management

---

## 📝 Sample Queries

**Portfolio Overview**
```sql
SELECT 
    COUNT(*) as total_loans,
    SUM(outstanding_balance) as total_exposure,
    SUM(ecl_amount) as total_ecl,
    SUM(ecl_amount)/SUM(outstanding_balance)*100 as coverage_ratio
FROM loan_portfolio;
```

**High-Risk Watchlist**
```sql
SELECT loan_id, product_type, outstanding_balance, ecl_amount
FROM loan_portfolio
WHERE ifrs9_stage = 3 OR ecl_rate > 10
ORDER BY ecl_amount DESC
LIMIT 20;
```

**Product Risk Analysis**
```sql
SELECT 
    product_type,
    COUNT(*) as loans,
    SUM(ecl_amount)/SUM(outstanding_balance)*100 as ecl_rate
FROM loan_portfolio
GROUP BY product_type
ORDER BY ecl_rate DESC;
```

See `sql_queries.sql` for additional queries.

---

## 🔮 Future Enhancements

**Phase 3: Automation**
- Cloud Functions for automated processing
- Cloud Scheduler for daily/monthly runs
- Email alerts for threshold breaches
- Looker Studio dashboards

**Phase 4: Advanced Analytics**
- Predictive PD/LGD models (ML)
- Early warning system
- Stress testing scenarios
- Portfolio optimization

---

## 📧 Contact

**Japponjot Singh**  
Email: japponjot.singh@gmail.com  
LinkedIn: https://www.linkedin.com/in/japponjot-singh/  
GitHub: https://github.com/japponjotsingh

---

## 📄 License

This project is for educational and portfolio purposes.

---

## 🙏 Acknowledgments

- IFRS Foundation for standards guidance
- Google Cloud Platform for infrastructure
- Python and SQL open-source communities

---

*Last Updated: December 2024*
