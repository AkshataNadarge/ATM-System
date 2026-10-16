import pandas as pd

FILE_NAME = "ATM_Accounts.xlsx"


# Initialize Excel file
def initialize_file():
    try:
        data = pd.read_excel(FILE_NAME, dtype={"Mobile": str})
    except FileNotFoundError:
        data = pd.DataFrame(columns=["Name", "Mobile", "Balance"])
        data.to_excel(FILE_NAME, index=False)


# Find account using mobile number
def find_account(mobile):
    data = pd.read_excel(FILE_NAME, dtype={"Mobile": str})

    rows = data.index[data["Mobile"] == mobile].tolist()

    if len(rows) > 0:
        return data, rows[0]

    return data, None


# 1. Add new account
def add_account():
    print("\n--- ADD NEW ACCOUNT ---")

    name = input("Enter name: ").strip()
    mobile = input("Enter 10-digit mobile number: ").strip()

    if name == "":
        print("Name cannot be empty.")
        return

    if not mobile.isdigit() or len(mobile) != 10:
        print("Invalid mobile number.")
        return

    data, index = find_account(mobile)

    if index is not None:
        print("Account already exists!")
        return

    try:
        balance = float(input("Enter initial balance: Rs. "))

        if balance < 0:
            print("Balance cannot be negative.")
            return

    except ValueError:
        print("Enter a valid amount.")
        return

    new_account = pd.DataFrame([{
        "Name": name,
        "Mobile": mobile,
        "Balance": balance
    }])

    data = pd.concat([data, new_account], ignore_index=True)

    data.to_excel(FILE_NAME, index=False)

    print("Account created successfully!")


# 2. Deposit money
def deposit_money():
    print("\n--- DEPOSIT MONEY ---")

    mobile = input("Enter mobile number: ").strip()

    data, index = find_account(mobile)

    if index is None:
        print("Account not found!")
        return

    try:
        amount = float(input("Enter deposit amount: Rs. "))

        if amount <= 0:
            print("Amount must be greater than zero.")
            return

    except ValueError:
        print("Enter a valid amount.")
        return

    balance = float(data.loc[index, "Balance"])

    updated_balance = balance + amount

    data.loc[index, "Balance"] = updated_balance

    data.to_excel(FILE_NAME, index=False)

    print("Deposit successful!")
    print("Updated balance: Rs.", round(updated_balance, 2))


# 3. Withdraw money
def withdraw_money():
    print("\n--- WITHDRAW MONEY ---")

    mobile = input("Enter mobile number: ").strip()

    data, index = find_account(mobile)

    if index is None:
        print("Account not found!")
        return

    try:
        amount = float(input("Enter withdrawal amount: Rs. "))

        if amount <= 0:
            print("Amount must be greater than zero.")
            return

    except ValueError:
        print("Enter a valid amount.")
        return

    balance = float(data.loc[index, "Balance"])

    if amount > balance:
        print("Insufficient balance!")
        return

    updated_balance = balance - amount

    data.loc[index, "Balance"] = updated_balance

    data.to_excel(FILE_NAME, index=False)

    print("Withdrawal successful!")
    print("Remaining balance: Rs.", round(updated_balance, 2))


# 4. Check balance
def check_balance():
    print("\n--- CHECK BALANCE ---")

    mobile = input("Enter mobile number: ").strip()

    data, index = find_account(mobile)

    if index is None:
        print("Account not found!")
        return

    print("Customer name:", data.loc[index, "Name"])
    print("Mobile number:", mobile)

    print(
        "Available balance: Rs.",
        round(float(data.loc[index, "Balance"]), 2)
    )


# Main menu
def main():
    initialize_file()

    while True:
        print("\n====== ATM MANAGEMENT SYSTEM ======")
        print("1. Add New Account")
        print("2. Deposit Money")
        print("3. Withdraw Money")
        print("4. Check Balance")
        print("5. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_account()

        elif choice == "2":
            deposit_money()

        elif choice == "3":
            withdraw_money()

        elif choice == "4":
            check_balance()

        elif choice == "5":
            print("Thank you for using ATM!")
            break

        else:
            print("Invalid choice! Please try again.")


if __name__ == "__main__":
    main()