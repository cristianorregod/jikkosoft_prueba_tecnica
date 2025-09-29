"""
This module contains utilities for CSV file operations with customer transactions.

The module provides functionality for:
- Saving transaction data to CSV files
- Loading transaction data from CSV files
- Data validation and error handling
- Date format standardization

The CSV format includes the following fields:
- timestamp: Date and time of the transaction (format: YYYY-MM-DD HH:MM:SS)
- customer_id: Unique identifier for the customer
- amount: Transaction amount in decimal format
"""
import csv
from datetime import datetime
from typing import List
from dataclasses import asdict
from src.customer_analytics import Transaction

class TransactionCSVHandler:
    DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

    @staticmethod
    def save_transactions(transactions: List[Transaction], filepath: str) -> None:
        """
        Save transactions to a CSV file.
        
        Args:
            transactions: List of Transaction objects to save
            filepath: Path to the CSV file
        """
        with open(filepath, 'w', newline='') as csvfile:
            fieldnames = ['timestamp', 'customer_id', 'amount']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for transaction in transactions:
                row = asdict(transaction)
                row['timestamp'] = transaction.timestamp.strftime(TransactionCSVHandler.DATE_FORMAT)
                writer.writerow(row)

    @staticmethod
    def load_transactions(filepath: str) -> List[Transaction]:
        """
        Load transactions from a CSV file.
        
        Args:
            filepath: Path to the CSV file
            
        Returns:
            List of Transaction objects
            
        Raises:
            ValueError: If the CSV file has an invalid format
        """
        transactions = []
        required_fields = {'timestamp', 'customer_id', 'amount'}
        
        with open(filepath, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            
            # Verify CSV has required fields
            if not required_fields.issubset(set(reader.fieldnames or [])):
                raise ValueError(
                    f"CSV file must contain fields: {', '.join(required_fields)}"
                )
            
            for row in reader:
                try:
                    transaction = Transaction(
                        timestamp=datetime.strptime(row['timestamp'], TransactionCSVHandler.DATE_FORMAT),
                        customer_id=row['customer_id'],
                        amount=float(row['amount'])
                    )
                    transactions.append(transaction)
                except (ValueError, KeyError) as e:
                    raise ValueError(f"Invalid data format in CSV: {str(e)}")
                
        return transactions