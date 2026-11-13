# ============================================================
#  savings_account.py
#  Contains the SavingsAccount class.
#
#  OOP Concepts demonstrated here:
#    - INHERITANCE : SavingsAccount inherits from Account
#    - POLYMORPHISM: withdraw() is overridden with a new rule
# ============================================================

from account import Account         # Import the parent class
from transaction import Transaction # Import Transaction to record withdrawals


# ============================================================
# INHERITANCE + POLYMORPHISM: SavingsAccount class
# - Inherits everything from Account (no need to rewrite deposit, check_balance, etc.)
# - Adds a new property: minimum_balance
# - Overrides withdraw() to enforce the minimum balance rule
#   This is POLYMORPHISM — same method name, different behavior
# ============================================================

class SavingsAccount(Account):
    """
    A savings account that extends the base Account class.

    INHERITANCE  : Gets deposit(), check_balance(), display_transactions()
                   and all other features from Account for free.

    POLYMORPHISM : Overrides withdraw() to add a minimum balance restriction.
                   The same method name behaves differently here compared to Account.
    """

    def __init__(self, account_number, owner_name, initial_deposit, minimum_balance=500):
        # Call the parent (Account) constructor to initialize common fields
        super().__init__(account_number, owner_name, initial_deposit)

        # Extra property that only SavingsAccount has
        self.minimum_balance = minimum_balance

    def withdraw(self, amount):
        """
        POLYMORPHISM: Overrides the withdraw() method from Account.
        Rule: The balance after withdrawal must NOT go below the minimum balance.
        """
        if amount <= 0:
            print("  ERROR: Withdrawal amount must be greater than zero.")
            return False

        # Check if this withdrawal would break the minimum balance rule
        if (self.get_balance() - amount) < self.minimum_balance:
            print(f"  ERROR: Cannot withdraw. You must keep a minimum balance of ${self.minimum_balance:.2f}")
            print(f"  Current Balance         : ${self.get_balance():.2f}")
            print(f"  Maximum you can withdraw: ${self.get_balance() - self.minimum_balance:.2f}")
            return False

        # Update the balance using the protected method from Account
        new_balance = self.get_balance() - amount
        self._set_balance(new_balance)

        # Record this transaction
        transaction = Transaction("Withdrawal", amount, "Cash withdrawal")
        self.transactions.append(transaction)

        print(f"  SUCCESS: ${amount:.2f} withdrawn successfully.")
        print(f"  Remaining Balance: ${self.get_balance():.2f}")
        return True

    def get_minimum_balance(self):
        """Return the minimum balance requirement for this savings account."""
        return self.minimum_balance

