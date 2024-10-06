from pin_auth import pad
from deposit_amount import deposit
from balance_check import get_balance
from withdraw_amount import withdraw
from amount_enter import enter_amount
from common_utils import talk

def main():
    # Step 1: Enter PIN
    pad("ATM System", "Welcome, please enter your PIN.", "Thank you, PIN accepted.")

    # Step 2: Enter Deposit Amount
    deposit_amount = enter_amount("Deposit Amount", "Please enter the amount to deposit.", "Thank you, amount accepted.")
    deposit("user123", deposit_amount)

    # Step 3: Check Balance
    balance = get_balance("user123")
    talk(f"Your current balance is {balance}")

    # Step 4: Enter Withdrawal Amount
    withdraw_amount = enter_amount("Withdraw Amount", "Please enter the amount to withdraw.", "Thank you, amount accepted.")
    withdraw("user123", withdraw_amount)

    # Step 5: Check Balance Again
    balance = get_balance("user123")
    talk(f"Your current balance is {balance}")

if __name__ == "__main__":
    main()
