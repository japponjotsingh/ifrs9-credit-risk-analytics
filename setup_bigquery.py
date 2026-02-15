"""
BigQuery Setup Script for IFRS 9 Credit Risk Analytics
This script creates the necessary BigQuery dataset and table
"""

from google.cloud import bigquery
import os

# Configuration
PROJECT_ID = "your-gcp-project-id"  # Replace with your GCP project ID
DATASET_ID = "credit_risk_ifrs9"
TABLE_ID = "loan_portfolio"

def create_bigquery_dataset(client, dataset_id):
    """Create BigQuery dataset if it doesn't exist"""
    dataset_ref = f"{PROJECT_ID}.{dataset_id}"
    
    try:
        client.get_dataset(dataset_ref)
        print(f"Dataset {dataset_id} already exists")
    except Exception:
        dataset = bigquery.Dataset(dataset_ref)
        dataset.location = "US"  # Change to your preferred location
        dataset.description = "IFRS 9 Credit Risk Analytics Data"
        
        dataset = client.create_dataset(dataset, timeout=30)
        print(f"Created dataset {dataset_id}")


def create_loan_portfolio_table(client, dataset_id, table_id):
    """Create loan portfolio table with schema"""
    
    table_ref = f"{PROJECT_ID}.{dataset_id}.{table_id}"
    
    schema = [
        bigquery.SchemaField("loan_id", "STRING", mode="REQUIRED", description="Unique loan identifier"),
        bigquery.SchemaField("reporting_date", "DATE", mode="REQUIRED", description="Reporting date for this snapshot"),
        bigquery.SchemaField("product_type", "STRING", mode="REQUIRED", description="Type of loan product"),
        bigquery.SchemaField("origination_date", "DATE", mode="REQUIRED", description="Date when loan was originated"),
        bigquery.SchemaField("original_amount", "FLOAT64", mode="REQUIRED", description="Original loan amount"),
        bigquery.SchemaField("outstanding_balance", "FLOAT64", mode="REQUIRED", description="Current outstanding balance (EAD)"),
        bigquery.SchemaField("credit_score_origination", "INTEGER", mode="REQUIRED", description="Credit score at origination"),
        bigquery.SchemaField("credit_score_current", "INTEGER", mode="REQUIRED", description="Current credit score"),
        bigquery.SchemaField("days_past_due", "INTEGER", mode="REQUIRED", description="Current days past due"),
        bigquery.SchemaField("interest_rate", "FLOAT64", mode="REQUIRED", description="Interest rate percentage"),
        bigquery.SchemaField("industry_sector", "STRING", mode="NULLABLE", description="Industry sector for business loans"),
        bigquery.SchemaField("geography", "STRING", mode="REQUIRED", description="Geographic region"),
        bigquery.SchemaField("pd_12m", "FLOAT64", mode="REQUIRED", description="12-month Probability of Default"),
        bigquery.SchemaField("pd_lifetime", "FLOAT64", mode="REQUIRED", description="Lifetime Probability of Default"),
        bigquery.SchemaField("lgd", "FLOAT64", mode="REQUIRED", description="Loss Given Default"),
        bigquery.SchemaField("ifrs9_stage", "INTEGER", mode="REQUIRED", description="IFRS 9 staging (1, 2, or 3)"),
        bigquery.SchemaField("ecl_amount", "FLOAT64", mode="REQUIRED", description="Expected Credit Loss amount"),
        bigquery.SchemaField("ecl_rate", "FLOAT64", mode="REQUIRED", description="ECL as percentage of outstanding balance"),
    ]
    
    table = bigquery.Table(table_ref, schema=schema)
    table.description = "IFRS 9 Loan Portfolio with ECL calculations"
    
    # Partition by reporting_date for efficient querying
    table.time_partitioning = bigquery.TimePartitioning(
        type_=bigquery.TimePartitioningType.DAY,
        field="reporting_date",
    )
    
    # Cluster by stage and product for better query performance
    table.clustering_fields = ["ifrs9_stage", "product_type"]
    
    try:
        table = client.create_table(table)
        print(f"Created table {table_id}")
    except Exception as e:
        print(f"Table {table_id} might already exist: {e}")


def load_data_to_bigquery(client, dataset_id, table_id, csv_file):
    """Load CSV data into BigQuery table"""
    
    table_ref = f"{PROJECT_ID}.{dataset_id}.{table_id}"
    
    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1,
        autodetect=False,
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,  # Overwrite existing data
    )
    
    with open(csv_file, "rb") as source_file:
        job = client.load_table_from_file(source_file, table_ref, job_config=job_config)
    
    job.result()  # Wait for the job to complete
    
    table = client.get_table(table_ref)
    print(f"Loaded {table.num_rows} rows into {table_id}")


def main():
    """Main setup function"""
    
    # Initialize BigQuery client
    # Make sure you have set up authentication:
    # export GOOGLE_APPLICATION_CREDENTIALS="path/to/your/service-account-key.json"
    
    try:
        client = bigquery.Client(project=PROJECT_ID)
        print(f"Connected to project: {PROJECT_ID}")
        
        # Create dataset
        create_bigquery_dataset(client, DATASET_ID)
        
        # Create table
        create_loan_portfolio_table(client, DATASET_ID, TABLE_ID)
        
        # Load data
        csv_file = "loan_portfolio_data.csv"
        if os.path.exists(csv_file):
            load_data_to_bigquery(client, DATASET_ID, TABLE_ID, csv_file)
        else:
            print(f"CSV file {csv_file} not found. Please run generate_sample_data.py first.")
        
        print("\nSetup completed successfully!")
        print(f"\nYou can now query your data using:")
        print(f"SELECT * FROM `{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}` LIMIT 10")
        
    except Exception as e:
        print(f"Error during setup: {e}")
        print("\nMake sure you have:")
        print("1. Created a GCP project")
        print("2. Enabled BigQuery API")
        print("3. Set up authentication (service account key)")
        print("4. Updated PROJECT_ID in this script")


if __name__ == "__main__":
    main()
