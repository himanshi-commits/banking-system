# ============================================================
#         BANKING MANAGEMENT SYSTEM
#         Built with Python OOP Concepts
#         Concepts Used: Classes, Inheritance, Abstraction,
#                        Encapsulation, Polymorphism
# ============================================================

from abc import ABC, abstractmethod   # For Abstraction
from datetime import datetime         # For recording date and time of transactions


# ============================================================
# ABSTRACTION: Abstract base class defining the banking contract.
# Any class that inherits from BankOperations MUST implement
# deposit(), withdraw(), and check_balance().
# This ensures a consistent interface across all account types.
# ============================================================

class BankOperations(ABC):
    """Abstract base class that defines what operations a bank account must support."""

    @abstractmethod
    def deposit(self, amount):
        pass  # Must be implemented by child classes

    @abstractmethod
    def withdraw(self, amount):
        pass  # Must be implemented by child classes

    @abstractmethod
    def check_balance(self):
        pass  # Must be implemented by child classes


# ============================================================
# CLASS: Transaction
# Stores details about a single transaction (deposit, withdraw, etc.)
# ============================================================

class Transaction:
    """Represents a single banking transaction."""

    def __init__(self, transaction_type, amount, description):
        self.transaction_type = transaction_type   # e.g., "Deposit", "Withdrawal"
        self.amount = amount                       # How much money was involved
        self.description = description             # A short note about the transaction
        # Record the exact date and time the transaction happened
        self.date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def display(self):
        """Print the transaction details in a readable format."""
        print(f"  [{self.date_time}]  {self.transaction_type:<12}  "
              f"Amount: ${self.amount:<10.2f}  Note: {self.description}")


# ============================================================
# ENCAPSULATION + ABSTRACTION: Account class
# - Inherits from BankOperations (fulfills the abstract contract)
# - Uses private attributes __balance and __account_number
#   so that outside code cannot directly change them.
# - Provides public getter methods to safely access private data.
# ============================================================

