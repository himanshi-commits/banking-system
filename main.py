# ============================================================
#  main.py
#  The entry point of the Banking Management System.
#  Imports the Bank class and helper functions,
#  then runs the main menu loop.
# ============================================================

from bank import Bank           # The Bank class manages all accounts
from helpers import (           # Helper functions for input and display
    get_valid_amount,
    get_valid_account_number,
    print_separator,
    print_menu
)


def main():
    """Main function — creates the bank and runs the menu loop."""

    # Create the Bank object (this holds all accounts in memory)
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

            if not name:
                print("  ERROR: Name cannot be empty.")
                continue

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
            break  # Stop the loop and exit the program

        # ---- Invalid choice ----
        else:
            print("\n  ERROR: Invalid choice. Please enter a number between 1 and 7.")


# ============================================================
# Run main() only when this file is executed directly.
# This is a Python best practice.
# ============================================================

if __name__ == "__main__":
    main()


