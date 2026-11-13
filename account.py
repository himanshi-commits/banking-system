# ============================================================
#  account.py
#  Contains:
#    - BankOperations: Abstract base class (Abstraction)
#    - Account: Base account class (Encapsulation)
# ============================================================

from abc import ABC, abstractmethod   # For Abstraction
from transaction import Transaction   # Import Transaction to record operations


# ============================================================
# ABSTRACTION: Abstract base class — defines the banking contract.
# Any class inheriting from BankOperations MUST implement
# deposit(), withdraw(), and check_balance().
# ============================================================

class BankOperations(ABC):
    """Abstract base class that defines what a bank account must be able to do."""

    @abstractmethod
    def deposit(self, amount):
        pass  # Child class must implement this

    @abstractmethod
    def withdraw(self, amount):
        pass  # Child class must implement this

    @abstractmethod
    def check_balance(self):
        pass  # Child class must implement this


# ============================================================
# ENCAPSULATION + ABSTRACTION: Account class
# - Inherits from BankOperations (fulfills the abstract contract)
# - Uses private attributes __balance and __account_number
#   so outside code cannot directly change them.
# - Provides getter methods to safely read private data.
# ============================================================

class Account(BankOperations):
    """
    Base class for a bank account.
    Implements the BankOperations abstract class.
    Uses encapsulation to protect balance and account number.
    """

    def __init__(self, account_number, owner_name, initial_deposit):
        # ENCAPSULATION: Private attributes (double underscore = private in Python)
        self.__account_number = account_number
        self.__balance = initial_deposit

        # Public attribute (name is safe to access directly)
        self.owner_name = owner_name

        # List to store all transactions for this account
        self.transactions = []

        # Record the opening deposit as the very first transaction
        opening_transaction = Transaction("Deposit", initial_deposit, "Account opening deposit")
        self.transactions.append(opening_transaction)

    # ---- Getter methods (safe, read-only access to private data) ----

    def get_account_number(self):
        """Return the account number."""
        return self.__account_number

    def get_balance(self):
        """Return the current balance."""
        return self.__balance

    # ---- Protected method to update balance (for child classes) ----

    def _set_balance(self, new_balance):
        """
        Protected method to update the balance.
        Single underscore = 'for internal/child class use only'.
        Used by SavingsAccount to update balance after withdrawal.
        """
        self.__balance = new_balance

    # ---- Implementing the abstract methods from BankOperations ----

    def deposit(self, amount):
        """Add money to the account."""
        if amount <= 0:
            print("  ERROR: Deposit amount must be greater than zero.")
            return False

        # Update the balance
        self.__balance += amount

        # Record this transaction
        transaction = Transaction("Deposit", amount, "Cash deposit")
        self.transactions.append(transaction)

        print(f"  SUCCESS: ${amount:.2f} deposited successfully.")
        print(f"  New Balance: ${self.__balance:.2f}")
        return True

    def withdraw(self, amount):
        """
        Remove money from the account.
        NOTE: This method is OVERRIDDEN in SavingsAccount (Polymorphism).
        """
        if amount <= 0:
            print("  ERROR: Withdrawal amount must be greater than zero.")
            return False

        if amount > self.__balance:
            print(f"  ERROR: Insufficient balance. Current balance is ${self.__balance:.2f}")
            return False

        # Deduct the amount
        self.__balance -= amount

        # Record this transaction
        transaction = Transaction("Withdrawal", amount, "Cash withdrawal")
        self.transactions.append(transaction)

        print(f"  SUCCESS: ${amount:.2f} withdrawn successfully.")
        print(f"  Remaining Balance: ${self.__balance:.2f}")
        return True

    def check_balance(self):
        """Display the current account balance."""
        print(f"  Account Holder : {self.owner_name}")
        print(f"  Account Number : {self.__account_number}")
        print(f"  Current Balance: ${self.__balance:.2f}")

    def display_transactions(self):
        """Show all transactions for this account."""
        if len(self.transactions) == 0:
            print("  No transactions found.")
        else:
            print(f"  Transactions for Account #{self.__account_number} ({self.owner_name}):")
            print("  " + "-" * 70)
            for transaction in self.transactions:
                transaction.display()
            print("  " + "-" * 70)

