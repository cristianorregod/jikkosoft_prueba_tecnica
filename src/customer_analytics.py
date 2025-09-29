"""
This module contains the implementation for generating and analyzing customer transaction data.
"""
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List, Dict, Tuple
import random
import heapq
from collections import defaultdict

@dataclass
class Transaction:
    timestamp: datetime
    customer_id: str
    amount: float

class CustomerAnalytics:
    def generate_transaction_data(
        self,
        num_transactions: int,
        start_date: datetime,
        end_date: datetime,
        num_customers: int
    ) -> List[Transaction]:
        """
        Generate a dataset of customer transactions.
        
        Args:
            num_transactions: Number of transactions to generate
            start_date: Start date for transaction range
            end_date: End date for transaction range
            num_customers: Number of unique customers to generate
            
        Returns:
            List of Transaction objects
        """
        if num_transactions < 0 or num_customers < 0:
            raise ValueError("Number of transactions and customers must be positive")
        if start_date >= end_date:
            raise ValueError("Start date must be before end date")
            
        # Generate customer IDs
        customer_ids = [f"CUST{i:06d}" for i in range(num_customers)]
        
        # Calculate time range in seconds
        time_range = int((end_date - start_date).total_seconds())
        
        transactions = []
        for _ in range(num_transactions):
            # Generate random timestamp within the range
            random_seconds = random.randint(0, time_range)
            timestamp = start_date + timedelta(seconds=random_seconds)
            
            # Select random customer
            customer_id = random.choice(customer_ids)
            
            # Generate random amount between $1 and $1000 with 2 decimal places
            amount = round(random.uniform(1.0, 1000.0), 2)
            
            transactions.append(Transaction(timestamp, customer_id, amount))
        
        # Sort transactions by timestamp to simulate real-world ordering
        transactions.sort(key=lambda x: x.timestamp)
        
        return transactions

    def get_top_customers(
        self,
        transactions: List[Transaction],
        start_date: datetime,
        end_date: datetime,
        top_n: int = 10
    ) -> List[Tuple[str, int]]:
        """
        Get the top N customers by transaction frequency in a given date range.
        
        Args:
            transactions: List of transactions to analyze
            start_date: Start date for analysis
            end_date: End date for analysis
            top_n: Number of top customers to return
            
        Returns:
            List of tuples containing (customer_id, transaction_count) sorted by count descending
            
        Time Complexity: O(n log k) where n is number of transactions and k is top_n
        Space Complexity: O(m) where m is number of unique customers
        """
        if top_n < 1:
            raise ValueError("top_n must be positive")
        if start_date >= end_date:
            raise ValueError("Start date must be before end date")
            
        # Count transactions per customer within the date range
        customer_counts = defaultdict(int)
        for transaction in transactions:
            if start_date <= transaction.timestamp <= end_date:
                customer_counts[transaction.customer_id] += 1
        
        # Use a min heap to keep track of top N customers
        heap = []
        for customer_id, count in customer_counts.items():
            if len(heap) < top_n:
                heapq.heappush(heap, (count, customer_id))
            else:
                # If current count is larger than smallest count in heap
                if count > heap[0][0]:
                    heapq.heapreplace(heap, (count, customer_id))
        
        # Convert heap to sorted list of (customer_id, count) tuples
        result = [(cid, cnt) for cnt, cid in heap]
        result.sort(key=lambda x: (-x[1], x[0]))  # Sort by count desc, then by customer_id
        print("RESULT", result)  # Debug print statement
        return result