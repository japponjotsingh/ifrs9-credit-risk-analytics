# 🏦 IFRS 9 Automated Credit Risk Analytics

> End-to-end cloud-based credit risk reporting system implementing IFRS 9 Expected Credit Loss calculations on Google Cloud Platform

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![GCP](https://img.shields.io/badge/GCP-BigQuery-orange.svg)](https://cloud.google.com/bigquery)
[![IFRS 9](https://img.shields.io/badge/IFRS%209-Compliant-green.svg)](https://www.ifrs.org/)

---

## 📊 Project Results

### Portfolio Overview
- **Total Loans Analyzed:** 5,000
- **Total Outstanding Balance:** $259,505,668.66
- **Total ECL Amount:** $6,662,534.01
- **Overall Coverage Ratio:** 2.57%

### IFRS 9 Staging Distribution

| Stage | Description | Loan Count | % of Portfolio | Total Exposure | Total ECL | Coverage % |
|-------|-------------|------------|----------------|----------------|-----------|------------|
| **Stage 1** | Performing | 2,531 | 50.6% | $140.6M | $361K | 0.26% |
| **Stage 2** | SICR Detected | 2,366 | 47.3% | $112.8M | $5.5M | 4.92% |
| **Stage 3** | Default | 103 | 2.1% | $6.1M | $756K | 12.31% |

### Risk by Product Type

| Product | ECL Rate | Risk Level | Key Characteristic |
|---------|----------|------------|-------------------|
| **Credit Card** | 14.26% | Highest | Unsecured exposure |
| **SME Loan** | 8.73% | High | Business concentration |
| **Personal Loan** | 8.55% | High | Unsecured consumer debt |
| **Auto Loan** | 3.85% | Moderate | Secured by collateral |
| **Mortgage** | 1.85% | Low | Strong collateral backing |

### Credit Quality Distribution

| Credit Band | Score Range | Loan Count | % of Portfolio | Risk Assessment |
|-------------|-------------|------------|----------------|-----------------|
| **Fair (650-699)** | 650-699 | 1,158 | 23.2% | Largest segment - middle market |
| **Good (700-749)** | 700-749 | 1,002 | 20.0% | Strong credit quality |
| **Excellent (750+)** | 750+ | 1,034 | 20.7% | Premium borrowers |
| **Poor (600-649)** | 600-649 | 950 | 19.0% | Requires monitoring |
| **Very Poor (<600)** | <600 | 851 | 17.0% | High risk segment |

### Key Risk Metrics

**Top Risk Exposure:**
- Loan ID: LN0002300
- ECL Amount: $23,287.26
- Requires immediate review and potential provisioning

**Default Rate:** 2.1% (103 loans in Stage 3)
**SICR Detection:** 47.3% of portfolio actively monitored in Stage 2

---

## 🎯 Project Objective

Build a production-ready automated system for IFRS 9 Expected Credit Loss (ECL) calculation and reporting, demonstrating:
- Cloud data engineering capabilities
- Credit risk analytics expertise
- Regulatory compliance implementation
- Automated reporting workflows

---

## ✨ Key Features

### Phase 1 - Foundation ✅ (Completed)
- ✅ **Realistic Data Generation:** 5,000 synthetic loans across 5 product types
- ✅ **Risk Parameter Calculations:** PD, LGD, and EAD models
- ✅ **IFRS 9 Staging Logic:** Automated Stage 1/2/3 classification
- ✅ **ECL Computation:** Both 12-month and lifetime ECL
- ✅ **BigQuery Integration:** Cloud data warehouse setup
- ✅ **Analytics Queries:** 10+ professional SQL queries
- ✅ **Documentation:** Comprehensive guides and READMEs

### Phase 2 - Automation 🚧 (Planned)
- ⏳ Cloud Functions for automated processing
- ⏳ Cloud Scheduler for daily/monthly runs
- ⏳ Vertex AI integration for insights
- ⏳ Automated report generation (PDF/PowerPoint)
- ⏳ Email notifications and alerts
- ⏳ Interactive Looker Studio dashboards

---

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────┐    ┌─────────────────┐
│  Data Generator │───▶│   BigQuery   │───▶│  Analytics SQL  │
│    (Python)     │    │ (Cloud DWH)  │    │   (Queries)     │
└─────────────────┘    └──────────────┘    └─────────────────┘
                              │                       │
                              ▼                       ▼
                       ┌──────────────┐    ┌─────────────────┐
                       │ Cloud Funcs  │    │  AI Insights    │
                       │ (Automation) │    │ (Vertex AI)     │
                       └──────────────┘    └─────────────────┘
                              │                       │
                              └───────────┬───────────┘
                                          ▼
                                  ┌──────────────┐
                                  │   Reports    │
                                  │ & Dashboards │
                                  └──────────────┘
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Google Cloud Platform account (free tier available)
- Basic understanding of SQL and credit risk concepts

### Step 1: Clone Repository
```bash
git clone https://github.com/yourusername/ifrs9-automation.git
cd ifrs9-automation
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Generate Sample Data
```bash
python generate_sample_data.py
```

This creates `loan_portfolio_data.csv` with 5,000 synthetic loans.

### Step 4: Set Up Google Cloud Platform

1. **Create GCP Project:**
   - Go to https://console.cloud.google.com
   - Create new project: "ifrs9-analytics"
   - Enable BigQuery API

2. **Create Service Account:**
   - Navigate to IAM & Admin → Service Accounts
   - Create account with "BigQuery Admin" role
   - Download JSON key

3. **Set Authentication:**
   ```bash
   export GOOGLE_APPLICATION_CREDENTIALS="path/to/key.json"
   ```

### Step 5: Load Data to BigQuery

1. Edit `setup_bigquery.py` with your Project ID
2. Run setup:
   ```bash
   python setup_bigquery.py
   ```

### Step 6: Run Analytics Queries

Access BigQuery Console and run queries from `sql_queries.sql`:

**Example - Portfolio Summary:**
```sql
SELECT 
    ifrs9_stage,
    COUNT(*) as loan_count,
    ROUND(SUM(outstanding_balance), 2) as total_exposure,
    ROUND(SUM(ecl_amount), 2) as total_ecl,
    ROUND(SUM(ecl_amount)/SUM(outstanding_balance)*100, 2) as coverage_pct
FROM `your-project-id.credit_risk_ifrs9.loan_portfolio`
GROUP BY ifrs9_stage
ORDER BY ifrs9_stage;
```

---

## 📂 Project Structure

```
ifrs9-automation/
├── README.md                      # This file
├── QUICKSTART.md                  # 5-minute setup guide
├── DATA_SUMMARY.md                # Detailed data documentation
├── GITHUB_README.md               # GitHub project page
├── requirements.txt               # Python dependencies
├── generate_sample_data.py        # Synthetic data generator
├── setup_bigquery.py              # GCP/BigQuery setup
├── sql_queries.sql                # Analytical queries (10+)
├── loan_portfolio_data.csv        # Generated dataset
└── automation/                    # Phase 2 (coming soon)
    ├── cloud_functions/
    ├── workflows/
    └── reports/
```

---

## 💼 Business Impact & Use Cases

### Regulatory Compliance
- **IFRS 9 Standards:** Automated ECL calculation meeting accounting requirements
- **Audit Trail:** Complete data lineage and calculation transparency
- **Reporting:** Ready-to-use templates for regulatory submissions

### Risk Management
- **Proactive Monitoring:** Early detection of credit deterioration (Stage 2)
- **Portfolio Analytics:** Comprehensive risk metrics and KPIs
- **Concentration Risk:** Geographic and sector analysis

### Operational Efficiency
- **Automation:** Reduces manual calculation time from days to minutes
- **Scalability:** Cloud-native architecture handles portfolio growth
- **Real-time:** Up-to-date risk metrics for decision-making

---

## 📈 Sample Analytics & Insights

### Portfolio Health Indicators
- ✅ **Low Default Rate:** 2.1% in Stage 3 indicates effective credit management
- ✅ **Proactive Monitoring:** 47.3% in Stage 2 shows early risk detection
- ✅ **Diversified Portfolio:** Spread across 5 product types and 5 regions

### Risk Concentrations
- ⚠️ **High-Risk Products:** Credit Cards (14.26% ECL) need targeted mitigation
- ⚠️ **Credit Quality:** 17% in Very Poor segment drives 51% of total ECL
- ⚠️ **Top Exposures:** LN0002300 requires immediate attention

### Strategic Opportunities
- 💡 **Middle Market:** Fair credit segment (23.2%) represents growth opportunity
- 💡 **Premium Segment:** 20.7% excellent credit offers expansion potential
- 💡 **Product Mix:** Mortgage portfolio provides stability with low ECL (1.85%)

---

## 🛠️ Tech Stack

**Languages & Libraries:**
- Python 3.8+ (Pandas, NumPy, Google Cloud BigQuery)
- SQL (BigQuery Standard SQL)

**Cloud Platform:**
- Google Cloud Platform
- BigQuery (Data Warehouse)
- Cloud Functions (Serverless Computing)
- Vertex AI (Machine Learning)
- Cloud Scheduler (Orchestration)
- Looker Studio (Visualization)

**Development Tools:**
- Jupyter Notebook
- Git/GitHub
- VS Code

---

## 📚 Skills Demonstrated

### Technical Skills
✅ Cloud Data Engineering (GCP/BigQuery)  
✅ ETL Pipeline Development  
✅ SQL Analytics (Complex queries, window functions, CTEs)  
✅ Python Data Processing (Pandas, NumPy)  
✅ API Integration (Google Cloud SDK)  
✅ Data Modeling & Architecture  
✅ Automation & Orchestration  

### Domain Expertise
✅ IFRS 9 Accounting Standards  
✅ Credit Risk Analytics  
✅ Expected Credit Loss Modeling  
✅ Risk Parameter Estimation (PD, LGD, EAD)  
✅ SICR Detection Logic  
✅ Financial Reporting & Compliance  
✅ Portfolio Management  

---

## 📊 Key SQL Queries

### 1. Portfolio Overview
```sql
SELECT 
    COUNT(*) as total_loans,
    SUM(outstanding_balance) as total_exposure,
    SUM(ecl_amount) as total_ecl,
    SUM(ecl_amount) / SUM(outstanding_balance) * 100 as coverage_ratio
FROM loan_portfolio;
```

### 2. High-Risk Loans (Watchlist)
```sql
SELECT loan_id, product_type, outstanding_balance, ecl_amount
FROM loan_portfolio
WHERE ifrs9_stage = 3 OR ecl_rate > 10
ORDER BY ecl_amount DESC
LIMIT 20;
```

### 3. Product Risk Analysis
```sql
SELECT 
    product_type,
    COUNT(*) as loans,
    SUM(ecl_amount) / SUM(outstanding_balance) * 100 as ecl_rate
FROM loan_portfolio
GROUP BY product_type
ORDER BY ecl_rate DESC;
```

See `sql_queries.sql` for 10+ additional analytics queries.

---

## 🎓 Learning Outcomes

After completing this project, you will understand:
- ✅ IFRS 9 regulatory requirements and implementation
- ✅ Cloud-based data warehouse architecture (BigQuery)
- ✅ Automated data pipeline development
- ✅ Credit risk modeling and analytics
- ✅ Production-grade code organization
- ✅ SQL optimization for large datasets
- ✅ Data visualization and reporting

---

## 🔮 Roadmap

- [x] **Phase 1:** Data foundation and analytics (COMPLETE)
  - [x] Synthetic data generation
  - [x] BigQuery setup
  - [x] SQL analytics queries
  - [x] Documentation
  
- [ ] **Phase 2:** Cloud automation and orchestration
  - [ ] Cloud Functions for automated ECL calculation
  - [ ] Cloud Scheduler for daily/monthly runs
  - [ ] Error handling and monitoring
  
- [ ] **Phase 3:** AI-powered insights
  - [ ] Vertex AI integration
  - [ ] Automated narrative generation
  - [ ] Anomaly detection
  
- [ ] **Phase 4:** Real-time dashboards
  - [ ] Looker Studio dashboards
  - [ ] Email notifications
  - [ ] Executive summaries
  
- [ ] **Phase 5:** Advanced ML models
  - [ ] Predictive PD/LGD models
  - [ ] Early warning system
  - [ ] Stress testing scenarios

---

## 🎯 Portfolio Showcase

This project is perfect for demonstrating:
- **Data Engineering:** Cloud-native architecture, ETL pipelines
- **Analytics:** SQL proficiency, data modeling
- **Domain Knowledge:** Banking regulations, credit risk
- **Automation:** Workflow design, scheduled jobs
- **Communication:** Documentation, visualization, reporting

**Ideal for roles in:**
- Credit Risk Analytics
- Data Engineering
- Financial Services Technology
- Risk Management
- Data Science (Banking/Finance)

---

## 📧 Contact

**Your Name**  
📧 Email: japponjot.singh@gmail.com
💼 LinkedIn: https://www.linkedin.com/in/japponjot-singh/
🌐 Github: https://github.com/japponjotsingh


---

## 📄 License

This project is for educational and portfolio purposes. Feel free to use and modify for learning.

---

## 🙏 Acknowledgments

- IFRS Foundation for accounting standards guidance
- Google Cloud Platform for cloud infrastructure
- Python and SQL communities for excellent tools and libraries

---

## ⭐ Show Your Support

If you found this project helpful:
- ⭐ **Star this repository**
- 🔄 **Fork it** to create your own version
- 💬 **Share feedback** via issues
- 📢 **Share** with others learning credit risk analytics

---

**Built with ❤️ to demonstrate modern credit risk analytics capabilities**

*Last Updated: December 2024*
