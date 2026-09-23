
import streamlit as st
from hello import Bank  

st.set_page_config(page_title="🏦 Bank Management System", page_icon="🏦")

st.title("🏦 Bank Management System")

bank = Bank()

menu = st.sidebar.selectbox("Select Action", [
    "Create Account",
    "Deposit Money",
    "Withdraw Money",
    "View Account Details",
    "Update Account Details",
    "Delete Account"
])

if menu == "Create Account":
    st.subheader("Create New Account")

    name = st.text_input("Name")
    age = st.number_input("Age", min_value=0, step=1)
    email = st.text_input("Email")
    pin = st.text_input("4-digit PIN", type="password")

    if st.button("Create Account"):
        if name and email and pin and age:
            if len(pin) == 4 and pin.isdigit():
                res = bank.create_account(name, int(age), email, int(pin))
                if res["status"]:
                    st.success(f" Account created! Your Account Number is: {res['account_no']}")
                else:
                    st.warning(res["msg"])
            else:
                st.warning("PIN must be exactly 4 digits.")
        else:
            st.warning("Please fill all fields properly.")

elif menu == "Deposit Money":
    st.subheader("Deposit Money")

    acc_no = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")
    amount = st.number_input("Amount to deposit", min_value=1, max_value=10000, step=1)

    if st.button("Deposit"):
        if acc_no and pin:
            res = bank.deposit_money(acc_no, int(pin), amount)
            if res["status"]:
                st.success("Amount deposited successfully!")
            else:
                st.warning(res["msg"])
        else:
            st.warning("Please enter Account Number and PIN.")

elif menu == "Withdraw Money":
    st.subheader("Withdraw Money")

    acc_no = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")
    amount = st.number_input("Amount to withdraw", min_value=1, step=1)

    if st.button("Withdraw"):
        if acc_no and pin:
            res = bank.withdraw_money(acc_no, int(pin), amount)
            if res["status"]:
                st.success(" Amount withdrawn successfully!")
            else:
                st.warning(res["msg"])
        else:
            st.warning("Please enter Account Number and PIN.")

elif menu == "View Account Details":
    st.subheader("View Your Account Details")

    acc_no = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")

    if st.button("Show Details"):
        if acc_no and pin:
            user = bank.show_details(acc_no, int(pin))
            if user:
                st.json(user)
            else:
                st.error(" Account not found or wrong PIN.")
        else:
            st.warning("Please enter Account Number and PIN.")

elif menu == "Update Account Details":
    st.subheader("Update Your Account Details")

    acc_no = st.text_input("Account Number")
    pin = st.text_input("Current PIN", type="password")

    new_name = st.text_input("New Name (leave blank to skip)")
    new_email = st.text_input("New Email (leave blank to skip)")
    new_pin = st.text_input("New 4-digit PIN (leave blank to skip)", type="password")

    if st.button("Update"):
        if acc_no and pin:
            valid_new_pin = None
            if new_pin:
                if len(new_pin) == 4 and new_pin.isdigit():
                    valid_new_pin = int(new_pin)
                else:
                    st.warning("New PIN must be exactly 4 digits.")
                    valid_new_pin = None

            res = bank.update_details(acc_no, int(pin), new_name or None, new_email or None, valid_new_pin)
            if res["status"]:
                st.success(" Details updated successfully!")
            else:
                st.warning(res["msg"])
        else:
            st.warning("Please enter Account Number and PIN.")

elif menu == "Delete Account":
    st.subheader("Delete Your Account")

    acc_no = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")

    if st.button("Delete Account"):
        if acc_no and pin:
            res = bank.delete_account(acc_no, int(pin))
            if res["status"]:
                st.success(" Account deleted successfully!")
            else:
                st.warning(res["msg"])
        else:
            st.warning("Please enter Account Number and PIN.")
