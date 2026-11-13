# ============================================================
#  helpers.py
#  Contains helper functions used by the main menu.
#  These functions handle user input validation and display.
# ============================================================


def get_valid_amount(prompt):
    """
    Ask the user for a money amount.
    Keeps asking until a valid positive number is entered.
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
    Ask the user for an account number.
    Keeps asking until a valid whole number is entered.
    """
    while True:
        try:
            account_number = int(input(prompt))
            return account_number
        except ValueError:
            print("  Invalid input. Please enter a valid account number (digits only).")


def print_separator():
    """Print a visual separator line between sections."""
    print("\n" + "=" * 45)


def print_menu():
    """Display the main banking menu."""
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

