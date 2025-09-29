"""
Tests for the CSV handler module.
"""
import os
import pytest
from datetime import datetime
from src.customer_analytics import Transaction
from src.csv_handler import TransactionCSVHandler

class TestTransactionCSVHandler:
    def setup_method(self):
        self.test_file = "test_transactions.csv"
        self.test_transactions = [
            Transaction(
                timestamp=datetime(2023, 1, 1, 12, 0, 0),
                customer_id="CUST001",
                amount=100.50
            ),
            Transaction(
                timestamp=datetime(2023, 1, 2, 15, 30, 0),
                customer_id="CUST002",
                amount=200.75
            )
        ]

    def teardown_method(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_save_and_load_transactions(self):
        """Test saving and loading transactions to/from CSV"""
        # Save transactions
        TransactionCSVHandler.save_transactions(self.test_transactions, self.test_file)
        assert os.path.exists(self.test_file)

        # Load transactions
        loaded_transactions = TransactionCSVHandler.load_transactions(self.test_file)
        
        # Verify loaded data
        assert len(loaded_transactions) == len(self.test_transactions)
        
        for original, loaded in zip(self.test_transactions, loaded_transactions):
            assert original.timestamp == loaded.timestamp
            assert original.customer_id == loaded.customer_id
            assert original.amount == loaded.amount

    def test_file_not_found(self):
        """Test loading from non-existent file"""
        with pytest.raises(FileNotFoundError):
            TransactionCSVHandler.load_transactions("nonexistent.csv")

    def test_invalid_csv_format(self, tmp_path):
        """Test loading from invalid CSV format"""
        # Create invalid CSV file
        invalid_file = tmp_path / "invalid.csv"
        with open(invalid_file, 'w') as f:
            f.write("invalid,csv,format\n1,2,3\n")
        
        with pytest.raises(ValueError):
            TransactionCSVHandler.load_transactions(str(invalid_file))