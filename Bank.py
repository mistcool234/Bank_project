import streamlit as st

class Account:
    def __init__(self, account_holder, account_number, balance=0):
        self.account_holder = account_holder
        self.account_number = account_number
        self.balance = balance

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            return f"Deposited ${amount}. New balance: ${self.balance}"
        else:
            return "Deposit amount must be positive."

    def withdraw(self, amount):
        if amount > 0 and amount <= self.balance:
            self.balance -= amount
            return f"Withdrew ${amount}. New balance: ${self.balance}"
        elif amount > self.balance:
            return "Insufficient funds."
        else:
            return "Withdrawal amount must be positive."

    def get_balance(self):
        return self.balance
class SavingsAccount(Account):
    def __init__(self, account_holder, account_number, balance=0, interest_rate=0.02, withdraw_limit=500):
        super().__init__(account_holder, account_number, balance)
        self.interest_rate = interest_rate
        self.withdraw_limit = withdraw_limit

    def withdraw(self, amount):
        if amount > self.withdraw_limit:
            return f"Withdrawal amount exceeds the limit of ${self.withdraw_limit}. You cannot withdraw more than $500 at a time."
        elif amount > 0 and amount <= self.balance:
            self.balance -= amount
            return f"Withdrew ${amount}. New balance: ${self.balance}"
        elif amount > self.balance:
            return "Insufficient funds."
        else:
            return "Withdrawal amount must be positive."

    def apply_interest(self):
        interest = self.balance * self.interest_rate
        self.balance += interest
        return f"Applied interest of ${interest}. New balance: ${self.balance}"
        
class CurrentAccount(Account):
    def __init__(self, account_holder, account_number, balance=0, overdraft_limit=500):
        super().__init__(account_holder, account_number, balance)
        self.overdraft_limit = overdraft_limit

    def withdraw(self, amount):
        if amount > 0 and amount <= self.balance + self.overdraft_limit:
            self.balance -= amount
            return f"Withdrew ${amount}. New balance: ${self.balance}"
        elif amount > self.balance + self.overdraft_limit:
            return "Overdraft limit exceeded."
        else:
            return "Withdrawal amount must be positive."
# Streamlit GUI
savings = SavingsAccount("Alice", "S123", 1000)
current = CurrentAccount("Bob", "C456", 500)

# Initialize session state for balances
if "savings_balance" not in st.session_state:
    st.session_state["savings_balance"] = savings.get_balance()
if "current_balance" not in st.session_state:
    st.session_state["current_balance"] = current.get_balance()

st.title("Rising Phonix Bank")

account_type = st.radio("Select Account Type:", ["Savings", "Current"])
amount = st.number_input("Enter Amount:", min_value=0.0, step=0.01)

if st.button("Deposit"):
    if account_type == "Savings":
        st.session_state["savings_balance"] += amount
        st.success(f"Deposited ${amount}. Updated Savings Account Balance: ${st.session_state['savings_balance']}")
    elif account_type == "Current":
        st.session_state["current_balance"] += amount
        st.success(f"Deposited ${amount}. Updated Current Account Balance: ${st.session_state['current_balance']}")

if st.button("Withdraw"):
    if account_type == "Savings":
        if amount > savings.withdraw_limit:
            st.error(f"You cannot withdraw more than ${savings.withdraw_limit} at a time.")
        elif amount <= st.session_state["savings_balance"]:
            st.session_state["savings_balance"] -= amount
            st.success(f"Withdrew ${amount}. Updated Savings Account Balance: ${st.session_state['savings_balance']}")
        else:
            st.error("Insufficient funds.")
    elif account_type == "Current":
        if amount <= st.session_state["current_balance"]:
            st.session_state["current_balance"] -= amount
            st.success(f"Withdrew ${amount}. Updated Current Account Balance: ${st.session_state['current_balance']}")
        else:
            st.error("Insufficient funds.")


