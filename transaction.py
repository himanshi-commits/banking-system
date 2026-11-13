# ============================================================
#  transaction.py
#  Contains the Transaction class.
#  Each object of this class stores details of one transaction.
# ============================================================

from datetime import datetime   # For recording the date and time


class Transaction:
    """Represents a single banking transaction (deposit, withdrawal, transfer)."""

    def __init__(self, transaction_type, amount, description):
        self.transaction_type = transaction_type   # e.g., "Deposit", "Withdrawal"
        self.amount = amount                       # How much money was involved
        self.description = description             # A short note about the transaction

        # Automatically record the date and time when this transaction is created
        self.date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def display(self):
        """Print the transaction details in a readable format."""
        print(f"  [{self.date_time}]  {self.transaction_type:<12}  "
              f"Amount: ${self.amount:<10.2f}  Note: {self.description}")

