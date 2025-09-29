"""
This script demonstrates the customer analytics solution using CSV files.
"""
from datetime import datetime
from customer_analytics import CustomerAnalytics
from csv_handler import TransactionCSVHandler

def generate_and_save_dataset():
    """Generate sample dataset and save to CSV"""
    print("Generating transaction dataset...")
    analytics = CustomerAnalytics()
    
    # Generate sample data
    transactions = analytics.generate_transaction_data(
        num_transactions=100000,  # 100k transactions
        start_date=datetime(2023, 1, 1),
        end_date=datetime(2023, 12, 31),
        num_customers=10000  # 10k customers
    )
    
    # Save to CSV
    csv_path = 'transactions.csv'
    TransactionCSVHandler.save_transactions(transactions, csv_path)
    print(f"Dataset saved to {csv_path}")
    return csv_path

def analyze_top_customers(csv_path: str):
    """Analyze top customers from CSV data"""
    print("\nAnalyzing customer frequencies...")
    
    # Load transactions from CSV
    print("Loading transactions from CSV...")
    transactions = TransactionCSVHandler.load_transactions(csv_path)
    
    # Analyze top customers
    analytics = CustomerAnalytics()
    top_customers = analytics.get_top_customers(
        transactions=transactions,
        start_date=datetime(2023, 1, 1),
        end_date=datetime(2023, 12, 31),
        top_n=10
    )
    
    # Print results
    print("\nTop 10 Customers by Transaction Frequency:")
    print("-" * 45)
    print(f"{'Customer ID':<15} {'Transaction Count':<15}")
    print("-" * 45)
    for customer_id, count in top_customers:
        print(f"{customer_id:<15} {count:<15}")

if __name__ == "__main__":
    # Generate and save dataset
    csv_path = generate_and_save_dataset()
    
    # Analyze the dataset
    analyze_top_customers(csv_path)