class Account(BankOperations):
    """
    Base class for a bank account.
    Implements BankOperations (abstract class).
    Uses encapsulation to protect the balance and account number.
    """

    def __init__(self, account_number, owner_name, initial_deposit):
        # ENCAPSULATION: Private attributes (double underscore = private in Python)
        self.__account_number = account_number
        self.__balance = initial_deposit

        # Public attribute (name doesn't need to be private)
        self.owner_name = owner_name

        # List to store all transactions for this account
        self.transactions = []

        # Record the opening deposit as the first transaction
        opening_transaction = Transaction("Deposit", initial_deposit, "Account opening deposit")
        self.transactions.append(opening_transaction)

    # ---- Getter methods (safe way to read private data) ----

    def get_account_number(self):
        """Return the account number (read-only access)."""
        return self.__account_number

    def get_balance(self):
        """Return the current balance (read-only access)."""
        return self.__balance

    # ---- Internal helper to update balance safely ----

    def _set_balance(self, new_balance):
        """
        Protected method to update the balance.
        Using a single underscore means: 'for internal/child class use only'.
        This is used by child classes like SavingsAccount.
        """
        self.__balance = new_balance

    # ---- Implementing abstract methods from BankOperations ----

    def deposit(self, amount):
        """Add money to the account."""
        # Basic validation
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
        This method will be OVERRIDDEN in SavingsAccount (Polymorphism).
        """
        # Validate the amount
        if amount <= 0:
            print("  ERROR: Withdrawal amount must be greater than zero.")
            return False

        # Check if there is enough balance
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


# ============================================================
# INHERITANCE + POLYMORPHISM: SavingsAccount class
# - Inherits everything from Account
# - Adds a new property: minimum_balance
# - Overrides withdraw() to enforce minimum balance rule
#   This is POLYMORPHISM — same method name, different behavior
# ============================================================

class SavingsAccount(Account):
    """
    A savings account that inherits from Account.
    INHERITANCE: Gets all features of Account for free.
    POLYMORPHISM: Overrides the withdraw() method to add a
                  minimum balance restriction.
    """

    def __init__(self, account_number, owner_name, initial_deposit, minimum_balance=500):
        # Call the parent class constructor to set up basic account info
        super().__init__(account_number, owner_name, initial_deposit)

        # Additional property specific to SavingsAccount
        self.minimum_balance = minimum_balance

    def withdraw(self, amount):
        """
        POLYMORPHISM: Override withdraw() from Account.
        SavingsAccount has a special rule — after withdrawal,
        the balance must not go below the minimum balance.
        """
        # Validate the amount
        if amount <= 0:
            print("  ERROR: Withdrawal amount must be greater than zero.")
            return False

        # Check if withdrawal would go below minimum balance
        if (self.get_balance() - amount) < self.minimum_balance:
            print(f"  ERROR: Cannot withdraw. You must keep a minimum balance of ${self.minimum_balance:.2f}")
            print(f"  Current Balance : ${self.get_balance():.2f}")
            print(f"  Maximum you can withdraw: ${self.get_balance() - self.minimum_balance:.2f}")
            return False

        # Use the parent's private balance update via the protected setter
        new_balance = self.get_balance() - amount
        self._set_balance(new_balance)

        # Record this transaction
        transaction = Transaction("Withdrawal", amount, "Cash withdrawal")
        self.transactions.append(transaction)

        print(f"  SUCCESS: ${amount:.2f} withdrawn successfully.")
        print(f"  Remaining Balance: ${self.get_balance():.2f}")
        return True

    def get_minimum_balance(self):
        """Return the minimum balance requirement."""
        return self.minimum_balance


# ============================================================
# CLASS: Bank
# Manages all accounts. Acts as the main controller.
# Stores accounts in a dictionary {account_number: account_object}
# ============================================================

class Bank:
    """
    The Bank class manages all accounts.
    It creates accounts, finds them, and coordinates transfers.
    """

    def __init__(self, bank_name):
        self.bank_name = bank_name
        # Dictionary to store all accounts: {account_number: Account object}
        self.accounts = {}
        # Counter to generate unique account numbers automatically
        self.next_account_number = 1001

    def generate_account_number(self):
        """Generate a unique account number and increment the counter."""
        account_number = self.next_account_number
        self.next_account_number += 1
        return account_number

    def create_account(self, owner_name, initial_deposit):
        """Create a new SavingsAccount and add it to the bank."""
        # Generate a unique account number
        account_number = self.generate_account_number()

        # Create a SavingsAccount object (using Inheritance)
        new_account = SavingsAccount(account_number, owner_name, initial_deposit)

        # Store the account in the dictionary
        self.accounts[account_number] = new_account

        print(f"\n  SUCCESS: Account created successfully!")
        print(f"  Account Holder : {owner_name}")
        print(f"  Account Number : {account_number}")
        print(f"  Initial Deposit: ${initial_deposit:.2f}")
        print(f"  Minimum Balance: ${new_account.get_minimum_balance():.2f}")

    def find_account(self, account_number):
        """
        Look up an account by account number.
        Returns the account object if found, otherwise None.
        """
        return self.accounts.get(account_number, None)

    def deposit(self, account_number, amount):
        """Find the account and deposit money into it."""
        account = self.find_account(account_number)
        if account is None:
            print(f"  ERROR: Account #{account_number} not found.")
            return
        account.deposit(amount)

    def withdraw(self, account_number, amount):
        """Find the account and withdraw money from it."""
        account = self.find_account(account_number)
        if account is None:
            print(f"  ERROR: Account #{account_number} not found.")
            return
        account.withdraw(amount)

    def transfer(self, sender_account_number, receiver_account_number, amount):
        """
        Transfer money from one account to another.
        Both accounts must exist, and sender must have enough balance.
        """
        # Check if sender account exists
        sender = self.find_account(sender_account_number)
        if sender is None:
            print(f"  ERROR: Sender account #{sender_account_number} not found.")
            return

        # Check if receiver account exists
        receiver = self.find_account(receiver_account_number)
        if receiver is None:
            print(f"  ERROR: Receiver account #{receiver_account_number} not found.")
            return

        # Check if sender has enough balance (considering minimum balance)
        # We attempt to withdraw from sender first
        print(f"\n  Transferring ${amount:.2f} from Account #{sender_account_number} "
              f"to Account #{receiver_account_number}...")

        # Validate amount
        if amount <= 0:
            print("  ERROR: Transfer amount must be greater than zero.")
            return

        # Check if sender can withdraw this amount (respects minimum balance)
        available = sender.get_balance() - sender.get_minimum_balance()
        if amount > available:
            print(f"  ERROR: Insufficient funds for transfer.")
            print(f"  Sender Balance  : ${sender.get_balance():.2f}")
            print(f"  Minimum Balance : ${sender.get_minimum_balance():.2f}")
            print(f"  Max Transfer    : ${available:.2f}")
            return

        # Deduct from sender
        sender_new_balance = sender.get_balance() - amount
        sender._set_balance(sender_new_balance)
        # Record outgoing transaction for sender
        sender.transactions.append(
            Transaction("Transfer Out", amount,
                        f"Transferred to Account #{receiver_account_number}")
        )

        # Add to receiver
        receiver_new_balance = receiver.get_balance() + amount
        receiver._set_balance(receiver_new_balance)
        # Record incoming transaction for receiver
        receiver.transactions.append(
            Transaction("Transfer In", amount,
                        f"Received from Account #{sender_account_number}")
        )

        print(f"  SUCCESS: Transfer completed!")
        print(f"  Sender   ({sender.owner_name})   New Balance: ${sender.get_balance():.2f}")
        print(f"  Receiver ({receiver.owner_name}) New Balance: ${receiver.get_balance():.2f}")

    def check_balance(self, account_number):
        """Find the account and display its balance."""
        account = self.find_account(account_number)
        if account is None:
            print(f"  ERROR: Account #{account_number} not found.")
            return
        account.check_balance()

    def view_transactions(self, account_number):
        """Find the account and display all its transactions."""
        account = self.find_account(account_number)
        if account is None:
            print(f"  ERROR: Account #{account_number} not found.")
            return
        account.display_transactions()


# ============================================================
# HELPER FUNCTIONS: Input validation helpers for the menu
# These keep the menu code clean and easy to read.
# ============================================================

def get_valid_amount(prompt):
    """
    Ask the user for a money amount and keep asking until they enter
    a valid positive number.
    """
    while True:
        try:
            amount = float(input(prompt))
            if amount <= 0:
                print("  Please enter an amount greater than zero.")
            else:
                return amount
        except ValueError:
            print("  Invalid input. Please enter a number (e.g., 500 or 1000.50).")


def get_valid_account_number(prompt):
    """
    Ask the user for an account number and keep asking until they enter
    a valid integer.
    """
    while True:
        try:
            account_number = int(input(prompt))
            return account_number
        except ValueError:
            print("  Invalid input. Please enter a valid account number (digits only).")


def print_separator():
    """Print a visual separator line."""
    print("\n" + "=" * 45)


def print_menu():
    """Display the main menu."""
    print("\n" + "=" * 45)
    print("       BANKING MANAGEMENT SYSTEM")
    print("=" * 45)
    print("  1. Create Account")
    print("  2. Deposit Money")
    print("  3. Withdraw Money")
    print("  4. Transfer Money")
    print("  5. Check Balance")
    print("  6. View All Transactions")
    print("  7. Exit")
    print("=" * 45)


# ============================================================
# MAIN PROGRAM: The entry point that runs everything.
# Creates a Bank object and displays the menu in a loop.
# ============================================================

def main():
    """Main function — starts the banking system."""

    # Create a Bank object (this holds all accounts)
    bank = Bank("Python National Bank")

    print("\nWelcome to Python National Bank!")
    print("Powered by Object-Oriented Programming")

    # Keep showing the menu until the user chooses to exit
    while True:
        print_menu()

        choice = input("  Enter your choice (1-7): ").strip()

        # ---- Option 1: Create Account ----
        if choice == "1":
            print_separator()
            print("  CREATE NEW ACCOUNT")
            print_separator()

            name = input("  Enter your full name: ").strip()

            # Make sure name is not empty
            if not name:
                print("  ERROR: Name cannot be empty.")
                continue

            # Ask for initial deposit (must be at least $500 for minimum balance)
            print("  Note: Minimum balance requirement is $500.00")
            initial_deposit = get_valid_amount("  Enter initial deposit amount: $")

            if initial_deposit < 500:
                print("  ERROR: Initial deposit must be at least $500 (minimum balance requirement).")
                continue

            bank.create_account(name, initial_deposit)

        # ---- Option 2: Deposit Money ----
        elif choice == "2":
            print_separator()
            print("  DEPOSIT MONEY")
            print_separator()

            account_number = get_valid_account_number("  Enter account number: ")
            amount = get_valid_amount("  Enter deposit amount: $")

            print()
            bank.deposit(account_number, amount)

        # ---- Option 3: Withdraw Money ----
        elif choice == "3":
            print_separator()
            print("  WITHDRAW MONEY")
            print_separator()

            account_number = get_valid_account_number("  Enter account number: ")
            amount = get_valid_amount("  Enter withdrawal amount: $")

            print()
            bank.withdraw(account_number, amount)

        # ---- Option 4: Transfer Money ----
        elif choice == "4":
            print_separator()
            print("  TRANSFER MONEY")
            print_separator()

            sender_acc = get_valid_account_number("  Enter YOUR account number (sender): ")
            receiver_acc = get_valid_account_number("  Enter RECEIVER'S account number: ")

            # Make sure sender and receiver are different
            if sender_acc == receiver_acc:
                print("  ERROR: Sender and receiver cannot be the same account.")
                continue

            amount = get_valid_amount("  Enter transfer amount: $")

            bank.transfer(sender_acc, receiver_acc, amount)

        # ---- Option 5: Check Balance ----
        elif choice == "5":
            print_separator()
            print("  CHECK BALANCE")
            print_separator()

            account_number = get_valid_account_number("  Enter account number: ")
            print()
            bank.check_balance(account_number)

        # ---- Option 6: View All Transactions ----
        elif choice == "6":
            print_separator()
            print("  VIEW ALL TRANSACTIONS")
            print_separator()

            account_number = get_valid_account_number("  Enter account number: ")
            print()
            bank.view_transactions(account_number)

        # ---- Option 7: Exit ----
        elif choice == "7":
            print("\n  Thank you for using Python National Bank!")
            print("  Goodbye! Have a great day!\n")
            break  # Exit the while loop, ending the program

        # ---- Invalid choice ----
        else:
            print("\n  ERROR: Invalid choice. Please enter a number between 1 and 7.")


# ============================================================
# Run the program only when this file is executed directly.
# This is a Python best practice.
# ============================================================

if __name__ == "__main__":
    main()

