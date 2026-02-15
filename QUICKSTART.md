# QUICK START GUIDE - IFRS 9 Credit Risk Automation

## 🚀 5-Minute Setup

### 1️⃣ Generate Data (1 minute)

```bash
# Install dependencies
pip install pandas numpy

# Generate synthetic loan portfolio
python generate_sample_data.py
```

**Output:** `loan_portfolio_data.csv` with 5,000 loans

---

### 2️⃣ Set Up GCP (2 minutes)

**Create GCP Project:**
1. Go to https://console.cloud.google.com
2. Click "New Project" → Name it "ifrs9-analytics"
3. Copy your Project ID

**Enable BigQuery:**
1. Search "BigQuery API" in search bar
2. Click "Enable"

**Create Service Account:**
1. Go to IAM & Admin → Service Accounts
2. Create Service Account → Name: "ifrs9-automation"
3. Grant role: "BigQuery Admin"
4. Create JSON key → Download

---

### 3️⃣ Configure & Load (2 minutes)

```bash
# Set authentication (replace with your path)
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/key.json"

# Install BigQuery library
pip install google-cloud-bigquery

# Edit setup_bigquery.py - Update line 10:
# PROJECT_ID = "your-project-id"  # Replace with YOUR project ID

# Run setup
python setup_bigquery.py
```

---

### 4️⃣ Query Data (30 seconds)

Go to: https://console.cloud.google.com/bigquery

Run this query:
```sql
SELECT 
    ifrs9_stage,
    COUNT(*) as loans,
    ROUND(SUM(outstanding_balance), 2) as exposure,
    ROUND(SUM(ecl_amount), 2) as ecl,
    ROUND(SUM(ecl_amount) / SUM(outstanding_balance) * 100, 2) as coverage_pct
FROM `your-project-id.credit_risk_ifrs9.loan_portfolio`
GROUP BY ifrs9_stage
ORDER BY ifrs9_stage;
```

---

## ✅ Success Indicators

You should see:
- ✓ ~2,500 loans in Stage 1
- ✓ ~2,400 loans in Stage 2  
- ✓ ~100 loans in Stage 3
- ✓ Total ECL around $6-7M
- ✓ Coverage ratios: Stage 1 (~0.5%), Stage 2 (~3-5%), Stage 3 (~30%+)

---

## 🎯 What You've Built

You now have:
1. ✅ Realistic IFRS 9 loan portfolio dataset
2. ✅ Cloud-based data warehouse (BigQuery)
3. ✅ Automated ECL calculations
4. ✅ Production-ready SQL analytics
5. ✅ Foundation for automation & AI integration

---

## 📊 Try These Queries Next

### High-Risk Loans
```sql
SELECT loan_id, product_type, outstanding_balance, ecl_amount, days_past_due
FROM `your-project-id.credit_risk_ifrs9.loan_portfolio`
WHERE ifrs9_stage = 3
ORDER BY ecl_amount DESC
LIMIT 10;
```

### ECL by Product
```sql
SELECT 
    product_type,
    COUNT(*) as loans,
    ROUND(SUM(ecl_amount), 2) as total_ecl
FROM `your-project-id.credit_risk_ifrs9.loan_portfolio`
GROUP BY product_type
ORDER BY total_ecl DESC;
```

---

## 🔥 Common Issues

**"Module not found"**
```bash
pip install pandas numpy google-cloud-bigquery
```

**"Authentication failed"**
```bash
# Check your environment variable
echo $GOOGLE_APPLICATION_CREDENTIALS

# Make sure path is correct
export GOOGLE_APPLICATION_CREDENTIALS="/correct/path/to/key.json"
```

**"Permission denied"**
- Ensure service account has "BigQuery Admin" role
- Check in IAM & Admin → IAM

---

## 🚀 Next Steps

**Phase 2 - Automation:**
- Scheduled daily ECL calculations
- Cloud Functions for data processing
- Automated reports with AI insights
- Email notifications
- Interactive dashboards

**Ready to continue?** Let me know and we'll build the automation layer!

---

## 💼 For Your Portfolio

This project demonstrates:
- Modern cloud data architecture (GCP/BigQuery)
- Real-world credit risk analytics (IFRS 9)
- Production-ready data engineering
- SQL and Python proficiency
- Automation-first mindset

**Perfect for:** Data Analyst, Risk Analyst, Credit Risk roles

---

## 📧 Questions?

Stuck? Check:
1. README.md for detailed documentation
2. sql_queries.sql for more analytics examples
3. GCP Console logs for error messages

**Pro Tip:** Take screenshots of your BigQuery results for your portfolio!
