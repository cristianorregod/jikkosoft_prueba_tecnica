"""
Tests for the customer analytics module.
"""
from datetime import datetime, timedelta
import pytest
from src.customer_analytics import CustomerAnalytics, Transaction
import time

class TestCustomerAnalytics:
    def setup_method(self):
        self.analytics = CustomerAnalytics()
        self.start_date = datetime(2023, 1, 1)
        self.end_date = datetime(2023, 12, 31)

    def test_generate_transaction_data_basic(self):
        """Test basic transaction data generation"""
        num_transactions = 1000
        num_customers = 100
        
        transactions = self.analytics.generate_transaction_data(
            num_transactions,
            self.start_date,
            self.end_date,
            num_customers
        )
        
        assert len(transactions) == num_transactions
        assert all(isinstance(t, Transaction) for t in transactions)
        assert all(self.start_date <= t.timestamp <= self.end_date for t in transactions)
        assert all(1.0 <= t.amount <= 1000.0 for t in transactions)
        
        unique_customers = len(set(t.customer_id for t in transactions))
        assert unique_customers <= num_customers
        
        # Verify transactions are sorted by timestamp
        timestamps = [t.timestamp for t in transactions]
        assert timestamps == sorted(timestamps)

    def test_generate_transaction_data_validation(self):
        """Test input validation for transaction generation"""
        with pytest.raises(ValueError, match="must be positive"):
            self.analytics.generate_transaction_data(-1, self.start_date, self.end_date, 10)
            
        with pytest.raises(ValueError, match="must be positive"):
            self.analytics.generate_transaction_data(100, self.start_date, self.end_date, -1)
            
        with pytest.raises(ValueError, match="Start date must be before end date"):
            self.analytics.generate_transaction_data(100, self.end_date, self.start_date, 10)

    def test_get_top_customers_basic(self):
        """Test basic top customers functionality"""
        transactions = [
            Transaction(self.start_date, "customer1", 100.0),
            Transaction(self.start_date, "customer1", 200.0),
            Transaction(self.start_date, "customer2", 150.0),
            Transaction(self.end_date, "customer3", 300.0)
        ]
        
        top_customers = self.analytics.get_top_customers(
            transactions,
            self.start_date,
            self.end_date
        )
        
        assert len(top_customers) == 3
        assert top_customers[0] == ("customer1", 2)
        assert top_customers[1] == ("customer2", 1)
        assert top_customers[2] == ("customer3", 1)

    def test_get_top_customers_date_filtering(self):
        """Test that date range filtering works correctly"""
        mid_date = datetime(2023, 6, 1)
        transactions = [
            Transaction(self.start_date, "customer1", 100.0),
            Transaction(mid_date, "customer2", 150.0),
            Transaction(self.end_date, "customer3", 300.0)
        ]
        
        # Test first half of year
        top_customers = self.analytics.get_top_customers(
            transactions,
            self.start_date,
            mid_date
        )
        assert len(top_customers) == 2
        assert top_customers[0][0] in ["customer1", "customer2"]

    def test_get_top_customers_validation(self):
        """Test input validation for top customers analysis"""
        transactions = []
        
        with pytest.raises(ValueError, match="top_n must be positive"):
            self.analytics.get_top_customers(transactions, self.start_date, self.end_date, 0)
            
        with pytest.raises(ValueError, match="Start date must be before end date"):
            self.analytics.get_top_customers(transactions, self.end_date, self.start_date)

    def test_performance_large_dataset(self):
        """Test performance with a large dataset"""
        num_transactions = 100_000
        num_customers = 10_000
        
        # Generate large dataset
        start_time = time.time()
        transactions = self.analytics.generate_transaction_data(
            num_transactions,
            self.start_date,
            self.end_date,
            num_customers
        )
        gen_time = time.time() - start_time
        
        # Analyze performance
        start_time = time.time()
        top_customers = self.analytics.get_top_customers(transactions, self.start_date, self.end_date)
        analysis_time = time.time() - start_time
        
        # Basic assertions
        assert len(transactions) == num_transactions
        assert len(top_customers) == 10
        
        # Performance assertions (adjust thresholds as needed)
        assert gen_time < 2.0, f"Data generation took too long: {gen_time:.2f}s"
        assert analysis_time < 1.0, f"Analysis took too long: {analysis_time:.2f}s"