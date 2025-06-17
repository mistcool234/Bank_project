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
