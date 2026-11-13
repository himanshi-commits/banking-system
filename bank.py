# ============================================================
#  bank.py
#  Contains the Bank class.
#  The Bank manages all accounts and coordinates operations
#  like deposit, withdrawal, transfer, and balance checks.
# ============================================================

from savings_account import SavingsAccount   # Bank creates SavingsAccount objects
from transaction import Transaction           # Needed for recording transfer transactions


class Bank:
    """
    The Bank class is the main controller of the system.
    It holds all accounts in a dictionary and provides
    methods to perform banking operations on them.
    """

    def __init__(self, bank_name):
        self.bank_name = bank_name

        # Dictionary to store all accounts: { account_number: Account object }
        self.accounts = {}

        # Counter to automatically generate unique account numbers
        self.next_account_number = 1001

    def generate_account_number(self):
        """Generate a unique account number and increment the counter for next time."""
        account_number = self.next_account_number
        self.next_account_number += 1
        return account_number

    def create_account(self, owner_name, initial_deposit):
        """Create a new SavingsAccount and store it in the bank."""
        account_number = self.generate_account_number()

        # Create a SavingsAccount object (demonstrates Inheritance in action)
        new_account = SavingsAccount(account_number, owner_name, initial_deposit)

        # Save it in our accounts dictionary
        self.accounts[account_number] = new_account

        print(f"\n  SUCCESS: Account created successfully!")
        print(f"  Account Holder : {owner_name}")
        print(f"  Account Number : {account_number}")
        print(f"  Initial Deposit: ${initial_deposit:.2f}")
        print(f"  Minimum Balance: ${new_account.get_minimum_balance():.2f}")

    def find_account(self, account_number):
        """
        Search for an account by its account number.
        Returns the account object if found, or None if not found.
        """
        return self.accounts.get(account_number, None)

    def deposit(self, account_number, amount):
        """Find the account and deposit the given amount into it."""
        account = self.find_account(account_number)
        if account is None:
            print(f"  ERROR: Account #{account_number} not found.")
            return
        account.deposit(amount)

    def withdraw(self, account_number, amount):
        """Find the account and withdraw the given amount from it."""
        account = self.find_account(account_number)
        if account is None:
            print(f"  ERROR: Account #{account_number} not found.")
            return
        account.withdraw(amount)

    def transfer(self, sender_account_number, receiver_account_number, amount):
        """
        Transfer money from one account to another.
        - Both accounts must exist.
        - Sender must have enough balance (above minimum balance after transfer).
        - Both accounts get their transactions recorded.
        """
        # Look up both accounts
        sender = self.find_account(sender_account_number)
        if sender is None:
            print(f"  ERROR: Sender account #{sender_account_number} not found.")
            return

        receiver = self.find_account(receiver_account_number)
        if receiver is None:
            print(f"  ERROR: Receiver account #{receiver_account_number} not found.")
            return

        # Validate the transfer amount
        if amount <= 0:
            print("  ERROR: Transfer amount must be greater than zero.")
            return

        print(f"\n  Transferring ${amount:.2f} from Account #{sender_account_number} "
              f"to Account #{receiver_account_number}...")

        # Check if sender has enough funds (must keep minimum balance)
        available = sender.get_balance() - sender.get_minimum_balance()
        if amount > available:
            print(f"  ERROR: Insufficient funds for transfer.")
            print(f"  Sender Balance  : ${sender.get_balance():.2f}")
            print(f"  Minimum Balance : ${sender.get_minimum_balance():.2f}")
            print(f"  Max Transfer    : ${available:.2f}")
            return

        # Deduct from sender and record the outgoing transaction
        sender._set_balance(sender.get_balance() - amount)
        sender.transactions.append(
            Transaction("Transfer Out", amount,
                        f"Transferred to Account #{receiver_account_number}")
        )

        # Add to receiver and record the incoming transaction
        receiver._set_balance(receiver.get_balance() + amount)
        receiver.transactions.append(
            Transaction("Transfer In", amount,
                        f"Received from Account #{sender_account_number}")
        )

        print(f"  SUCCESS: Transfer completed!")
        print(f"  Sender   ({sender.owner_name})   New Balance: ${sender.get_balance():.2f}")
        print(f"  Receiver ({receiver.owner_name}) New Balance: ${receiver.get_balance():.2f}")

    def check_balance(self, account_number):
        """Find the account and show its current balance."""
        account = self.find_account(account_number)
        if account is None:
            print(f"  ERROR: Account #{account_number} not found.")
            return
        account.check_balance()

    def view_transactions(self, account_number):
        """Find the account and display all of its past transactions."""
        account = self.find_account(account_number)
        if account is None:
            print(f"  ERROR: Account #{account_number} not found.")
            return
        account.display_transactions()

